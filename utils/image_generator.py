import os
import yaml
import glob
from pathlib import Path
from openai import AzureOpenAI
from typing import List, Dict, Set
import requests
import logging
from tqdm import tqdm
from dotenv import load_dotenv
import time
import argparse

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiting constants
REQUESTS_PER_MINUTE = 3
SECONDS_PER_REQUEST = 60 / REQUESTS_PER_MINUTE

class ImageGenerator:
    def __init__(self, base_dir: str, override_existing: bool = False):
        """Initialize the image generator with the base directory of the project.
        
        Args:
            base_dir: Base directory of the project
            override_existing: If True, will regenerate images even if they already exist
        """
        self.base_dir = Path(base_dir)
        self.assets_dir = self.base_dir / 'assets'
        self.data_dir = self.base_dir / 'src' / '.data'
        self.override_existing = override_existing
        
        # Initialize DALL-E client
        self.client = AzureOpenAI(
            api_key=os.getenv('AZURE_DALLE_API_KEY'),
            api_version=os.getenv('AZURE_DALLE_API_VERSION'),
            azure_endpoint=os.getenv('AZURE_DALLE_ENDPOINT')
        )
        self.dalle_deployment = os.getenv('AZURE_DALLE_DEPLOYMENT')

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
                    
                    # Add 'new_home' to path if it's not there and it's in the solutions directory
                    if '/solutions/' in image_path and '/new_home/' not in image_path:
                        clean_path = image_path.replace('/assets/', '/assets/new_home/')
                    else:
                        clean_path = image_path
                    
                    # Ensure all text fields are strings
                    image_metadata[clean_path] = {
                        'alt': str(alt or ''),
                        'caption': str(caption or ''),
                        'title': str(title or ''),
                        'description': str(description or ''),
                        'section_title': str(section_title or ''),
                        'section_description': str(section_description or ''),
                        'page_context': {k: str(v or '') for k, v in page_context.items()},
                        'hero_context': {k: str(v or '') for k, v in hero_context.items()}
                    }
                    logger.info(f"Found image: {clean_path} in {yaml_file}")

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
            # Remove 'new_home' from the path if it exists
            clean_path = path.replace('/new_home/', '/')
            full_path = self.base_dir / clean_path.lstrip('/')
            
            # Include image if it's missing or if override is enabled
            if not full_path.exists() or self.override_existing:
                missing_images[clean_path] = metadata
                status = "Missing" if not full_path.exists() else "Will override"
                logger.info(f"{status} image: {clean_path} with metadata: {metadata}")
        return missing_images

    def generate_image_prompt(self, image_path: str, metadata: Dict) -> str:
        """Generate a prompt for image creation based on the image path and metadata."""
        # Extract all context from metadata
        page_context = metadata.get('page_context', {})
        hero_context = metadata.get('hero_context', {})
        
        # Build comprehensive context
        context_elements = [
            f"Page: {page_context.get('page_title')} - {page_context.get('page_description')}",
            f"Section: {metadata.get('section_title')} - {metadata.get('section_description')}",
            f"Hero Context: {hero_context.get('hero_title')} - {hero_context.get('hero_description')}",
            f"Image Context: {metadata.get('title')} - {metadata.get('description')}",
            f"Specific: {metadata.get('alt')} - {metadata.get('caption')}"
        ]
        
        # Filter out empty contexts and join
        context = '. '.join(filter(lambda x: x and not x.endswith(' - '), context_elements))
        
        # Base style components
        style_prompt = ("High-quality digital illustration, professional atmosphere, "
                       "subtle colors, photorealistic rendering, cinematic composition")
        
        # Specific prompts based on the content type
        if 'data_sheets' in image_path or 'ds-case' in image_path:
            scenes = [
                ("Aerial view of a modern product development lab where engineers collaborate on technical specifications. "
                 "Digital displays show version-controlled product documentation. "
                 "Clean, organized workspace with 3D product models and specification sheets."),
                
                ("Close-up of an innovative touchscreen interface displaying interactive product specifications. "
                 "Engineer's hands elegantly navigating through different versions. "
                 "Modern industrial design studio in the background."),
                
                ("Split-screen view: physical product prototype on one side, detailed digital specifications on the other. "
                 "Professional reviewing documentation on a large curved display. "
                 "Contemporary R&D facility with glass walls.")
            ]
        
        elif 'kb-case' in image_path:
            scenes = [
                ("Dynamic knowledge hub with interactive wall displays showing organized documentation trees. "
                 "Knowledge worker using gesture controls to organize content. "
                 "Open-concept office with collaborative zones."),
                
                ("Immersive virtual documentation space with floating information panels. "
                 "Professional using augmented reality to manage knowledge base structure. "
                 "Modern tech office with city skyline view."),
                
                ("Birds-eye view of a circular desk setup with multiple floating displays. "
                 "Content specialist orchestrating knowledge flow between different departments. "
                 "Minimalist office design with natural elements.")
            ]
        
        elif 'api-case' in image_path:
            scenes = [
                ("Innovative visualization of API endpoints as an interconnected 3D network. "
                 "Developer using holographic interface to navigate documentation. "
                 "High-tech workspace with ambient lighting."),
                
                ("Split view showing clean code structure alongside interactive API documentation. "
                 "Professional using multi-screen setup for comprehensive documentation review. "
                 "Modern coding lab with collaborative spaces."),
                
                ("Aerial shot of development team space with large interactive API mapping display. "
                 "Developer documenting API endpoints using advanced visualization tools. "
                 "Contemporary tech office with industrial design elements.")
            ]
        
        elif 'release-case' in image_path:
            scenes = [
                ("Command center style room with timeline visualization of software releases. "
                 "Product manager orchestrating release documentation on curved display wall. "
                 "Modern release management hub with data visualization."),
                
                ("Innovative 3D timeline showing version history and release notes. "
                 "Professional using gesture controls to navigate release documentation. "
                 "Contemporary office with dramatic lighting."),
                
                ("Overhead view of release planning space with interactive documentation displays. "
                 "Team lead reviewing comprehensive release notes on transparent screen. "
                 "High-tech office with futuristic elements.")
            ]
        
        elif 'templates' in image_path:
            scenes = [
                ("Creative studio with multiple floating displays showing template variations. "
                 "Designer crafting documentation templates using gesture controls. "
                 "Modern design lab with artistic elements."),
                
                ("Innovative template builder interface on large touchscreen wall. "
                 "Content specialist customizing templates with intuitive controls. "
                 "Contemporary creative space with inspiration boards."),
                
                ("Aerial view of documentation design lab with interactive template previews. "
                 "Professional fine-tuning templates on advanced design station. "
                 "Stylish office with collaborative zones.")
            ]
        
        else:
            scenes = [
                ("Modern documentation center with interactive knowledge displays. "
                 "Professional using advanced tools to manage content. "
                 "Contemporary office with innovative design."),
                
                ("Creative workspace with floating documentation interfaces. "
                 "Specialist organizing content using gesture controls. "
                 "High-tech environment with artistic elements."),
                
                ("Aerial view of documentation hub with multiple visualization screens. "
                 "Team member crafting content on advanced workstation. "
                 "Modern office with unique architectural features.")
            ]
        
        # Select a scene based on the image path to ensure consistency for the same image
        scene_index = hash(image_path) % len(scenes)
        selected_scene = scenes[scene_index]
        
        return (f"{selected_scene} {style_prompt}. "
                f"The scene should specifically illustrate: {context}")

    def generate_and_save_image(self, image_path: str, metadata: Dict) -> bool:
        """Generate an image using Azure OpenAI and save it to the correct location."""
        try:
            prompt = self.generate_image_prompt(image_path, metadata)
            logger.info(f"Generating image for: {image_path}")
            logger.info(f"Using prompt: {prompt}")

            # Add rate limit delay
            logger.info(f"Waiting {SECONDS_PER_REQUEST} seconds for rate limit...")
            time.sleep(SECONDS_PER_REQUEST)

            response = self.client.images.generate(
                model=self.dalle_deployment,
                prompt=prompt,
                n=1,
                size="1024x1024"
            )

            if response.data:
                # Keep the full path including new_home if it exists
                full_path = self.base_dir / image_path.lstrip('/')
                full_path.parent.mkdir(parents=True, exist_ok=True)

                # Download and save the image
                image_url = response.data[0].url
                response = requests.get(image_url)
                if response.status_code == 200:
                    with open(full_path, 'wb') as f:
                        f.write(response.content)
                    logger.info(f"Successfully saved image to {full_path}")
                    return True
                else:
                    logger.error(f"Failed to download image from {image_url}")
                    return False
            else:
                logger.error("No image data received from API")
                return False

        except Exception as e:
            logger.error(f"Error generating image for {image_path}: {e}")
            return False

    def process_all_files(self):
        """Process all YAML files and generate missing images."""
        yaml_files = self.find_yaml_files()
        all_image_metadata = {}
        
        # Collect all image paths and metadata
        for yaml_file in yaml_files:
            image_metadata = self.extract_image_paths(yaml_file)
            all_image_metadata.update(image_metadata)

        # Find missing images
        missing_images = self.get_missing_images(all_image_metadata)
        
        if not missing_images:
            logger.info("No missing images found!")
            return

        logger.info(f"Found {len(missing_images)} missing images")
        total_time_estimate = len(missing_images) * SECONDS_PER_REQUEST
        logger.info(f"Estimated time to complete: {total_time_estimate/60:.1f} minutes")
        
        # Generate missing images with progress bar
        with tqdm(total=len(missing_images), desc="Generating images") as pbar:
            for image_path, metadata in missing_images.items():
                success = self.generate_and_save_image(image_path, metadata)
                if success:
                    pbar.set_description(f"Generated {image_path}")
                else:
                    pbar.set_description(f"Failed {image_path}")
                pbar.update(1)

def main():
    import argparse
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate images for Docsie documentation')
    parser.add_argument('--override', '-o', action='store_true', 
                       help='Override existing images (default: False)')
    args = parser.parse_args()
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    # Initialize and run the image generator with override from command line
    generator = ImageGenerator(project_root, override_existing=args.override)
    generator.process_all_files()

if __name__ == "__main__":
    main()
