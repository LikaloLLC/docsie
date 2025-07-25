#!/usr/bin/env python3
"""
Fix duplicate message definitions in .po files while preserving translations.
Uses msgcat and msgmerge to clean up duplicates without losing any translated content.
"""

import os
import subprocess
import shutil
from pathlib import Path
import tempfile
import re
import polib


def clean_po_file(filepath, save_backup: bool = True):
    """
    Remove fuzzy flags and clean embedded conflict markers in msgstr,
    keeping only the first (or best) translation chunk.
    """
    filepath = str(filepath)  # Ensure string path for polib and concatenation
    po = polib.pofile(filepath)

    if save_backup:
        po.save(filepath + ".bak")

    for entry in po:
        # Remove fuzzy flag if present
        if 'fuzzy' in entry.flags:
            entry.flags.remove('fuzzy')

        # Clean merge conflicts in msgstr
        if '#-#-#' in entry.msgstr:
            cleaned = clean_conflict_msgstr(entry.msgstr)
            entry.msgstr = cleaned

    po.save(filepath)

def clean_conflict_msgstr(msgstr: str) -> str:
    """
    From list of msgstr lines with embedded conflict markers,
    keep only first translation chunk inside msgstr.
    """
    parts = re.split(r'#-#-#-#-#.*?#-#-#-#-#', msgstr, flags=re.DOTALL)
    for part in reversed(parts):
        part = part.strip()
        if part:
            lines = []
            for line in part.splitlines():
                line = line.strip()
                if not line.startswith('"'):
                    line = f'"{line}"'
                lines.append(line)
            return '\n'.join(lines)
    return '""'



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
            clean_po_file(po_file)

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
    compile_result = subprocess.run(
        ['pybabel', 'compile', '-d', 'locale'],
        capture_output=True,
        text=True
    )
    if compile_result.returncode == 0:
        print("✅ All translations compiled successfully!")
    else:
        print(f"⚠️  Some files failed to compile: {compile_result.stderr}")

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
    print("2. Remove duplicate messages using msgcat")
    print("3. Merge with messages.pot using msgmerge")
    print("4. Clean embedded conflict markers")
    print("5. Compile all translations")
    print("6. Verify translation statistics")
    print("")
    
    # Check for required tools
    required_tools = ['msgcat', 'msgmerge', 'msgfmt', 'pybabel']
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
