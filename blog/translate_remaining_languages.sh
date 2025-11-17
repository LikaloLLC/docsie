#!/bin/bash

# BlogVi Translation Script - Translates only the remaining 4 languages
# Targets: Chinese, Portuguese BR, Hungarian, Norwegian

echo "Starting BlogVi translations for remaining languages at $(date)"
echo "================================================"

# Path to the BlogVi run script
BLOGVI_SCRIPT="/Users/philippetrounev/PycharmProjects/docsie-site/.external/BlogVi/run_blog_gen.py"
BLOG_DIR="/Users/philippetrounev/PycharmProjects/docsie-site/blog"

# Only the remaining untranslated languages
LANGUAGES=(
    "zh"      # Chinese
    "pt-br"   # Portuguese (Brazil)
    "hu"      # Hungarian
    "no"      # Norwegian
)

# Function to count cached articles for a language
count_cached_articles() {
    local lang=$1
    local count=$(ls -1 "$BLOG_DIR/.translation_cache/$lang/"*.json 2>/dev/null | wc -l | tr -d ' ')
    echo "$count"
}

# Check if languages are already translated
echo "Checking current translation status:"
echo "================================================"
skip_languages=()
for lang in "${LANGUAGES[@]}"; do
    cached_count=$(count_cached_articles "$lang")
    echo "$lang: $cached_count articles cached"
    if [ "$cached_count" -ge 189 ]; then
        echo "  ✓ $lang already fully translated, will skip"
        skip_languages+=("$lang")
    fi
done
echo "================================================"

# Remove already translated languages from the list
REMAINING_LANGUAGES=()
for lang in "${LANGUAGES[@]}"; do
    skip=false
    for skip_lang in "${skip_languages[@]}"; do
        if [ "$lang" = "$skip_lang" ]; then
            skip=true
            break
        fi
    done
    if [ "$skip" = false ]; then
        REMAINING_LANGUAGES+=("$lang")
    fi
done

if [ ${#REMAINING_LANGUAGES[@]} -eq 0 ]; then
    echo "All languages are already translated! Nothing to do."
    exit 0
fi

# Log file
LOG_FILE="$BLOG_DIR/translation_remaining_log_$(date +%Y%m%d_%H%M%S).txt"

echo ""
echo "Languages to translate: ${REMAINING_LANGUAGES[@]}"
echo "Logging to: $LOG_FILE"
echo "Total languages to translate: ${#REMAINING_LANGUAGES[@]}"
echo "================================================"

# Main translation loop
for i in "${!REMAINING_LANGUAGES[@]}"; do
    lang="${REMAINING_LANGUAGES[$i]}"
    echo "================================================" | tee -a "$LOG_FILE"
    echo "[$((i+1))/${#REMAINING_LANGUAGES[@]}] Starting translation for: $lang at $(date)" | tee -a "$LOG_FILE"
    
    # Check existing cache
    cached_count=$(count_cached_articles "$lang")
    echo "Already cached articles for $lang: $cached_count" | tee -a "$LOG_FILE"
    
    # Skip if already fully translated
    if [ "$cached_count" -ge 189 ]; then
        echo "✓ $lang already fully translated, skipping..." | tee -a "$LOG_FILE"
        continue
    fi
    
    # Run the translation
    echo "Running: python $BLOGVI_SCRIPT $BLOG_DIR --translate-only --languages $lang --all-ai" | tee -a "$LOG_FILE"
    
    # Execute translation with error handling
    if python "$BLOGVI_SCRIPT" "$BLOG_DIR" --translate-only --languages "$lang" --all-ai 2>&1 | tee -a "$LOG_FILE"; then
        echo "✓ Successfully completed translation for $lang at $(date)" | tee -a "$LOG_FILE"
    else
        echo "✗ Error during translation for $lang at $(date)" | tee -a "$LOG_FILE"
        echo "Continuing with next language..." | tee -a "$LOG_FILE"
    fi
    
    # Check final cache count
    final_count=$(count_cached_articles "$lang")
    new_articles=$((final_count - cached_count))
    echo "Final cached articles for $lang: $final_count (added: $new_articles)" | tee -a "$LOG_FILE"
    
    # Small delay between languages to avoid overwhelming the API
    if [ $i -lt $((${#REMAINING_LANGUAGES[@]} - 1)) ]; then
        echo "Waiting 60 seconds before next language..." | tee -a "$LOG_FILE"
        sleep 60
    fi
done

echo "================================================" | tee -a "$LOG_FILE"
echo "All translations completed at $(date)" | tee -a "$LOG_FILE"

# Summary report
echo -e "\nFINAL SUMMARY:" | tee -a "$LOG_FILE"
echo "================================================" | tee -a "$LOG_FILE"

# Check all 17 configured languages
ALL_LANGS=("en" "es" "fr" "de" "ja" "ko" "pt-pt" "pt-br" "ru" "zh" "it" "nl" "pl" "sv" "da" "no" "tr" "hu")
total_cached=0

for lang in "${ALL_LANGS[@]}"; do
    if [ "$lang" = "en" ]; then
        # English is source, not translated
        printf "%-10s: source language (not translated)\n" "$lang" | tee -a "$LOG_FILE"
    else
        count=$(count_cached_articles "$lang")
        total_cached=$((total_cached + count))
        printf "%-10s: %3d articles cached\n" "$lang" "$count" | tee -a "$LOG_FILE"
    fi
done

echo "================================================" | tee -a "$LOG_FILE"
echo "Total cached across all translated languages: $total_cached articles" | tee -a "$LOG_FILE"

# Cost estimation
total_articles=$((total_cached))
estimated_cost=$(echo "scale=2; $total_articles * 0.12" | bc)
echo "Estimated total translation cost: \$$estimated_cost" | tee -a "$LOG_FILE"

echo -e "\nTranslation log saved to: $LOG_FILE"
echo -e "\nTo monitor progress in real-time, run:"
echo "tail -f $LOG_FILE"