#!/bin/bash

# Script to untrack language-specific generated files that shouldn't be in git

echo "Untracking language-specific generated files..."

# Find all language directories
for lang_dir in ar bn cs da de el es fi fr he hi hr hu id it ja ko ms nl no pl pt ro ru sr sv ta th tr uk ur vi zh; do
    # Untrack all styles directories in language folders
    if [ -d "$lang_dir/styles" ]; then
        echo "Processing $lang_dir/styles/..."
        git rm -r --cached "$lang_dir/styles/" 2>/dev/null || true
    fi
    
    # Untrack pricing_v2 generated files
    if [ -d "$lang_dir/pricing_v2" ]; then
        for file in generated_plan_cards.html index_backup.html plans_value_focused.html; do
            if [ -f "$lang_dir/pricing_v2/$file" ]; then
                echo "Processing $lang_dir/pricing_v2/$file"
                git rm --cached "$lang_dir/pricing_v2/$file" 2>/dev/null || true
            fi
        done
    fi
    
done

echo "Done! The files have been untracked but remain in your working directory."
echo "They will now be ignored by git according to .gitignore rules."