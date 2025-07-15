#!/usr/bin/env python3
"""
Mark translation entries with errors as fuzzy so they get retranslated.
This is a last resort when translations have format errors that can't be automatically fixed.
"""

import subprocess
import re
from pathlib import Path


def get_error_line_numbers(po_file_path):
    """Get line numbers of entries with errors"""
    
    cmd = ['msgfmt', '--check', str(po_file_path), '-o', '/dev/null']
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        return []
    
    # Extract line numbers from error messages
    error_lines = []
    for line in result.stderr.split('\n'):
        if 'error:' in line and str(po_file_path) in line:
            match = re.search(r':(\d+):', line)
            if match:
                error_lines.append(int(match.group(1)))
    
    return list(set(error_lines))  # Remove duplicates


def mark_entry_fuzzy(lines, error_line):
    """Mark the entry containing the error line as fuzzy"""
    
    # Find the msgid for this error
    i = error_line - 1  # Convert to 0-based
    
    # Handle bounds
    if i >= len(lines):
        return False
    
    # Find start of entry (msgid)
    while i > 0 and not lines[i].startswith('msgid '):
        i -= 1
    
    if i == 0 and not lines[i].startswith('msgid '):
        return False
    
    # Look for existing flags before msgid
    flag_line = i - 1
    while flag_line >= 0 and (lines[flag_line].strip() == '' or lines[flag_line].startswith('#')):
        if lines[flag_line].startswith('#,'):
            # Found flags line
            if 'fuzzy' not in lines[flag_line]:
                lines[flag_line] = lines[flag_line].rstrip() + ', fuzzy\n'
            return True
        flag_line -= 1
    
    # No flags found, insert new fuzzy flag
    # Find where to insert (after other # lines but before msgid)
    insert_pos = i
    j = i - 1
    while j >= 0 and lines[j].startswith('#'):
        insert_pos = j
        j -= 1
    
    lines.insert(insert_pos, '#, fuzzy\n')
    return True


def process_po_file(po_file_path):
    """Process a single .po file"""
    
    error_lines = get_error_line_numbers(po_file_path)
    if not error_lines:
        return 0
    
    # Read file
    with open(po_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Mark entries as fuzzy
    marked = 0
    # Sort in reverse to avoid index shifting when inserting lines
    for error_line in sorted(error_lines, reverse=True):
        if mark_entry_fuzzy(lines, error_line):
            marked += 1
    
    # Write back
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return marked


def main():
    """Mark all problematic entries as fuzzy"""
    
    print("🔍 Marking translation errors as fuzzy...")
    print("=" * 50)
    
    locale_dir = Path("locale")
    total_marked = 0
    
    for lang_dir in sorted(locale_dir.iterdir()):
        if not lang_dir.is_dir() or lang_dir.name in ['messages.pot', '.cache']:
            continue
        
        po_file = lang_dir / "LC_MESSAGES" / "messages.po"
        if not po_file.exists():
            continue
        
        marked = process_po_file(po_file)
        if marked > 0:
            print(f"{lang_dir.name}: Marked {marked} entries as fuzzy")
            total_marked += 1
    
    print("\n" + "=" * 50)
    
    if total_marked > 0:
        print(f"✅ Fixed {total_marked} files")
        print("\nCompiling translations...")
        
        # Try to compile
        result = subprocess.run(['pybabel', 'compile', '-d', 'locale'],
                              capture_output=True, text=True)
        
        if 'error' not in result.stderr:
            print("✅ All translations compiled successfully!")
            print("\nFuzzy entries will be retranslated when you run:")
            print("  sh build_multilingual.sh --translate")
        else:
            # Count remaining errors
            error_count = result.stderr.count('error:')
            print(f"⚠️  {error_count} errors remain. You may need to run --force to retranslate all")
    else:
        print("✓ No errors found to mark as fuzzy")


if __name__ == "__main__":
    main()