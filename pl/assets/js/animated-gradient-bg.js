// Animated Gradient Background System
// Automatically creates continuous animated gradient background

(function() {
  'use strict';

  // Initialize animated background on page load
  function initAnimatedBackground() {
    // Create animated gradient container
    const gradientContainer = document.createElement('div');
    gradientContainer.className = 'animated-gradient-container';
    
    // Create gradient orbs
    const orbsContainer = document.createElement('div');
    orbsContainer.className = 'gradient-orbs';
    
    // Add 5 gradient orbs with different colors
    for (let i = 0; i < 5; i++) {
      const orb = document.createElement('div');
      orb.className = 'gradient-orb';
      orbsContainer.appendChild(orb);
    }
    
    // Create floating shapes
    const shapesContainer = document.createElement('div');
    shapesContainer.className = 'floating-shapes';
    
    // Add 5 floating shapes
    for (let i = 0; i < 5; i++) {
      const shape = document.createElement('div');
      shape.className = 'floating-shape';
      shapesContainer.appendChild(shape);
    }
    
    // Add to gradient container
    gradientContainer.appendChild(orbsContainer);
    gradientContainer.appendChild(shapesContainer);
    
    // Insert at the beginning of body
    document.body.insertBefore(gradientContainer, document.body.firstChild);
    
    // Ensure all content is wrapped in main-content-wrapper
    wrapMainContent();
  }
  
  // Wrap existing content to ensure it's above the background
  function wrapMainContent() {
    // Check if wrapper already exists
    if (document.querySelector('.main-content-wrapper')) {
      return;
    }
    
    // Create wrapper
    const wrapper = document.createElement('div');
    wrapper.className = 'main-content-wrapper';
    
    // Move all body children (except our gradient container) into wrapper
    const gradientContainer = document.querySelector('.animated-gradient-container');
    const children = Array.from(document.body.children);
    
    children.forEach(child => {
      if (child !== gradientContainer && child !== wrapper) {
        wrapper.appendChild(child);
      }
    });
    
    // Add wrapper to body
    document.body.appendChild(wrapper);
  }
  
  // Performance optimization: Reduce animations when tab is not visible
  let animationsPaused = false;
  
  document.addEventListener('visibilitychange', function() {
    const orbs = document.querySelectorAll('.gradient-orb');
    const shapes = document.querySelectorAll('.floating-shape');
    
    if (document.hidden && !animationsPaused) {
      animationsPaused = true;
      orbs.forEach(el => el.style.animationPlayState = 'paused');
      shapes.forEach(el => el.style.animationPlayState = 'paused');
    } else if (!document.hidden && animationsPaused) {
      animationsPaused = false;
      orbs.forEach(el => el.style.animationPlayState = 'running');
      shapes.forEach(el => el.style.animationPlayState = 'running');
    }
  });
  
  // Optimize for mobile: Remove some elements on small screens
  function optimizeForMobile() {
    if (window.innerWidth < 768) {
      const shapes = document.querySelectorAll('.floating-shape');
      // Keep only first 3 shapes on mobile
      shapes.forEach((shape, index) => {
        if (index >= 3) {
          shape.style.display = 'none';
        }
      });
    }
  }
  
  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      initAnimatedBackground();
      optimizeForMobile();
    });
  } else {
    initAnimatedBackground();
    optimizeForMobile();
  }
  
  // Re-optimize on resize
  let resizeTimeout;
  window.addEventListener('resize', function() {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(optimizeForMobile, 250);
  });
  
})();