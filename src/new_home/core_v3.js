/**
 * Core v3 JavaScript
 * Modular, maintainable JavaScript for v3 design system
 */

// Namespace for v3 functionality
const DocsieV3 = {
  
  // Initialize all modules
  init() {
    this.initNavigation();
    this.initAnimations();
    this.initForms();
    this.initAnalytics();
  },
  
  // Navigation functionality
  initNavigation() {
    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.nav-mobile-toggle');
    const mobileMenu = document.querySelector('.nav-links');
    
    if (mobileMenuBtn && mobileMenu) {
      mobileMenuBtn.addEventListener('click', () => {
        mobileMenu.classList.toggle('active');
        mobileMenuBtn.classList.toggle('active');
      });
    }
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          const offset = 80; // Account for fixed header
          const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
          
          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
          });
        }
      });
    });
    
    // Active link highlighting
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    window.addEventListener('scroll', () => {
      let current = '';
      
      sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        
        if (pageYOffset >= sectionTop - 100) {
          current = section.getAttribute('id');
        }
      });
      
      navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').includes(current)) {
          link.classList.add('active');
        }
      });
    });
  },
  
  // Animation functionality
  initAnimations() {
    // Intersection Observer for animations
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          
          // Staggered animations for children
          const children = entry.target.querySelectorAll('.animate-child');
          children.forEach((child, index) => {
            setTimeout(() => {
              child.classList.add('visible');
            }, index * 100);
          });
        }
      });
    }, observerOptions);
    
    // Observe all animated elements
    const animatedElements = document.querySelectorAll('.animate-fade-in, .animate-slide-up');
    animatedElements.forEach(el => observer.observe(el));
    
    // Parallax effect for hero section
    const hero = document.querySelector('.hero-section');
    if (hero) {
      window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallax = hero.querySelector('.parallax');
        if (parallax) {
          parallax.style.transform = `translateY(${scrolled * 0.5}px)`;
        }
      });
    }
  },
  
  // Form functionality
  initForms() {
    // Migration assessment form
    const assessmentForm = document.querySelector('#migration-assessment');
    if (assessmentForm) {
      assessmentForm.addEventListener('submit', (e) => {
        e.preventDefault();
        this.handleAssessmentForm(assessmentForm);
      });
    }
    
    // Sample docs form
    const sampleDocsForm = document.querySelector('#sample-docs-form');
    if (sampleDocsForm) {
      sampleDocsForm.addEventListener('submit', (e) => {
        e.preventDefault();
        this.handleSampleDocsForm(sampleDocsForm);
      });
    }
    
    // Input validation
    const inputs = document.querySelectorAll('.input[required]');
    inputs.forEach(input => {
      input.addEventListener('blur', () => {
        this.validateInput(input);
      });
    });
  },
  
  // Handle assessment form submission
  handleAssessmentForm(form) {
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);
    
    // Basic validation
    if (!data.email || !data.current_tool || !data.doc_count) {
      this.showNotification('Please fill in all required fields', 'error');
      return;
    }
    
    // Show loading state
    const submitBtn = form.querySelector('[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;
    
    // Simulate API call (replace with actual endpoint)
    setTimeout(() => {
      // Success response
      this.showNotification('Assessment request received! We\'ll contact you within 24 hours.', 'success');
      form.reset();
      submitBtn.textContent = originalText;
      submitBtn.disabled = false;
      
      // Track event
      this.trackEvent('Assessment Form', 'Submit', data.current_tool);
    }, 1500);
  },
  
  // Handle sample docs form submission
  handleSampleDocsForm(form) {
    const formData = new FormData(form);
    const files = formData.getAll('docs');
    
    if (files.length === 0) {
      this.showNotification('Please select at least one document', 'error');
      return;
    }
    
    // Show upload progress
    const progressBar = form.querySelector('.upload-progress');
    if (progressBar) {
      progressBar.style.display = 'block';
      // Simulate upload progress
      let progress = 0;
      const interval = setInterval(() => {
        progress += 10;
        progressBar.querySelector('.progress-fill').style.width = progress + '%';
        
        if (progress >= 100) {
          clearInterval(interval);
          this.showNotification('Documents uploaded! We\'ll send you the migrated versions within 24 hours.', 'success');
          form.reset();
          progressBar.style.display = 'none';
        }
      }, 200);
    }
  },
  
  // Input validation
  validateInput(input) {
    const value = input.value.trim();
    const type = input.type;
    let isValid = true;
    
    if (input.hasAttribute('required') && !value) {
      isValid = false;
      this.showInputError(input, 'This field is required');
    } else if (type === 'email' && !this.isValidEmail(value)) {
      isValid = false;
      this.showInputError(input, 'Please enter a valid email address');
    }
    
    if (isValid) {
      this.clearInputError(input);
    }
    
    return isValid;
  },
  
  // Email validation
  isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  },
  
  // Show input error
  showInputError(input, message) {
    input.classList.add('error');
    let errorEl = input.parentElement.querySelector('.input-error');
    
    if (!errorEl) {
      errorEl = document.createElement('span');
      errorEl.className = 'input-error';
      input.parentElement.appendChild(errorEl);
    }
    
    errorEl.textContent = message;
  },
  
  // Clear input error
  clearInputError(input) {
    input.classList.remove('error');
    const errorEl = input.parentElement.querySelector('.input-error');
    if (errorEl) {
      errorEl.remove();
    }
  },
  
  // Show notification
  showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
      notification.classList.add('visible');
    }, 10);
    
    // Remove after 5 seconds
    setTimeout(() => {
      notification.classList.remove('visible');
      setTimeout(() => {
        notification.remove();
      }, 300);
    }, 5000);
  },
  
  // Analytics tracking
  initAnalytics() {
    // Track CTA clicks
    document.querySelectorAll('[data-track]').forEach(element => {
      element.addEventListener('click', () => {
        const data = element.dataset.track.split(',');
        this.trackEvent(data[0], data[1], data[2]);
      });
    });
    
    // Track scroll depth
    let maxScroll = 0;
    window.addEventListener('scroll', () => {
      const scrollPercent = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
      
      if (scrollPercent > maxScroll) {
        maxScroll = scrollPercent;
        
        // Track milestones
        if (maxScroll >= 25 && maxScroll < 26) {
          this.trackEvent('Scroll Depth', '25%');
        } else if (maxScroll >= 50 && maxScroll < 51) {
          this.trackEvent('Scroll Depth', '50%');
        } else if (maxScroll >= 75 && maxScroll < 76) {
          this.trackEvent('Scroll Depth', '75%');
        } else if (maxScroll >= 90) {
          this.trackEvent('Scroll Depth', '90%');
        }
      }
    });
  },
  
  // Track event (integrate with your analytics)
  trackEvent(category, action, label = null) {
    // Google Analytics
    if (typeof gtag !== 'undefined') {
      gtag('event', action, {
        event_category: category,
        event_label: label
      });
    }
    
    // Console log for development
    if (window.location.hostname === 'localhost') {
      console.log('Track Event:', { category, action, label });
    }
  }
};

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => DocsieV3.init());
} else {
  DocsieV3.init();
}

// Export for use in other modules
window.DocsieV3 = DocsieV3;