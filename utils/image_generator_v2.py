"""
Docsie Image Generator V2 - Enhanced with Startup-Specific Styles
=================================================================

Enhanced version with:
- Ability to regenerate specific images by path
- Startup-specific illustration variations
- Design system color integration
- Isometric style consistency
- More creative and varied prompts

Features:
- Target specific images for regeneration
- Multiple visual style variations
- Design system aware (soft blue, lavender, deep indigo)
- Consistent isometric perspective
- Startup-focused scenarios

Usage:
    # Regenerate specific image
    python utils/image_generator_v2.py --image "/assets/solutions/api-documentation-hero.jpg"
    
    # Regenerate all images with a specific pattern
    python utils/image_generator_v2.py --pattern "*hero*"
    
    # Use specific style variation
    python utils/image_generator_v2.py --style startup --variation 3
    
    # Generate with HD quality
    python utils/image_generator_v2.py --quality hd
"""

import os
import yaml
import glob
from pathlib import Path
from openai import OpenAI
from typing import List, Dict, Set, Optional
import requests
import logging
from tqdm import tqdm
from dotenv import load_dotenv
import time
import argparse
import threading
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import fnmatch

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiting constants
REQUESTS_PER_MINUTE = 5
SECONDS_PER_REQUEST = 60 / REQUESTS_PER_MINUTE
MAX_THREADS = 3

# Design System Colors
DESIGN_COLORS = {
    'soft_blue': '#CFE8FF',
    'lavender': '#E3D9FF',
    'deep_indigo': '#2E2E8F',
    'white': '#FFFFFF',
    'accent_orange': '#FB923C',
    'accent_green': '#13AF4B',
    'gradient_1': 'from soft blue (#CFE8FF) to lavender (#E3D9FF)',
    'gradient_2': 'from lavender (#E3D9FF) to deep indigo (#2E2E8F)',
    'gradient_3': 'from white to soft blue (#CFE8FF)'
}

# Startup-Specific Style Variations
STARTUP_VARIATIONS = {
    'collaboration': [
        "Diverse startup team in minimalist coworking space, brainstorming around floating holographic {concept} interfaces",
        "Young entrepreneurs collaborating on {concept} with AR glasses showing data visualizations in isometric view",
        "Remote team members as floating avatars connected by glowing data streams, working on {concept} together",
        "Startup founders high-fiving with {concept} success metrics floating above in isometric bubbles"
    ],
    'innovation': [
        "Rocket ship launching from laptop screen with {concept} modules orbiting in isometric space",
        "Light bulb transforming into {concept} interface with creative sparks and geometric patterns",
        "Innovation lab with floating {concept} prototypes and holographic testing environments",
        "Startup garage with {concept} blueprints projected on walls and floating 3D models"
    ],
    'growth': [
        "Ascending bar charts transforming into cityscape with {concept} buildings in isometric view",
        "Plant growing through keyboard with {concept} features as blooming flowers in geometric style",
        "Startup journey path with {concept} milestones as floating checkpoint orbs",
        "Growth rocket trajectory with {concept} metrics as constellation points"
    ],
    'automation': [
        "Robot assistants organizing {concept} workflows in isometric factory of ideas",
        "AI brain network processing {concept} with neural pathways as data streams",
        "Automated assembly line creating {concept} components with robotic precision",
        "Smart assistant hologram managing {concept} tasks in floating interface panels"
    ],
    'connection': [
        "Network of startup offices connected by {concept} data bridges in isometric city",
        "Global team members as nodes in {concept} constellation map with real-time connections",
        "API endpoints as friendly robots shaking hands and exchanging {concept} data packets",
        "Digital handshake between platforms with {concept} integration flowing between"
    ]
}

class EnhancedImageGenerator:
    def __init__(self, base_dir: str, override_existing: bool = False, quality: str = "standard"):
        self.base_dir = Path(base_dir)
        self.assets_dir = self.base_dir / 'assets'
        self.data_dir = self.base_dir / 'src' / '.data'
        self.override_existing = override_existing
        self.quality = quality
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Thread-safe rate limiter
        self.rate_limiter_lock = threading.Lock()
        self.last_request_time = 0

    def find_yaml_files(self) -> List[Path]:
        """Find all YAML files in the data directory."""
        yaml_files = []
        for pattern in ['**/*.yaml', '**/*.yml']:
            yaml_files.extend(self.data_dir.glob(pattern))
        return yaml_files

    def extract_image_paths(self, yaml_file: Path) -> Dict[str, Dict]:
        """Extract image paths and metadata from YAML files."""
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            if not data:
                return {}

            image_metadata = {}
            items_to_process = data if isinstance(data, list) else [data]
            
            for item in items_to_process:
                if not isinstance(item, dict):
                    continue
                    
                # Get context
                page_context = {
                    'page_title': item.get('title', ''),
                    'page_description': item.get('description', ''),
                    'category': item.get('category', '')
                }
                
                components = item.get('components', {})
                if not isinstance(components, dict):
                    continue
                
                # Process all image-containing components
                self._process_component_images(components, image_metadata, page_context)
                
            return image_metadata

        except Exception as e:
            logger.error(f"Error processing YAML file {yaml_file}: {str(e)}")
            return {}

    def _process_component_images(self, components: Dict, image_metadata: Dict, page_context: Dict):
        """Process images from all components."""
        for comp_name, comp_data in components.items():
            if not isinstance(comp_data, dict):
                continue
                
            # Direct image in component
            if 'image' in comp_data:
                self._add_image_metadata(
                    comp_data['image'],
                    image_metadata,
                    page_context,
                    comp_data.get('title', ''),
                    comp_data.get('description', '')
                )
            
            # Gallery images
            if 'gallery_images' in comp_data:
                for img in comp_data.get('gallery_images', []):
                    if isinstance(img, dict) and 'image' in img:
                        self._add_image_metadata(
                            img['image'],
                            image_metadata,
                            page_context,
                            img.get('alt', ''),
                            img.get('caption', '')
                        )
            
            # Carousel slides
            if 'carousel_slides' in comp_data:
                for slide in comp_data.get('carousel_slides', []):
                    if isinstance(slide, dict) and 'image' in slide:
                        self._add_image_metadata(
                            slide['image'],
                            image_metadata,
                            page_context,
                            slide.get('alt', ''),
                            slide.get('caption', '')
                        )

    def _add_image_metadata(self, image_path: str, image_metadata: Dict, 
                           page_context: Dict, title: str = '', description: str = ''):
        """Add image metadata entry."""
        if not image_path or not image_path.startswith('/assets/'):
            return
            
        metadata = {
            'title': title,
            'description': description,
            'page_context': page_context
        }
        
        # Handle both original and new_home paths for solutions
        if '/solutions/' in image_path and '/new_home/' not in image_path:
            new_home_path = image_path.replace('/assets/', '/assets/new_home/')
            image_metadata[image_path] = metadata.copy()
            image_metadata[new_home_path] = metadata.copy()
        else:
            image_metadata[image_path] = metadata

    def generate_startup_prompt(self, image_path: str, metadata: Dict, 
                               style_variation: Optional[str] = None, 
                               variation_index: Optional[int] = None) -> str:
        """Generate startup-specific prompts with design system colors."""
        
        # Extract context
        page_title = metadata.get('page_context', {}).get('page_title', '')
        description = metadata.get('description', metadata.get('title', ''))
        
        # Determine concept from context
        concept = self._extract_concept(image_path, page_title, description)
        
        # Base style with design system colors
        base_style = f"""Flat vector isometric illustration. Clean, modern SaaS design with soft gradients. 
        Color palette: soft blue (#CFE8FF), lavender (#E3D9FF), deep indigo (#2E2E8F), white background. 
        Rounded UI elements, subtle shadows, floating icons in isometric perspective. 
        Visual balance, minimalist layout, startup aesthetic. No text or labels."""
        
        # Choose variation category
        if not style_variation:
            # Auto-select based on image type
            if 'hero' in image_path:
                style_variation = random.choice(['innovation', 'growth', 'collaboration'])
            elif 'case' in image_path:
                style_variation = 'collaboration'
            elif 'api' in image_path or 'integration' in image_path:
                style_variation = 'connection'
            elif 'ai' in image_path or 'automation' in image_path:
                style_variation = 'automation'
            else:
                style_variation = random.choice(list(STARTUP_VARIATIONS.keys()))
        
        # Get specific variation
        variations = STARTUP_VARIATIONS.get(style_variation, STARTUP_VARIATIONS['innovation'])
        if variation_index is not None and 0 <= variation_index < len(variations):
            prompt_template = variations[variation_index]
        else:
            prompt_template = random.choice(variations)
        
        # Build complete prompt
        specific_prompt = prompt_template.format(concept=concept)
        
        # Add specific details based on image type
        if 'hero' in image_path:
            details = "Main focal point centered, with supporting elements floating around. Hero composition."
        elif 'screen' in image_path or 'interface' in image_path:
            details = "Clean device mockup (laptop or tablet) showing the interface, floating UI elements around it."
        elif 'case' in image_path:
            details = "Real-world scenario showing the solution in action, people interacting with technology."
        else:
            details = "Balanced composition with primary element and supporting visual metaphors."
        
        return f"{specific_prompt} {details} {base_style}"

    def _extract_concept(self, image_path: str, page_title: str, description: str) -> str:
        """Extract the main concept from context."""
        path_lower = image_path.lower()
        
        # Map common paths to concepts
        concept_map = {
            'api': 'API documentation',
            'technical': 'technical documentation',
            'training': 'training materials',
            'knowledge': 'knowledge base',
            'support': 'customer support',
            'quality': 'quality management',
            'ai': 'AI-powered documentation',
            'content': 'content management',
            'product': 'product documentation',
            'user-manual': 'user manuals',
            'sop': 'standard operating procedures',
            'release': 'release notes',
            'style': 'style guides'
        }
        
        # Check path for concepts
        for key, value in concept_map.items():
            if key in path_lower:
                return value
        
        # Fallback to page title
        if page_title:
            return page_title.lower().replace('docsie', '').strip()
        
        return 'documentation platform'

    def filter_images_by_criteria(self, all_images: Dict[str, Dict], 
                                 specific_image: Optional[str] = None,
                                 pattern: Optional[str] = None) -> Dict[str, Dict]:
        """Filter images based on criteria."""
        if specific_image:
            # Return only the specific image if it exists
            if specific_image in all_images:
                return {specific_image: all_images[specific_image]}
            else:
                logger.warning(f"Image not found: {specific_image}")
                return {}
        
        elif pattern:
            # Filter by pattern
            filtered = {}
            for path, metadata in all_images.items():
                if fnmatch.fnmatch(path, pattern):
                    filtered[path] = metadata
            return filtered
        
        else:
            # Return all images
            return all_images

    def wait_for_rate_limit(self):
        """Thread-safe rate limiting."""
        with self.rate_limiter_lock:
            current_time = time.time()
            time_since_last = current_time - self.last_request_time
            if time_since_last < SECONDS_PER_REQUEST:
                sleep_time = SECONDS_PER_REQUEST - time_since_last
                time.sleep(sleep_time)
            self.last_request_time = time.time()

    def generate_and_save_image(self, image_path: str, metadata: Dict, 
                               style_variation: Optional[str] = None,
                               variation_index: Optional[int] = None) -> bool:
        """Generate and save an image with startup-specific styling."""
        try:
            # Generate prompt
            prompt = self.generate_startup_prompt(
                image_path, metadata, style_variation, variation_index
            )
            logger.info(f"🎨 Generating: {image_path}")
            logger.info(f"📝 Prompt: {prompt[:150]}...")
            
            # Rate limiting
            self.wait_for_rate_limit()
            
            # Generate image
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1024x1024",
                quality=self.quality,
                style="vivid"  # More vibrant, artistic style
            )
            
            if response.data and response.data[0].url:
                # Download and save
                full_path = self.base_dir / image_path.lstrip('/')
                full_path.parent.mkdir(parents=True, exist_ok=True)
                
                img_response = requests.get(response.data[0].url)
                if img_response.status_code == 200:
                    with open(full_path, 'wb') as f:
                        f.write(img_response.content)
                    logger.info(f"✅ Saved to: {full_path}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error generating {image_path}: {e}")
            return False

    def process_images(self, specific_image: Optional[str] = None, 
                      pattern: Optional[str] = None,
                      style_variation: Optional[str] = None,
                      variation_index: Optional[int] = None):
        """Process and generate images based on criteria."""
        # Collect all image metadata
        all_images = {}
        yaml_files = self.find_yaml_files()
        
        for yaml_file in yaml_files:
            images = self.extract_image_paths(yaml_file)
            all_images.update(images)
        
        # Filter based on criteria
        target_images = self.filter_images_by_criteria(all_images, specific_image, pattern)
        
        if not target_images:
            logger.info("No images found matching criteria")
            return
        
        # Check which need generation
        images_to_generate = {}
        for path, metadata in target_images.items():
            full_path = self.base_dir / path.lstrip('/')
            if not full_path.exists() or self.override_existing:
                images_to_generate[path] = metadata
        
        if not images_to_generate:
            logger.info("No images need generation")
            return
        
        logger.info(f"Generating {len(images_to_generate)} images...")
        
        # Generate images
        success_count = 0
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            futures = {
                executor.submit(
                    self.generate_and_save_image, 
                    path, 
                    metadata,
                    style_variation,
                    variation_index
                ): path
                for path, metadata in images_to_generate.items()
            }
            
            with tqdm(total=len(futures)) as pbar:
                for future in as_completed(futures):
                    path = futures[future]
                    try:
                        if future.result():
                            success_count += 1
                    except Exception as e:
                        logger.error(f"Failed {path}: {e}")
                    pbar.update(1)
        
        logger.info(f"✨ Generated {success_count}/{len(images_to_generate)} images")

def main():
    parser = argparse.ArgumentParser(
        description='Enhanced Image Generator with Startup Styles'
    )
    parser.add_argument('--image', '-i', type=str,
                       help='Generate specific image by path')
    parser.add_argument('--pattern', '-p', type=str,
                       help='Generate images matching pattern (e.g., "*hero*")')
    parser.add_argument('--override', '-o', action='store_true',
                       help='Override existing images')
    parser.add_argument('--quality', '-q', choices=['standard', 'hd'], 
                       default='standard',
                       help='Image quality (hd costs more)')
    parser.add_argument('--style', '-s', 
                       choices=list(STARTUP_VARIATIONS.keys()),
                       help='Style variation to use')
    parser.add_argument('--variation', '-v', type=int,
                       help='Specific variation index (0-3)')
    
    args = parser.parse_args()
    
    # Initialize generator
    project_root = Path(__file__).parent.parent
    generator = EnhancedImageGenerator(
        project_root,
        override_existing=args.override,
        quality=args.quality
    )
    
    # Process images
    generator.process_images(
        specific_image=args.image,
        pattern=args.pattern,
        style_variation=args.style,
        variation_index=args.variation
    )

if __name__ == "__main__":
    main()