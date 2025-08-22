// Components v3 JavaScript - Interactive Elements

// Problem Assessment Flow
function startAssessment() {
  // Simple assessment modal or redirect to assessment page
  const questions = [
    {
      question: "Where are your docs currently?",
      options: ["Confluence", "SharePoint", "PDFs", "Multiple tools", "No system"]
    },
    {
      question: "Biggest pain point?",
      options: ["Can't find anything", "Version confusion", "No collaboration", "Migration cost"]
    },
    {
      question: "Team size?",
      options: ["< 10", "10-50", "50-200", "200+"]
    }
  ];
  
  // For now, just redirect to demo booking with context
  window.location.href = '/assessment/';
}

// Animation on scroll
document.addEventListener('DOMContentLoaded', function() {
  // Intersection Observer for animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };
  
  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        
        // Add staggered animations for children
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
  const animatedElements = document.querySelectorAll('.fade-in, .slide-up, .bounce-in');
  animatedElements.forEach(el => observer.observe(el));
  
  // Problem card hover effects
  const problemCards = document.querySelectorAll('.problem-card');
  problemCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateX(8px)';
    });
    
    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateX(0)';
    });
  });
  
  // Trust signal counter animation
  const counters = document.querySelectorAll('[data-counter]');
  counters.forEach(counter => {
    const target = parseInt(counter.getAttribute('data-counter'));
    const duration = 2000;
    const increment = target / (duration / 16);
    let current = 0;
    
    const updateCounter = () => {
      current += increment;
      if (current < target) {
        counter.textContent = Math.floor(current);
        requestAnimationFrame(updateCounter);
      } else {
        counter.textContent = target;
      }
    };
    
    // Start animation when visible
    const counterObserver = new IntersectionObserver(function(entries) {
      if (entries[0].isIntersecting) {
        updateCounter();
        counterObserver.disconnect();
      }
    });
    
    counterObserver.observe(counter);
  });
  
  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
  
  // Mobile menu toggle
  const mobileMenuBtn = document.querySelector('#mobile-menu-btn');
  const mobileMenu = document.querySelector('#mobile-menu');
  
  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', function() {
      mobileMenu.classList.toggle('hidden');
      this.classList.toggle('active');
    });
  }
  
  // Form validation for migration assessment
  const migrationForm = document.querySelector('#migration-form');
  if (migrationForm) {
    migrationForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const formData = new FormData(this);
      const data = Object.fromEntries(formData);
      
      // Simple validation
      if (!data.email || !data.current_tool) {
        alert('Please fill in all required fields');
        return;
      }
      
      // Submit to backend or show success message
      console.log('Migration assessment requested:', data);
      
      // Show success message
      const successMsg = document.createElement('div');
      successMsg.className = 'badge badge-success p-4 mt-4';
      successMsg.textContent = 'Thank you! We\'ll send your migration plan within 24 hours.';
      this.appendChild(successMsg);
      
      // Reset form
      this.reset();
    });
  }
  
  // Interactive comparison table
  const comparisonToggles = document.querySelectorAll('[data-comparison]');
  comparisonToggles.forEach(toggle => {
    toggle.addEventListener('click', function() {
      const tool = this.getAttribute('data-comparison');
      const rows = document.querySelectorAll(`[data-tool="${tool}"]`);
      
      rows.forEach(row => {
        row.classList.toggle('highlight');
      });
    });
  });
  
  // Lazy loading for images
  const lazyImages = document.querySelectorAll('img[data-src]');
  const imageObserver = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.getAttribute('data-src');
        img.removeAttribute('data-src');
        imageObserver.unobserve(img);
      }
    });
  });
  
  lazyImages.forEach(img => imageObserver.observe(img));
  
  // Copy to clipboard for code snippets
  const copyButtons = document.querySelectorAll('[data-copy]');
  copyButtons.forEach(button => {
    button.addEventListener('click', function() {
      const textToCopy = this.getAttribute('data-copy');
      navigator.clipboard.writeText(textToCopy).then(() => {
        const originalText = this.textContent;
        this.textContent = 'Copied!';
        setTimeout(() => {
          this.textContent = originalText;
        }, 2000);
      });
    });
  });
});