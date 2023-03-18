document.addEventListener('DOMContentLoaded', () => {
  const carousel = document.querySelector('.carousel');
  const carouselContainer = document.querySelector('.carousel-container');
  const carouselItems = document.querySelectorAll('.carousel-item');
  const carouselBtnPrev = document.querySelector('.carousel-btn-prev');
  const carouselBtnNext = document.querySelector('.carousel-btn-next');
  const carouselItemWidth = carouselItems[0].offsetWidth;
  let currentIndex = 0;
  let autoplayInterval;

  // Set the initial position of the carousel container
  carouselContainer.style.transform = `translateX(-${currentIndex * carouselItemWidth}px)`;

  // Add event listeners to the previous and next buttons
  carouselBtnPrev.addEventListener('click', () => {
    if (currentIndex > 0) {
      currentIndex--;
    } else {
      currentIndex = carouselItems.length - 1;
    }
    updateCarousel();
  });

  carouselBtnNext.addEventListener('click', () => {
    if (currentIndex < carouselItems.length - 1) {
      currentIndex++;
    } else {
      currentIndex = 0;
    }
    updateCarousel();
  });

  // Autoplay functionality
  function startAutoplay() {
    autoplayInterval = setInterval(() => {
      if (currentIndex === carouselItems.length - 1) {
        currentIndex = 0;
      } else {
        currentIndex++;
      }
      updateCarousel();
    }, 3000);
  }

  function stopAutoplay() {
    clearInterval(autoplayInterval);
  }

  startAutoplay();

  // Pause autoplay when the user interacts with the carousel
  carousel.addEventListener('mouseenter', stopAutoplay);
  carousel.addEventListener('mouseleave', startAutoplay);

  function updateCarousel() {
    // Remove the active class from all items
    carouselItems.forEach(item => item.classList.remove('active'));

    // Add the active class to the current item
    carouselItems[currentIndex].classList.add('active');

    // Position the next and previous items
    if (currentIndex === 0) {
      carouselItems[carouselItems.length - 1].style.zIndex = 1;
      carouselItems[1].style.zIndex = 0;
    } else if (currentIndex === carouselItems.length - 1) {
      carouselItems[0].style.zIndex = 1;
      carouselItems[currentIndex - 1].style.zIndex = 0;
    } else {
      carouselItems[currentIndex - 1].style.zIndex = 0;
      carouselItems[currentIndex + 1].style.zIndex = 0;
    }

    // Update the position of the carousel container
    carouselContainer.style.transform = `translateX(-${currentIndex * carouselItemWidth}px)`;
  }
});
