#!/usr/bin/env python3
"""
Generate pricing HTML from configuration file
"""
import json
import os


def load_config(config_path):
    """Load pricing configuration from JSON file"""
    with open(config_path, 'r') as f:
        return json.load(f)


def generate_pricing_context(config):
    """Generate context for pricing components"""
    context = {
        'starter_features': [
            {
                'name': 'Up to 5 team members',
                'description': 'Perfect for small teams'
            },
            {
                'name': '2 documentation sites',
                'description': 'Multiple product docs'
            },
            {
                'name': '2 custom domains',
                'description': 'Professional branding'
            },
            {
                'name': '50 AI writing assists/month',
                'description': 'Content creation help'
            },
            {
                'name': '40K auto-translations/month',
                'description': 'Global reach'
            },
            {
                'name': '3 GB storage',
                'description': 'Store docs, images & videos'
            },
            {
                'name': 'Templates & collaboration tools',
                'description': 'Get started fast'
            },
            {
                'name': 'Email support',
                'description': 'Get help when needed'
            }
        ],
        'premium_features': [
            {
                'name': 'Up to 15 team members',
                'description': 'Scale your team'
            },
            {
                'name': '3 documentation sites',
                'description': 'More products/services'
            },
            {
                'name': '100 AI writing assists/month',
                'description': '2x more content help'
            },
            {
                'name': 'Snippets (Reusable content)',
                'description': 'Save time with reusable blocks',
                'highlight': True
            },
            {
                'name': 'Ghost translations',
                'description': 'Instant multilingual docs',
                'highlight': True
            },
            {
                'name': 'Project management tools',
                'description': 'Organize workflows',
                'highlight': True
            },
            {
                'name': 'Advanced file manager',
                'description': 'Better asset organization'
            },
            {
                'name': 'In-app help widget',
                'description': 'Reduce support tickets by 40%'
            },
            {
                'name': '80K auto-translations/month',
                'description': '2x translation power'
            },
            {
                'name': '50 GB storage',
                'description': '16x more space'
            },
            {
                'name': 'Priority email support',
                'description': 'Faster response times'
            }
        ],
        'business_features': [
            {
                'name': 'Up to 40 team members',
                'description': 'Large team collaboration'
            },
            {
                'name': '5 documentation sites',
                'description': 'Multiple product lines'
            },
            {
                'name': '500 AI writing assists/month',
                'description': '5x content creation'
            },
            {
                'name': '24/7 AI chatbot support',
                'description': 'Instant customer help',
                'highlight': True
            },
            {
                'name': 'Image annotation tools',
                'description': 'Visual documentation'
            },
            {
                'name': 'Advanced analytics dashboard',
                'description': 'Track performance'
            },
            {
                'name': 'Granular permissions',
                'description': 'Control who sees what'
            },
            {
                'name': 'Editorial style guide',
                'description': 'Consistent brand voice'
            },
            {
                'name': 'Support ticket system',
                'description': 'Integrated customer service'
            },
            {
                'name': '1.6M auto-translations/month',
                'description': 'Enterprise-scale translation'
            },
            {
                'name': '100 GB storage',
                'description': 'Massive file capacity'
            },
            {
                'name': 'Phone + priority support',
                'description': 'Direct access to experts'
            }
        ],
        'enterprise_features': [
            {
                'name': '90+ team members',
                'description': 'Unlimited collaboration'
            },
            {
                'name': '10 separate workspaces',
                'description': 'Department isolation'
            },
            {
                'name': '1000 AI writing assists/month',
                'description': 'Maximum productivity'
            },
            {
                'name': 'Multiple help widgets',
                'description': 'Product-specific support'
            },
            {
                'name': 'SAML/SSO integration',
                'description': 'Enterprise security'
            },
            {
                'name': 'IDML export',
                'description': 'Professional publishing'
            },
            {
                'name': 'Dedicated success manager',
                'description': 'White-glove support'
            },
            {
                'name': '3.2M characters auto-translations/month',
                'description': 'Global enterprise scale'
            },
            {
                'name': '1 TB storage',
                'description': 'Enterprise-grade capacity'
            },
            {
                'name': '99.9% SLA guarantee',
                'description': 'Mission-critical uptime'
            },
            {
                'name': 'Custom integrations',
                'description': 'Connect your tech stack'
            }
        ]
    }
    return context

def generate_plan_card(plan_id, plan_data, all_plans):
    """Generate HTML for a single pricing plan card"""
    
    # Determine color classes based on plan color
    color_map = {
        'green': {
            'bg': 'from-green-500 to-green-600',
            'button': 'from-green-600 to-green-700',
            'button_hover': 'from-green-700 to-green-800',
            'badge_bg': 'bg-green-50',
            'badge_border': 'border-green-200',
            'badge_text': 'text-green-700'
        },
        'blue': {
            'bg': 'from-blue-500 to-blue-600',
            'button': 'from-blue-600 to-blue-700',
            'button_hover': 'from-blue-700 to-blue-800',
            'badge_bg': 'bg-blue-50',
            'badge_border': 'border-blue-200',
            'badge_text': 'text-blue-700'
        },
        'purple': {
            'bg': 'from-purple-500 to-purple-600',
            'button': 'from-purple-600 to-purple-700',
            'button_hover': 'from-purple-700 to-purple-800',
            'badge_bg': 'bg-purple-50',
            'badge_border': 'border-purple-200',
            'badge_text': 'text-purple-700'
        },
        'gray': {
            'bg': 'from-gray-700 to-gray-900',
            'button': 'from-gray-700 to-gray-900',
            'button_hover': 'from-gray-800 to-black',
            'badge_bg': 'bg-gray-800',
            'badge_border': '',
            'badge_text': 'text-white'
        }
    }
    
    colors = color_map.get(plan_data.get('color', 'gray'))
    
    # Start building the card HTML
    html_parts = []
    
    # Card wrapper
    card_classes = "pricing-card bg-white rounded-2xl shadow-sm hover:shadow-lg transition-all duration-300 p-8 relative"
    if plan_data.get('is_popular'):
        card_classes = "pricing-card bg-white rounded-2xl border-2 border-blue-500 shadow-lg hover:shadow-xl transition-all duration-300 p-8 relative"
    elif plan_id == 'enterprise':
        card_classes = "pricing-card bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl border border-gray-300 shadow-sm hover:shadow-lg transition-all duration-300 p-8 relative"
    else:
        card_classes += " border border-gray-200"
    
    html_parts.append(f'<!-- {plan_data["name"]} Plan -->')
    html_parts.append(f'<div class="{card_classes}">')
    
    # Popular badge
    if plan_data.get('is_popular'):
        html_parts.append("""  <div class="absolute -top-3 left-1/2 transform -translate-x-1/2">
    <span class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-3 py-1.5 text-xs font-medium rounded-full">{% trans %}MOST POPULAR{% endtrans %}</span>
  </div>""")
    
    # Social proof badge (skip for premium since it already has MOST POPULAR)
    if plan_data.get('badge') and not plan_data.get('is_popular'):
        badge_position = "right-4" if plan_id == 'enterprise' else "left-1/2 transform -translate-x-1/2"
        badge_style = f"""  <div class="absolute -top-3 {badge_position}">
    <div class="{colors['badge_bg']} {colors['badge_border']} rounded-full px-3 py-1 text-xs font-medium {colors['badge_text']}">
      {{% trans %}}{plan_data['badge']}{{% endtrans %}}
    </div>
  </div>"""
        html_parts.append(badge_style)
    
    # Plan header
    mt_class = "mt-4" if plan_data.get('is_popular') or plan_data.get('badge') else ""
    html_parts.append(f"""  
  <div class="text-center mb-6 {mt_class}">
    <div class="w-12 h-12 bg-gradient-to-r {colors['bg']} rounded-xl mx-auto mb-4 flex items-center justify-center">
      <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{plan_data['icon']}"/>
      </svg>
    </div>
    <h3 class="text-xl font-semibold text-gray-900 mb-2">{{% trans %}}{plan_data['name']}{{% endtrans %}}</h3>
    <p class="text-gray-600 text-sm">{{% trans %}}{plan_data['description']}{{% endtrans %}}</p>
  </div>""")
    
    # Pricing
    if plan_data['pricing'].get('contact'):
        html_parts.append("""  
  <div class="text-center mb-6">
    <div class="text-3xl font-bold text-gray-900">{% trans %}Contact Us{% endtrans %}</div>
    <div class="text-gray-600 text-sm">{% trans %}for pricing details{% endtrans %}</div>
  </div>""")
    elif plan_data['pricing'].get('custom'):
        html_parts.append("""  
  <div class="text-center mb-6">
    <div class="text-2xl font-bold text-gray-900">{% trans %}Custom Pricing{% endtrans %}</div>
    <div class="text-gray-600 text-sm">{% trans %}Tailored to your needs{% endtrans %}</div>
  </div>""")
    else:
        monthly_price = plan_data['pricing']['monthly']
        annual_price = plan_data['pricing']['annual']
        annual_monthly = round(annual_price / 12)
        savings_percent = round((1 - (annual_monthly / monthly_price)) * 100)
        
        html_parts.append(f"""  
  <div class="text-center mb-6">
    <div class="text-sm text-gray-600 mb-2">
      <span class="monthly-price" style="display:none;">
        <span class="text-2xl font-bold text-gray-900">${monthly_price}</span>
        <span class="text-gray-600">{{% trans %}}/month{{% endtrans %}}</span>
      </span>
      <span class="annual-price">
        <span class="text-2xl font-bold text-gray-900">${annual_monthly}</span>
        <span class="text-gray-600">{{% trans %}}/month{{% endtrans %}}</span>
        <span class="text-xs text-green-600 font-medium ml-2">{{% trans %}}(Save {savings_percent}%){{% endtrans %}}</span>
      </span>
    </div>
    <div class="text-xs text-gray-500">
      <span class="monthly-price" style="display:none;">{{% trans %}}Billed monthly{{% endtrans %}}</span>
      <span class="annual-price">{{% trans %}}Billed ${annual_price} annually{{% endtrans %}}</span>
    </div>
  </div>""")
    
    # CTA Button
    button_text = "Talk to Sales" if plan_id == 'enterprise' else "Book Demo"
    html_parts.append(f"""
  <button class="w-full bg-gradient-to-r {colors['button']} text-white py-3 px-6 rounded-xl font-medium hover:{colors['button_hover']} transition-all duration-300 mb-6" onclick="Calendly.initPopupWidget({{url: 'https://calendly.com/docsie-io/demo-call'}})">
    {{% trans %}}{button_text}{{% endtrans %}}
  </button>""")
    
    # Features header
    if plan_data.get('features_inherit'):
        inherit_plan = all_plans[plan_data['features_inherit']]
        html_parts.append(f"""
  <div class="mb-4">
    <p class="text-sm font-semibold text-gray-900 mb-3">{{% trans %}}Everything in {inherit_plan['name']}, plus:{{% endtrans %}}</p>
  </div>""")
    else:
        html_parts.append("""
  <div class="mb-4">
    <p class="text-sm font-semibold text-gray-900 mb-3">{% trans %}What you get:{% endtrans %}</p>
  </div>""")
    
    # Features list
    html_parts.append("""
  <ul class="space-y-3">""")
    
    for feature in plan_data['features']:
        # Use different styling for highlighted features instead of stars
        if feature.get('highlight'):
            feature_html = f"""    <li class="flex items-start">
      <svg class="w-5 h-5 text-blue-600 mr-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
      </svg>
      <span class="text-gray-700 text-sm"><strong class="text-blue-600">{{% trans %}}{feature['name']}{{% endtrans %}}</strong> - {{% trans %}}{feature['description']}{{% endtrans %}}</span>
    </li>"""
        else:
            feature_html = f"""    <li class="flex items-start">
      <svg class="w-5 h-5 text-green-600 mr-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
      </svg>
      <span class="text-gray-700 text-sm"><strong>{{% trans %}}{feature['name']}{{% endtrans %}}</strong> - {{% trans %}}{feature['description']}{{% endtrans %}}</span>
    </li>"""
        html_parts.append(feature_html)
    
    html_parts.append("  </ul>")
    
    # Footer section
    footer_parts = []
    if plan_data.get('perfect_for'):
        footer_parts.append(f'    <p class="text-xs text-gray-600 text-center font-medium">{{% trans %}}Perfect for: {plan_data["perfect_for"]}{{% endtrans %}}</p>')
    
    if plan_data.get('upgrade_stat'):
        footer_parts.append(f'    <p class="text-xs text-blue-600 text-center font-semibold mt-2">{{% trans %}}{plan_data["upgrade_stat"]}{{% endtrans %}}</p>')
    
    if plan_data.get('trust_stat'):
        footer_parts.append(f'    <p class="text-xs text-purple-600 text-center font-semibold mt-2">{{% trans %}}{plan_data["trust_stat"]}{{% endtrans %}}</p>')
    
    if footer_parts:
        html_parts.append("""
  <div class="mt-6 pt-4 border-t border-gray-100">""")
        html_parts.extend(footer_parts)
        html_parts.append("  </div>")
    
    html_parts.append("</div>")
    
    return '\n'.join(html_parts)


def generate_comparison_table(config):
    """Generate the feature comparison table"""
    html_parts = []
    
    html_parts.append("""<table class="w-full">
  <thead>
    <tr class="border-b border-gray-200">
      <th class="text-left py-4 px-4 font-medium text-gray-900">{% trans %}Features{% endtrans %}</th>
      <th class="text-center py-4 px-4 font-medium text-gray-900">{% trans %}Premium{% endtrans %}</th>
      <th class="text-center py-4 px-4 font-medium text-gray-900">{% trans %}Enterprise{% endtrans %}</th>
    </tr>
  </thead>
  <tbody>""")

    for category in config['comparison_features']:
        # Category header
        html_parts.append(f"""    <tr class="bg-gray-50">
      <td colspan="3" class="py-3 px-4 font-semibold text-gray-900">{{% trans %}}{category['category']}{{% endtrans %}}</td>
    </tr>""")
        
        # Features in category
        for feature in category['features']:
            html_parts.append(f"""    <tr class="border-b border-gray-100">
      <td class="py-4 px-4 text-gray-700">{{% trans %}}{feature['name']}{{% endtrans %}}</td>
      <td class="text-center py-4 px-4">{feature.get('premium', '—')}</td>
      <td class="text-center py-4 px-4">{feature.get('enterprise', '—')}</td>
    </tr>""")
    
    html_parts.append("""  </tbody>
</table>""")
    
    return '\n'.join(html_parts)


def main():
    # Load configuration
    config_path = 'src/pricing_v2/pricing_plans_config.json'
    config = load_config(config_path)
    
    # Generate pricing context
    print("Generating pricing context...")
    context = generate_pricing_context(config)
    
    # Save context as JSON for use in templates
    import json
    with open('src/pricing_v2/pricing_context.json', 'w') as f:
        json.dump(context, f, indent=2)
    print("✓ Saved pricing context to src/pricing_v2/pricing_context.json")
    
    # Generate comparison table (keeping this for now)
    print("Generating comparison table...")
    table_html = generate_comparison_table(config)
    
    # Save comparison table
    with open('src/pricing_v2/generated_comparison_table.html', 'w') as f:
        f.write(table_html)
    print("✓ Saved comparison table to src/pricing_v2/generated_comparison_table.html")
    
    print("\nDone! The pricing page now uses modular V2 components.")


if __name__ == '__main__':
    main()