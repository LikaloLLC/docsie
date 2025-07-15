#!/usr/bin/env python3
"""
Fetch entitlements from Chargebee API and save to a JSON configuration file.
This script will be used to sync pricing and entitlements data from Chargebee.
"""

import json
import os
import sys
from typing import Dict, List, Any
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CHARGEBEE_API_KEY = os.getenv('CHARGEBEE_API_KEY')
CHARGEBEE_SITE = os.getenv('CHARGEBEE_SITE')

if not CHARGEBEE_API_KEY or not CHARGEBEE_SITE:
    print("Error: Please set CHARGEBEE_API_KEY and CHARGEBEE_SITE in your .env file")
    sys.exit(1)

class ChargebeeClient:
    def __init__(self, api_key: str, site: str):
        self.api_key = api_key
        self.site = site
        self.base_url = f"https://{site}.chargebee.com/api/v2"
        self.session = requests.Session()
        self.session.auth = (api_key, '')
        
    def get_items(self) -> List[Dict[str, Any]]:
        """Fetch all items from Chargebee (v2 API uses items instead of plans)"""
        url = f"{self.base_url}/items"
        params = {'limit': 100}
        response = self.session.get(url, params=params)
        
        # Print response for debugging
        print(f"Items API Response Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Response: {response.text}")
            
        response.raise_for_status()
        data = response.json()
        return data.get('list', [])
    
    def get_item_prices(self) -> List[Dict[str, Any]]:
        """Fetch all item prices from Chargebee"""
        url = f"{self.base_url}/item_prices"
        params = {'limit': 100}
        response = self.session.get(url, params=params)
        
        response.raise_for_status()
        data = response.json()
        return data.get('list', [])
    
    def get_entitlements(self) -> List[Dict[str, Any]]:
        """Fetch all entitlements from Chargebee"""
        url = f"{self.base_url}/entitlements"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('list', [])
    
    def get_features(self) -> List[Dict[str, Any]]:
        """Fetch all features from Chargebee"""
        url = f"{self.base_url}/features"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('list', [])
    
    def get_item_entitlements(self, item_id: str) -> List[Dict[str, Any]]:
        """Fetch entitlements for a specific item (plan)"""
        url = f"{self.base_url}/items/{item_id}/item_entitlements"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('list', [])

def fetch_and_save_entitlements():
    """Main function to fetch all pricing data from Chargebee"""
    client = ChargebeeClient(CHARGEBEE_API_KEY, CHARGEBEE_SITE)
    
    print("Fetching data from Chargebee...")
    
    # Create the output structure
    pricing_data = {
        "items": [],
        "item_prices": [],
        "features": [],
        "entitlements": [],
        "item_entitlements": {}
    }
    
    try:
        # Fetch items (plans in v2)
        print("Fetching items...")
        items_data = client.get_items()
        for item_wrapper in items_data:
            item = item_wrapper.get('item', {})
            pricing_data['items'].append({
                'id': item.get('id'),
                'name': item.get('name'),
                'description': item.get('description'),
                'type': item.get('type'),
                'status': item.get('status'),
                'enabled_in_portal': item.get('enabled_in_portal'),
                'metadata': item.get('metadata', {})
            })
            
            # Try to fetch entitlements for this item
            try:
                print(f"  Fetching entitlements for item: {item.get('id')}")
                item_entitlements = client.get_item_entitlements(item.get('id'))
                pricing_data['item_entitlements'][item.get('id')] = item_entitlements
            except Exception as e:
                print(f"  Warning: Could not fetch entitlements for {item.get('id')}: {e}")
        
        # Fetch item prices
        print("Fetching item prices...")
        try:
            item_prices_data = client.get_item_prices()
            for price_wrapper in item_prices_data:
                price = price_wrapper.get('item_price', {})
                pricing_data['item_prices'].append({
                    'id': price.get('id'),
                    'item_id': price.get('item_id'),
                    'name': price.get('name'),
                    'description': price.get('description'),
                    'price': price.get('price'),
                    'currency_code': price.get('currency_code'),
                    'period': price.get('period'),
                    'period_unit': price.get('period_unit'),
                    'pricing_model': price.get('pricing_model'),
                    'status': price.get('status')
                })
        except Exception as e:
            print(f"Warning: Could not fetch item prices: {e}")
        
        # Fetch features
        print("Fetching features...")
        features_data = client.get_features()
        for feature_item in features_data:
            feature = feature_item.get('feature', {})
            pricing_data['features'].append({
                'id': feature.get('id'),
                'name': feature.get('name'),
                'description': feature.get('description'),
                'type': feature.get('type'),
                'levels': feature.get('levels', [])
            })
        
        # Fetch entitlements
        print("Fetching entitlements...")
        entitlements_data = client.get_entitlements()
        for entitlement_item in entitlements_data:
            entitlement = entitlement_item.get('entitlement', {})
            pricing_data['entitlements'].append({
                'id': entitlement.get('id'),
                'name': entitlement.get('name'),
                'feature_id': entitlement.get('feature_id'),
                'feature_type': entitlement.get('feature_type'),
                'value': entitlement.get('value')
            })
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Chargebee: {e}")
        sys.exit(1)
    
    # Save to JSON file
    output_file = 'chargebee_pricing_data.json'
    with open(output_file, 'w') as f:
        json.dump(pricing_data, f, indent=2)
    
    print(f"\nData saved to {output_file}")
    
    # Print summary
    print("\nSummary:")
    print(f"- Items: {len(pricing_data['items'])}")
    print(f"- Item Prices: {len(pricing_data['item_prices'])}")
    print(f"- Features: {len(pricing_data['features'])}")
    print(f"- Entitlements: {len(pricing_data['entitlements'])}")
    print(f"- Items with entitlements: {len(pricing_data['item_entitlements'])}")
    
    # Print item names for reference
    if pricing_data['items']:
        print("\nItems found:")
        for item in pricing_data['items']:
            print(f"  - {item['id']}: {item['name']} ({item['type']})")
    
    # Print item prices for reference
    if pricing_data['item_prices']:
        print("\nItem Prices found:")
        for price in pricing_data['item_prices']:
            print(f"  - {price['id']}: {price['name']} - {price['currency_code']} {price['price']/100 if price['price'] else 'N/A'}/{price['period_unit']}")

if __name__ == "__main__":
    fetch_and_save_entitlements()