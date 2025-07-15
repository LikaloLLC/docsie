#!/usr/bin/env python3
"""
Generate pricing page content from configuration file.
This script reads the pricing configuration and generates the HTML content
for the pricing_v2 page with properly formatted entitlements.
"""

import json
import os
from typing import Dict, List, Any

def load_pricing_config(config_path: str = "pricing_config.json") -> Dict[str, Any]:
    """Load pricing configuration from JSON file"""
    with open(config_path, 'r') as f:
        return json.load(f)

def format_price(price: int) -> str:
    """Format price from cents to dollars"""
    return f"${price / 100:,.0f}" if price else "Free"

def generate_plan_html(plan_id: str, plan_data: Dict[str, Any], is_most_popular: bool = False) -> str:
    """Generate HTML for a single pricing plan"""
    
    # Determine border and badge styling
    border_class = "border-2 border-blue-500" if is_most_popular else "border border-gray-200"
    
    # Popular badge
    popular_badge = ""
    if is_most_popular:
        popular_badge = """
            <div class="absolute -top-4 left-1/2 transform -translate-x-1/2">
              <span class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-4 py-2 text-sm font-medium rounded-full">{% trans %}Most Popular{% endtrans %}</span>
            </div>"""
    
    # Icon and color based on plan
    icon_colors = {
        "standard": ("green", "M13 10V3L4 14h7v7l9-11h-7z"),
        "premium": ("blue", "M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"),
        "business": ("purple", "M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"),
        "organization": ("gray", "M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.031 9-11.622 0-1.042-.133-2.052-.382-3.016z")
    }
    
    color, icon_path = icon_colors.get(plan_id, ("gray", ""))
    
    # Price display
    if plan_id == "organization":
        price_display = """
            <div class="text-center mb-6">
              <div class="text-3xl font-bold text-gray-900">{% trans %}Custom Pricing{% endtrans %}</div>
              <div class="text-gray-600 text-sm"></div>
            </div>"""
        cta_text = "{% trans %}Talk to Sales{% endtrans %}"
    else:
        monthly_price = plan_data['price']['monthly']
        yearly_price = plan_data['price']['yearly']
        yearly_monthly = yearly_price // 12
        
        price_display = f"""
            <div class="text-center mb-6">
              <div class="text-3xl font-bold text-gray-900" id="{plan_id}-price">${yearly_monthly}</div>
              <div class="text-gray-600 text-sm" id="{plan_id}-period">{{% trans %}}/per month{{% endtrans %}}</div>
              <div class="text-xs text-gray-600 mt-1" id="{plan_id}-billing">{{% trans %}}billed annually{{% endtrans %}}</div>
            </div>"""
        cta_text = "{% trans %}Book Demo{% endtrans %}"
    
    # Generate feature list
    features_html = ""
    for feature in plan_data['highlighted_features']:
        features_html += f"""
              <li class="flex items-start">
                <svg class="w-5 h-5 text-green-600 mr-3 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                <span class="text-gray-700 text-sm">{{% trans %}}{feature}{{% endtrans %}}</span>
              </li>"""
    
    # Generate the complete plan card
    return f"""
          <!-- {plan_data['name']} Plan -->
          <div class="pricing-card bg-white rounded-2xl {border_class} shadow-sm hover:shadow-lg transition-all duration-300 p-8 relative">
            {popular_badge}
            
            <div class="text-center mb-6{' mt-4' if is_most_popular else ''}">
              <div class="w-12 h-12 bg-gradient-to-r from-{color}-500 to-{color}-600 rounded-xl mx-auto mb-4 flex items-center justify-center">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{icon_path}"/>
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900 mb-2">{{% trans %}}{plan_data['name']}{{% endtrans %}}</h3>
              <p class="text-gray-600 text-sm">{{% trans %}}{plan_data['description']}{{% endtrans %}}</p>
            </div>
            
            {price_display}

            <button class="w-full bg-gradient-to-r from-{color if plan_id != 'organization' else 'gray'}-600 to-{color if plan_id != 'organization' else 'gray'}-{'700' if plan_id != 'organization' else '900'} text-white py-3 px-6 rounded-xl font-medium hover:from-{color if plan_id != 'organization' else 'gray'}-700 hover:to-{color if plan_id != 'organization' else 'gray'}-{'800' if plan_id != 'organization' else 'black'} transition-all duration-300 mb-6" onclick="Calendly.initPopupWidget({{url: 'https://calendly.com/docsie-io/demo-call'}})">
              {cta_text}
            </button>

            <ul class="space-y-3">
{features_html}
            </ul>
          </div>"""

def generate_feature_comparison_table(config: Dict[str, Any]) -> str:
    """Generate the detailed feature comparison table"""
    
    # This would generate a comprehensive comparison table
    # For now, returning a placeholder
    return """
              <!-- Feature comparison table would go here -->
              <div class="text-center text-gray-600">
                <p>{% trans %}Detailed feature comparison coming soon{% endtrans %}</p>
              </div>"""

def update_pricing_page(config: Dict[str, Any]):
    """Update the pricing_v2 page with new configuration"""
    
    # Generate plan cards HTML
    plans_html = ""
    plan_order = ["standard", "premium", "business", "organization"]
    
    for plan_id in plan_order:
        if plan_id in config['plans']:
            plan_data = config['plans'][plan_id]
            is_most_popular = plan_data.get('mostPopular', False)
            plans_html += generate_plan_html(plan_id, plan_data, is_most_popular)
    
    # Update the pricing toggle JavaScript to use new plan IDs
    pricing_js = """
  // Update prices based on toggle state
  function updatePrices(isAnnual) {
    const plans = {
      'standard': { monthly: 45, yearly: 399 },
      'premium': { monthly: 199, yearly: 2040 },
      'business': { monthly: 449, yearly: 2988 },
      'organization': { monthly: 900, yearly: 8388 }
    };
    
    Object.keys(plans).forEach(planId => {
      const priceEl = document.getElementById(`${planId}-price`);
      const periodEl = document.getElementById(`${planId}-period`);
      const billingEl = document.getElementById(`${planId}-billing`);
      
      if (priceEl && periodEl && billingEl) {
        if (isAnnual) {
          const monthlyEquivalent = Math.round(plans[planId].yearly / 12);
          priceEl.textContent = '$' + monthlyEquivalent;
          periodEl.textContent = '/per month';
          billingEl.textContent = 'billed annually';
        } else {
          priceEl.textContent = '$' + plans[planId].monthly;
          periodEl.textContent = '/per month';
          billingEl.textContent = 'billed monthly';
        }
      }
    });
    
    // Update label styles
    if (isAnnual) {
      monthlyLabel.className = 'px-4 py-2 text-sm font-medium text-gray-600';
      annualLabel.className = 'px-4 py-2 text-sm font-medium text-blue-600 font-semibold';
    } else {
      monthlyLabel.className = 'px-4 py-2 text-sm font-medium text-blue-600 font-semibold';
      annualLabel.className = 'px-4 py-2 text-sm font-medium text-gray-600';
    }
  }"""
    
    print("Pricing page configuration generated successfully!")
    print("\nKey changes needed in pricing_v2/index.html:")
    print("1. Replace the current plan cards with the generated HTML")
    print("2. Update the pricing toggle JavaScript")
    print("3. Add proper translation tags for all new features")
    print("\nGenerated plans HTML structure is ready to be integrated.")
    
    # Save the generated HTML for reference
    with open('generated_pricing_plans.html', 'w') as f:
        f.write(plans_html)
    
    with open('pricing_toggle_update.js', 'w') as f:
        f.write(pricing_js)

if __name__ == "__main__":
    config = load_pricing_config()
    update_pricing_page(config)