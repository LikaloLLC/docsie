document.addEventListener('DOMContentLoaded', function() {
  const track = document.querySelector('.reviews-track');
  const cards = document.querySelectorAll('.review-card');
  const prevButton = document.querySelector('.nav-button.prev');
  const nextButton = document.querySelector('.nav-button.next');
  
  let currentIndex = 0;
  
  // Hide prev button initially
  prevButton.style.display = 'none';
  
  function updateTrack() {
    const container = document.querySelector('.reviews-carousel');
    const containerWidth = container.clientWidth - 120; // Account for padding
    const visibleCards = getVisibleCards();
    const cardWidth = containerWidth / visibleCards;
    const gap = 30;
    
    // Set width for all cards
    cards.forEach(card => {
      card.style.minWidth = `${cardWidth - gap}px`;
    });
    
    const offset = currentIndex * (cardWidth);
    track.style.transform = `translateX(-${offset}px)`;
    
    // Update button visibility
    prevButton.style.display = currentIndex === 0 ? 'none' : 'flex';
    nextButton.style.display = currentIndex >= cards.length - visibleCards ? 'none' : 'flex';
  }
  
  function getVisibleCards() {
    const width = window.innerWidth;
    if (width <= 768) return 1;
    if (width <= 968) return 2;
    return 3;
  }
  
  prevButton.addEventListener('click', () => {
    if (currentIndex > 0) {
      currentIndex--;
      updateTrack();
    }
  });
  
  nextButton.addEventListener('click', () => {
    if (currentIndex < cards.length - getVisibleCards()) {
      currentIndex++;
      updateTrack();
    }
  });
  
  // Initial setup
  updateTrack();
  
  // Update on window resize with debounce
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      currentIndex = 0; // Reset position
      updateTrack();
    }, 250);
  });
}); 