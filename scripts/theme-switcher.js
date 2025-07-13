/**
 * Theme Switcher for A/B Testing Monochrome vs Color
 * YC-inspired minimal design for potentially higher conversions
 */

(function() {
  'use strict';
  
  // Configuration
  const THEMES = {
    COLOR: 'color',
    MONOCHROME: 'monochrome'
  };
  
  const STORAGE_KEY = 'docsie-theme-preference';
  const AB_TEST_KEY = 'docsie-theme-ab-test';
  const AB_TEST_ENABLED = true; // Set to false to disable A/B testing
  
  class ThemeSwitcher {
    constructor() {
      this.currentTheme = this.getTheme();
      this.init();
    }
    
    init() {
      // Apply theme on load
      this.applyTheme(this.currentTheme);
      
      // Track theme view in analytics
      this.trackThemeView(this.currentTheme);
      
      // Add theme toggle button (optional - for testing)
      if (window.location.search.includes('theme-toggle')) {
        this.addToggleButton();
      }
    }
    
    getTheme() {
      // Check for manual preference first
      const savedTheme = localStorage.getItem(STORAGE_KEY);
      if (savedTheme) {
        return savedTheme;
      }
      
      // A/B Test: Randomly assign theme
      if (AB_TEST_ENABLED) {
        let abTestVariant = localStorage.getItem(AB_TEST_KEY);
        if (!abTestVariant) {
          // 50/50 split
          abTestVariant = Math.random() < 0.5 ? THEMES.COLOR : THEMES.MONOCHROME;
          localStorage.setItem(AB_TEST_KEY, abTestVariant);
          
          // Track assignment in analytics
          if (typeof gtag !== 'undefined') {
            gtag('event', 'ab_test_assigned', {
              'experiment_name': 'theme_color_vs_monochrome',
              'variant': abTestVariant
            });
          }
        }
        return abTestVariant;
      }
      
      // Default to color theme
      return THEMES.COLOR;
    }
    
    applyTheme(theme) {
      const root = document.documentElement;
      
      // Remove all theme classes
      root.classList.remove('theme-color', 'theme-monochrome');
      
      // Apply new theme
      if (theme === THEMES.MONOCHROME) {
        root.classList.add('theme-monochrome');
        
        // Load monochrome CSS if not already loaded
        if (!document.querySelector('link[href*="design-tokens-monochrome.css"]')) {
          const link = document.createElement('link');
          link.rel = 'stylesheet';
          link.href = '/styles/design-tokens-monochrome.css';
          document.head.appendChild(link);
        }
      } else {
        root.classList.add('theme-color');
      }
      
      this.currentTheme = theme;
    }
    
    toggleTheme() {
      const newTheme = this.currentTheme === THEMES.COLOR ? THEMES.MONOCHROME : THEMES.COLOR;
      this.applyTheme(newTheme);
      
      // Save preference
      localStorage.setItem(STORAGE_KEY, newTheme);
      
      // Track toggle
      this.trackThemeToggle(newTheme);
    }
    
    trackThemeView(theme) {
      if (typeof gtag !== 'undefined') {
        gtag('event', 'page_view', {
          'theme_variant': theme,
          'experiment_name': 'theme_color_vs_monochrome'
        });
      }
    }
    
    trackThemeToggle(theme) {
      if (typeof gtag !== 'undefined') {
        gtag('event', 'theme_toggled', {
          'new_theme': theme,
          'experiment_name': 'theme_color_vs_monochrome'
        });
      }
    }
    
    addToggleButton() {
      const button = document.createElement('button');
      button.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
          <path d="M10 2a8 8 0 100 16 8 8 0 000-16zM2 10a8 8 0 0112.906-6.32L5.68 12.906A7.962 7.962 0 012 10zm8 8a7.962 7.962 0 01-6.32-3.094L12.906 5.68A7.962 7.962 0 0118 10a8 8 0 01-8 8z"/>
        </svg>
      `;
      button.className = 'theme-toggle-button';
      button.style.cssText = `
        position: fixed;
        bottom: 80px;
        right: 20px;
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: var(--color-brand-primary);
        color: white;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        z-index: 9998;
        transition: all 0.2s;
      `;
      
      button.addEventListener('click', () => this.toggleTheme());
      button.addEventListener('mouseenter', () => {
        button.style.transform = 'scale(1.1)';
      });
      button.addEventListener('mouseleave', () => {
        button.style.transform = 'scale(1)';
      });
      
      document.body.appendChild(button);
    }
  }
  
  // Initialize theme switcher
  window.docsieTheme = new ThemeSwitcher();
  
  // Expose toggle function globally
  window.toggleDocsieTheme = function() {
    window.docsieTheme.toggleTheme();
  };
  
  // Track conversions with theme data
  const originalCalendlyInit = window.Calendly ? window.Calendly.initPopupWidget : null;
  if (originalCalendlyInit) {
    window.Calendly.initPopupWidget = function(options) {
      // Track conversion with theme variant
      if (typeof gtag !== 'undefined') {
        gtag('event', 'conversion', {
          'theme_variant': window.docsieTheme.currentTheme,
          'experiment_name': 'theme_color_vs_monochrome',
          'conversion_type': 'demo_booking'
        });
      }
      return originalCalendlyInit.call(this, options);
    };
  }
})();