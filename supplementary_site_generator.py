from staticjinja import Site
from jinja2 import Environment
import gettext
import sys
import os
import yaml
import shutil
import argparse

def is_hidden(filepath):
    """Check if a file or directory should be hidden (starts with .)"""
    filename = os.path.basename(filepath)
    return filename.startswith('.')

def copy_styles():
    """Copy component styles to output directory"""
    components_dir = 'src/.templates/components'
    output_dir = 'solutions/styles/components'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Copy component styles
    for component in os.listdir(components_dir):
        component_dir = os.path.join(components_dir, component)
        if os.path.isdir(component_dir):
            style_file = os.path.join(component_dir, 'style.css')
            if os.path.exists(style_file):
                shutil.copy2(
                    style_file, 
                    os.path.join(output_dir, f'{component}.css')
                )
    
    # Copy main supplementary page style
    shutil.copy2(
        'src/.templates/supplementary_page.css',
        'solutions/styles/supplementary_page.css'
    )

def load_component_data():
    """Load component configurations from YAML files"""
    components_data = {}
    components_dir = 'src/.templates/components'
    
    if not os.path.exists(components_dir):
        print(f"Warning: Components directory not found at {components_dir}")
        return components_data
    
    for root, _, files in os.walk(components_dir):
        for filename in files:
            if filename.endswith('.yaml'):
                try:
                    component_name = filename[:-5]  # Remove .yaml extension
                    file_path = os.path.join(root, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        components_data[component_name] = yaml.safe_load(file)
                    print(f"Loaded component data: {component_name}")
                except Exception as e:
                    print(f"Error loading component {filename}: {str(e)}")
    
    # Also load component templates
    for component_dir in os.listdir(components_dir):
        component_path = os.path.join(components_dir, component_dir)
        if os.path.isdir(component_path):
            if component_dir not in components_data:
                components_data[component_dir] = {}
            # Add template path information
            components_data[component_dir]['_template_path'] = os.path.join('components', component_dir, f'{component_dir}.html')
    
    return components_data

def load_all_supplementary_pages():
    """Load all supplementary pages from YAML files in .data directory and its subdirectories"""
    pages_data = []
    data_dir = 'src/.data'
    skipped_files = []
    
    if not os.path.exists(data_dir):
        print(f"Error: Data directory not found at {data_dir}")
        return pages_data
    
    for root, _, files in os.walk(data_dir):
        for filename in files:
            if filename.endswith('.yaml') and not is_hidden(filename):
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = yaml.safe_load(file)
                        if data is None:
                            print(f"Warning: Empty YAML file: {file_path}")
                            continue
                            
                        # If the file contains a list, extend pages_data
                        if isinstance(data, list):
                            # Enhance each page with its source file info
                            for page in data:
                                if isinstance(page, dict):
                                    page['_source_file'] = os.path.relpath(file_path, data_dir)
                                    pages_data.append(page)
                                else:
                                    print(f"Warning: Invalid page data in {file_path}")
                                    
                        # If it's a single page definition, append it
                        elif isinstance(data, dict):
                            data['_source_file'] = os.path.relpath(file_path, data_dir)
                            pages_data.append(data)
                        else:
                            print(f"Warning: Unexpected data format in {file_path}")
                            
                        print(f"Loaded {len(data) if isinstance(data, list) else 1} pages from {os.path.relpath(file_path, data_dir)}")
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")
                    skipped_files.append(file_path)
    
    if skipped_files:
        print("\nSkipped files due to errors:")
        for file in skipped_files:
            print(f"- {os.path.relpath(file, data_dir)}")
    
    print(f"\nTotal pages loaded: {len(pages_data)}")
    return pages_data

def generate_supplementary_pages(env, force_version=False, ui_version='v2'):
    """Generate supplementary pages from YAML data with component support"""
    # Use V2 template for better header/footer
    template = env.get_template('.templates/supplementary_page_v2.html')
    
    # Load all page data from YAML files
    pages_data = load_all_supplementary_pages()
    
    # Create a lookup dictionary for pages by URL
    pages_by_url = {}
    for page in pages_data:
        page_id = page.get('id', '')
        category = page.get('category', '').lower()
        if category and category != 'solutions':
            url = f"/solutions/{category}/{page_id}"
        else:
            url = f"/solutions/{page_id}"
        pages_by_url[url] = page
        # Also add with trailing slash
        pages_by_url[url + "/"] = page
    
    # Define lookup function for templates
    def get_page_by_url(url):
        """Lookup function to get page data by URL"""
        # Remove trailing slash and normalize
        clean_url = url.rstrip('/')
        return pages_by_url.get(clean_url) or pages_by_url.get(clean_url + "/")
    
    # Register the lookup function as a global in the Jinja environment
    env.globals['get_page_by_url'] = get_page_by_url
    
    # Load component configurations
    components_data = load_component_data()
    
    # Create output directory if it doesn't exist
    os.makedirs('solutions', exist_ok=True)
    
    # Copy styles before generating pages
    copy_styles()
    
    # Generate each page
    for page in pages_data:
        try:
            print(f"\nProcessing page: {page.get('id', 'unknown')}")
            
            # Override UI version if version flag is used
            if force_version:
                page['ui_version'] = ui_version
                print(f"  Forcing UI version {ui_version} for {page.get('id', 'unknown')}")
            
            # Create context with all necessary variables
            context = {
                'page': page,
                'components': components_data,
                'styles_path': '/styles',
                'get_page_by_url': get_page_by_url
            }
            
            # Debug component data
            if 'components' in page:
                print(f"Components found: {', '.join(page['components'].keys())}")
                for comp_name, comp_data in page['components'].items():
                    if isinstance(comp_data, dict) and 'items' in comp_data:
                        print(f"  {comp_name} has {len(comp_data['items'])} items")
            
            output = template.render(**context)
            
            # Create the output file with directory structure
            category = page.get('category', '').lower()
            if category and category != 'solutions':
                output_path = os.path.join('solutions', category, page['id'], 'index.html')
            else:
                output_path = os.path.join('solutions', page['id'], 'index.html')
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Write the file
            with open(output_path, 'w') as file:
                file.write(output)
            print(f"Generated: {output_path}")
            
        except Exception as e:
            print(f"Error processing page {page.get('id', 'unknown')}: {str(e)}")
            raise  # Re-raise the exception for full traceback

def verify_components():
    """Verify that all component templates exist and are accessible"""
    components = [
        'hero',
        'features',
        'gallery',
        'related',
        'reviews',
        'carousel',
        'stats',
        'comparison',
        'cta_section'
    ]
    
    missing_components = []
    for component in components:
        template_path = f'src/.templates/components/{component}/{component}.html'
        style_path = f'src/.templates/components/{component}/style.css'
        
        if not os.path.exists(template_path):
            missing_components.append(f"Template missing: {template_path}")
        if not os.path.exists(style_path):
            missing_components.append(f"Style missing: {style_path}")
    
    if missing_components:
        print("\nWarning: Missing component files:")
        for missing in missing_components:
            print(f"- {missing}")
    else:
        print("\nAll component files found successfully!")
    
    return len(missing_components) == 0

def render_site(force_version=False, ui_version='v1'):
    # Verify components first
    verify_components()
    
    # Ensure styles are copied first
    ensure_styles()
    
    # Create site with standard configuration and ignore hidden files
    site = Site.make_site(
        searchpath="src",
        env_globals={
            "render_component": lambda name, config, **kwargs: render_component_with_version(site._env, name, config, ui_version, **kwargs)
        },
        extensions=['jinja2.ext.i18n', 'jinja_markdown.MarkdownExtension']
    )
    
    # Generate supplementary pages using the same Jinja environment
    generate_supplementary_pages(site._env, force_version=force_version, ui_version=ui_version)
    print("\nSite generation completed!")

def debug_render_component(env, name, config, **kwargs):
    """Debug wrapper for component rendering with version support"""
    try:
        print(f"\nRendering component: {name}")
        print(f"Config: {config}")
        print(f"Config type: {type(config)}")
        if isinstance(config, dict):
            print(f"Config keys: {config.keys()}")
            if 'items' in config:
                print(f"Items type: {type(config['items'])}")
                print(f"Items content: {config['items']}")
        if config:
            template = env.get_template(f'.templates/components/{name}/{name}.html')
            result = template.render(section=config, **kwargs)
            print(f"Successfully rendered {name}")
            return result
        else:
            print(f"No config provided for {name}")
            return ''
    except Exception as e:
        print(f"Error rendering component {name}: {str(e)}")
        print(f"Config type: {type(config)}")
        if isinstance(config, dict):
            print(f"Config keys: {config.keys()}")
        raise

def render_component_with_version(env, name, config, ui_version='v1', **kwargs):
    """
    Generic component rendering with version support and fallbacks
    
    Args:
        env: Jinja2 environment
        name: Component name (e.g., 'hero', 'features')
        config: Component configuration
        ui_version: UI version (e.g., 'v1', 'v2', 'v3')
        **kwargs: Additional template variables
    
    Returns:
        Rendered component HTML
    """
    try:
        print(f"\nRendering component: {name} (requested version: {ui_version})")
        
        if not config:
            print(f"No config provided for {name}")
            return ''
        
        # Try to find the best version of the component
        component_versions = []
        
        # Check for specific version first (e.g., hero_v2)
        if ui_version != 'v1':
            versioned_name = f"{name}_{ui_version}"
            versioned_path = f'.templates/components/{versioned_name}/{versioned_name}.html'
            try:
                env.get_template(versioned_path)
                component_versions.append((versioned_name, versioned_path))
                print(f"Found versioned component: {versioned_name}")
            except:
                print(f"Version {ui_version} not found for {name}")
        
        # Always add v1 (original) as fallback
        original_path = f'.templates/components/{name}/{name}.html'
        try:
            env.get_template(original_path)
            component_versions.append((name, original_path))
            print(f"Found original component: {name}")
        except:
            print(f"Original component not found: {name}")
        
        # Use the first available version
        if component_versions:
            selected_name, selected_path = component_versions[0]
            print(f"Using component: {selected_name}")
            
            template = env.get_template(selected_path)
            result = template.render(section=config, **kwargs)
            print(f"Successfully rendered {selected_name}")
            return result
        else:
            print(f"No version of component {name} found")
            return f"<!-- Component {name} not found -->"
            
    except Exception as e:
        print(f"Error rendering component {name}: {str(e)}")
        print(f"Config type: {type(config)}")
        if isinstance(config, dict):
            print(f"Config keys: {config.keys()}")
        # Return fallback with error info
        return f"<!-- Error rendering {name}: {str(e)} -->"

def ensure_styles():
    """Ensure styles are in the correct location"""
    # Create styles directory if it doesn't exist
    os.makedirs('styles/components', exist_ok=True)
    
    # Start with the main supplementary page style
    styles_to_copy = {
        'src/.templates/supplementary_page.css': 'styles/supplementary_page.css'
    }
    
    # Dynamically discover all component styles
    components_dir = 'src/.templates/components'
    if os.path.exists(components_dir):
        for component_name in os.listdir(components_dir):
            component_path = os.path.join(components_dir, component_name)
            if os.path.isdir(component_path):
                style_file = os.path.join(component_path, 'style.css')
                if os.path.exists(style_file):
                    dst_path = f'styles/components/{component_name}.css'
                    styles_to_copy[style_file] = dst_path
    
    # Copy each style file
    for src, dst in styles_to_copy.items():
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            print(f"Copied style: {src} -> {dst}")
        else:
            print(f"Warning: Style file not found: {src}")

def main():
    parser = argparse.ArgumentParser(description='Generate supplementary site pages')
    parser.add_argument('--v2', action='store_true', 
                       help='Force all pages to use v2 UI components')
    parser.add_argument('--v3', action='store_true', 
                       help='Force all pages to use v3 UI components')
    parser.add_argument('--v4', action='store_true', 
                       help='Force all pages to use v4 UI components')
    parser.add_argument('--version', type=str, 
                       help='Specify UI version explicitly (e.g., v2, v3, v4)')
    
    args = parser.parse_args()
    
    # Determine the UI version
    ui_version = 'v2'  # default changed to v2
    if args.version:
        ui_version = args.version if args.version.startswith('v') else f'v{args.version}'
    elif args.v4:
        ui_version = 'v4'
    elif args.v3:
        ui_version = 'v3'
    elif args.v2:
        ui_version = 'v2'
    
    # Always force the version to ensure consistency
    force_version = True
    
    print(f"🚀 Generating all pages with {ui_version} UI components")
    
    render_site(force_version=force_version, ui_version=ui_version)

if __name__ == "__main__":
    main()