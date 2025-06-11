document.addEventListener('DOMContentLoaded', function() {
    // Initialize testimonial carousel
    initTestimonialCarousel();
    
    // Animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Observe all fade-in elements
    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach(el => {
        observer.observe(el);
    });



    // Parallax effect for hero
    let ticking = false;
    function updateParallax() {
        const hero = document.querySelector('.lab-hero');
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.3;
        
        if (hero && scrolled < hero.offsetHeight) {
            hero.style.backgroundPosition = `center ${rate}px`;
        }
        ticking = false;
    }

    window.addEventListener('scroll', function() {
        if (!ticking) {
            requestAnimationFrame(updateParallax);
            ticking = true;
        }
    });

    // Service cards hover effects
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(-5px)';
        });
    });
    
/**
 * Initialize the testimonial carousel
 */
function initTestimonialCarousel() {
    // Store the testimonial data
    const cards = [
        {
            image: "images/KZT172877KZ.jpg"
        },
        {
            image: "images/KZT172877RU.jpg"
        }
    ];

    // Create a deep copy of the cards with processed image paths
    const processedCards = cards.map(card => {
        return {
            ...card,
            image: `/static/${card.image}` // Add static base URL once
        };
    });

    let currentIndex = 0;
    let isAnimating = false;
    
    const container = document.querySelector('.carousel-container');
    if (!container) return;

    const prevButton = container.querySelector('.nav-button.prev');
    const nextButton = container.querySelector('.nav-button.next');
    function createCard(data, index) {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <div class="card-image">
                <img src="${data.image}" alt="Certificate" class="certificate-img">
            </div>
        `;
        return card;
    }

    function renderCards() {
        const existingCards = container.querySelectorAll('.card');
        existingCards.forEach(card => card.remove());

        // Create only visible cards
        const visibleIndices = [
            (currentIndex - 1 + processedCards.length) % processedCards.length, // left
            currentIndex, // center
            (currentIndex + 1) % processedCards.length // right
        ];

        visibleIndices.forEach((cardIndex, position) => {
            const card = createCard(processedCards[cardIndex], cardIndex);
            
            if (position === 0) card.classList.add('left');
            else if (position === 1) card.classList.add('active');
            else if (position === 2) card.classList.add('right');
            
            container.appendChild(card);
        });
    }

    function nextCard() {
        if (isAnimating) return;
        isAnimating = true;

        const activeCard = container.querySelector('.card.active');
        const rightCard = container.querySelector('.card.right');
        const leftCard = container.querySelector('.card.left');

        // Animation for disappearing
        if (leftCard) {
            leftCard.classList.add('exiting-left');
            setTimeout(() => leftCard.remove(), 600);
        }
        
        if (activeCard) {
            activeCard.classList.remove('active');
            activeCard.classList.add('left');
        }
        
        if (rightCard) {
            rightCard.classList.remove('right');
            rightCard.classList.add('active');
        }

        // Create new right card
        currentIndex = (currentIndex + 1) % processedCards.length;
        const newRightIndex = (currentIndex + 1) % processedCards.length;
        const newCard = createCard(processedCards[newRightIndex], newRightIndex);
        newCard.classList.add('entering-right');
        container.appendChild(newCard);

        setTimeout(() => {
            newCard.classList.remove('entering-right');
            newCard.classList.add('right');
            isAnimating = false;
        }, 100);
    }

    function prevCard() {
        if (isAnimating) return;
        isAnimating = true;

        const activeCard = container.querySelector('.card.active');
        const rightCard = container.querySelector('.card.right');
        const leftCard = container.querySelector('.card.left');

        // Animation for disappearing
        if (rightCard) {
            rightCard.classList.add('exiting-right');
            setTimeout(() => rightCard.remove(), 600);
        }
        
        if (activeCard) {
            activeCard.classList.remove('active');
            activeCard.classList.add('right');
        }
        
        if (leftCard) {
            leftCard.classList.remove('left');
            leftCard.classList.add('active');
        }

        // Create new left card
        currentIndex = (currentIndex - 1 + processedCards.length) % processedCards.length;
        const newLeftIndex = (currentIndex - 1 + processedCards.length) % processedCards.length;
        const newCard = createCard(processedCards[newLeftIndex], newLeftIndex);
        newCard.classList.add('entering-left');
        container.appendChild(newCard);

        setTimeout(() => {
            newCard.classList.remove('entering-left');
            newCard.classList.add('left');
            isAnimating = false;
        }, 100);
    }

    // Setup event listeners
    if (prevButton) {
        prevButton.addEventListener('click', prevCard);
    }
    
    if (nextButton) {
        nextButton.addEventListener('click', nextCard);
    }

    // Initialize
    renderCards();
}
});