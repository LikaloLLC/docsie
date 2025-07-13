#!/usr/bin/env python3
"""
Build Helper - Centralized build utilities for Docsie
Handles pre-build tasks like image optimization
"""

import os
import sys
import subprocess
from pathlib import Path

class BuildHelper:
    def __init__(self):
        self.root_path = Path(__file__).parent.parent
        
    def optimize_images(self, force=False):
        """
        Run image optimization before build
        This is smart - it only optimizes new/changed images
        """
        print("🖼️  Checking for images that need optimization...")
        
        # Path to the optimization script
        optimizer_script = self.root_path / 'utils' / 'optimize_images_v2.py'
        
        if not optimizer_script.exists():
            print("❌ Image optimizer script not found!")
            return False
            
        try:
            # Build command
            cmd = [sys.executable, str(optimizer_script)]
            if force:
                cmd.append('--force')
                
            # Run the optimizer
            result = subprocess.run(
                cmd,
                cwd=str(self.root_path),
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Check if any images were actually optimized
                if "✅ Optimized:" in result.stdout:
                    print("✅ Images optimized successfully")
                else:
                    print("✔️  All images already optimized")
                return True
            else:
                print(f"❌ Image optimization failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error running image optimizer: {e}")
            return False
    
    def pre_build(self, force_optimize=False):
        """
        Run all pre-build tasks
        """
        print("\n🔧 Running pre-build tasks...")
        
        # 1. Optimize images
        if not self.optimize_images(force=force_optimize):
            print("⚠️  Warning: Image optimization failed, continuing build...")
        
        # Future: Add other pre-build tasks here
        # - Check for missing translations
        # - Validate YAML files
        # - etc.
        
        print("✅ Pre-build tasks complete\n")
        return True

def main():
    """CLI interface for build helper"""
    import argparse
    parser = argparse.ArgumentParser(description='Docsie build helper')
    parser.add_argument('--optimize-images', action='store_true', 
                        help='Run image optimization only')
    parser.add_argument('--force', action='store_true',
                        help='Force re-optimization of all images')
    
    args = parser.parse_args()
    
    helper = BuildHelper()
    
    if args.optimize_images:
        helper.optimize_images(force=args.force)
    else:
        helper.pre_build(force_optimize=args.force)

if __name__ == '__main__':
    main()