#!/usr/bin/env python3
"""
Rebuild the pricing page with proper structure
"""

def rebuild_pricing_page():
    """Rebuild the pricing page HTML with clean structure"""
    
    # Read the current file to extract the non-duplicate sections
    with open('src/pricing_v2/index.html', 'r') as f:
        content = f.read()
    
    # Find key sections
    lines = content.split('\n')
    
    # Extract header (up to Pricing Plans section)
    header_end = -1
    for i, line in enumerate(lines):
        if '<!-- Pricing Plans -->' in line:
            header_end = i
            break
    
    # Extract footer (from ROI Value Proposition)
    roi_start = -1
    for i, line in enumerate(lines):
        if 'See the Value in Every Plan' in line and i > 150:
            # Go back to find the section start
            for j in range(i, 0, -1):
                if '<!-- ROI Value Proposition -->' in lines[j]:
                    roi_start = j
                    break
            break
    
    # Build the clean file
    clean_lines = []
    
    # Add header
    if header_end > 0:
        clean_lines.extend(lines[:header_end])
    
    # Add Pricing Plans section
    clean_lines.extend([
        '  <!-- Pricing Plans -->',
        '  <section class="py-16 bg-white">',
        '    <div class="container mx-auto max-w-7xl px-4 md:px-6">',
        '      ',
        '      <!-- Plan Tabs -->',
        '      <div class="flex justify-center mb-8">',
        '        <div class="bg-gray-100 rounded-lg p-1 flex">',
        '          <button class="px-6 py-3 rounded-md text-sm font-medium bg-white text-gray-900 shadow-sm" id="shared-plans-tab">',
        '            {% trans %}Shared Hosting Plans{% endtrans %}',
        '          </button>',
        '          <button class="px-6 py-3 rounded-md text-sm font-medium text-gray-600 hover:text-gray-900" id="private-plans-tab">',
        '            {% trans %}Dedicated Hosting{% endtrans %}',
        '          </button>',
        '        </div>',
        '      </div>',
        '',
        '      <!-- Usage Hint -->',
        '      <div class="text-center mb-12">',
        '        <p class="text-gray-600">',
        '          <svg class="w-5 h-5 inline-block text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">',
        '            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>',
        '          </svg>',
        '          {% trans %}Not sure which plan is right for you? Most teams with 5-15 members choose Premium.{% endtrans %}',
        '        </p>',
        '      </div>',
        '',
        '      <!-- Shared Plans Content -->',
        '      <div id="shared-plans-content" class="plans-content">',
        '        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">',
        '          {% include \'pricing_v2/generated_plan_cards.html\' %}',
        '        </div>',
        '      </div>',
        '',
        '      <!-- Feature Comparison Link -->',
        '      <div class="text-center mt-12">',
        '        <button id="toggle-features" class="inline-flex items-center text-blue-600 hover:text-blue-700 font-medium">',
        '          <span id="toggle-text">{% trans %}See full feature comparison{% endtrans %}</span>',
        '          <svg class="w-5 h-5 ml-2 transform transition-transform" id="toggle-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">',
        '            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>',
        '          </svg>',
        '        </button>',
        '      </div>',
        '',
        '      <!-- Collapsible Feature Comparison Table -->',
        '      <div id="features-comparison" class="hidden mt-12 overflow-x-auto">',
        '        <div class="bg-white rounded-2xl border border-gray-200 p-8">',
        '          <h3 class="text-2xl font-bold text-gray-900 mb-6">{% trans %}Detailed Feature Comparison{% endtrans %}</h3>',
        '          {% include \'pricing_v2/generated_comparison_table.html\' %}',
        '        </div>',
        '      </div>',
        '',
        '      <!-- Private Plans Content -->',
        '      <div id="private-plans-content" class="plans-content hidden">',
        '        <div class="max-w-4xl mx-auto text-center">',
        '          <div class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-12 border border-gray-200">',
        '            <div class="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl mx-auto mb-6 flex items-center justify-center">',
        '              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">',
        '                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2"/>',
        '              </svg>',
        '            </div>',
        '            <h2 class="text-3xl font-bold text-gray-900 mb-4">Dedicated Private Hosting</h2>',
        '            <p class="text-xl text-gray-600 mb-8 leading-relaxed">',
        '              Get comprehensive isolation, control, enhanced performance, and heightened security for your knowledge base with our dedicated private hosting.',
        '            </p>',
        '            <p class="text-lg text-gray-700 mb-8">',
        '              Arrange a meeting with our team to discuss your requirements and receive a personalized quote.',
        '            </p>',
        '            <button class="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 px-8 rounded-xl font-medium hover:from-blue-700 hover:to-purple-700 transition-all duration-300 text-lg" onclick="Calendly.initPopupWidget({url: \'https://calendly.com/docsie-io/demo-call\'})">',
        '              Schedule Consultation',
        '            </button>',
        '          </div>',
        '        </div>',
        '      </div>',
        '',
        '    </div>',
        '  </section>',
        ''
    ])
    
    # Add footer sections starting from ROI
    if roi_start > 0:
        # Find where the duplicate content ends in the footer sections
        footer_lines = []
        skip_duplicate = False
        
        for i in range(roi_start, len(lines)):
            line = lines[i]
            
            # Skip obvious duplicate content
            if '<li class="flex items-start">' in line and i < roi_start + 50:
                skip_duplicate = True
            elif skip_duplicate and '</li>' in line:
                continue
            elif skip_duplicate and '<section' in line:
                skip_duplicate = False
            
            if not skip_duplicate:
                footer_lines.append(line)
        
        clean_lines.extend(footer_lines)
    
    # Write the clean file
    with open('src/pricing_v2/index_clean.html', 'w') as f:
        f.write('\n'.join(clean_lines))
    
    print("Clean pricing page saved to src/pricing_v2/index_clean.html")
    print("Review the file and then move it to replace index.html")


if __name__ == '__main__':
    rebuild_pricing_page()