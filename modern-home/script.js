// Modern Homepage JavaScript
class KnowledgeGraph {
  constructor(svgElement) {
    this.svg = svgElement;
    this.nodes = [];
    this.connections = [];
    this.visibleNodes = new Set();
    this.visibleConnections = new Set();
    this.animationId = null;
    this.isRunning = false;
    
    this.init();
  }

  init() {
    this.generateNodes();
    this.generateConnections();
    this.startAnimation();
    this.setupResetInterval();
  }

  generateNodes() {
    const nodeCount = 25;
    this.nodes = [];
    
    for (let i = 0; i < nodeCount; i++) {
      // Create nodes in a network pattern with some randomness
      const baseX = 100 + (i % 5) * 140 + Math.sin(i * 0.5) * 60;
      const baseY = 100 + Math.floor(i / 5) * 120 + Math.cos(i * 0.3) * 40;
      
      const node = {
        id: i,
        x: Math.max(50, Math.min(750, baseX)),
        y: Math.max(50, Math.min(550, baseY)),
        size: 3 + Math.random() * 4,
        delay: i * 200 + Math.random() * 100, // milliseconds
        element: null,
        glowElement: null,
        pulseElement: null
      };
      
      this.nodes.push(node);
    }
  }

  generateConnections() {
    this.connections = [];
    
    for (let i = 0; i < this.nodes.length; i++) {
      for (let j = i + 1; j < this.nodes.length; j++) {
        const nodeA = this.nodes[i];
        const nodeB = this.nodes[j];
        
        // Calculate distance between nodes
        const distance = Math.sqrt(
          Math.pow(nodeA.x - nodeB.x, 2) + 
          Math.pow(nodeA.y - nodeB.y, 2)
        );
        
        // Only connect nearby nodes with some randomness
        if (distance < 150 && Math.random() > 0.7) {
          const connection = {
            id: this.connections.length,
            from: i,
            to: j,
            delay: Math.max(nodeA.delay, nodeB.delay) + 500,
            element: null
          };
          
          this.connections.push(connection);
        }
      }
    }
  }

  createNodeElements(node) {
    // Create glow effect
    const glow = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    glow.setAttribute('cx', node.x);
    glow.setAttribute('cy', node.y);
    glow.setAttribute('r', node.size + 3);
    glow.classList.add('knowledge-node-glow');
    this.svg.appendChild(glow);
    node.glowElement = glow;

    // Create main node
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', node.x);
    circle.setAttribute('cy', node.y);
    circle.setAttribute('r', node.size);
    circle.classList.add('knowledge-node');
    circle.style.animationDelay = `${node.delay}ms`;
    this.svg.appendChild(circle);
    node.element = circle;

    // Create pulse effect
    const pulse = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    pulse.setAttribute('cx', node.x);
    pulse.setAttribute('cy', node.y);
    pulse.setAttribute('r', node.size);
    pulse.classList.add('knowledge-node-pulse');
    pulse.style.animationDelay = `${node.delay + 1000}ms`;
    this.svg.appendChild(pulse);
    node.pulseElement = pulse;
  }

  createConnectionElement(connection) {
    const nodeA = this.nodes[connection.from];
    const nodeB = this.nodes[connection.to];
    
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', nodeA.x);
    line.setAttribute('y1', nodeA.y);
    line.setAttribute('x2', nodeB.x);
    line.setAttribute('y2', nodeB.y);
    line.classList.add('knowledge-connection');
    line.style.animationDelay = `${connection.delay}ms`;
    
    // Calculate line length for dash animation
    const length = Math.sqrt(
      Math.pow(nodeB.x - nodeA.x, 2) + 
      Math.pow(nodeB.y - nodeA.y, 2)
    );
    line.style.strokeDasharray = length;
    line.style.strokeDashoffset = length;
    
    this.svg.appendChild(line);
    connection.element = line;
  }

  startAnimation() {
    if (this.isRunning) return;
    this.isRunning = true;

    // Clear existing elements
    this.clearSVG();
    this.visibleNodes.clear();
    this.visibleConnections.clear();

    // Animate nodes
    this.nodes.forEach((node, index) => {
      setTimeout(() => {
        if (!this.isRunning) return;
        this.createNodeElements(node);
        this.visibleNodes.add(index);
      }, node.delay);
    });

    // Animate connections
    this.connections.forEach((connection, index) => {
      setTimeout(() => {
        if (!this.isRunning) return;
        this.createConnectionElement(connection);
        this.visibleConnections.add(index);
      }, connection.delay);
    });
  }

  clearSVG() {
    while (this.svg.firstChild) {
      this.svg.removeChild(this.svg.firstChild);
    }
    
    // Reset node elements
    this.nodes.forEach(node => {
      node.element = null;
      node.glowElement = null;
      node.pulseElement = null;
    });
    
    // Reset connection elements
    this.connections.forEach(connection => {
      connection.element = null;
    });
  }

  setupResetInterval() {
    // Reset animation every 15 seconds
    setInterval(() => {
      this.resetAnimation();
    }, 15000);
  }

  resetAnimation() {
    this.isRunning = false;
    
    setTimeout(() => {
      this.startAnimation();
    }, 1000);
  }

  destroy() {
    this.isRunning = false;
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
    }
    this.clearSVG();
  }
}

// Mobile Menu Functionality
function toggleMobileMenu() {
  const mobileNav = document.getElementById('mobile-nav');
  const menuBtn = document.querySelector('.mobile-menu-btn');
  const icon = menuBtn.querySelector('i');
  
  if (mobileNav.classList.contains('active')) {
    mobileNav.classList.remove('active');
    icon.classList.remove('fa-times');
    icon.classList.add('fa-bars');
  } else {
    mobileNav.classList.add('active');
    icon.classList.remove('fa-bars');
    icon.classList.add('fa-times');
  }
}

// Close mobile menu when clicking on links
function closeMobileMenu() {
  const mobileNav = document.getElementById('mobile-nav');
  const menuBtn = document.querySelector('.mobile-menu-btn');
  const icon = menuBtn.querySelector('i');
  
  mobileNav.classList.remove('active');
  icon.classList.remove('fa-times');
  icon.classList.add('fa-bars');
}

// Smooth scrolling for anchor links
function setupSmoothScrolling() {
  const links = document.querySelectorAll('a[href^="#"]');
  
  links.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href');
      const targetSection = document.querySelector(targetId);
      
      if (targetSection) {
        const navHeight = document.querySelector('.modern-nav').offsetHeight;
        const targetPosition = targetSection.offsetTop - navHeight - 20;
        
        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
        
        // Close mobile menu if open
        closeMobileMenu();
      }
    });
  });
}

// Navbar scroll effect
function setupNavbarScrollEffect() {
  const navbar = document.querySelector('.modern-nav');
  let lastScrollTop = 0;
  
  window.addEventListener('scroll', function() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (scrollTop > 100) {
      navbar.style.background = 'rgba(255, 255, 255, 0.98)';
      navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
    } else {
      navbar.style.background = 'rgba(255, 255, 255, 0.95)';
      navbar.style.boxShadow = 'none';
    }
    
    lastScrollTop = scrollTop;
  });
}

// Intersection Observer for animations
function setupScrollAnimations() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, observerOptions);

  // Observe elements for scroll animations
  const animatedElements = document.querySelectorAll(`
    .stat-card,
    .feature-card,
    .ai-feature-card,
    .security-card,
    .industry-card,
    .testimonial-card
  `);

  animatedElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
  });
}

// Counter animation for stats
function animateCounters() {
  const counters = document.querySelectorAll('.stat-value');
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(counter => {
    observer.observe(counter);
  });
}

function animateCounter(element) {
  const text = element.textContent;
  const number = parseInt(text.match(/\d+/)[0]);
  const suffix = text.replace(/\d+/, '');
  let current = 0;
  const increment = number / 60; // 60 frames for 1 second at 60fps
  
  const timer = setInterval(() => {
    current += increment;
    if (current >= number) {
      current = number;
      clearInterval(timer);
    }
    element.innerHTML = Math.floor(current) + suffix;
  }, 1000 / 60);
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  // Initialize Knowledge Graph
  const knowledgeGraphSVG = document.getElementById('knowledge-graph');
  if (knowledgeGraphSVG) {
    const knowledgeGraph = new KnowledgeGraph(knowledgeGraphSVG);
    
    // Store reference for potential cleanup
    window.knowledgeGraph = knowledgeGraph;
  }
  
  // Setup other functionality
  setupSmoothScrolling();
  setupNavbarScrollEffect();
  setupScrollAnimations();
  animateCounters();
  
  // Close mobile menu when clicking outside
  document.addEventListener('click', function(e) {
    const mobileNav = document.getElementById('mobile-nav');
    const menuBtn = document.querySelector('.mobile-menu-btn');
    
    if (mobileNav && mobileNav.classList.contains('active')) {
      if (!mobileNav.contains(e.target) && !menuBtn.contains(e.target)) {
        closeMobileMenu();
      }
    }
  });
  
  // Close mobile menu on window resize
  window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
      closeMobileMenu();
    }
  });
});

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
  if (window.knowledgeGraph) {
    window.knowledgeGraph.destroy();
  }
});

// Utility function for debouncing
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Export functions for global access
window.toggleMobileMenu = toggleMobileMenu;
window.closeMobileMenu = closeMobileMenu; 