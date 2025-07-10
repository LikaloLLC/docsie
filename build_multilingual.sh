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
    
    # Extract from templates and Python files
    pybabel extract -F babel.cfg -o locale/messages.pot . || {
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

# Function to compile translation files
compile_translations() {
    local langs="$1"
    print_step "Compiling translation files..."
    
    if [ -z "$langs" ]; then
        # Compile all
        pybabel compile -d locale || {
            print_error "Failed to compile translations"
            return 1
        }
    else
        # Compile specific languages
        for lang in $langs; do
            if [ "$lang" != "en" ]; then
                pybabel compile -d locale -l $lang || {
                    print_warning "Failed to compile $lang"
                }
            fi
        done
    fi
    
    print_success "Translation compilation complete"
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
    echo "  -f, --force         Force re-translation (ignore cache)"
    echo "  -v, --verbose       Verbose output"
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
    echo ""
}

# Parse command line arguments
SKIP_EXTRACT=true      # Default to skipping extraction
SKIP_TRANSLATE=true    # Default to skipping API translation
SKIP_YAML=true         # Default to skipping YAML translation
SKIP_GENERATE=false
EXTRACT_ONLY=false
TRANSLATE_ONLY=false
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
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
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
    else
        echo "Mode: Full build"
    fi
    echo ""
    
    # Check dependencies
    check_dependencies
    
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