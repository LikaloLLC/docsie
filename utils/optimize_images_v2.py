#!/usr/bin/env python3
"""
Improved Image Optimization Script for Docsie
- Better directory structure
- Maintains original directory hierarchy
- Easy workflow for new images
"""

import os
import sys
from pathlib import Path
from PIL import Image
import subprocess
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import shutil

# Configuration
IMAGE_SIZES = [320, 640, 768, 1024, 1280, 1920]
QUALITY_WEBP = 85
QUALITY_AVIF = 80
QUALITY_JPEG = 85
MAX_WORKERS = 4

class ImageOptimizerV2:
    def __init__(self, base_path='.'):
        self.base_path = Path(base_path).resolve()
        # Use a cleaner structure: /assets/optimized/
        self.optimized_root = self.base_path / 'assets' / 'optimized'
        
        self.results = {
            'optimized': [],
            'errors': [],
            'total_saved': 0
        }
        
        # Manifest for tracking optimization
        self.manifest_path = self.optimized_root / 'manifest.json'
        self.manifest = self.load_manifest()
    
    def load_manifest(self):
        """Load optimization manifest"""
        if self.manifest_path.exists():
            with open(self.manifest_path, 'r') as f:
                return json.load(f)
        return {}
    
    def save_manifest(self):
        """Save optimization manifest"""
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.manifest_path, 'w') as f:
            json.dump(self.manifest, f, indent=2)
    
    def get_file_hash(self, file_path):
        """Get hash of file for cache validation"""
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def should_optimize(self, file_path):
        """Check if file needs optimization"""
        file_str = str(file_path)
        file_hash = self.get_file_hash(file_path)
        
        if file_str in self.manifest:
            return self.manifest[file_str]['hash'] != file_hash
        return True
    
    def get_optimized_path(self, original_path, width=None, format='jpg'):
        """Get the optimized image path"""
        # Get path relative to base
        try:
            rel_path = original_path.relative_to(self.base_path)
        except ValueError:
            # If path is already relative
            rel_path = original_path
        
        # Remove 'assets/' prefix if present
        path_str = str(rel_path)
        if path_str.startswith('assets/'):
            path_without_assets = path_str[7:]  # Remove 'assets/'
        else:
            path_without_assets = path_str
        
        # Build optimized path maintaining directory structure
        # From: assets/solutions/kb-hero.jpg
        # To: assets/optimized/solutions/kb-hero-320w.jpg
        path_parts = list(Path(path_without_assets).parts)  # Convert to list
        filename = path_parts[-1]
        name_without_ext = Path(filename).stem
        
        if width:
            new_filename = f"{name_without_ext}-{width}w.{format}"
        else:
            new_filename = f"{name_without_ext}.{format}"
        
        path_parts[-1] = new_filename
        return self.optimized_root / Path(*path_parts)
    
    def optimize_image(self, image_path, force=False):
        """Optimize a single image"""
        image_path = Path(image_path)
        
        # Skip if already optimized
        if not force and not self.should_optimize(image_path):
            print(f"✓ Already optimized: {image_path}")
            return
        
        print(f"🔄 Optimizing: {image_path}")
        
        try:
            # Open image
            img = Image.open(image_path)
            
            # Convert RGBA to RGB if needed
            if img.mode in ('RGBA', 'LA'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[-1])
                img = rgb_img
            
            # Get original size
            original_size = os.path.getsize(image_path)
            
            # Generate responsive sizes
            sizes_created = []
            for width in IMAGE_SIZES:
                if width >= img.width:
                    width = img.width
                
                # Calculate height maintaining aspect ratio
                height = int(img.height * (width / img.width))
                
                # Resize image
                resized = img.resize((width, height), Image.Resampling.LANCZOS)
                
                # Save WebP version
                webp_path = self.get_optimized_path(image_path, width, 'webp')
                webp_path.parent.mkdir(parents=True, exist_ok=True)
                resized.save(webp_path, 'WEBP', quality=QUALITY_WEBP, method=6)
                sizes_created.append({
                    'width': width,
                    'format': 'webp',
                    'path': str(webp_path.relative_to(self.base_path)),
                    'size': os.path.getsize(webp_path)
                })
                
                # Save optimized JPEG
                jpeg_path = self.get_optimized_path(image_path, width, 'jpg')
                resized.save(jpeg_path, 'JPEG', quality=QUALITY_JPEG, optimize=True)
                sizes_created.append({
                    'width': width,
                    'format': 'jpeg',
                    'path': str(jpeg_path.relative_to(self.base_path)),
                    'size': os.path.getsize(jpeg_path)
                })
                
                if width == img.width:
                    break
            
            # Calculate total saved
            total_optimized_size = sum(s['size'] for s in sizes_created)
            saved = original_size - (total_optimized_size / len(set(s['width'] for s in sizes_created)))
            self.results['total_saved'] += max(0, saved)
            
            # Update manifest
            self.manifest[str(image_path)] = {
                'hash': self.get_file_hash(image_path),
                'original_size': original_size,
                'sizes': sizes_created
            }
            
            self.results['optimized'].append(str(image_path))
            print(f"✅ Optimized: {image_path} (saved {saved/1024:.1f}KB)")
            
        except Exception as e:
            print(f"❌ Error optimizing {image_path}: {e}")
            self.results['errors'].append({
                'file': str(image_path),
                'error': str(e)
            })
    
    def find_images(self, directory=None):
        """Find all images to optimize"""
        if directory is None:
            directory = self.base_path / 'assets'
        else:
            directory = Path(directory)
        
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
        images = []
        
        for ext in image_extensions:
            images.extend(directory.glob(f'**/*{ext}'))
            images.extend(directory.glob(f'**/*{ext.upper()}'))
        
        # Filter out already optimized images
        return [img for img in images if 'optimized' not in str(img)]
    
    def optimize_all(self, directory=None, parallel=True):
        """Optimize all images in directory"""
        images = self.find_images(directory)
        print(f"Found {len(images)} images to process")
        
        if parallel:
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = {
                    executor.submit(self.optimize_image, img): img 
                    for img in images
                }
                
                for future in as_completed(futures):
                    future.result()
        else:
            for img in images:
                self.optimize_image(img)
        
        # Save manifest
        self.save_manifest()
        
        # Print summary
        print("\n" + "="*50)
        print("Optimization Summary:")
        print(f"✅ Optimized: {len(self.results['optimized'])} images")
        print(f"❌ Errors: {len(self.results['errors'])} images")
        print(f"💾 Total saved: {self.results['total_saved']/1024/1024:.1f} MB")
        
        if self.results['errors']:
            print("\nErrors:")
            for error in self.results['errors']:
                print(f"  - {error['file']}: {error['error']}")
    
    def clean_old_optimized(self):
        """Clean up old optimized images from wrong location"""
        old_path = self.base_path / 'assets' / 'images' / 'optimized'
        if old_path.exists():
            print(f"🧹 Cleaning up old optimized images from {old_path}")
            shutil.rmtree(old_path)
            print("✅ Cleaned up old optimized images")

def main():
    """Main function"""
    import argparse
    parser = argparse.ArgumentParser(description='Optimize images for web (v2)')
    parser.add_argument('directory', nargs='?', default='assets', 
                        help='Directory to process (default: assets)')
    parser.add_argument('--force', action='store_true', 
                        help='Force re-optimization of all images')
    parser.add_argument('--sequential', action='store_true',
                        help='Process images sequentially (slower)')
    parser.add_argument('--clean', action='store_true',
                        help='Clean up old optimized images')
    
    args = parser.parse_args()
    
    # Check dependencies
    try:
        from PIL import Image
    except ImportError:
        print("❌ Pillow not installed. Run: pip install Pillow")
        sys.exit(1)
    
    # Create optimizer
    optimizer = ImageOptimizerV2('.')
    
    # Clean old optimized images if requested
    if args.clean:
        optimizer.clean_old_optimized()
    
    # Clear manifest if force
    if args.force:
        optimizer.manifest = {}
    
    # Run optimization
    optimizer.optimize_all(args.directory, parallel=not args.sequential)

if __name__ == '__main__':
    main()