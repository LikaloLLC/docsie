"""
Image Style Preview - Shows example prompts for each variation
=============================================================

This script helps preview what prompts will be generated for different
style variations without actually calling the API.
"""

import argparse
from pathlib import Path
from image_generator_v2 import STARTUP_VARIATIONS, DESIGN_COLORS

def preview_styles():
    """Preview all available style variations."""
    
    print("\n🎨 DESIGN SYSTEM COLORS")
    print("=" * 50)
    for name, value in DESIGN_COLORS.items():
        print(f"{name:15} : {value}")
    
    print("\n\n📸 STARTUP STYLE VARIATIONS")
    print("=" * 50)
    
    # Example concepts
    example_concepts = {
        'API Documentation': 'API documentation',
        'Knowledge Base': 'knowledge base',
        'AI Features': 'AI-powered documentation',
        'Training': 'training materials'
    }
    
    for style_name, variations in STARTUP_VARIATIONS.items():
        print(f"\n\n🚀 {style_name.upper()} STYLE")
        print("-" * 40)
        
        for i, variation in enumerate(variations):
            print(f"\nVariation {i + 1}:")
            # Show example with different concepts
            for concept_name, concept in example_concepts.items():
                filled = variation.format(concept=concept)
                print(f"  {concept_name:20} → {filled}")

def generate_prompt_examples(image_type='hero', count=5):
    """Generate example prompts for a specific image type."""
    
    print(f"\n\n💡 EXAMPLE PROMPTS FOR {image_type.upper()} IMAGES")
    print("=" * 50)
    
    base_style = """Flat vector isometric illustration. Clean, modern SaaS design with soft gradients. 
Color palette: soft blue (#CFE8FF), lavender (#E3D9FF), deep indigo (#2E2E8F), white background. 
Rounded UI elements, subtle shadows, floating icons in isometric perspective. 
Visual balance, minimalist layout, startup aesthetic. No text or labels."""
    
    # Map image types to preferred styles
    style_map = {
        'hero': ['innovation', 'growth', 'collaboration'],
        'case': ['collaboration', 'connection'],
        'api': ['connection', 'automation'],
        'ai': ['automation', 'innovation'],
        'support': ['collaboration', 'connection']
    }
    
    preferred_styles = style_map.get(image_type, list(STARTUP_VARIATIONS.keys()))
    
    import random
    for i in range(count):
        style = random.choice(preferred_styles)
        variations = STARTUP_VARIATIONS[style]
        prompt_template = random.choice(variations)
        
        # Example concept
        concept = "documentation platform"
        specific_prompt = prompt_template.format(concept=concept)
        
        # Add image-type specific details
        if 'hero' in image_type:
            details = "Main focal point centered, with supporting elements floating around. Hero composition."
        elif 'case' in image_type:
            details = "Real-world scenario showing the solution in action, people interacting with technology."
        elif 'api' in image_type:
            details = "API endpoints as friendly characters or geometric shapes exchanging data."
        else:
            details = "Balanced composition with primary element and supporting visual metaphors."
        
        full_prompt = f"{specific_prompt} {details} {base_style}"
        
        print(f"\n🎯 Example {i + 1} (Style: {style})")
        print(f"Prompt: {full_prompt[:200]}...")

def list_startup_concepts():
    """List common startup-specific visual concepts."""
    
    print("\n\n🏢 STARTUP VISUAL CONCEPTS")
    print("=" * 50)
    
    concepts = {
        'Growth Metaphors': [
            'Rocket ship launching',
            'Plant growing through keyboard',
            'Ascending charts and graphs',
            'Startup journey path',
            'Exponential curves'
        ],
        'Collaboration': [
            'Diverse team in workspace',
            'Remote team connections',
            'Virtual avatars collaborating',
            'Digital handshakes',
            'Team high-fives'
        ],
        'Innovation': [
            'Light bulb moments',
            'Innovation lab',
            'Startup garage',
            'AR/VR interfaces',
            'Holographic displays'
        ],
        'Automation': [
            'Friendly robots',
            'AI assistants',
            'Automated workflows',
            'Smart systems',
            'Neural networks'
        ],
        'Connection': [
            'API handshakes',
            'Data bridges',
            'Network nodes',
            'Integration flows',
            'Connected platforms'
        ]
    }
    
    for category, items in concepts.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  • {item}")

def main():
    parser = argparse.ArgumentParser(
        description='Preview image generation styles and prompts'
    )
    parser.add_argument('--type', '-t', default='hero',
                       help='Image type to preview (hero, case, api, etc.)')
    parser.add_argument('--count', '-c', type=int, default=5,
                       help='Number of example prompts to generate')
    parser.add_argument('--concepts', action='store_true',
                       help='Show startup visual concepts')
    
    args = parser.parse_args()
    
    # Show all information
    preview_styles()
    
    if args.concepts:
        list_startup_concepts()
    
    generate_prompt_examples(args.type, args.count)

if __name__ == "__main__":
    main()