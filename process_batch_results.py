#!/usr/bin/env python3
"""Process results from a completed batch"""

import sys
from yaml_batch_translator import YAMLBatchTranslator
import json
import yaml
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: python process_batch_results.py <batch_id>")
        return
    
    batch_id = sys.argv[1]
    translator = YAMLBatchTranslator()
    
    print(f"Processing results for batch: {batch_id}")
    print("Reconstructing file mapping from batch results...")
    
    file_mapping = {}
    
    try:
        # Get all results
        results = []
        for result in translator.client.messages.batches.results(batch_id):
            results.append(result)
        
        print(f"Found {len(results)} results")
        
        # For each result, reconstruct the mapping
        for result in results:
            custom_id = result.custom_id
            
            # Extract filename from custom_id (format: filename_lang_timestamp)
            parts = custom_id.rsplit('_', 2)
            if len(parts) >= 3:
                filename = parts[0]
                lang = parts[1]
                
                # Handle subdirectory files
                if filename in ['saas', 'it-services', 'energy', 'manufacturing', 'compliance', 'government']:
                    yaml_path = translator.src_data_dir / 'industries' / f"{filename}.yaml"
                elif filename in ['ai-pilot-program', 'documentation-from-video', 'custom-ai-content-prompts', 
                                'ai-chatbot', 'ai-agents', 'ai-technical-writer']:
                    yaml_path = translator.src_data_dir / 'AI' / f"{filename}.yaml"
                else:
                    yaml_path = translator.src_data_dir / f"{filename}.yaml"
                
                if yaml_path.exists():
                    with open(yaml_path, 'r') as f:
                        yaml_data = yaml.safe_load(f)
                    
                    file_mapping[custom_id] = {
                        'file': str(yaml_path),
                        'yaml_data': yaml_data,
                        'target_lang': lang
                    }
                    print(f"  ✓ Mapped: {custom_id} -> {yaml_path.relative_to(translator.src_data_dir)}")
                else:
                    print(f"  ✗ File not found for: {filename}")
    
    except Exception as e:
        print(f"Error building mapping: {e}")
        return
    
    print(f"\nSuccessfully mapped {len(file_mapping)} files")
    
    # Process the results
    processed = translator.process_batch_results(batch_id, file_mapping)
    print(f"\nTotal processed: {processed} files")

if __name__ == "__main__":
    main()