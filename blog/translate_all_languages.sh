#!/bin/bash

# BlogVi Translation Script - Translates all configured languages sequentially
# Excludes: English (source), Russian and German (already running)

echo "Starting BlogVi translations at $(date)"
echo "================================================"

# Path to the BlogVi run script
BLOGVI_SCRIPT="/Users/philippetrounev/PycharmProjects/docsie-site/.external/BlogVi/run_blog_gen.py"
BLOG_DIR="/Users/philippetrounev/PycharmProjects/docsie-site/blog"

# All languages from settings.yaml except en, ru, de
LANGUAGES=(
    "es"      # Spanish
    "ja"      # Japanese
    "pt-pt"   # Portuguese (Portugal)
    "sv"      # Swedish
    "zh"      # Chinese
    "pt-br"   # Portuguese (Brazil)
    "hu"      # Hungarian
    "ko"      # Korean
    "fr"      # French
    "it"      # Italian
    "nl"      # Dutch
    "da"      # Danish
    "no"      # Norwegian
    "tr"      # Turkish
    "pl"      # Polish
)

# Function to count cached articles for a language
count_cached_articles() {
    local lang=$1
    local count=$(ls -1 "$BLOG_DIR/.translation_cache/$lang/"*.json 2>/dev/null | wc -l | tr -d ' ')
    echo "$count"
}

# Log file
LOG_FILE="$BLOG_DIR/translation_log_$(date +%Y%m%d_%H%M%S).txt"

echo "Logging to: $LOG_FILE"
echo "Total languages to translate: ${#LANGUAGES[@]}"
echo "================================================"

# Main translation loop
for i in "${!LANGUAGES[@]}"; do
    lang="${LANGUAGES[$i]}"
    echo "================================================" | tee -a "$LOG_FILE"
    echo "[$((i+1))/${#LANGUAGES[@]}] Starting translation for: $lang at $(date)" | tee -a "$LOG_FILE"
    
    # Check existing cache
    cached_count=$(count_cached_articles "$lang")
    echo "Already cached articles for $lang: $cached_count" | tee -a "$LOG_FILE"
    
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
    if [ $i -lt $((${#LANGUAGES[@]} - 1)) ]; then
        echo "Waiting 60 seconds before next language..." | tee -a "$LOG_FILE"
        sleep 60
    fi
done

echo "================================================" | tee -a "$LOG_FILE"
echo "All translations completed at $(date)" | tee -a "$LOG_FILE"

# Summary report
echo -e "\nFINAL SUMMARY:" | tee -a "$LOG_FILE"
echo "================================================" | tee -a "$LOG_FILE"

# Check all languages including the ones that were already running
ALL_LANGS=("ru" "de" "${LANGUAGES[@]}")
total_cached=0

for lang in "${ALL_LANGS[@]}"; do
    count=$(count_cached_articles "$lang")
    total_cached=$((total_cached + count))
    printf "%-10s: %3d articles cached\n" "$lang" "$count" | tee -a "$LOG_FILE"
done

echo "================================================" | tee -a "$LOG_FILE"
echo "Total cached across all languages: $total_cached articles" | tee -a "$LOG_FILE"

echo -e "\nTranslation log saved to: $LOG_FILE"
echo -e "\nTo monitor progress in real-time, run:"
echo "tail -f $LOG_FILE"