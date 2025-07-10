"""
Docsie Image Generator using OpenAI GPT-Image-1

This script automatically generates missing images for solution pages based on YAML metadata.
It uses the latest OpenAI GPT-Image-1 model with sophisticated prompts that create a mix of:
- Modern startup-style illustrations for hero images
- Professional photography for case studies
- Clean UI mockups for interfaces

Features:
- Latest GPT-Image-1 model for superior quality
- Multi-threaded generation (3x faster)
- Smart prompt mixing: illustrations + photography
- AI-powered prompt generation (optional)
- Thread-safe rate limiting

Requirements:
- OPENAI_API_KEY environment variable set
- openai>=1.0.0 package installed

Usage:
    python utils/image_generator.py                    # Generate with pre-defined smart prompts (medium quality)
    python utils/image_generator.py --override         # Regenerate all images
    python utils/image_generator.py --quality hd       # Use high quality (costs more, superior results)
    python utils/image_generator.py --ai-prompts       # Use AI to generate unique prompts (costs more)
"""

import os
import yaml
import glob
from pathlib import Path
from openai import OpenAI
from typing import List, Dict, Set
import requests
import logging
from tqdm import tqdm
from dotenv import load_dotenv
import time
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiting constants for OpenAI GPT-Image-1
# Standard tier: 5 requests per minute for images
REQUESTS_PER_MINUTE = 5
SECONDS_PER_REQUEST = 60 / REQUESTS_PER_MINUTE

# Threading configuration
MAX_THREADS = 3  # Conservative to respect rate limits

class ImageGenerator:
    def __init__(self, base_dir: str, override_existing: bool = False, quality: str = "standard"):
        """Initialize the image generator with the base directory of the project.
        
        Args:
            base_dir: Base directory of the project
            override_existing: If True, will regenerate images even if they already exist
            quality: Image quality - "standard" or "hd" (hd costs more)
        """
        self.base_dir = Path(base_dir)
        self.assets_dir = self.base_dir / 'assets'
        self.data_dir = self.base_dir / 'src' / '.data'
        self.override_existing = override_existing
        self.quality = quality
        
        # Initialize OpenAI client for GPT-Image-1
        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        
        # Thread-safe rate limiter
        self.rate_limiter_lock = threading.Lock()
        self.last_request_time = 0
        
        # AI-powered prompt generation (optional)
        self.use_ai_prompts = os.getenv('USE_AI_PROMPTS', 'false').lower() == 'true'

    def find_yaml_files(self) -> List[Path]:
        """Find all YAML files in the data directory."""
        yaml_files = []
        for pattern in ['**/*.yaml', '**/*.yml']:
            yaml_files.extend(self.data_dir.glob(pattern))
        logger.info(f"Found {len(yaml_files)} YAML files to process")
        for yaml_file in yaml_files:
            logger.info(f"Will process: {yaml_file}")
        return yaml_files

    def extract_image_paths(self, yaml_file: Path) -> Dict[str, Dict]:
        """Extract image paths and their metadata from YAML files."""
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            if not data or not isinstance(data, (dict, list)):
                logger.warning(f"No valid data found in {yaml_file}")
                return {}

            image_metadata = {}
            
            # Handle both single-item and list-based YAML structures
            items_to_process = data if isinstance(data, list) else [data]
            
            for item in items_to_process:
                if not isinstance(item, dict):
                    continue
                    
                # Get top-level context
                page_context = {
                    'page_title': item.get('title', ''),
                    'page_description': item.get('description', ''),
                    'category': item.get('category', '')
                }
                
                components = item.get('components', {})
                if not isinstance(components, dict):
                    continue
                
                # Get hero component context
                hero = components.get('hero', {})
                if isinstance(hero, dict):
                    hero_context = {
                        'hero_title': hero.get('title', ''),
                        'hero_description': hero.get('description', '')
                    }
                else:
                    hero_context = {'hero_title': '', 'hero_description': ''}
                
                # Function to process image paths and combine context
                def process_image(image_path, alt='', caption='', title='', description='', section_title='', section_description=''):
                    if not image_path or not isinstance(image_path, str):
                        return
                    
                    if not image_path.startswith('/assets/'):
                        logger.debug(f"Skipping non-asset image path: {image_path}")
                        return
                    
                    # Create metadata object
                    metadata = {
                        'alt': str(alt or ''),
                        'caption': str(caption or ''),
                        'title': str(title or ''),
                        'description': str(description or ''),
                        'section_title': str(section_title or ''),
                        'section_description': str(section_description or ''),
                        'page_context': {k: str(v or '') for k, v in page_context.items()},
                        'hero_context': {k: str(v or '') for k, v in hero_context.items()}
                    }
                    
                    # For solution images, we need both the original path and the new_home path
                    if '/solutions/' in image_path and '/new_home/' not in image_path:
                        # Original path (what solution pages expect)
                        original_path = image_path
                        # New home path (where images are currently being generated)
                        new_home_path = image_path.replace('/assets/', '/assets/new_home/')
                        
                        # Add both paths to metadata with cross-reference
                        metadata_with_alt = metadata.copy()
                        metadata_with_alt['alternate_path'] = new_home_path
                        image_metadata[original_path] = metadata_with_alt
                        
                        metadata_with_alt2 = metadata.copy()
                        metadata_with_alt2['alternate_path'] = original_path
                        image_metadata[new_home_path] = metadata_with_alt2
                        
                        logger.info(f"Found solution image: {original_path} (also generating at {new_home_path})")
                    else:
                        # Non-solution images or already in new_home path
                        image_metadata[image_path] = metadata
                        logger.info(f"Found image: {image_path} in {yaml_file}")

                # Process hero image
                if isinstance(hero, dict) and 'image' in hero:
                    process_image(
                        hero['image'],
                        title=hero.get('title', ''),
                        description=hero.get('description', ''),
                        section_title='Hero Section',
                        section_description='Main hero section of the page'
                    )

                # Process carousel images
                carousel = components.get('carousel', {})
                if isinstance(carousel, dict):
                    for slide in carousel.get('carousel_slides', []):
                        if isinstance(slide, dict):
                            process_image(
                                slide.get('image', ''),
                                alt=slide.get('alt', ''),
                                caption=slide.get('caption', ''),
                                section_title=carousel.get('title', ''),
                                section_description=carousel.get('description', '')
                            )

                # Process gallery images
                gallery = components.get('gallery', {})
                if isinstance(gallery, dict):
                    for gallery_item in gallery.get('gallery_images', []):
                        if isinstance(gallery_item, dict):
                            process_image(
                                gallery_item.get('image', ''),
                                alt=gallery_item.get('alt', ''),
                                caption=gallery_item.get('caption', ''),
                                section_title=gallery.get('title', ''),
                                section_description=gallery.get('description', '')
                            )

                # Process other sections with images
                for section_name, section_data in components.items():
                    if isinstance(section_data, dict) and 'image' in section_data:
                        process_image(
                            section_data['image'],
                            title=section_data.get('title', ''),
                            description=section_data.get('description', ''),
                            section_title=section_name.replace('_', ' ').title(),
                            section_description=section_data.get('description', '')
                        )

            return image_metadata

        except Exception as e:
            logger.error(f"Error processing YAML file {yaml_file}: {str(e)}")
            return {}

    def get_missing_images(self, image_metadata: Dict[str, Dict]) -> Dict[str, Dict]:
        """Find which images are missing or need to be regenerated."""
        missing_images = {}
        for path, metadata in image_metadata.items():
            # Use the original path for checking file existence
            full_path = self.base_dir / path.lstrip('/')
            
            # Check if the image exists at this path
            exists_here = full_path.exists()
            
            # Check if image exists at alternate path (for solution images)
            alternate_path = metadata.get('alternate_path')
            exists_at_alternate = False
            alternate_full_path = None
            
            if alternate_path:
                alternate_full_path = self.base_dir / alternate_path.lstrip('/')
                exists_at_alternate = alternate_full_path.exists()
            
            # Decide what action to take
            if not exists_here or self.override_existing:
                if exists_at_alternate and not self.override_existing:
                    # Image exists at alternate location - mark for copying
                    metadata_copy = metadata.copy()
                    metadata_copy['copy_from'] = str(alternate_full_path)
                    metadata_copy['action'] = 'copy'
                    missing_images[path] = metadata_copy
                    logger.info(f"Will copy image: {path} from {alternate_path}")
                else:
                    # Image doesn't exist anywhere or override is enabled - mark for generation
                    metadata_copy = metadata.copy()
                    metadata_copy['action'] = 'generate'
                    missing_images[path] = metadata_copy
                    status = "Missing" if not exists_here else "Will override"
                    logger.info(f"{status} image: {path} - will generate via API")
        return missing_images

    def generate_image_prompt(self, image_path: str, metadata: Dict) -> str:
        """Generate sophisticated prompts mixing illustrations and photography based on image type."""
        
        # Extract context
        page_title = metadata.get('page_context', {}).get('page_title', '')
        alt_text = metadata.get('alt', '')
        caption = metadata.get('caption', '')
        
        # Determine visual style based on image type and purpose
        if 'hero' in image_path or 'banner' in image_path:
            # Hero images: Modern startup-style illustrations with your design system
            base_style = "Flat vector isometric illustration. Clean, modern SaaS design with soft gradients. Color palette: soft blue (#CFE8FF), lavender (#E3D9FF), deep indigo (#2E2E8F), white background. Rounded UI elements, subtle shadows, floating icons in isometric perspective. Visual balance, minimalist layout, startup aesthetic"
        elif 'case' in image_path:
            # Case study images: Realistic photography
            base_style = "Professional photograph, high-resolution, clean modern aesthetic, natural lighting, realistic human subjects, contemporary office environment"
        elif 'screen' in image_path or 'portal' in image_path:
            # Interface/screen images: UI mockups with illustration style
            base_style = "Clean interface design mockup, modern dashboard aesthetic, professional UI/UX design, contemporary color scheme, realistic screen elements"
        else:
            # Default: Mix of illustration and photography
            base_style = "Professional illustration with photographic elements, modern business aesthetic, clean design, contemporary workspace"
        
        # Create sophisticated prompts mixing styles based on image type
        if 'api-docs' in image_path or 'api-case' in image_path:
            if 'hero' in image_path:
                variations = [
                    f"Diverse startup team collaborating around floating holographic API documentation interfaces, data streams connecting their devices in isometric view. {base_style}",
                    f"API endpoints as friendly geometric characters shaking hands and exchanging colorful data packets in a minimalist isometric city. {base_style}",
                    f"Developer's desk transforming into a rocket ship launching API connections to cloud platforms, isometric perspective. {base_style}"
                ]
                import random
                return random.choice(variations)
            elif 'case1' in image_path:
                return f"Professional developer sitting at a modern desk, viewing an interactive API console on a large monitor with code examples and endpoint testing interface visible on screen. Clean, well-lit office environment with natural lighting. {base_style}"
            elif 'case2' in image_path:
                return f"Close-up view of hands typing code while viewing API documentation with syntax highlighting and multiple programming language examples side-by-side on a high-resolution display. {base_style}"
            elif 'case3' in image_path:
                return f"Professional woman developer reviewing API authentication documentation on her laptop, with security tokens and authorization examples clearly visible on the screen. Modern office setting. {base_style}"
            else:
                return f"Modern isometric illustration showing API integration workflow with connected services, data pipelines, and documentation interfaces in a clean startup aesthetic. {base_style}"
        
        elif 'tech-docs' in image_path or 'tech-case' in image_path:
            if 'hero' in image_path:
                variations = [
                    f"Technical documentation growing like a digital tree with branches of code snippets, diagrams blooming as flowers, isometric garden view. {base_style}",
                    f"Startup team building a documentation fortress with blocks of knowledge, each block glowing with different technical concepts. {base_style}",
                    f"Documentation portal as a futuristic command center with floating holographic manuals and interactive guides. {base_style}"
                ]
                import random
                return random.choice(variations)
            elif 'case1' in image_path:
                return f"Software engineer creating technical documentation, typing on a laptop with architectural diagrams and system documentation visible on the screen. Modern tech office environment. {base_style}"
            elif 'case2' in image_path:
                return f"Professional reviewing comprehensive developer guides on multiple monitors, with code snippets, diagrams, and technical specifications clearly visible. Clean workspace setup. {base_style}"
            elif 'case3' in image_path:
                return f"Team of developers collaborating on system architecture documentation, with whiteboards showing technical diagrams and laptops displaying detailed technical specs. {base_style}"
            else:
                return f"Geometric illustration showing technical documentation workflow with system components, code repositories, and knowledge transfer in modern SaaS style. {base_style}"
        
        elif 'training-docs' in image_path or 'training-case' in image_path:
            if 'case1' in image_path:
                return f"HR professional creating employee onboarding materials on her computer, with training modules and interactive learning content visible on the screen. Modern office setting. {base_style}"
            elif 'case2' in image_path:
                return f"Sales team leader developing product training documentation, with product knowledge slides and training materials displayed on a large monitor. Corporate training room. {base_style}"
            elif 'case3' in image_path:
                return f"Learning and development specialist creating certification program content, with assessment modules and completion certificates visible on screen. Professional training environment. {base_style}"
            else:
                return f"Corporate trainer developing interactive learning materials on a laptop with training modules and educational content on display. {base_style}"
        
        elif 'quality-docs' in image_path or 'quality-case' in image_path:
            if 'case1' in image_path:
                return f"Quality manager documenting manufacturing processes, viewing detailed process workflows and quality control procedures on a computer screen. Industrial office setting. {base_style}"
            elif 'case2' in image_path:
                return f"Compliance specialist tracking quality metrics and documentation compliance on a dashboard displayed on dual monitors. Professional regulatory environment. {base_style}"
            elif 'case3' in image_path:
                return f"Quality assurance team reviewing quality metrics and performance indicators on large displays showing charts and compliance tracking data. Modern quality control center. {base_style}"
            else:
                return f"Quality professional managing documentation systems with quality control processes and metrics visible on screen. {base_style}"
        
        elif 'dev-portal' in image_path:
            if 'screen1' in image_path:
                return f"Developer accessing a comprehensive documentation hub with API references, guides, and resources clearly organized on screen. Modern development workspace. {base_style}"
            elif 'screen2' in image_path:
                return f"Software engineer using developer tools and resources from a documentation portal, with code samples and integration guides visible on the monitor. {base_style}"
            elif 'screen3' in image_path:
                return f"Development team collaborating using a developer community portal with forums, resources, and shared documentation visible on their screens. {base_style}"
            else:
                return f"Professional developer navigating a modern developer portal with comprehensive documentation and tools. {base_style}"
        
        elif 'ai-docs' in image_path or 'ai-case' in image_path:
            if 'case1' in image_path:
                return f"Content creator using AI to generate comprehensive documentation, with AI writing assistant interface and generated content visible on screen. Modern creative workspace. {base_style}"
            elif 'case2' in image_path:
                return f"Professional reviewing AI-translated documentation in multiple languages, with translation interface and language options displayed on a large monitor. {base_style}"
            elif 'case3' in image_path:
                return f"Technical writer receiving AI-powered content optimization suggestions, with editing interface and improvement recommendations visible on screen. {base_style}"
            else:
                return f"Knowledge worker using AI-powered documentation tools with intelligent content generation visible on computer screen. {base_style}"
        
        elif 'support' in image_path or 'support-case' in image_path:
            if 'case1' in image_path:
                return f"Customer support agent using a comprehensive self-service knowledge base, with help articles and FAQ solutions displayed on screen. Modern support center. {base_style}"
            elif 'case2' in image_path:
                return f"Support manager analyzing ticket reduction metrics and customer satisfaction data on a dashboard showing positive trends. Professional support operations center. {base_style}"
            elif 'case3' in image_path:
                return f"Support team member quickly accessing relevant documentation to help customers, with knowledge base search and solution articles visible on monitor. {base_style}"
            else:
                return f"Customer service professional using smart support documentation with instant access to help resources. {base_style}"
        
        else:
            # Generic fallback with startup variations
            variations = [
                f"Startup founder's journey visualized as ascending platforms with {page_title} milestones floating as achievement badges. {base_style}",
                f"Modern coworking space where entrepreneurs collaborate on {page_title}, ideas floating as colorful thought bubbles. {base_style}",
                f"Innovation hub with {page_title} concepts orbiting around central workspace like planets in isometric solar system. {base_style}",
                f"Digital transformation represented by {page_title} evolving from paper to holographic interfaces in startup setting. {base_style}"
            ]
            import random
            return random.choice(variations)

    def generate_ai_prompt(self, image_path: str, metadata: Dict) -> str:
        """Use GPT to generate sophisticated image prompts based on context."""
        try:
            # Extract context for AI
            page_title = metadata.get('page_context', {}).get('page_title', '')
            page_description = metadata.get('page_context', {}).get('page_description', '')
            alt_text = metadata.get('alt', '')
            caption = metadata.get('caption', '')
            
            # Determine visual style
            if 'hero' in image_path:
                style_instruction = "Create a modern startup landing page style illustration"
            elif 'case' in image_path:
                style_instruction = "Create a professional photograph showing real people in action"
            elif 'screen' in image_path:
                style_instruction = "Create a clean UI/UX mockup or interface design"
            else:
                style_instruction = "Create a professional illustration with modern business aesthetic"

            # AI prompt for generating image prompts
            ai_prompt = f"""
You are an expert at creating detailed image generation prompts for GPT-Image-1. 

Context:
- Page: {page_title}
- Description: {page_description}
- Image purpose: {alt_text} - {caption}
- Image filename: {image_path}

Task: {style_instruction}

Create a detailed, specific prompt that will generate a high-quality image. The prompt should:
1. Be specific about visual elements, composition, and style
2. Include lighting, colors, and atmosphere details
3. Specify if it should be photographic or illustrative
4. Be under 200 words
5. Focus on modern, professional, relatable imagery

Generate only the image prompt, no explanation:
"""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": ai_prompt}],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.warning(f"AI prompt generation failed: {e}. Using fallback.")
            return self.generate_image_prompt(image_path, metadata)

    def wait_for_rate_limit(self):
        """Thread-safe rate limiting"""
        with self.rate_limiter_lock:
            current_time = time.time()
            time_since_last = current_time - self.last_request_time
            if time_since_last < SECONDS_PER_REQUEST:
                sleep_time = SECONDS_PER_REQUEST - time_since_last
                logger.info(f"Rate limiting: waiting {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
            self.last_request_time = time.time()

    def generate_and_save_image(self, image_path: str, metadata: Dict) -> bool:
        """Generate or copy an image based on the action specified in metadata."""
        try:
            # Check if we should copy from existing location or generate new
            action = metadata.get('action', 'generate')
            
            if action == 'copy':
                # Copy from existing location instead of generating
                return self.copy_existing_image(image_path, metadata)
            else:
                # Generate new image using API
                return self.generate_new_image(image_path, metadata)

        except Exception as e:
            logger.error(f"Error processing image for {image_path}: {e}")
            return False

    def copy_existing_image(self, image_path: str, metadata: Dict) -> bool:
        """Copy an existing image from alternate location."""
        try:
            copy_from = metadata.get('copy_from')
            if not copy_from:
                logger.error(f"No copy_from path specified for {image_path}")
                return False
            
            source_path = Path(copy_from)
            if not source_path.exists():
                logger.error(f"Source image does not exist: {source_path}")
                return False
            
            # Prepare destination path
            full_path = self.base_dir / image_path.lstrip('/')
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy the file
            import shutil
            shutil.copy2(source_path, full_path)
            logger.info(f"📋 Copied image from {source_path} to {full_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error copying image for {image_path}: {e}")
            return False

    def generate_new_image(self, image_path: str, metadata: Dict) -> bool:
        """Generate a new image using OpenAI GPT-Image-1."""
        try:
            # Choose prompt generation method
            if self.use_ai_prompts:
                prompt = self.generate_ai_prompt(image_path, metadata)
                logger.info(f"🤖 AI-generated prompt for: {image_path}")
            else:
                prompt = self.generate_image_prompt(image_path, metadata)
                logger.info(f"📝 Pre-defined prompt for: {image_path}")
            
            logger.info(f"Using prompt: {prompt[:100]}...")  # Truncate for cleaner logs

            # Thread-safe rate limiting
            self.wait_for_rate_limit()

            # Map quality parameter to GPT-Image-1 format
            api_quality = "high" if self.quality == "hd" else "medium"
            
            response = self.client.images.generate(
                model="gpt-image-1",  # Use latest GPT-Image-1 model
                prompt=prompt,
                n=1,
                size="1024x1024",  # Options: "1024x1024", "1024x1536", "1536x1024"
                quality=api_quality  # "high", "medium", or "low"
            )

            if response.data:
                # Keep the full path including new_home if it exists
                full_path = self.base_dir / image_path.lstrip('/')
                full_path.parent.mkdir(parents=True, exist_ok=True)

                # GPT-Image-1 returns base64-encoded images, not URLs
                if hasattr(response.data[0], 'b64_json') and response.data[0].b64_json:
                    # Decode base64 image data
                    import base64
                    image_data = base64.b64decode(response.data[0].b64_json)
                    with open(full_path, 'wb') as f:
                        f.write(image_data)
                    logger.info(f"🎨 Generated and saved image to {full_path}")
                    return True
                elif hasattr(response.data[0], 'url') and response.data[0].url:
                    # Fallback for URL-based responses (older models)
                    image_url = response.data[0].url
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        with open(full_path, 'wb') as f:
                            f.write(response.content)
                        logger.info(f"🎨 Generated and saved image to {full_path}")
                        return True
                    else:
                        logger.error(f"Failed to download image from {image_url}")
                        return False
                else:
                    logger.error("No valid image data (b64_json or url) received from API")
                    return False
            else:
                logger.error("No image data received from API")
                return False

        except Exception as e:
            logger.error(f"Error generating image for {image_path}: {e}")
            return False

    def process_all_files(self, specific_image=None):
        """Process all YAML files and generate missing images."""
        yaml_files = self.find_yaml_files()
        all_image_metadata = {}
        
        # Collect all image paths and metadata
        for yaml_file in yaml_files:
            image_metadata = self.extract_image_paths(yaml_file)
            all_image_metadata.update(image_metadata)

        # Filter to specific image if requested
        if specific_image:
            if specific_image in all_image_metadata:
                all_image_metadata = {specific_image: all_image_metadata[specific_image]}
                logger.info(f"Targeting specific image: {specific_image}")
            else:
                logger.error(f"Image not found in YAML files: {specific_image}")
                return

        # Find missing images
        missing_images = self.get_missing_images(all_image_metadata)
        
        if not missing_images:
            logger.info("No missing images found!")
            return

        logger.info(f"Found {len(missing_images)} missing images")
        total_time_estimate = len(missing_images) * SECONDS_PER_REQUEST / MAX_THREADS
        logger.info(f"Estimated time with {MAX_THREADS} threads: {total_time_estimate/60:.1f} minutes")
        
        # Generate missing images with multi-threading
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            with tqdm(total=len(missing_images), desc="Generating images") as pbar:
                # Submit all tasks
                future_to_path = {
                    executor.submit(self.generate_and_save_image, image_path, metadata): image_path
                    for image_path, metadata in missing_images.items()
                }
                
                # Process completed tasks
                for future in as_completed(future_to_path):
                    image_path = future_to_path[future]
                    try:
                        success = future.result()
                        if success:
                            pbar.set_description(f"✅ Generated {os.path.basename(image_path)}")
                        else:
                            pbar.set_description(f"❌ Failed {os.path.basename(image_path)}")
                    except Exception as e:
                        logger.error(f"Error generating {image_path}: {e}")
                        pbar.set_description(f"❌ Error {os.path.basename(image_path)}")
                    pbar.update(1)

def main():
    import argparse
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate images for Docsie documentation using GPT-Image-1 (latest OpenAI model)')
    parser.add_argument('--override', '-o', action='store_true', 
                       help='Override existing images (default: False)')
    parser.add_argument('--quality', '-q', choices=['standard', 'hd'], default='standard',
                       help='Image quality: standard (medium) or hd (high) (default: standard)')
    parser.add_argument('--ai-prompts', action='store_true',
                       help='Use AI to generate sophisticated prompts (requires extra GPT-4 calls)')
    parser.add_argument('--image', '-i', type=str,
                       help='Generate only this specific image path (e.g., /assets/solutions/api-documentation-hero.jpg)')
    args = parser.parse_args()
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    # Set AI prompts environment variable if specified
    if args.ai_prompts:
        os.environ['USE_AI_PROMPTS'] = 'true'
    
    # Initialize and run the image generator with command line options
    generator = ImageGenerator(
        project_root, 
        override_existing=args.override,
        quality=args.quality
    )
    generator.process_all_files(specific_image=args.image)

if __name__ == "__main__":
    main()
