#!/bin/bash

# Build Multilingual Site Script
# Orchestrates the complete translation and build workflow for Docsie

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
PYTHON_CMD="${PYTHON_CMD:-python3}"
DEFAULT_LANGS=""  # Empty means all languages
SKIP_CACHE=false
VERBOSE=false
QUICK_MODE=false

# Function to print colored output
print_step() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check dependencies
check_dependencies() {
    print_step "Checking dependencies..."
    
    # Check Python
    if ! command_exists "$PYTHON_CMD"; then
        print_error "Python not found. Please install Python 3.8+ or set PYTHON_CMD environment variable"
        exit 1
    fi
    
    # Check required Python packages
    $PYTHON_CMD -c "import yaml" 2>/dev/null || {
        print_error "PyYAML not installed. Run: pip install -r requirements.txt"
        exit 1
    }
    
    $PYTHON_CMD -c "import jinja2" 2>/dev/null || {
        print_error "Jinja2 not installed. Run: pip install -r requirements.txt"
        exit 1
    }
    
    $PYTHON_CMD -c "import babel" 2>/dev/null || {
        print_error "Babel not installed. Run: pip install -r requirements.txt"
        exit 1
    }
    
    # Check for .env file
    if [ ! -f ".env" ]; then
        print_warning "No .env file found. Make sure ANTHROPIC_API_KEY is set for translations"
    fi
    
    print_success "All dependencies checked"
}

# Function to extract translatable strings
extract_strings() {
    print_step "Extracting translatable strings..."
    
    # Extract from templates and Python files in src directory only
    pybabel extract -F babel.cfg -o locale/messages.pot src/ || {
        print_error "Failed to extract strings"
        return 1
    }
    
    # Extract from YAML files if the script exists
    if [ -f "extract_yaml_strings.py" ]; then
        $PYTHON_CMD extract_yaml_strings.py || {
            print_warning "Failed to extract YAML strings"
        }
    fi
    
    print_success "String extraction complete"
}

# Function to update/initialize translation files
update_translations() {
    local langs="$1"
    print_step "Updating translation files..."
    
    if [ -z "$langs" ]; then
        # Get all enabled languages from config
        langs=$($PYTHON_CMD -c "
import yaml
with open('translation_config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    enabled = [code for code, info in config['languages'].items() if info.get('enabled', False)]
    print(' '.join(enabled))
" 2>/dev/null || echo "")
    fi
    
    for lang in $langs; do
        if [ "$lang" = "en" ]; then
            continue
        fi
        
        if [ -f "locale/$lang/LC_MESSAGES/messages.po" ]; then
            # Update existing
            pybabel update -i locale/messages.pot -d locale -l $lang || {
                print_warning "Failed to update $lang"
            }
        else
            # Initialize new
            mkdir -p locale/$lang/LC_MESSAGES
            pybabel init -i locale/messages.pot -d locale -l $lang || {
                print_warning "Failed to initialize $lang"
            }
        fi
    done
    
    print_success "Translation files updated"
}

# Function to translate missing strings using Claude API
translate_missing() {
    local langs="$1"
    print_step "Translating missing strings with Claude API..."
    
    if [ -n "$langs" ]; then
        # Specific languages
        $PYTHON_CMD translation_system.py translate $langs || {
            print_warning "Some translations may have failed"
        }
    else
        # All languages
        $PYTHON_CMD translation_system.py translate --all || {
            print_warning "Some translations may have failed"
        }
    fi
    
    print_success "API translation complete"
}

# Function to fix duplicate messages in .po files
fix_duplicate_messages() {
    local langs="$1"
    print_step "Fixing duplicate messages in translation files..."
    
    if [ -z "$langs" ]; then
        # Get all languages
        langs=$(ls locale | grep -v messages.pot | grep -v .cache | tr '\n' ' ')
    fi
    
    local fixed_count=0
    local error_count=0
    
    for lang in $langs; do
        if [ "$lang" = "en" ]; then
            continue
        fi
        
        local po_file="locale/$lang/LC_MESSAGES/messages.po"
        if [ ! -f "$po_file" ]; then
            continue
        fi
        
        # Create backup
        cp "$po_file" "$po_file.backup"
        
        # Remove duplicates using msguniq
        if msguniq "$po_file" -o "$po_file.tmp" 2>/dev/null; then
            # Merge with pot file to ensure proper formatting
            if msgmerge --update --no-fuzzy-matching --backup=off "$po_file.tmp" locale/messages.pot 2>/dev/null; then
                mv "$po_file.tmp" "$po_file"
                ((fixed_count++))
                rm -f "$po_file.backup"
            else
                mv "$po_file.backup" "$po_file"
                ((error_count++))
            fi
        else
            ((error_count++))
        fi
        
        rm -f "$po_file.tmp"
    done
    
    if [ $fixed_count -gt 0 ]; then
        print_success "Fixed $fixed_count language files"
    fi
    if [ $error_count -gt 0 ]; then
        print_warning "$error_count files had errors"
    fi
}

# Function to fix format placeholder errors and remove incorrect format flags
fix_placeholder_errors() {
    local langs="$1"
    print_step "Fixing placeholder format errors and format flags..."
    
    # First, use msgattrib to remove python-format flags from messages without placeholders
    if [ -z "$langs" ]; then
        langs=$(ls locale | grep -v messages.pot | grep -v .cache | tr '\n' ' ')
    fi
    
    for lang in $langs; do
        if [ "$lang" = "en" ]; then
            continue
        fi
        
        local po_file="locale/$lang/LC_MESSAGES/messages.po"
        if [ ! -f "$po_file" ]; then
            continue
        fi
        
        # Remove python-format flag from entries without actual format strings
        msgattrib --no-python-format "$po_file" -o "$po_file.tmp" 2>/dev/null && mv "$po_file.tmp" "$po_file"
    done
    
    # Create a more robust Python script for fixing placeholders
    cat > /tmp/fix_placeholders.py << 'EOF'
#!/usr/bin/env python3
import re
import sys
from pathlib import Path

def fix_po_file(po_file_path):
    """Fix placeholder mismatches in a .po file"""
    
    with open(po_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_count = 0
    i = 0
    
    while i < len(lines):
        # Find msgid/msgstr pairs
        if lines[i].startswith('msgid "'):
            msgid_lines = [lines[i]]
            i += 1
            
            # Collect multi-line msgid
            while i < len(lines) and lines[i].startswith('"'):
                msgid_lines.append(lines[i])
                i += 1
            
            # Now we should be at msgstr
            if i < len(lines) and lines[i].startswith('msgstr "'):
                msgstr_lines = [lines[i]]
                msgstr_start = i
                i += 1
                
                # Collect multi-line msgstr
                while i < len(lines) and lines[i].startswith('"'):
                    msgstr_lines.append(lines[i])
                    i += 1
                
                # Extract full strings
                msgid = ''.join(line.strip()[1:-1] for line in msgid_lines if line.strip().startswith('"'))
                msgstr = ''.join(line.strip()[1:-1] for line in msgstr_lines if line.strip().startswith('"'))
                
                if msgstr:  # Only process translated strings
                    # Extract placeholders
                    msgid_ph = re.findall(r'%(?:\([^)]+\))?[sdiouxXeEfFgGcrp%]', msgid)
                    msgstr_ph = re.findall(r'%(?:\([^)]+\))?[sdiouxXeEfFgGcrp%]', msgstr)
                    
                    # Fix if same number of placeholders but wrong types
                    if msgid_ph and msgstr_ph and len(msgid_ph) == len(msgstr_ph):
                        new_msgstr = msgstr
                        changed = False
                        
                        for orig, trans in zip(msgid_ph, msgstr_ph):
                            if orig != trans:
                                # Replace the wrong placeholder with the correct one
                                new_msgstr = new_msgstr.replace(trans, orig, 1)
                                changed = True
                        
                        if changed:
                            # Reconstruct msgstr lines
                            if len(msgstr_lines) == 1:
                                lines[msgstr_start] = f'msgstr "{new_msgstr}"\n'
                            else:
                                # Handle multi-line msgstr
                                # Keep the structure but update content
                                lines[msgstr_start] = 'msgstr ""\n'
                                lines[msgstr_start + 1] = f'"{new_msgstr}"\n'
                                # Remove extra lines if any
                                for j in range(msgstr_start + 2, msgstr_start + len(msgstr_lines)):
                                    if j < len(lines):
                                        lines[j] = ''
                            
                            fixed_count += 1
        else:
            i += 1
    
    if fixed_count > 0:
        # Write back
        with open(po_file_path, 'w', encoding='utf-8') as f:
            f.writelines(line for line in lines if line)
        
    return fixed_count

# Main
import os
langs = sys.argv[1:] if len(sys.argv) > 1 else []
if not langs:
    langs = [d for d in os.listdir('locale') if os.path.isdir(f'locale/{d}') and d not in ['messages.pot', '.cache']]

total_fixed = 0
for lang in langs:
    if lang == 'en':
        continue
    
    po_file = Path(f'locale/{lang}/LC_MESSAGES/messages.po')
    if po_file.exists():
        fixed = fix_po_file(po_file)
        if fixed > 0:
            print(f"  Fixed {fixed} placeholders in {lang}")
            total_fixed += 1

print(f"\nTotal files fixed: {total_fixed}")
EOF
    
    # Run the Python script
    $PYTHON_CMD /tmp/fix_placeholders.py $langs || print_warning "Some placeholder fixes may have failed"
    
    # Clean up
    rm -f /tmp/fix_placeholders.py
}

# Function to compile translation files
compile_translations() {
    local langs="$1"
    print_step "Compiling translation files..."
    
    if [ -z "$langs" ]; then
        # Compile all with -f flag to force compilation despite errors
        pybabel compile -d locale -f 2>&1 | {
            error_count=0
            while IFS= read -r line; do
                if [[ "$line" == *"error:"* ]]; then
                    ((error_count++))
                fi
            done
            
            if [ $error_count -gt 0 ]; then
                print_warning "Compiled with $error_count format errors (translations will work but may have issues)"
                print_warning "Run with --force flag to retranslate and fix these errors"
            else
                print_success "Translation compilation complete"
            fi
        }
    else
        # Compile specific languages
        for lang in $langs; do
            if [ "$lang" != "en" ]; then
                pybabel compile -d locale -l $lang -f 2>&1 | grep -q "error:" && {
                    print_warning "Compiled $lang with format errors"
                } || {
                    print_success "Compiled $lang successfully"
                }
            fi
        done
    fi
}

# Function to translate YAML files
translate_yaml() {
    local langs="$1"
    print_step "Translating YAML content files..."
    
    # Check which translator is available
    if [ -f "yaml_translator_mt.py" ]; then
        # Use multi-threaded translator with caching (fastest for immediate results)
        print_step "Using multi-threaded translator with caching..."
        
        if [ -n "$langs" ]; then
            # Specific languages
            $PYTHON_CMD yaml_translator_mt.py $langs || {
                print_warning "Failed to translate YAML for $langs"
            }
        else
            # All languages - get from locale directory
            LANGS=$(ls locale | grep -v messages.pot | grep -v .cache | tr '\n' ' ')
            $PYTHON_CMD yaml_translator_mt.py $LANGS || {
                print_warning "Some YAML translations may have failed"
            }
        fi
    elif [ -f "yaml_batch_translator.py" ]; then
        # Use batch translator (cheaper but slower)
        print_step "Using batch translator for YAML files..."
        
        if [ -n "$langs" ]; then
            # Specific languages
            for lang in $langs; do
                $PYTHON_CMD yaml_batch_translator.py -l $lang $FORCE_FLAG || {
                    print_warning "Failed to translate YAML for $lang"
                }
            done
        else
            # All languages
            $PYTHON_CMD yaml_batch_translator.py $FORCE_FLAG || {
                print_warning "Some YAML translations may have failed"
            }
        fi
    elif [ -f "yaml_translator.py" ]; then
        # Fallback to single-file translator
        print_warning "Using single-file translator (slower). Consider using yaml_batch_translator.py"
        
        if [ -n "$langs" ]; then
            # Specific languages
            for lang in $langs; do
                $PYTHON_CMD yaml_translator.py -l $lang $FORCE_FLAG || {
                    print_warning "Failed to translate YAML for $lang"
                }
            done
        else
            # All languages
            $PYTHON_CMD yaml_translator.py $FORCE_FLAG || {
                print_warning "Some YAML translations may have failed"
            }
        fi
    else
        print_warning "No YAML translator found, skipping YAML translation"
        return 0
    fi
    
    print_success "YAML translation complete"
}

# Function to run pre-build tasks
run_prebuild() {
    print_step "Running pre-build tasks (image optimization, etc.)..."
    
    # Generate pricing HTML from configuration
    if [ -f "generate_pricing_html.py" ]; then
        print_step "Generating pricing HTML from configuration..."
        $PYTHON_CMD generate_pricing_html.py || {
            print_warning "Failed to generate pricing HTML, continuing..."
        }
    fi
    
    # Run additional build helper tasks
    if [ -f "utils/build_helper.py" ]; then
        $PYTHON_CMD utils/build_helper.py || {
            print_warning "Pre-build tasks failed, continuing..."
        }
    fi
    
    print_success "Pre-build tasks complete"
}

# Function to generate main site
generate_main_site() {
    print_step "Generating main site with main.py..."
    
    $PYTHON_CMD main.py || {
        print_error "Failed to generate main site"
        return 1
    }
    
    print_success "Main site generated"
}

# Function to generate supplementary pages (English)
generate_supplementary_en() {
    print_step "Generating English supplementary pages..."
    
    $PYTHON_CMD supplementary_site_generator.py || {
        print_error "Failed to generate supplementary pages"
        return 1
    }
    
    print_success "English supplementary pages generated"
}

# Function to generate multilingual pages
generate_multilingual() {
    local langs="$1"
    print_step "Generating multilingual site..."
    
    # Generate main multilingual pages
    if [ -f "generate_all_languages.py" ]; then
        $PYTHON_CMD generate_all_languages.py || {
            print_error "Failed to generate multilingual pages"
            return 1
        }
    fi
    
    # Generate supplementary multilingual pages
    if [ -f "generate_supplementary_multilingual.py" ]; then
        $PYTHON_CMD generate_supplementary_multilingual.py || {
            print_error "Failed to generate supplementary multilingual pages"
            return 1
        }
    fi
    
    print_success "Multilingual site generated"
}

# Function to show usage
usage() {
    echo "Usage: $0 [OPTIONS] [LANGUAGES]"
    echo ""
    echo "Build multilingual Docsie site with translations"
    echo ""
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  -q, --quick         Quick mode: skip extraction and API translation"
    echo "  -f, --force         Force re-translation (ignore cache, run everything)"
    echo "  -t, --translate     Enable translation (don't skip extraction/translation)"
    echo "  -v, --verbose       Verbose output"
    echo "  --fix               Fix translation errors (duplicates, placeholders)"
    echo "  --skip-extract      Skip string extraction"
    echo "  --skip-translate    Skip API translation"
    echo "  --skip-yaml         Skip YAML translation"
    echo "  --skip-generate     Skip site generation"
    echo "  --extract-only      Only extract strings and exit"
    echo "  --translate-only    Only translate and exit"
    echo ""
    echo "Examples:"
    echo "  $0                  # Build everything for all languages"
    echo "  $0 de fr es         # Build for specific languages"
    echo "  $0 --quick          # Quick rebuild (skip extraction/translation)"
    echo "  $0 --force ru       # Force retranslate Russian"
    echo "  $0 --fix            # Fix translation errors before building"
    echo ""
}

# Parse command line arguments
SKIP_EXTRACT=true      # Default to skipping extraction
SKIP_TRANSLATE=true    # Default to skipping API translation
SKIP_YAML=true         # Default to skipping YAML translation
SKIP_GENERATE=false
EXTRACT_ONLY=false
TRANSLATE_ONLY=false
FIX_ONLY=false
FORCE_FLAG=""
LANGUAGES=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -q|--quick)
            QUICK_MODE=true
            SKIP_EXTRACT=true
            SKIP_TRANSLATE=true
            shift
            ;;
        -f|--force)
            FORCE_FLAG="--force"
            SKIP_CACHE=true
            SKIP_EXTRACT=false
            SKIP_TRANSLATE=false
            SKIP_YAML=false
            shift
            ;;
        -t|--translate)
            SKIP_EXTRACT=false
            SKIP_TRANSLATE=false
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        --fix)
            FIX_ONLY=true
            shift
            ;;
        --skip-extract)
            SKIP_EXTRACT=true
            shift
            ;;
        --skip-translate)
            SKIP_TRANSLATE=true
            shift
            ;;
        --skip-yaml)
            SKIP_YAML=true
            shift
            ;;
        --skip-generate)
            SKIP_GENERATE=true
            shift
            ;;
        --extract-only)
            EXTRACT_ONLY=true
            shift
            ;;
        --translate-only)
            TRANSLATE_ONLY=true
            shift
            ;;
        -*)
            print_error "Unknown option: $1"
            usage
            exit 1
            ;;
        *)
            # Assume it's a language code
            LANGUAGES="$LANGUAGES $1"
            shift
            ;;
    esac
done

# Main workflow
main() {
    echo -e "${GREEN}🚀 Docsie Multilingual Build System${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Show configuration
    if [ -n "$LANGUAGES" ]; then
        echo "Languages: $LANGUAGES"
    else
        echo "Languages: All enabled"
    fi
    
    if [ "$QUICK_MODE" = true ]; then
        echo "Mode: Quick (skip extraction & API translation)"
    elif [ "$EXTRACT_ONLY" = true ]; then
        echo "Mode: Extract only"
    elif [ "$TRANSLATE_ONLY" = true ]; then
        echo "Mode: Translate only"
    elif [ "$FIX_ONLY" = true ]; then
        echo "Mode: Fix translation errors"
    else
        echo "Mode: Full build"
    fi
    echo ""
    
    # Check dependencies
    check_dependencies
    
    # Fix-only mode
    if [ "$FIX_ONLY" = true ]; then
        fix_duplicate_messages "$LANGUAGES"
        fix_placeholder_errors "$LANGUAGES"
        compile_translations "$LANGUAGES"
        print_success "Translation fixes complete!"
        exit 0
    fi
    
    # Extract strings
    if [ "$EXTRACT_ONLY" = true ]; then
        extract_strings
        update_translations "$LANGUAGES"
        print_success "Extraction complete!"
        exit 0
    fi
    
    # Step 1: Extract translatable strings
    if [ "$SKIP_EXTRACT" = false ]; then
        extract_strings
        update_translations "$LANGUAGES"
    fi
    
    # Step 2: Translate missing strings
    if [ "$SKIP_TRANSLATE" = false ]; then
        translate_missing "$LANGUAGES"
        compile_translations "$LANGUAGES"
    fi
    
    # Step 3: Translate YAML files
    if [ "$SKIP_YAML" = false ]; then
        translate_yaml "$LANGUAGES"
    fi
    
    # Translate only mode
    if [ "$TRANSLATE_ONLY" = true ]; then
        print_success "Translation complete!"
        exit 0
    fi
    
    # Step 4: Generate sites
    if [ "$SKIP_GENERATE" = false ]; then
        # Run pre-build tasks including pricing HTML generation
        run_prebuild
        
        # Generate main site (English)
        generate_main_site
        
        # Generate supplementary pages (English)
        generate_supplementary_en
        
        # Generate multilingual versions
        generate_multilingual "$LANGUAGES"
    fi
    
    echo ""
    echo -e "${GREEN}✨ Build complete!${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Show next steps
    echo -e "\n${BLUE}Next steps:${NC}"
    echo "1. Test locally: sh start.sh"
    echo "2. Commit changes: git add . && git commit -m 'Update translations'"
    echo "3. Deploy: git push origin main"
}

# Run main function
main