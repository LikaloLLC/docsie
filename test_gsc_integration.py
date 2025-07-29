#!/usr/bin/env python3
"""
Test Google Search Console API connection and fetch some basic data
"""
import sys
from pathlib import Path

# Add BlogVi to path if needed
sys.path.insert(0, str(Path(__file__).parent / '.external/BlogVi/src'))

from blog_vi.core.gsc_integration import GSCIntegration

def test_gsc_connection():
    """Test GSC API connection and fetch some data"""
    
    print("Testing Google Search Console API connection...")
    print("=" * 60)
    
    try:
        # Initialize GSC with your credentials
        # Using domain property format for GSC API
        gsc = GSCIntegration(
            credentials_path="/Users/philippetrounev/PycharmProjects/docsie-site/docsie-io-0f57d9e21566.json",
            site_url="sc-domain:docsie.io"
        )
        
        print("✅ Successfully authenticated with GSC!")
        print()
        
        # Test 1: Fetch recent performance data
        print("Fetching performance data for last 7 days...")
        from datetime import datetime, timedelta
        
        end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        data = gsc.fetch_performance_data(
            start_date=start_date,
            end_date=end_date,
            row_limit=10  # Just get a few rows for testing
        )
        
        print(f"✅ Fetched {len(data)} rows of data")
        
        if data:
            print("\nSample data (first row):")
            print(f"  Page: {data[0]['keys'][0]}")
            print(f"  Query: {data[0]['keys'][1]}")
            print(f"  Clicks: {data[0]['clicks']}")
            print(f"  Impressions: {data[0]['impressions']}")
            print(f"  CTR: {data[0]['ctr']:.2%}")
            print(f"  Position: {data[0]['position']:.1f}")
        
        # Test 2: Find low CTR pages
        print("\n" + "=" * 60)
        print("Finding low CTR opportunities...")
        
        low_ctr_pages = gsc.get_low_ctr_pages(
            min_impressions=500,  # Lower threshold for testing
            max_ctr=0.02
        )
        
        print(f"✅ Found {len(low_ctr_pages)} pages with CTR < 2%")
        
        if low_ctr_pages:
            print("\nTop 3 opportunities:")
            for i, page in enumerate(low_ctr_pages[:3], 1):
                print(f"\n{i}. {page['page']}")
                print(f"   Impressions: {page['impressions']:,}")
                print(f"   Clicks: {page['clicks']}")
                print(f"   CTR: {page['ctr']:.2%}")
                print(f"   Avg Position: {page['avg_position']:.1f}")
                if page['top_queries']:
                    print(f"   Top Query: '{page['top_queries'][0]['query']}'")
        
        # Test 3: Find near first page
        print("\n" + "=" * 60)
        print("Finding pages near first page (positions 4-10)...")
        
        near_first = gsc.get_near_first_page()
        print(f"✅ Found {len(near_first)} pages ranking 4-10")
        
        if near_first:
            print("\nTop 3 near-first-page opportunities:")
            for i, page in enumerate(near_first[:3], 1):
                print(f"\n{i}. {page['page']}")
                print(f"   Avg Position: {page['avg_position']:.1f}")
                print(f"   Impressions: {page['total_impressions']:,}")
                print(f"   Clicks: {page['total_clicks']}")
        
        # Test 4: Find content gaps
        print("\n" + "=" * 60)
        print("Finding content gap opportunities...")
        
        gaps = gsc.find_content_gaps(min_impressions=100)  # Lower threshold for testing
        print(f"✅ Found {len(gaps)} potential content gaps")
        
        if gaps:
            print("\nTop 3 content gaps:")
            for i, gap in enumerate(gaps[:3], 1):
                print(f"\n{i}. Query: '{gap['query']}'")
                print(f"   Impressions: {gap['impressions']:,}")
                print(f"   Avg Position: {gap['avg_position']:.1f}")
                print(f"   Currently ranking {gap['page_count']} pages")
        
        # Generate a report
        print("\n" + "=" * 60)
        print("Generating full report...")
        
        report_dir = Path("gsc_test_reports")
        report_path = gsc.save_report(report_dir)
        print(f"✅ Report saved to: {report_path}")
        
        print("\n🎉 All tests passed! GSC integration is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    test_gsc_connection()