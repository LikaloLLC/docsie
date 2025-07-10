#!/usr/bin/env python3
"""
Intelligent Link Fixer for Docsie Static Site
Parses linkchecker CSV output and automatically fixes broken links
"""

import csv
import re
import os
import shutil
import requests
from urllib.parse import urlparse, urljoin
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import difflib
from dataclasses import dataclass
import json
import time


@dataclass
class BrokenLink:
    """Represents a broken link with context"""
    url: str
    parent_url: str
    line_number: int
    column_number: int
    error_type: str
    error_message: str
    source_file: str = ""
    confidence: float = 0.0
    suggested_fix: str = ""
    fix_reason: str = ""


class LinkFixer:
    def __init__(self, csv_file: str, src_dir: str = "src", dry_run: bool = True):
        self.csv_file = csv_file
        self.src_dir = Path(src_dir)
        self.dry_run = dry_run
        self.broken_links: List[BrokenLink] = []
        self.fixes_applied = 0
        self.backup_dir = Path("backups")
        
    def parse_csv(self) -> List[BrokenLink]:
        """Parse linkchecker CSV output"""
        broken_links = []
        
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                # Skip comment lines starting with #
                lines = [line for line in f if not line.strip().startswith('#')]
                
            # Parse as semicolon-delimited
            reader = csv.DictReader(lines, delimiter=';')
            for row in reader:
                # Skip successful links - valid=True or result is 200 OK
                if (row.get('valid') == 'True' or 
                    '200 OK' in row.get('result', '') or
                    'filtered' in row.get('result', '') or
                    'ignored' in row.get('result', '')):
                    continue
                    
                link = BrokenLink(
                    url=row.get('urlname', ''),
                    parent_url=row.get('parentname', ''),
                    line_number=int(row.get('line', 0) or 0),
                    column_number=int(row.get('column', 0) or 0),
                    error_type=row.get('result', ''),
                    error_message=row.get('infostring', ''),
                    source_file=self._get_source_file(row.get('parentname', ''))
                )
                broken_links.append(link)
                    
        except Exception as e:
            print(f"Error parsing CSV: {e}")
            
        return broken_links
    
    def _get_source_file(self, parent_url: str) -> str:
        """Map parent URL to source file"""
        if not parent_url:
            return ""
            
        # Remove domain and convert to source file path
        parsed = urlparse(parent_url)
        path = parsed.path.strip('/')
        
        # Handle index files
        if not path or path.endswith('/'):
            path += 'index.html'
        elif not path.endswith('.html'):
            path += '/index.html'
            
        return str(self.src_dir / path)
    
    def check_redirect(self, url: str) -> Tuple[bool, str, str]:
        """Check if URL redirects and return new URL"""
        try:
            response = requests.head(url, allow_redirects=False, timeout=10)
            if response.status_code in [301, 302, 303, 307, 308]:
                new_url = response.headers.get('location', '')
                if new_url:
                    return True, new_url, f"Redirect {response.status_code}"
        except Exception as e:
            pass
        return False, "", ""
    
    def apply_pattern_fixes(self, url: str) -> Tuple[bool, str, str]:
        """Apply common pattern-based fixes"""
        original_url = url
        
        # Handle malformed URLs like /blog/https://...
        if '/blog/https://' in url:
            # Extract the actual URL after /blog/
            actual_url = url.split('/blog/', 1)[1]
            return True, actual_url, "Extract URL from malformed path"
        
        # Handle whitespace in URLs
        if url.strip() != url:
            return True, url.strip(), "Remove leading/trailing whitespace"
        
        # Common patterns to fix
        patterns = [
            # Double paths
            (r'/blog/blog/', '/blog/', "Remove duplicate path segment"),
            (r'/docs/docs/', '/docs/', "Remove duplicate path segment"),
            
            # Protocol upgrade
            (r'^http://', 'https://', "Upgrade to HTTPS"),
            
            # Trailing slash issues for directories
            (r'([^/.])$', r'\1/', "Add trailing slash"),
            
            # Remove .html extension
            (r'\.html$', '/', "Remove .html extension"),
        ]
        
        for pattern, replacement, reason in patterns:
            new_url = re.sub(pattern, replacement, url)
            if new_url != url:
                # Test if the fix works (skip for external URLs)
                if not new_url.startswith('http'):
                    try:
                        test_url = f"http://localhost:8081{new_url}"
                        response = requests.head(test_url, timeout=5)
                        if response.status_code == 200:
                            return True, new_url, reason
                    except:
                        pass
                else:
                    # For external URLs, just return the fix
                    return True, new_url, reason
                    
        return False, "", ""
    
    def find_similar_urls(self, broken_url: str) -> List[Tuple[str, float]]:
        """Find similar URLs using fuzzy matching"""
        # This would need a list of valid URLs from your site
        # For now, return empty list
        return []
    
    def suggest_fixes(self) -> None:
        """Generate fix suggestions for all broken links"""
        print(f"Analyzing {len(self.broken_links)} broken links...")
        
        for link in self.broken_links:
            print(f"\nAnalyzing: {link.url}")
            
            # 1. Check for redirects
            is_redirect, new_url, reason = self.check_redirect(link.url)
            if is_redirect:
                link.suggested_fix = new_url
                link.fix_reason = reason
                link.confidence = 0.9
                continue
                
            # 2. Apply pattern fixes
            has_pattern_fix, new_url, reason = self.apply_pattern_fixes(link.url)
            if has_pattern_fix:
                link.suggested_fix = new_url
                link.fix_reason = reason
                link.confidence = 0.7
                continue
                
            # 3. Fuzzy matching (placeholder)
            similar_urls = self.find_similar_urls(link.url)
            if similar_urls:
                best_match, similarity = similar_urls[0]
                if similarity > 0.8:
                    link.suggested_fix = best_match
                    link.fix_reason = f"Similar URL match ({similarity:.2f})"
                    link.confidence = similarity * 0.6
                    continue
                    
            # 4. No fix found
            link.suggested_fix = ""
            link.fix_reason = "No automatic fix available"
            link.confidence = 0.0
    
    def create_backup(self) -> None:
        """Create backup of source files"""
        if not self.dry_run:
            self.backup_dir.mkdir(exist_ok=True)
            backup_path = self.backup_dir / f"backup_{int(time.time())}"
            shutil.copytree(self.src_dir, backup_path)
            print(f"Backup created at: {backup_path}")
    
    def apply_fixes(self, min_confidence: float = 0.7) -> None:
        """Apply fixes to source files"""
        if not self.dry_run:
            self.create_backup()
            
        high_confidence_fixes = [
            link for link in self.broken_links 
            if link.confidence >= min_confidence and link.suggested_fix
        ]
        
        print(f"\nApplying {len(high_confidence_fixes)} high-confidence fixes...")
        
        for link in high_confidence_fixes:
            if self.dry_run:
                print(f"[DRY RUN] Would fix: {link.url} → {link.suggested_fix}")
                print(f"  Reason: {link.fix_reason} (confidence: {link.confidence:.2f})")
            else:
                success = self._replace_in_file(link)
                if success:
                    self.fixes_applied += 1
                    print(f"Fixed: {link.url} → {link.suggested_fix}")
    
    def _replace_in_file(self, link: BrokenLink) -> bool:
        """Replace broken link in source file"""
        if not link.source_file or not Path(link.source_file).exists():
            return False
            
        try:
            with open(link.source_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Replace the broken URL
            new_content = content.replace(link.url, link.suggested_fix)
            
            if new_content != content:
                with open(link.source_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                return True
                
        except Exception as e:
            print(f"Error updating {link.source_file}: {e}")
            
        return False
    
    def generate_report(self) -> None:
        """Generate summary report"""
        print(f"\n{'='*60}")
        print("LINK FIXING REPORT")
        print(f"{'='*60}")
        
        total_broken = len(self.broken_links)
        fixable = len([l for l in self.broken_links if l.confidence >= 0.7])
        
        print(f"Total broken links: {total_broken}")
        print(f"Automatically fixable: {fixable}")
        print(f"Fixes applied: {self.fixes_applied}")
        
        # Group by error type
        error_types = {}
        for link in self.broken_links:
            error_types[link.error_type] = error_types.get(link.error_type, 0) + 1
            
        print(f"\nError types:")
        for error_type, count in sorted(error_types.items()):
            print(f"  {error_type}: {count}")
            
        # Show unfixable links
        unfixable = [l for l in self.broken_links if l.confidence < 0.7]
        if unfixable:
            print(f"\nLinks requiring manual review ({len(unfixable)}):")
            for link in unfixable[:10]:  # Show first 10
                print(f"  {link.url}")
                print(f"    Error: {link.error_message}")
                print(f"    In: {link.source_file}")
    
    def run(self) -> None:
        """Main execution flow"""
        print("Starting intelligent link fixing...")
        
        # Parse CSV
        self.broken_links = self.parse_csv()
        if not self.broken_links:
            print("No broken links found in CSV!")
            return
            
        # Generate suggestions
        self.suggest_fixes()
        
        # Apply fixes
        self.apply_fixes()
        
        # Generate report
        self.generate_report()


def main():
    import argparse
    import time
    
    parser = argparse.ArgumentParser(description='Fix broken links from linkchecker CSV')
    parser.add_argument('csv_file', help='CSV file from linkchecker')
    parser.add_argument('--src-dir', default='src', help='Source directory')
    parser.add_argument('--dry-run', action='store_true', help='Show fixes without applying')
    parser.add_argument('--min-confidence', type=float, default=0.7, 
                       help='Minimum confidence for auto-fix')
    
    args = parser.parse_args()
    
    if not Path(args.csv_file).exists():
        print(f"CSV file not found: {args.csv_file}")
        return
        
    fixer = LinkFixer(args.csv_file, args.src_dir, args.dry_run)
    fixer.run()


if __name__ == "__main__":
    main()