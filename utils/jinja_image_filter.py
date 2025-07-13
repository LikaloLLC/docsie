#!/usr/bin/env python3
"""
Jinja2 filter for automatic image optimization
"""
import os
from pathlib import Path

def optimized_image(image_path, sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"):
    """
    Convert image path to optimized picture element
    
    Usage in template:
    {{ image_path | optimized_image }}
    """
    print(f"DEBUG: optimized_image filter called with: {image_path}")
    if not image_path or not isinstance(image_path, str):
        return image_path
    
    # Check if this is an optimizable image
    if not any(image_path.startswith(prefix) for prefix in ['/assets/', 'assets/']):
        return f'<img src="{image_path}" alt="" loading="lazy">'
    
    # Extract image info
    image_path = image_path.lstrip('/')
    path_parts = Path(image_path).parts
    img_name = Path(image_path).stem
    
    # Build optimized path
    # From: assets/solutions/kb-hero.jpg
    # To: assets/optimized/solutions/kb-hero-{size}w.{format}
    # Remove 'assets/' prefix and add to optimized path
    path_without_assets = image_path.replace('assets/', '', 1)
    optimized_base = f"assets/optimized/{path_without_assets.rsplit('.', 1)[0]}"
    
    # Check if optimized versions exist
    if not os.path.exists(f"{optimized_base}-320w.jpg"):
        # Fallback to original image
        return f'<img src="/{image_path}" alt="" loading="lazy">'
    
    # Build picture element
    picture_html = f'''<picture class="block w-full h-full">
  <source type="image/webp" 
          srcset="/{optimized_base}-320w.webp 320w,
                  /{optimized_base}-640w.webp 640w,
                  /{optimized_base}-768w.webp 768w,
                  /{optimized_base}-1024w.webp 1024w">
  <img src="/{optimized_base}-320w.jpg" 
       srcset="/{optimized_base}-320w.jpg 320w,
               /{optimized_base}-640w.jpg 640w,
               /{optimized_base}-768w.jpg 768w,
               /{optimized_base}-1024w.jpg 1024w"
       sizes="{sizes}"
       alt=""
       loading="lazy"
       class="w-full h-full object-cover">
</picture>'''
    
    return picture_html

def optimized_image_url(image_path, width=None):
    """
    Get optimized image URL for a specific width
    
    Usage in template:
    {{ image_path | optimized_image_url(640) }}
    """
    if not image_path or not isinstance(image_path, str):
        return image_path
    
    # Check if this is an optimizable image
    if not any(image_path.startswith(prefix) for prefix in ['/assets/', 'assets/']):
        return image_path
    
    # Extract image info
    image_path = image_path.lstrip('/')
    path_without_assets = image_path.replace('assets/', '', 1)
    optimized_base = f"assets/optimized/{path_without_assets.rsplit('.', 1)[0]}"
    
    if width:
        # Return specific width
        return f"/{optimized_base}-{width}w.jpg"
    else:
        # Return smallest size
        return f"/{optimized_base}-320w.jpg"

def register_filters(env):
    """Register custom filters with Jinja2 environment"""
    env.filters['optimized_image'] = optimized_image
    env.filters['optimized_image_url'] = optimized_image_url