/**
 * Process Timeline V2 - Auto-cycling and Interactions
 */

(function() {
  'use strict';

  // Configuration
  const CYCLE_DURATION = 8000; // 8 seconds per step
  const PROGRESS_UPDATE_INTERVAL = 50; // Update progress every 50ms
  const TOTAL_STEPS = 3;

  // State
  let currentStep = 0;
  let progress = 0;
  let isPaused = false;
  let cycleTimer = null;
  let progressTimer = null;

  // DOM Elements
  const stepNavBtns = document.querySelectorAll('.step-nav-btn');
  const stepContents = document.querySelectorAll('.step-content');
  const progressFill = document.querySelector('.progress-fill');
  const stepIndicators = document.querySelectorAll('[data-step-indicator]');
  const timelineSection = document.querySelector('.process-timeline-v2');

  /**
   * Set active step
   */
  function setActiveStep(stepIndex) {
    // Validate step index
    if (stepIndex < 0 || stepIndex >= TOTAL_STEPS) return;

    // Update current step
    currentStep = stepIndex;
    progress = 0;

    // Update navigation buttons
    stepNavBtns.forEach((btn, index) => {
      if (index === stepIndex) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    // Update content visibility
    stepContents.forEach((content, index) => {
      if (index === stepIndex) {
        content.classList.add('active');
      } else {
        content.classList.remove('active');
      }
    });

    // Update progress indicators
    updateProgressIndicators();

    // Update progress bar
    updateProgressBar();
  }

  /**
   * Update progress bar
   */
  function updateProgressBar() {
    // Calculate total progress (step progress + current step position)
    const stepProgress = (currentStep / (TOTAL_STEPS - 1)) * 100;
    const cycleProgress = (progress / 100) * (100 / (TOTAL_STEPS - 1));
    const totalProgress = Math.min(stepProgress + cycleProgress, 100);

    progressFill.style.width = totalProgress + '%';
  }

  /**
   * Update progress indicators
   */
  function updateProgressIndicators() {
    stepIndicators.forEach((indicator, index) => {
      const stepNumber = indicator.querySelector('.progress-step-number');
      const stepLabel = indicator.querySelector('p');

      if (index <= currentStep) {
        stepNumber.classList.add('active');
        stepNumber.style.color = '#FF6738';
        if (stepLabel) {
          stepLabel.style.color = '#B24934';
        }
      } else {
        stepNumber.classList.remove('active');
        stepNumber.style.color = 'rgba(124, 90, 73, 0.7)';
        if (stepLabel) {
          stepLabel.style.color = 'rgba(124, 90, 73, 0.7)';
        }
      }
    });
  }

  /**
   * Increment progress
   */
  function incrementProgress() {
    if (isPaused) return;

    progress += (100 / (CYCLE_DURATION / PROGRESS_UPDATE_INTERVAL));

    if (progress >= 100) {
      // Move to next step
      const nextStep = (currentStep + 1) % TOTAL_STEPS;
      setActiveStep(nextStep);
    } else {
      updateProgressBar();
    }
  }

  /**
   * Start auto-cycling
   */
  function startAutoCycle() {
    if (progressTimer) return; // Already running

    progressTimer = setInterval(incrementProgress, PROGRESS_UPDATE_INTERVAL);
  }

  /**
   * Stop auto-cycling
   */
  function stopAutoCycle() {
    if (progressTimer) {
      clearInterval(progressTimer);
      progressTimer = null;
    }
  }

  /**
   * Pause auto-cycling
   */
  function pauseAutoCycle() {
    isPaused = true;
  }

  /**
   * Resume auto-cycling
   */
  function resumeAutoCycle() {
    isPaused = false;
  }

  /**
   * Reset and restart auto-cycling
   */
  function resetAutoCycle() {
    stopAutoCycle();
    progress = 0;
    startAutoCycle();
  }

  /**
   * Initialize event listeners
   */
  function initEventListeners() {
    // Step navigation buttons
    stepNavBtns.forEach((btn, index) => {
      btn.addEventListener('click', () => {
        setActiveStep(index);
        resetAutoCycle();
      });
    });

    // Progress indicators
    stepIndicators.forEach((indicator, index) => {
      indicator.addEventListener('click', () => {
        setActiveStep(index);
        resetAutoCycle();
      });
    });

    // Pause on hover over timeline section
    if (timelineSection) {
      timelineSection.addEventListener('mouseenter', pauseAutoCycle);
      timelineSection.addEventListener('mouseleave', resumeAutoCycle);
    }

    // Pause on visibility change (user switches tabs)
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        pauseAutoCycle();
      } else {
        resumeAutoCycle();
      }
    });
  }

  /**
   * Initialize the component
   */
  function init() {
    // Set initial step
    setActiveStep(0);

    // Initialize event listeners
    initEventListeners();

    // Start auto-cycling
    startAutoCycle();
  }

  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
