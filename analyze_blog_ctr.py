#!/usr/bin/env python3
"""
Analyze blog CTR performance and identify optimization opportunities
Also checks for potential crawl budget issues
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
from collections import defaultdict

# Add BlogVi to path
sys.path.insert(0, str(Path(__file__).parent / '.external/BlogVi/src'))

from blog_vi.core.gsc_integration import GSCIntegration

def analyze_blog_performance():
    """Comprehensive blog CTR and crawl budget analysis"""
    
    print("🔍 Analyzing Docsie Blog Performance...")
    print("=" * 80)
    
    # Initialize GSC
    gsc = GSCIntegration(
        credentials_path="/Users/philippetrounev/PycharmProjects/docsie-site/docsie-io-0f57d9e21566.json",
        site_url="sc-domain:docsie.io"
    )
    
    # Fetch 90 days of data for better insights
    end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    
    print(f"📊 Analyzing data from {start_date} to {end_date}")
    
    # Fetch all data
    all_data = gsc.fetch_performance_data(
        start_date=start_date,
        end_date=end_date,
        row_limit=25000  # Max allowed
    )
    
    # Filter for blog pages only
    blog_data = [row for row in all_data if '/blog/' in row['keys'][0]]
    
    print(f"\n📝 Found {len(blog_data)} blog-related queries")
    
    # Analyze by page type
    analyze_by_page_type(blog_data)
    
    # CTR Analysis
    analyze_ctr_performance(blog_data)
    
    # Crawl Budget Analysis
    analyze_crawl_budget(blog_data, all_data)
    
    # Top performing content
    analyze_top_content(blog_data)
    
    # Generate actionable recommendations
    generate_recommendations(blog_data)

def analyze_by_page_type(data):
    """Categorize and analyze different page types"""
    page_types = {
        'articles': [],
        'categories': [],
        'glossary': [],
        'term_pages': [],
        'main_blog': []
    }
    
    for row in data:
        url = row['keys'][0]
        
        if '/blog/glossary/' in url and url.count('/') > 5:
            page_types['term_pages'].append(row)
        elif '/blog/glossary/' in url:
            page_types['glossary'].append(row)
        elif '/blog/articles/' in url:
            page_types['articles'].append(row)
        elif url.endswith('/blog/'):
            page_types['main_blog'].append(row)
        else:
            # Likely category pages
            page_types['categories'].append(row)
    
    print("\n📂 Performance by Page Type:")
    print("-" * 60)
    
    for page_type, rows in page_types.items():
        if not rows:
            continue
            
        total_clicks = sum(r['clicks'] for r in rows)
        total_impressions = sum(r['impressions'] for r in rows)
        avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        avg_position = sum(r['position'] for r in rows) / len(rows) if rows else 0
        
        print(f"\n{page_type.replace('_', ' ').title()}:")
        print(f"  Pages: {len(set(r['keys'][0] for r in rows))}")
        print(f"  Impressions: {total_impressions:,}")
        print(f"  Clicks: {total_clicks:,}")
        print(f"  CTR: {avg_ctr:.2f}%")
        print(f"  Avg Position: {avg_position:.1f}")

def analyze_ctr_performance(data):
    """Detailed CTR analysis"""
    print("\n🎯 CTR Optimization Opportunities:")
    print("-" * 60)
    
    # Aggregate by page
    page_stats = defaultdict(lambda: {
        'clicks': 0,
        'impressions': 0,
        'positions': [],
        'queries': []
    })
    
    for row in data:
        page = row['keys'][0]
        page_stats[page]['clicks'] += row['clicks']
        page_stats[page]['impressions'] += row['impressions']
        page_stats[page]['positions'].append(row['position'])
        page_stats[page]['queries'].append({
            'query': row['keys'][1],
            'impressions': row['impressions'],
            'clicks': row['clicks'],
            'ctr': row['ctr'],
            'position': row['position']
        })
    
    # Find worst CTR pages with high impressions
    low_ctr_pages = []
    for page, stats in page_stats.items():
        if stats['impressions'] >= 1000:  # Significant traffic
            ctr = stats['clicks'] / stats['impressions'] if stats['impressions'] > 0 else 0
            avg_position = sum(stats['positions']) / len(stats['positions'])
            
            if ctr < 0.02:  # Less than 2% CTR
                low_ctr_pages.append({
                    'page': page,
                    'impressions': stats['impressions'],
                    'clicks': stats['clicks'],
                    'ctr': ctr,
                    'avg_position': avg_position,
                    'top_queries': sorted(stats['queries'], 
                                         key=lambda x: x['impressions'], 
                                         reverse=True)[:3]
                })
    
    low_ctr_pages.sort(key=lambda x: x['impressions'], reverse=True)
    
    print(f"\n🚨 Found {len(low_ctr_pages)} pages with CTR < 2% and 1000+ impressions")
    
    for i, page in enumerate(low_ctr_pages[:10], 1):
        print(f"\n{i}. {page['page'].replace('https://www.docsie.io', '')}")
        print(f"   Impressions: {page['impressions']:,} | Clicks: {page['clicks']}")
        print(f"   CTR: {page['ctr']:.2%} | Avg Position: {page['avg_position']:.1f}")
        print("   Top queries:")
        for q in page['top_queries']:
            print(f"     - '{q['query']}' ({q['impressions']} impr, pos {q['position']:.1f})")

def analyze_crawl_budget(blog_data, all_data):
    """Check for potential crawl budget issues"""
    print("\n🕷️ Crawl Budget Analysis:")
    print("-" * 60)
    
    # Count unique pages
    all_pages = set(row['keys'][0] for row in all_data)
    blog_pages = set(row['keys'][0] for row in blog_data)
    
    print(f"\nTotal indexed pages: {len(all_pages):,}")
    print(f"Blog pages: {len(blog_pages):,}")
    print(f"Blog percentage: {len(blog_pages)/len(all_pages)*100:.1f}%")
    
    # Check for low-value pages getting traffic
    low_value_patterns = [
        '/page/', '/tag/', '?', '#', '/feed/', '/amp/',
        '/print/', '/pdf/', '/comment-page-'
    ]
    
    low_value_pages = []
    for row in all_data:
        url = row['keys'][0]
        if any(pattern in url for pattern in low_value_patterns):
            low_value_pages.append(row)
    
    if low_value_pages:
        total_lv_impressions = sum(r['impressions'] for r in low_value_pages)
        print(f"\n⚠️  Low-value pages found: {len(set(r['keys'][0] for r in low_value_pages))}")
        print(f"   Wasting {total_lv_impressions:,} impressions")
        print("   Consider: robots.txt blocking or noindex tags")
    
    # Check term pages impact
    term_pages = [row for row in blog_data if '/blog/glossary/' in row['keys'][0] 
                  and row['keys'][0].count('/') > 5]
    
    if term_pages:
        term_impressions = sum(r['impressions'] for r in term_pages)
        term_pages_count = len(set(r['keys'][0] for r in term_pages))
        
        print(f"\n📚 Term Pages Impact:")
        print(f"   Count: {term_pages_count}")
        print(f"   Total impressions: {term_impressions:,}")
        print(f"   Avg impressions per page: {term_impressions/term_pages_count:.1f}")
        
        if term_impressions/term_pages_count < 10:
            print("   ⚠️  Low traffic - may impact crawl budget")
            print("   Consider: Consolidating or noindexing low-value terms")

def analyze_top_content(data):
    """Identify top performing content"""
    print("\n🏆 Top Performing Blog Content:")
    print("-" * 60)
    
    # Aggregate by page
    page_performance = defaultdict(lambda: {'clicks': 0, 'impressions': 0})
    
    for row in data:
        page = row['keys'][0]
        page_performance[page]['clicks'] += row['clicks']
        page_performance[page]['impressions'] += row['impressions']
    
    # Sort by clicks
    top_pages = sorted(page_performance.items(), 
                      key=lambda x: x[1]['clicks'], 
                      reverse=True)[:10]
    
    print("\nTop 10 pages by clicks:")
    for i, (page, stats) in enumerate(top_pages, 1):
        ctr = stats['clicks'] / stats['impressions'] if stats['impressions'] > 0 else 0
        print(f"{i}. {page.replace('https://www.docsie.io/blog/', '/blog/')}")
        print(f"   Clicks: {stats['clicks']:,} | CTR: {ctr:.2%}")

def generate_recommendations(data):
    """Generate actionable recommendations"""
    print("\n💡 Actionable Recommendations:")
    print("=" * 80)
    
    recommendations = []
    
    # Check average CTR
    total_clicks = sum(r['clicks'] for r in data)
    total_impressions = sum(r['impressions'] for r in data)
    avg_ctr = total_clicks / total_impressions if total_impressions > 0 else 0
    
    print(f"\nOverall Blog CTR: {avg_ctr:.2%}")
    
    if avg_ctr < 0.02:
        recommendations.append({
            'priority': 'HIGH',
            'issue': 'Low overall CTR',
            'action': 'Review and optimize meta titles/descriptions across all blog posts'
        })
    
    # Check for term pages performance
    term_pages = [r for r in data if '/blog/glossary/' in r['keys'][0] 
                  and r['keys'][0].count('/') > 5]
    
    if term_pages:
        term_impressions = sum(r['impressions'] for r in term_pages)
        if term_impressions < 10000:  # Low traffic to term pages
            recommendations.append({
                'priority': 'MEDIUM',
                'issue': f'Term pages getting low traffic ({term_impressions:,} impressions)',
                'action': 'Consider consolidating term pages or improving internal linking'
            })
    
    # Position improvements
    near_first_page = [r for r in data if 4 <= r['position'] <= 10]
    if len(near_first_page) > 100:
        recommendations.append({
            'priority': 'HIGH',
            'issue': f'{len(near_first_page)} queries ranking positions 4-10',
            'action': 'Focus on these "low-hanging fruit" with content updates and internal links'
        })
    
    print("\n📋 Priority Actions:")
    for rec in sorted(recommendations, key=lambda x: x['priority']):
        print(f"\n[{rec['priority']}] {rec['issue']}")
        print(f"→ {rec['action']}")
    
    # Save detailed report
    report_data = {
        'generated_at': datetime.now().isoformat(),
        'summary': {
            'total_blog_queries': len(data),
            'unique_pages': len(set(r['keys'][0] for r in data)),
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'average_ctr': avg_ctr
        },
        'recommendations': recommendations
    }
    
    report_path = Path('gsc_reports') / f'blog_analysis_{datetime.now().strftime("%Y%m%d")}.json'
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: {report_path}")

if __name__ == "__main__":
    analyze_blog_performance()