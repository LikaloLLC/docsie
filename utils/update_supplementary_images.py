#!/usr/bin/env python3
"""
Update supplementary pages to use optimized images
"""

import json
import yaml
from pathlib import Path
import re

class SupplementaryImageUpdater:
    def __init__(self):
        self.project_root = Path('.').resolve()
        self.manifest_path = self.project_root / 'assets' / 'images' / 'optimized' / 'manifest.json'
        
    def load_manifest(self):
        """Load optimization manifest"""
        with open(self.manifest_path, 'r') as f:
            return json.load(f)
    
    def get_optimized_picture_tag(self, original_path):
        """Get optimized picture tag for an image path"""
        manifest = self.load_manifest()
        
        # Normalize path
        if original_path.startswith('/'):
            original_path = original_path[1:]
        
        # Check if image has been optimized
        if original_path in manifest:
            return manifest[original_path]['srcset']['picture_element']
        
        # Check with project root
        full_path = str(self.project_root / original_path)
        if full_path in manifest:
            return manifest[full_path]['srcset']['picture_element']
            
        return None
    
    def update_yaml_images(self, yaml_path):
        """Update image references in YAML file"""
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        
        updated = False
        manifest = self.load_manifest()
        
        def update_image_ref(item, key='image'):
            """Update image reference to use optimized version"""
            if isinstance(item, dict) and key in item:
                original_path = item[key]
                if original_path.startswith('/'):
                    original_path = original_path[1:]
                
                # Check if optimized version exists
                for manifest_key in manifest:
                    if manifest_key.endswith(original_path.split('/')[-1]):
                        # Use the smallest optimized version as src
                        sizes = manifest[manifest_key]['sizes']
                        jpeg_sizes = [s for s in sizes if s['format'] == 'jpeg']
                        if jpeg_sizes:
                            # Store original path and srcset info without changing the main key
                            item[key + '_original'] = item[key]
                            # Don't change the original key to maintain compatibility
                            # item[key] = '/' + jpeg_sizes[0]['path']
                            item[key + '_srcset'] = manifest[manifest_key]['srcset']
                            return True
            return False
        
        # Process all items recursively
        def process_item(item):
            nonlocal updated
            if isinstance(item, dict):
                # Update various image keys
                for img_key in ['image', 'hero_image', 'background_image']:
                    if img_key in item and update_image_ref(item, img_key):
                        updated = True
                
                # Process nested items
                for value in item.values():
                    process_item(value)
            elif isinstance(item, list):
                for sub_item in item:
                    process_item(sub_item)
        
        for page in data:
            process_item(page)
        
        if updated:
            # Create backup
            backup_path = yaml_path.with_suffix('.yaml.backup')
            yaml_path.rename(backup_path)
            
            # Write updated YAML
            with open(yaml_path, 'w') as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            
            print(f"✅ Updated {yaml_path}")
            return True
        
        return False
    
    def create_picture_template_helper(self):
        """Create a Jinja2 macro for picture elements"""
        helper_content = '''{% macro picture(src, alt="", sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw", class="") -%}
{%- set img_name = src.split('/')[-1].split('.')[0] -%}
{%- set img_ext = src.split('.')[-1] -%}
<picture{% if class %} class="{{ class }}"{% endif %}>
  <source type="image/webp" 
          srcset="/assets/images/optimized/assets/solutions/{{ img_name }}-320w.webp 320w,
                  /assets/images/optimized/assets/solutions/{{ img_name }}-640w.webp 640w,
                  /assets/images/optimized/assets/solutions/{{ img_name }}-768w.webp 768w,
                  /assets/images/optimized/assets/solutions/{{ img_name }}-1024w.webp 1024w">
  <img src="/assets/images/optimized/assets/solutions/{{ img_name }}-320w.jpg" 
       srcset="/assets/images/optimized/assets/solutions/{{ img_name }}-320w.jpg 320w,
               /assets/images/optimized/assets/solutions/{{ img_name }}-640w.jpg 640w,
               /assets/images/optimized/assets/solutions/{{ img_name }}-768w.jpg 768w,
               /assets/images/optimized/assets/solutions/{{ img_name }}-1024w.jpg 1024w"
       sizes="{{ sizes }}"
       alt="{{ alt }}"
       loading="lazy">
</picture>
{%- endmacro %}

{% macro picture_from_path(path, alt="", sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw", class="") -%}
{{ picture(path.split('/')[-1], alt, sizes, class) }}
{%- endmacro %}
'''
        
        helper_path = self.project_root / 'src' / '_picture_helper.html'
        with open(helper_path, 'w') as f:
            f.write(helper_content)
        
        print(f"✅ Created picture helper macro at {helper_path}")
    
    def update_templates(self):
        """Update template files to use optimized images"""
        templates_dir = self.project_root / 'src' / '.templates' / 'supplementary'
        
        if not templates_dir.exists():
            print(f"❌ Templates directory not found: {templates_dir}")
            return
        
        # Find all template files
        templates = list(templates_dir.glob('**/*.html'))
        
        for template in templates:
            with open(template, 'r') as f:
                content = f.read()
            
            # Pattern to match img tags with solution images
            img_pattern = r'<img\s+([^>]*?)src="(/assets/solutions/[^"]+)"([^>]*?)>'
            
            updated_content = content
            matches = list(re.finditer(img_pattern, content))
            
            if matches:
                print(f"🔄 Processing {template.name}")
                
                for match in reversed(matches):  # Process in reverse to maintain positions
                    full_match = match.group(0)
                    before_src = match.group(1)
                    img_src = match.group(2)
                    after_src = match.group(3)
                    
                    # Extract image name
                    img_name = img_src.split('/')[-1].split('.')[0]
                    
                    # Build picture element
                    picture_tag = f'''<picture>
  <source type="image/webp" 
          srcset="/assets/images/optimized/assets/solutions/{img_name}-320w.webp 320w,
                  /assets/images/optimized/assets/solutions/{img_name}-640w.webp 640w,
                  /assets/images/optimized/assets/solutions/{img_name}-768w.webp 768w,
                  /assets/images/optimized/assets/solutions/{img_name}-1024w.webp 1024w">
  <img {before_src}src="/assets/images/optimized/assets/solutions/{img_name}-320w.jpg"
       srcset="/assets/images/optimized/assets/solutions/{img_name}-320w.jpg 320w,
               /assets/images/optimized/assets/solutions/{img_name}-640w.jpg 640w,
               /assets/images/optimized/assets/solutions/{img_name}-768w.jpg 768w,
               /assets/images/optimized/assets/solutions/{img_name}-1024w.jpg 1024w"
       sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"{after_src}>
</picture>'''
                    
                    # Replace in content
                    updated_content = updated_content[:match.start()] + picture_tag + updated_content[match.end():]
                
                # Write updated content
                with open(template, 'w') as f:
                    f.write(updated_content)
                
                print(f"✅ Updated {template.name} with {len(matches)} optimized images")

def main():
    updater = SupplementaryImageUpdater()
    
    # Create picture helper macro
    updater.create_picture_template_helper()
    
    # Update YAML files
    yaml_files = [
        'src/.data/supplementary_pages.yaml',
        'src/.data/_es/supplementary_pages.yaml',
        'src/.data/_fr/supplementary_pages.yaml',
        'src/.data/_de/supplementary_pages.yaml',
        'src/.data/_pt/supplementary_pages.yaml',
        'src/.data/_ko/supplementary_pages.yaml',
        'src/.data/_ja/supplementary_pages.yaml',
    ]
    
    for yaml_file in yaml_files:
        yaml_path = updater.project_root / yaml_file
        if yaml_path.exists():
            updater.update_yaml_images(yaml_path)
    
    # Update templates
    updater.update_templates()
    
    print("\n🎉 Image optimization update complete!")
    print("Next steps:")
    print("1. Review the changes in the YAML files")
    print("2. Regenerate the supplementary pages with: python supplementary_site_generator.py")
    print("3. Test the pages locally to ensure images load correctly")

if __name__ == '__main__':
    main()