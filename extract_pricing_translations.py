#!/usr/bin/env python3
"""
Extract new translation strings from the updated pricing page.
This will help identify which strings need to be translated.
"""

import re
import json

# New translation strings from the pricing page update
NEW_PRICING_STRINGS = [
    # Plan features
    "50 AI Writing Actions/month",
    "100 AI Writing Actions/month", 
    "500 AI Writing Actions/month",
    "1000 AI Writing Actions/month",
    "In-App Help Widget",
    "Multiple In-App Help Widgets",
    "AI Chatbot",
    "50 GB Storage",
    "100 GB Storage",
    "1 TB Storage",
    "90+ Team Accounts",
    "Unlimited Workspaces",
    "10 Documentation Portals",
    "10 Custom Domains",
    
    # Additional strings that might be in the supplementary pages
    "AI-powered documentation",
    "Automated content generation",
    "Smart writing assistance",
    "Collaborative AI features",
    "Advanced analytics and insights",
    "Enterprise-grade security",
    "Priority support",
    "Dedicated account manager",
    "Custom integrations",
    "White-label options"
]

def create_translation_update_file():
    """Create a JSON file with strings that need translation"""
    
    translation_data = {
        "pricing_page_updates": {
            "new_features": NEW_PRICING_STRINGS,
            "updated_plans": {
                "standard": {
                    "name": "Standard",
                    "description": "Perfect for small teams starting their documentation journey"
                },
                "premium": {
                    "name": "Premium", 
                    "description": "Ideal for growing teams needing advanced features"
                },
                "business": {
                    "name": "Business",
                    "description": "For teams managing complex documentation at scale"
                },
                "enterprise": {
                    "name": "Enterprise",
                    "description": "Custom solutions for enterprise-grade security and control"
                }
            }
        },
        "languages_to_update": [
            "de", "es", "fr", "ja", "ko", "pt-br", "pt-pt", 
            "zh", "ru", "it", "nl", "sv", "da", "no", "fi",
            "pl", "cs", "hu", "ro", "tr", "ar", "he", "th",
            "vi", "id", "ms", "hi", "bn", "ta", "te"
        ]
    }
    
    with open('pricing_translation_updates.json', 'w', encoding='utf-8') as f:
        json.dump(translation_data, f, indent=2, ensure_ascii=False)
    
    print("Translation update file created: pricing_translation_updates.json")
    print(f"\nTotal new strings to translate: {len(NEW_PRICING_STRINGS)}")
    print("\nThese strings need to be added to:")
    print("1. The locale/messages.pot file for extraction")
    print("2. Each language's .po file for translation")
    print("3. The supplementary pages that reference pricing features")

if __name__ == "__main__":
    create_translation_update_file()
    
    # Also create a simple text file for manual review
    with open('new_pricing_strings.txt', 'w', encoding='utf-8') as f:
        f.write("New Pricing Page Translation Strings\n")
        f.write("=" * 40 + "\n\n")
        for string in NEW_PRICING_STRINGS:
            f.write(f"{string}\n")
    
    print("\nAlso created new_pricing_strings.txt for manual review")