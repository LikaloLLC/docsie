#!/usr/bin/env python3
"""
Fix duplicate message definitions in .po files while preserving translations.
Uses msgmerge to clean up duplicates without losing any translated content.
"""

import os
import subprocess
import shutil
from pathlib import Path
import tempfile
<<<<<<< HEAD

def fix_duplicate_messages():
    """Fix duplicate messages in all .po files"""
    
    locale_dir = Path("locale")
    pot_file = locale_dir / "messages.pot"
    
    if not pot_file.exists():
        print("❌ Error: messages.pot not found. Run extraction first.")
        return False
    
    # Get all language directories
    lang_dirs = [d for d in locale_dir.iterdir() 
                 if d.is_dir() and d.name not in ['messages.pot', '.cache']]
    
    success_count = 0
    error_count = 0
    
    print("🔧 Fixing duplicate messages in .po files...")
    print(f"   Found {len(lang_dirs)} languages to process")
    print("")
    
    for lang_dir in sorted(lang_dirs):
        lang_code = lang_dir.name
        po_file = lang_dir / "LC_MESSAGES" / "messages.po"
        
        if not po_file.exists():
            print(f"⚠️  {lang_code}: No messages.po file found, skipping")
            continue
        
        print(f"Processing {lang_code}...", end=" ", flush=True)
        
        # Create backup
        backup_file = po_file.with_suffix('.po.backup')
        shutil.copy2(po_file, backup_file)
        
        # Create a temporary file for the cleaned output
        with tempfile.NamedTemporaryFile(mode='w', suffix='.po', delete=False) as tmp:
            tmp_path = Path(tmp.name)
        
        try:
            # First, use msguniq to remove duplicates
            msguniq_cmd = ['msguniq', str(po_file), '-o', str(tmp_path)]
            result = subprocess.run(msguniq_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ msguniq failed: {result.stderr}")
                error_count += 1
                continue
            
            # Then use msgmerge to merge with the pot file
            # This ensures all messages are properly aligned and formatted
            msgmerge_cmd = [
                'msgmerge',
                '--update',
                '--no-fuzzy-matching',  # Don't create fuzzy entries
                '--backup=off',          # Don't create backup files
                str(tmp_path),
                str(pot_file)
            ]
            
            result = subprocess.run(msgmerge_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Copy the cleaned file back
                shutil.copy2(tmp_path, po_file)
                print("✅")
                success_count += 1
                
                # Remove backup if successful
                backup_file.unlink()
            else:
                print(f"❌ msgmerge failed: {result.stderr}")
                # Restore from backup
                shutil.copy2(backup_file, po_file)
                error_count += 1
                
        except Exception as e:
            print(f"❌ Error: {e}")
            # Restore from backup
            if backup_file.exists():
                shutil.copy2(backup_file, po_file)
            error_count += 1
            
        finally:
            # Clean up temporary file
            if tmp_path.exists():
                tmp_path.unlink()
    
    print("")
    print("=" * 50)
    print(f"✅ Successfully fixed: {success_count} languages")
    if error_count > 0:
        print(f"❌ Failed: {error_count} languages")
    
    # Now compile all the cleaned files
    print("")
    print("📦 Compiling cleaned translation files...")
    
=======
import re

def clean_embedded_conflicts_and_remove_fuzzy(po_path: Path):
    """
    Remove fuzzy flags and clean embedded conflict markers in msgstr,
    keeping only the first (or best) translation chunk.
    """
    with po_path.open('r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    in_msgstr = False
    msgstr_buffer = []
    conflict_detected = False

    for line in lines:
        # Skip fuzzy flags
        if line.strip() == '#, fuzzy':
            continue

        if line.startswith('msgstr '):
            in_msgstr = True
            msgstr_buffer = [line]
            conflict_detected = False
            continue

        if in_msgstr and (line.startswith('"') or line.strip() == ''):
            msgstr_buffer.append(line)
            if '#-#-#' in line:
                conflict_detected = True
            continue
        elif in_msgstr:
            # msgstr block ended, clean if conflicted
            if conflict_detected:
                cleaned_msgstr = clean_conflict_msgstr(msgstr_buffer)
                cleaned_lines.extend(cleaned_msgstr)
            else:
                cleaned_lines.extend(msgstr_buffer)
            msgstr_buffer = []
            in_msgstr = False
            cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)

    # Handle end of file inside msgstr block
    if in_msgstr:
        if conflict_detected:
            cleaned_msgstr = clean_conflict_msgstr(msgstr_buffer)
            cleaned_lines.extend(cleaned_msgstr)
        else:
            cleaned_lines.extend(msgstr_buffer)

    with po_path.open('w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)


def clean_conflict_msgstr(lines):
    """
    From list of msgstr lines with embedded conflict markers,
    keep only first translation chunk inside msgstr.
    """
    full = ''.join(lines)
    # Remove initial msgstr "" line
    full = re.sub(r'^msgstr\s+""\s*', '', full)

    # Split at conflict markers, which look like: "#-#-#-#-# ... #-#-#-#-#\n"
    chunks = re.split(r'"#-#-#-#-#.*?#-#-#-#-#\\n?"\n?', full, flags=re.DOTALL)
    if len(chunks) < 2:
        # no proper split, return original lines
        return lines

    first_translation = chunks[1].strip()

    # Rebuild clean msgstr
    clean = ['msgstr ""\n']
    for line in first_translation.splitlines():
        # Strip extra quotes if present and escape inner quotes if any
        line = line.strip()
        # Remove leading/trailing quotes if accidentally kept
        clean.append(line if line.startswith('"') else f'"{line}"\n')

    return clean


def fix_duplicate_messages():
    """Fix duplicate messages in all .po files, clean conflict markers, and compile"""

    locale_dir = Path("locale")
    pot_file = locale_dir / "messages.pot"

    if not pot_file.exists():
        print("❌ Error: messages.pot not found. Run extraction first.")
        return False

    lang_dirs = [d for d in locale_dir.iterdir()
                 if d.is_dir() and d.name not in ['messages.pot', '.cache']]

    success_count = 0
    error_count = 0

    print("🔧 Fixing duplicate/conflict messages in .po files...")
    print(f"   Found {len(lang_dirs)} languages to process\n")

    for lang_dir in sorted(lang_dirs):
        lang_code = lang_dir.name
        po_file = lang_dir / "LC_MESSAGES" / "messages.po"

        if not po_file.exists():
            print(f"⚠️  {lang_code}: No messages.po file found, skipping")
            continue

        print(f"Processing {lang_code}...", end=" ", flush=True)

        backup_file = po_file.with_suffix('.po.backup')
        shutil.copy2(po_file, backup_file)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.po', delete=False) as tmp:
            tmp_path = Path(tmp.name)

        try:
            # Step 1: Deduplicate with msgcat (keep first)
            msgcat_cmd = ['msgcat', '--use-first', str(po_file), '-o', str(tmp_path)]
            result = subprocess.run(msgcat_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ msgcat failed: {result.stderr}")
                error_count += 1
                continue

            # Step 2: Merge with .pot to update formatting
            msgmerge_cmd = [
                'msgmerge',
                '--update',
                '--no-fuzzy-matching',
                '--backup=off',
                str(tmp_path),
                str(pot_file)
            ]
            result = subprocess.run(msgmerge_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ msgmerge failed: {result.stderr}")
                shutil.copy2(backup_file, po_file)
                error_count += 1
                continue

            # Step 3: Overwrite original .po file
            shutil.copy2(tmp_path, po_file)

            # Step 4: Clean embedded conflict markers inside msgstrs
            clean_embedded_conflicts_and_remove_fuzzy(po_file)

            print("✅")
            success_count += 1
            backup_file.unlink()

        except Exception as e:
            print(f"❌ Error: {e}")
            if backup_file.exists():
                shutil.copy2(backup_file, po_file)
            error_count += 1
        finally:
            if tmp_path.exists():
                tmp_path.unlink()

    print("\n" + "=" * 50)
    print(f"✅ Successfully fixed: {success_count} languages")
    if error_count > 0:
        print(f"❌ Failed: {error_count} languages")

    print("\n📦 Compiling cleaned translation files...")
>>>>>>> pr-148
    compile_result = subprocess.run(
        ['pybabel', 'compile', '-d', 'locale'],
        capture_output=True,
        text=True
    )
<<<<<<< HEAD
    
=======
>>>>>>> pr-148
    if compile_result.returncode == 0:
        print("✅ All translations compiled successfully!")
    else:
        print(f"⚠️  Some files failed to compile: {compile_result.stderr}")
<<<<<<< HEAD
    
    return success_count > 0


def verify_translations():
    """Verify that translations are still intact after cleanup"""
    
    print("")
    print("🔍 Verifying translations...")
    
    locale_dir = Path("locale")
    
    for lang_dir in sorted(locale_dir.iterdir()):
        if not lang_dir.is_dir() or lang_dir.name in ['messages.pot', '.cache']:
            continue
            
        po_file = lang_dir / "LC_MESSAGES" / "messages.po"
        if not po_file.exists():
            continue
            
        # Count translated messages
        cmd = ['msgfmt', '--statistics', str(po_file), '-o', '/dev/null']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Statistics are printed to stderr
        stats = result.stderr.strip()
        if stats:
            print(f"   {lang_dir.name}: {stats}")


if __name__ == "__main__":
    print("🧹 Duplicate Message Fixer for Docsie")
    print("=" * 50)
    print("This script will:")
    print("1. Back up all .po files")
    print("2. Remove duplicate messages using msguniq")
    print("3. Merge with messages.pot using msgmerge")
    print("4. Compile all translations")
    print("5. Verify translation statistics")
    print("")
    
    # Check for required tools
    required_tools = ['msguniq', 'msgmerge', 'msgfmt', 'pybabel']
    missing_tools = []
    
    for tool in required_tools:
        result = subprocess.run(['which', tool], capture_output=True)
        if result.returncode != 0:
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"❌ Missing required tools: {', '.join(missing_tools)}")
        print("   Install gettext package: brew install gettext")
        exit(1)
    
    # Run the fixer
    if fix_duplicate_messages():
        verify_translations()
        print("")
        print("✨ All done! Your translations are clean and preserved.")
        print("   You can now run: sh build_multilingual.sh --translate")
    else:
        print("")
        print("❌ Failed to fix duplicate messages")
        exit(1)
=======

    return success_count > 0

if __name__ == "__main__":
    fix_duplicate_messages()
>>>>>>> pr-148
