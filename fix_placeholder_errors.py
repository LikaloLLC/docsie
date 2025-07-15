#!/usr/bin/env python3
"""
Fix placeholder format errors in .po files.
Ensures translated strings have the same format placeholders as the original msgid.
"""

import re
import os
from pathlib import Path
import polib

def extract_placeholders(text):
    """Extract all format placeholders from a string"""
    # Match Python format strings like %s, %d, %(name)s, etc.
    pattern = r'%(?:\([^)]+\))?[sdiouxXeEfFgGcrp%]'
    return re.findall(pattern, text)

def fix_placeholder_mismatches(po_file_path):
    """Fix placeholder mismatches in a single .po file"""
    
    try:
        po = polib.pofile(str(po_file_path))
        fixed_count = 0
        
        for entry in po:
            if not entry.msgstr or entry.fuzzy:
                continue
                
            # Extract placeholders from both msgid and msgstr
            msgid_placeholders = extract_placeholders(entry.msgid)
            msgstr_placeholders = extract_placeholders(entry.msgstr)
            
            # If placeholders don't match, fix them
            if msgid_placeholders != msgstr_placeholders:
                # Try to preserve the translation while fixing placeholders
                new_msgstr = entry.msgstr
                
                # Replace mismatched placeholders with correct ones
                if len(msgid_placeholders) == len(msgstr_placeholders):
                    # Same number of placeholders, just wrong types
                    for i, (orig, trans) in enumerate(zip(msgid_placeholders, msgstr_placeholders)):
                        if orig != trans:
                            # Replace the translated placeholder with the original
                            new_msgstr = new_msgstr.replace(trans, orig, 1)
                else:
                    # Different number of placeholders - mark as fuzzy
                    entry.flags.append('fuzzy')
                    print(f"  ⚠️  Marking as fuzzy (placeholder count mismatch): {entry.msgid[:50]}...")
                    continue
                
                entry.msgstr = new_msgstr
                fixed_count += 1
                
        if fixed_count > 0:
            po.save()
            print(f"  ✅ Fixed {fixed_count} placeholder mismatches")
            
        return fixed_count
        
    except Exception as e:
        print(f"  ❌ Error processing file: {e}")
        return 0

def fix_newline_mismatches(po_file_path):
    """Fix newline mismatches at beginning/end of strings"""
    
    try:
        po = polib.pofile(str(po_file_path))
        fixed_count = 0
        
        for entry in po:
            if not entry.msgstr or entry.fuzzy:
                continue
                
            # Check for newline mismatches at beginning
            if entry.msgid.startswith('\n') and not entry.msgstr.startswith('\n'):
                entry.msgstr = '\n' + entry.msgstr
                fixed_count += 1
            elif not entry.msgid.startswith('\n') and entry.msgstr.startswith('\n'):
                entry.msgstr = entry.msgstr.lstrip('\n')
                fixed_count += 1
                
            # Check for newline mismatches at end
            if entry.msgid.endswith('\n') and not entry.msgstr.endswith('\n'):
                entry.msgstr = entry.msgstr + '\n'
                fixed_count += 1
            elif not entry.msgid.endswith('\n') and entry.msgstr.endswith('\n'):
                entry.msgstr = entry.msgstr.rstrip('\n')
                fixed_count += 1
                
        if fixed_count > 0:
            po.save()
            print(f"  ✅ Fixed {fixed_count} newline mismatches")
            
        return fixed_count
        
    except Exception as e:
        print(f"  ❌ Error processing file: {e}")
        return 0

def main():
    """Fix all placeholder and format errors in .po files"""
    
    print("🔧 Fixing placeholder and format errors in .po files...")
    print("=" * 50)
    
    # Check if polib is installed
    try:
        import polib
    except ImportError:
        print("❌ polib not installed. Run: pip install polib")
        return False
    
    locale_dir = Path("locale")
    
    # Process each language
    for lang_dir in sorted(locale_dir.iterdir()):
        if not lang_dir.is_dir() or lang_dir.name in ['messages.pot', '.cache']:
            continue
            
        po_file = lang_dir / "LC_MESSAGES" / "messages.po"
        if not po_file.exists():
            continue
            
        print(f"\nProcessing {lang_dir.name}...")
        
        # Fix placeholder mismatches
        placeholder_fixes = fix_placeholder_mismatches(po_file)
        
        # Fix newline mismatches
        newline_fixes = fix_newline_mismatches(po_file)
        
        if placeholder_fixes == 0 and newline_fixes == 0:
            print("  ✓ No issues found")
    
    print("\n" + "=" * 50)
    print("✅ Placeholder fixing complete!")
    print("\nNow compiling all translations...")
    
    # Compile all translations
    import subprocess
    result = subprocess.run(['pybabel', 'compile', '-d', 'locale'], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ All translations compiled successfully!")
        return True
    else:
        print(f"⚠️  Some compilation errors remain: {result.stderr}")
        # Show which files have errors
        error_langs = []
        for line in result.stderr.split('\n'):
            if 'error:' in line and 'locale/' in line:
                lang = line.split('/')[1]
                if lang not in error_langs:
                    error_langs.append(lang)
        
        if error_langs:
            print(f"\nLanguages with remaining errors: {', '.join(error_langs)}")
            print("\nThese may need manual review or can be marked as fuzzy.")
        
        return False

if __name__ == "__main__":
    # First check if polib is installed
    try:
        import polib
    except ImportError:
        print("Installing polib...")
        import subprocess
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'polib'])
        import polib
    
    success = main()
    exit(0 if success else 1)