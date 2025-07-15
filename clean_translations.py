#!/usr/bin/env python3
"""
Clean and fix translation files to resolve compilation errors.
Handles:
1. Removes incorrect python-format flags
2. Fixes placeholder mismatches
3. Fixes newline mismatches
"""

import os
import re
import subprocess
from pathlib import Path


def clean_po_file(po_file_path):
    """Clean a single .po file of format errors"""
    
    print(f"Cleaning {po_file_path.parent.parent.name}...", end=" ", flush=True)
    
    # Read the file
    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    fixed_count = 0
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check for python-format flag
        if line == '#, python-format':
            # Look ahead to see if the msgid actually contains format strings
            j = i + 1
            found_msgid = False
            has_format = False
            
            while j < len(lines) and not found_msgid:
                if lines[j].startswith('msgid "'):
                    # Check this line and continuation lines for format strings
                    k = j
                    while k < len(lines) and (lines[k].startswith('msgid "') or lines[k].startswith('"')):
                        if re.search(r'%[sdiouxXeEfFgGcrp%]', lines[k]):
                            has_format = True
                            break
                        k += 1
                    found_msgid = True
                j += 1
            
            # Only keep the format flag if there are actual format strings
            if has_format:
                new_lines.append(line)
            else:
                fixed_count += 1
                # Skip this line (remove the flag)
            i += 1
            continue
        
        # Fix newline mismatches
        if line.startswith('msgid "') and i + 1 < len(lines):
            # Find the corresponding msgstr
            j = i + 1
            while j < len(lines) and not lines[j].startswith('msgstr "'):
                j += 1
            
            if j < len(lines):
                # Check for newline mismatch at start
                msgid_has_newline_start = '\\n' in lines[i][:15]
                msgstr_has_newline_start = '\\n' in lines[j][:15]
                
                if msgid_has_newline_start != msgstr_has_newline_start and lines[j] != 'msgstr ""':
                    if msgid_has_newline_start:
                        # Add newline to msgstr
                        lines[j] = lines[j].replace('msgstr "', 'msgstr "\\n', 1)
                    else:
                        # Remove newline from msgstr
                        lines[j] = lines[j].replace('msgstr "\\n', 'msgstr "', 1)
                    fixed_count += 1
        
        new_lines.append(line)
        i += 1
    
    if fixed_count > 0:
        # Write the cleaned content
        with open(po_file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        print(f"✅ Fixed {fixed_count} issues")
    else:
        print("✓")
    
    return fixed_count > 0


def compile_and_check(po_file_path):
    """Try to compile a .po file and return any errors"""
    
    cmd = ['msgfmt', '--check', str(po_file_path), '-o', '/dev/null']
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        return result.stderr
    return None


def mark_errors_as_fuzzy(po_file_path, error_lines):
    """Mark entries with errors as fuzzy so they get retranslated"""
    
    # Extract line numbers from error messages
    error_line_numbers = []
    for line in error_lines.split('\n'):
        if ':' in line and 'error:' in line:
            try:
                # Extract line number from error message like "file.po:123: error"
                parts = line.split(':')
                if len(parts) >= 2:
                    line_num = int(parts[1])
                    error_line_numbers.append(line_num)
            except:
                continue
    
    if not error_line_numbers:
        return 0
    
    # Read the file
    with open(po_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_count = 0
    
    # Mark problematic entries as fuzzy
    for error_line in error_line_numbers:
        # Find the msgid for this error (working backwards)
        i = error_line - 1  # Convert to 0-based index
        
        # Find the start of this entry
        while i > 0 and not lines[i].startswith('msgid "'):
            i -= 1
        
        # Find if there's already a flag line
        flag_line = i - 1
        while flag_line >= 0 and lines[flag_line].strip() == '':
            flag_line -= 1
        
        # Check if this is a flag line or comment
        if flag_line >= 0 and lines[flag_line].startswith('#'):
            if lines[flag_line].startswith('#,'):
                # Add fuzzy to existing flags
                if 'fuzzy' not in lines[flag_line]:
                    lines[flag_line] = lines[flag_line].rstrip() + ', fuzzy\n'
                    fixed_count += 1
            else:
                # Insert a new flag line
                lines.insert(flag_line + 1, '#, fuzzy\n')
                fixed_count += 1
        else:
            # No flags, add a new flag line before msgid
            lines.insert(i, '#, fuzzy\n')
            fixed_count += 1
    
    if fixed_count > 0:
        with open(po_file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    
    return fixed_count


def main():
    """Clean all translation files"""
    
    print("🧹 Cleaning translation files...")
    print("=" * 50)
    
    locale_dir = Path("locale")
    total_fixed = 0
    remaining_errors = []
    
    # Process each language
    for lang_dir in sorted(locale_dir.iterdir()):
        if not lang_dir.is_dir() or lang_dir.name in ['messages.pot', '.cache']:
            continue
        
        po_file = lang_dir / "LC_MESSAGES" / "messages.po"
        if not po_file.exists():
            continue
        
        # Clean the file
        if clean_po_file(po_file):
            total_fixed += 1
        
        # Check if there are still errors
        errors = compile_and_check(po_file)
        if errors:
            remaining_errors.append((lang_dir.name, errors))
    
    print("\n" + "=" * 50)
    print(f"✅ Cleaned {total_fixed} files")
    
    if remaining_errors:
        print(f"\n⚠️  {len(remaining_errors)} files still have errors.")
        print("\nMarking problematic entries as fuzzy for retranslation...")
        
        fuzzy_count = 0
        for lang, errors in remaining_errors:
            po_file = locale_dir / lang / "LC_MESSAGES" / "messages.po"
            marked = mark_errors_as_fuzzy(po_file, errors)
            if marked > 0:
                print(f"  Marked {marked} entries as fuzzy in {lang}")
                fuzzy_count += 1
        
        print(f"\n✅ Fixed {fuzzy_count} files by marking errors as fuzzy")
        print("\nNow compiling all translations...")
        
        # Try to compile again
        result = subprocess.run(['pybabel', 'compile', '-d', 'locale'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All translations compiled successfully!")
            print("\nFuzzy entries will be retranslated on next run with --translate flag")
            print("Run: sh build_multilingual.sh --translate")
        else:
            print(f"⚠️  Some compilation errors remain")
    else:
        print("\n✨ All files are now clean!")
        print("\nNow compiling all translations...")
        
        # Compile all
        result = subprocess.run(['pybabel', 'compile', '-d', 'locale'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All translations compiled successfully!")
            print("\nYou can now run: sh build_multilingual.sh")
        else:
            print(f"⚠️  Some files failed to compile: {result.stderr}")


if __name__ == "__main__":
    main()