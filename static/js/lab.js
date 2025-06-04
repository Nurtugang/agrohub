document.addEventListener('DOMContentLoaded', function() {
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

    // Slider functionality
    const sliderNext = document.querySelector('.slider-next');
    const sliderImages = [
        'https://images.unsplash.com/photo-1582719471384-894fbb16e074?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
        'https://images.unsplash.com/photo-1581092160607-ee22621dd758?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
        'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
    ];
    let currentSlide = 0;

    if (sliderNext) {
        sliderNext.addEventListener('click', function() {
            currentSlide = (currentSlide + 1) % sliderImages.length;
            
            const mainImage = document.querySelector('.slider-main img');
            const leftImage = document.querySelector('.slider-left img');
            const rightImage = document.querySelector('.slider-right img');
            
            if (mainImage && leftImage && rightImage) {
                mainImage.src = sliderImages[currentSlide];
                leftImage.src = sliderImages[(currentSlide + 1) % sliderImages.length];
                rightImage.src = sliderImages[(currentSlide + 2) % sliderImages.length];
            }
        });
    }

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
});