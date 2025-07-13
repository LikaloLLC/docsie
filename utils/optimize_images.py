#!/usr/bin/env python3
"""
Image Optimization Script for Docsie
Addresses:
1. Convert images to next-gen formats (WebP, AVIF)
2. Create responsive image sizes
3. Optimize image quality
4. Generate proper srcset attributes
5. Add lazy loading attributes
"""

import os
import sys
from pathlib import Path
from PIL import Image
import subprocess
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib

# Configuration
IMAGE_SIZES = [320, 640, 768, 1024, 1280, 1920]  # Common breakpoints
QUALITY_WEBP = 85
QUALITY_AVIF = 80
QUALITY_JPEG = 85
MAX_WORKERS = 4

class ImageOptimizer:
    def __init__(self, base_path='.'):
        self.base_path = Path(base_path)
        # Always use project root for optimized directory
        self.project_root = Path('.').resolve()
        self.optimized_dir = self.project_root / 'assets' / 'images' / 'optimized'
        self.optimized_dir.mkdir(parents=True, exist_ok=True)
        
        # Track optimization results
        self.results = {
            'optimized': [],
            'errors': [],
            'total_saved': 0
        }
        
        # Cache manifest to avoid re-optimizing
        self.manifest_path = self.optimized_dir / 'manifest.json'
        self.manifest = self.load_manifest()
    
    def load_manifest(self):
        """Load optimization manifest"""
        if self.manifest_path.exists():
            with open(self.manifest_path, 'r') as f:
                return json.load(f)
        return {}
    
    def save_manifest(self):
        """Save optimization manifest"""
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
            
            # Create output directory structure
            # Get path relative to project root
            try:
                rel_path = image_path.relative_to(self.project_root)
            except ValueError:
                # If image is not under project root, use full path
                rel_path = image_path
            
            output_base = self.optimized_dir / rel_path.parent
            output_base.mkdir(parents=True, exist_ok=True)
            
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
                webp_path = output_base / f"{image_path.stem}-{width}w.webp"
                resized.save(webp_path, 'WEBP', quality=QUALITY_WEBP, method=6)
                sizes_created.append({
                    'width': width,
                    'format': 'webp',
                    'path': str(webp_path.relative_to(self.project_root)),
                    'size': os.path.getsize(webp_path)
                })
                
                # Save AVIF version if supported
                if self.check_avif_support():
                    avif_path = output_base / f"{image_path.stem}-{width}w.avif"
                    self.save_avif(resized, avif_path)
                    sizes_created.append({
                        'width': width,
                        'format': 'avif',
                        'path': str(avif_path.relative_to(self.project_root)),
                        'size': os.path.getsize(avif_path)
                    })
                
                # Save optimized JPEG as fallback
                jpeg_path = output_base / f"{image_path.stem}-{width}w.jpg"
                resized.save(jpeg_path, 'JPEG', quality=QUALITY_JPEG, optimize=True)
                sizes_created.append({
                    'width': width,
                    'format': 'jpeg',
                    'path': str(jpeg_path.relative_to(self.project_root)),
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
                'sizes': sizes_created,
                'srcset': self.generate_srcset(sizes_created, rel_path)
            }
            
            self.results['optimized'].append(str(image_path))
            print(f"✅ Optimized: {image_path} (saved {saved/1024:.1f}KB)")
            
        except Exception as e:
            print(f"❌ Error optimizing {image_path}: {e}")
            self.results['errors'].append({
                'file': str(image_path),
                'error': str(e)
            })
    
    def check_avif_support(self):
        """Check if AVIF encoding is available"""
        try:
            subprocess.run(['avifenc', '--version'], 
                         capture_output=True, check=True)
            return True
        except:
            return False
    
    def save_avif(self, img, output_path):
        """Save image as AVIF using external encoder"""
        try:
            # Save temp PNG
            temp_path = output_path.with_suffix('.png')
            img.save(temp_path, 'PNG')
            
            # Convert to AVIF
            subprocess.run([
                'avifenc',
                '--min', '0',
                '--max', '63',
                '-a', 'end-usage=q',
                '-a', 'cq-level=23',
                '-a', 'tune=ssim',
                str(temp_path),
                str(output_path)
            ], check=True, capture_output=True)
            
            # Remove temp file
            temp_path.unlink()
            
        except Exception as e:
            print(f"Warning: Could not create AVIF: {e}")
    
    def generate_srcset(self, sizes_created, original_path):
        """Generate srcset and picture element HTML"""
        # Group by format
        by_format = {}
        for size in sizes_created:
            fmt = size['format']
            if fmt not in by_format:
                by_format[fmt] = []
            by_format[fmt].append(size)
        
        # Generate picture element
        picture_html = '<picture>\n'
        
        # AVIF sources
        if 'avif' in by_format:
            srcset = ', '.join([
                f"/{size['path']} {size['width']}w" 
                for size in by_format['avif']
            ])
            picture_html += f'  <source type="image/avif" srcset="{srcset}">\n'
        
        # WebP sources
        if 'webp' in by_format:
            srcset = ', '.join([
                f"/{size['path']} {size['width']}w" 
                for size in by_format['webp']
            ])
            picture_html += f'  <source type="image/webp" srcset="{srcset}">\n'
        
        # JPEG fallback
        if 'jpeg' in by_format:
            srcset = ', '.join([
                f"/{size['path']} {size['width']}w" 
                for size in by_format['jpeg']
            ])
            sizes = '(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw'
            picture_html += f'  <img src="/{by_format["jpeg"][0]["path"]}" srcset="{srcset}" sizes="{sizes}" alt="" loading="lazy">\n'
        
        picture_html += '</picture>'
        
        return {
            'picture_element': picture_html,
            'srcset_by_format': {
                fmt: ', '.join([f"/{s['path']} {s['width']}w" for s in sizes])
                for fmt, sizes in by_format.items()
            }
        }
    
    def find_images(self, directory=None):
        """Find all images to optimize"""
        if directory is None:
            directory = self.base_path
        
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
        images = []
        
        for ext in image_extensions:
            images.extend(Path(directory).glob(f'**/*{ext}'))
            images.extend(Path(directory).glob(f'**/*{ext.upper()}'))
        
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
        
        # Generate HTML helper
        self.generate_html_helper()
        
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
    
    def generate_html_helper(self):
        """Generate HTML helper file with optimized image tags"""
        helper_path = self.optimized_dir / 'image-tags.html'
        
        with open(helper_path, 'w') as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Optimized Image Tags</title>
    <style>
        body { font-family: monospace; padding: 20px; }
        .image-block { margin: 20px 0; padding: 20px; background: #f5f5f5; }
        .preview { max-width: 200px; margin: 10px 0; }
        pre { background: #fff; padding: 10px; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>Optimized Image Tags</h1>
    <p>Copy these tags to use optimized images in your templates:</p>
""")
            
            for img_path, data in self.manifest.items():
                if 'srcset' in data:
                    f.write(f"""
    <div class="image-block">
        <h3>{img_path}</h3>
        <div class="preview">{data['srcset']['picture_element']}</div>
        <pre><code>{html.escape(data['srcset']['picture_element'])}</code></pre>
    </div>
""")
            
            f.write("</body></html>")
        
        print(f"\n📄 HTML helper generated: {helper_path}")

def main():
    """Main function"""
    import argparse
    parser = argparse.ArgumentParser(description='Optimize images for web')
    parser.add_argument('directory', nargs='?', default='.', 
                        help='Directory to process (default: current)')
    parser.add_argument('--force', action='store_true', 
                        help='Force re-optimization of all images')
    parser.add_argument('--sequential', action='store_true',
                        help='Process images sequentially (slower)')
    
    args = parser.parse_args()
    
    # Check dependencies
    try:
        from PIL import Image
    except ImportError:
        print("❌ Pillow not installed. Run: pip install Pillow")
        sys.exit(1)
    
    # Create optimizer
    optimizer = ImageOptimizer(args.directory)
    
    # Clear manifest if force
    if args.force:
        optimizer.manifest = {}
    
    # Run optimization
    optimizer.optimize_all(parallel=not args.sequential)

if __name__ == '__main__':
    import html
    main()