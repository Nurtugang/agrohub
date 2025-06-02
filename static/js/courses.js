document.addEventListener('DOMContentLoaded', function() {
    // Animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);

    // Add the fade-in class to elements
    const courseCards = document.querySelectorAll('.course-card');
    courseCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = `all 0.4s ease ${index * 0.1}s`;
        
        observer.observe(card);
    });

    // Filter buttons interaction
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Animation effect for course cards
            courseCards.forEach((card, index) => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, 100 + index * 50);
            });
        });
    });

    // Category buttons interaction
    const categoryButtons = document.querySelectorAll('.category-btn');
    categoryButtons.forEach(button => {
        button.addEventListener('click', function() {
            categoryButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Animation effect for course cards
            courseCards.forEach((card, index) => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, 100 + index * 50);
            });
        });
    });

    // Hero section parallax effect
    const heroSection = document.querySelector('.hero-section');
    window.addEventListener('scroll', function() {
        if (heroSection && window.scrollY < heroSection.offsetHeight) {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.3;
            
            // Apply parallax effect to background
            heroSection.querySelector('.hero-content').style.transform = `translateY(${rate * 0.5}px)`;
        }
    });

    // Add hover effects to course cards
    courseCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Pagination interaction
    const paginationItems = document.querySelectorAll('.pagination-item');
    paginationItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            paginationItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            
            // Scroll to top of course grid
            const coursesGrid = document.querySelector('.courses-grid');
            if (coursesGrid) {
                coursesGrid.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
            
            // Animation effect for course cards (simulating page change)
            courseCards.forEach(card => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
            });
            
            setTimeout(() => {
                courseCards.forEach((card, index) => {
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, index * 50);
                });
            }, 500);
        });
    });

    // Add fade-in animation for visible elements on page load
    setTimeout(() => {
        courseCards.forEach(card => {
            if (isElementInViewport(card)) {
                card.classList.add('fade-in');
            }
        });
    }, 300);

    // Helper function to check if element is in viewport
    function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    // Add fade-in CSS class
    const style = document.createElement('style');
    style.textContent = `
        .fade-in {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    `;
    document.head.appendChild(style);
});
