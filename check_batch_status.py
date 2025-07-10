#!/usr/bin/env python3
"""Check the status of a specific batch"""

import os
from anthropic import Anthropic
import argparse

def check_batch_status(batch_id):
    """Check the status of a specific batch"""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        return
    
    client = Anthropic(api_key=api_key)
    
    try:
        batch = client.beta.messages.batches.retrieve(batch_id)
        
        print(f"\nBatch ID: {batch.id}")
        print(f"Status: {batch.processing_status}")
        print(f"Created at: {batch.created_at}")
        print(f"Expires at: {batch.expires_at}")
        print(f"Request counts: {batch.request_counts}")
        
        if batch.processing_status == 'ended':
            # Download results
            results_url = batch.results_url
            if results_url:
                print(f"\nResults available at: {results_url}")
                print("\nUse yaml_batch_translator.py with --check-batch flag to process the results")
            else:
                print("\nNo results URL available")
                
        return batch.processing_status
        
    except Exception as e:
        print(f"Error checking batch: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check batch status')
    parser.add_argument('batch_id', help='The batch ID to check')
    args = parser.parse_args()
    
    check_batch_status(args.batch_id)