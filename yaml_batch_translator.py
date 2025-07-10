#!/usr/bin/env python3
"""
Batch YAML Translation System - Uses Anthropic's Batch API for fast bulk translations
"""

import os
import yaml
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from translation_system import TranslationSystem
import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request
from datetime import datetime


class YAMLBatchTranslator:
    """Translates YAML content files using Anthropic's Batch API for speed"""
    
    def __init__(self):
        self.translation_system = TranslationSystem()
        self.src_data_dir = Path("src/.data")
        self.cache_dir = Path(".yaml_batch_cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.batch_status_dir = Path(".yaml_batch_status")
        self.batch_status_dir.mkdir(exist_ok=True)
        
        # Initialize Anthropic client
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("No ANTHROPIC_API_KEY found in environment")
        
        self.client = anthropic.Anthropic(api_key=api_key)
        
        # Fields that should not be translated
        self.skip_fields = ['.id', '.url', '.link', '.href', '.category', '.icon', 
                           '.image', '.alt', '.ui_version', '.hero_version', 
                           '.calendly_url', '.video_link']
    
    def _extract_translatable_strings(self, data: Any, context: str = "") -> List[Tuple[str, str]]:
        """Extract all translatable strings from YAML data with their contexts"""
        strings = []
        
        if isinstance(data, str) and data.strip():
            # Check if string should be translated
            if not data.startswith(('http://', 'https://', '/', '#', 'fas ', 'fab ')):
                if len(data) >= 3:
                    if not any(context.endswith(field) for field in self.skip_fields):
                        strings.append((context, data))
        
        elif isinstance(data, dict):
            for key, value in data.items():
                new_context = f"{context}.{key}" if context else key
                strings.extend(self._extract_translatable_strings(value, new_context))
        
        elif isinstance(data, list):
            for i, item in enumerate(data):
                new_context = f"{context}[{i}]"
                strings.extend(self._extract_translatable_strings(item, new_context))
        
        return strings
    
    def _rebuild_yaml_with_translations(self, data: Any, translations: Dict[str, str], context: str = "") -> Any:
        """Rebuild YAML structure with translated strings"""
        if isinstance(data, str):
            key = f"{context}:{data}"
            if key in translations:
                return translations[key]
            return data
        
        elif isinstance(data, dict):
            result = {}
            for key, value in data.items():
                new_context = f"{context}.{key}" if context else key
                result[key] = self._rebuild_yaml_with_translations(value, translations, new_context)
            return result
        
        elif isinstance(data, list):
            result = []
            for i, item in enumerate(data):
                new_context = f"{context}[{i}]"
                result.append(self._rebuild_yaml_with_translations(item, translations, new_context))
            return result
        
        else:
            return data
    
    def prepare_batch_requests(self, target_lang: str) -> Tuple[List[Request], Dict[str, Dict]]:
        """Prepare batch requests for all YAML files"""
        requests = []
        file_mapping = {}  # Maps custom_id to file info
        
        # Language info for prompts
        lang_info = self.translation_system.languages.get(target_lang, {})
        lang_name = lang_info.get('name', target_lang)
        
        # Find all YAML files
        yaml_files = list(self.src_data_dir.rglob("*.yaml"))
        yaml_files = [f for f in yaml_files if not any(part.startswith('_') for part in f.parts)]
        
        print(f"\n📁 Preparing batch translation for {len(yaml_files)} files to {lang_name}...")
        
        for yaml_file in yaml_files:
            # Skip if already translated (check cache)
            cache_file = self.cache_dir / f"{yaml_file.stem}_{target_lang}.json"
            if cache_file.exists():
                print(f"  ⏭️  Skipping {yaml_file.name} (already translated)")
                continue
            
            try:
                # Load YAML data
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    yaml_data = yaml.safe_load(f)
                
                if not yaml_data:
                    continue
                
                # Extract translatable strings
                strings = self._extract_translatable_strings(yaml_data)
                if not strings:
                    continue
                
                # Create translation prompt
                strings_dict = {f"{ctx}:{text}": text for ctx, text in strings}
                
                prompt = f"""Translate the following strings from English to {lang_name}.
Return a JSON object where keys are the original context:text pairs and values are the translations.

Important rules:
- Translate only the text values, not the keys
- Preserve all formatting, line breaks, and punctuation
- Keep technical terms that should remain in English
- Ensure the JSON is valid

Strings to translate:
{json.dumps(strings_dict, ensure_ascii=False, indent=2)}"""
                
                # Create batch request
                custom_id = f"{yaml_file.stem}_{target_lang}_{int(time.time() * 1000)}"
                
                request = Request(
                    custom_id=custom_id,
                    params=MessageCreateParamsNonStreaming(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=8192,
                        temperature=0.3,
                        messages=[{
                            "role": "user",
                            "content": prompt
                        }]
                    )
                )
                
                requests.append(request)
                file_mapping[custom_id] = {
                    'file': str(yaml_file),
                    'yaml_data': yaml_data,
                    'target_lang': target_lang
                }
                
                print(f"  📝 Prepared: {yaml_file.name} ({len(strings)} strings)")
                
            except Exception as e:
                print(f"  ❌ Error preparing {yaml_file}: {e}")
        
        return requests, file_mapping
    
    def submit_batch(self, requests: List[Request]) -> str:
        """Submit batch to Anthropic API"""
        if not requests:
            print("No requests to submit")
            return None
        
        print(f"\n📤 Submitting batch with {len(requests)} requests...")
        
        try:
            batch = self.client.messages.batches.create(requests=requests)
            print(f"✅ Batch submitted successfully!")
            print(f"   Batch ID: {batch.id}")
            print(f"   Status: {batch.processing_status}")
            return batch.id
        except Exception as e:
            print(f"❌ Error submitting batch: {e}")
            return None
    
    def check_batch_status(self, batch_id: str) -> str:
        """Check the status of a batch"""
        try:
            batch = self.client.messages.batches.retrieve(batch_id)
            return batch.processing_status
        except Exception as e:
            print(f"❌ Error checking batch status: {e}")
            return "error"
    
    def wait_for_batch(self, batch_id: str, check_interval: int = 30) -> bool:
        """Wait for batch to complete, checking periodically"""
        print(f"\n⏳ Waiting for batch {batch_id} to complete...")
        print(f"   (Checking every {check_interval} seconds)")
        
        start_time = time.time()
        while True:
            status = self.check_batch_status(batch_id)
            
            if status == "ended":
                elapsed = time.time() - start_time
                print(f"\n✅ Batch completed in {elapsed:.1f} seconds!")
                return True
            elif status == "failed" or status == "error":
                print(f"\n❌ Batch failed with status: {status}")
                return False
            else:
                print(f"   Status: {status} (elapsed: {int(time.time() - start_time)}s)", end='\r')
                time.sleep(check_interval)
    
    def process_batch_results(self, batch_id: str, file_mapping: Dict[str, Dict]) -> int:
        """Process completed batch results"""
        print(f"\n📥 Processing batch results...")
        
        try:
            # Retrieve batch details
            batch = self.client.messages.batches.retrieve(batch_id)
            
            # Get results
            results = []
            # The results method returns individual results directly
            for result in self.client.messages.batches.results(batch_id):
                results.append(result)
            
            print(f"   Found {len(results)} results")
            
            processed = 0
            for result in results:
                # Access the result correctly based on the structure
                custom_id = result.custom_id
                
                if custom_id not in file_mapping:
                    print(f"  ⚠️  Unknown custom_id: {custom_id}")
                    continue
                
                # Check if the result succeeded
                if result.result.type == "succeeded":
                    file_info = file_mapping[custom_id]
                    
                    try:
                        # Extract translation from response
                        # The content is in result.result.message.content array
                        message_content = result.result.message.content
                        if message_content and len(message_content) > 0:
                            content_text = message_content[0].text
                            translations = json.loads(content_text)
                        else:
                            print(f"  ⚠️  No content in response for {custom_id}")
                            continue
                        
                        # Rebuild YAML with translations
                        translated_data = self._rebuild_yaml_with_translations(
                            file_info['yaml_data'], 
                            translations
                        )
                        
                        # Save translated YAML
                        target_lang = file_info['target_lang']
                        yaml_file = Path(file_info['file'])
                        output_dir = self.src_data_dir / f"_{target_lang}"
                        relative_path = yaml_file.relative_to(self.src_data_dir)
                        output_file = output_dir / relative_path
                        
                        output_file.parent.mkdir(parents=True, exist_ok=True)
                        
                        with open(output_file, 'w', encoding='utf-8') as f:
                            yaml.dump(translated_data, f, allow_unicode=True, 
                                    default_flow_style=False, sort_keys=False)
                        
                        print(f"  ✅ Saved: {relative_path}")
                        
                        # Save to cache
                        cache_file = self.cache_dir / f"{yaml_file.stem}_{target_lang}.json"
                        with open(cache_file, 'w', encoding='utf-8') as f:
                            json.dump({
                                'translated': True,
                                'timestamp': datetime.now().isoformat()
                            }, f)
                        
                        processed += 1
                        
                    except Exception as e:
                        print(f"  ❌ Error processing result for {custom_id}: {e}")
                
                elif result.result.type == "errored":
                    print(f"  ❌ Request failed: {result.custom_id}")
                    if hasattr(result.result, 'error'):
                        print(f"     Error: {result.result.error}")
            
            return processed
            
        except Exception as e:
            print(f"❌ Error processing results: {e}")
            return 0
    
    def translate_all_yamls(self, target_langs: Optional[List[str]] = None):
        """Translate all YAML files to target languages using batch API"""
        if target_langs is None:
            target_langs = [code for code, info in self.translation_system.languages.items() 
                           if info.get('enabled', False) and code != 'en']
        
        for lang in target_langs:
            print(f"\n🌍 Processing language: {lang}")
            
            # Prepare batch requests
            requests, file_mapping = self.prepare_batch_requests(lang)
            
            if not requests:
                print("  ℹ️  No files to translate")
                continue
            
            # Save file mapping for recovery
            mapping_file = self.batch_status_dir / f"mapping_{lang}_{int(time.time())}.json"
            with open(mapping_file, 'w', encoding='utf-8') as f:
                json.dump(file_mapping, f)
            
            # Submit batch
            batch_id = self.submit_batch(requests)
            if not batch_id:
                continue
            
            # Save batch ID for recovery
            status_file = self.batch_status_dir / f"batch_{lang}.json"
            with open(status_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'batch_id': batch_id,
                    'mapping_file': str(mapping_file),
                    'language': lang,
                    'timestamp': datetime.now().isoformat()
                }, f)
            
            # Wait for completion
            if self.wait_for_batch(batch_id):
                # Process results
                processed = self.process_batch_results(batch_id, file_mapping)
                print(f"\n✅ Processed {processed} files for {lang}")
            
            # Clean up status file
            if status_file.exists():
                status_file.unlink()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Fast batch translation of YAML files using Anthropic Batch API')
    parser.add_argument('-l', '--language', '--langs', action='append', help='Target language code (can be used multiple times)')
    parser.add_argument('-f', '--force', action='store_true', help='Force retranslation even if files exist')
    parser.add_argument('-c', '--check', help='Check status of existing batch')
    parser.add_argument('-r', '--resume', action='store_true', help='Resume pending batches')
    
    args = parser.parse_args()
    
    translator = YAMLBatchTranslator()
    
    if args.check:
        # Check batch status
        status = translator.check_batch_status(args.check)
        print(f"Batch {args.check} status: {status}")
    elif args.resume:
        # Resume any pending batches
        print("🔍 Looking for pending batches...")
        for status_file in translator.batch_status_dir.glob("batch_*.json"):
            with open(status_file, 'r') as f:
                batch_info = json.load(f)
            
            print(f"\n📋 Found pending batch for {batch_info['language']}")
            print(f"   Batch ID: {batch_info['batch_id']}")
            
            # Load file mapping
            with open(batch_info['mapping_file'], 'r') as f:
                file_mapping = json.load(f)
            
            # Wait and process
            if translator.wait_for_batch(batch_info['batch_id']):
                processed = translator.process_batch_results(batch_info['batch_id'], file_mapping)
                print(f"   Processed {processed} files")
            
            # Clean up
            status_file.unlink()
    else:
        # Normal translation
        # Handle --force flag by clearing cache if needed
        if args.force:
            print("🗑️  Force mode: Clearing translation cache...")
            if translator.cache_dir.exists():
                import shutil
                shutil.rmtree(translator.cache_dir)
                translator.cache_dir.mkdir(parents=True, exist_ok=True)
        
        target_langs = args.language if args.language else None
        translator.translate_all_yamls(target_langs)
        
        print("\n✨ Batch translation complete!")