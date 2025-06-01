// Counter animation
function animateCounters() {
    const counters = document.querySelectorAll('.counter');
    
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-count'));
        const duration = 2000; // 2 seconds
        const stepTime = 50; // Update every 50ms
        const steps = duration / stepTime;
        const increment = target / steps;
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                counter.textContent = target;
                clearInterval(timer);
            } else {
                counter.textContent = Math.floor(current);
            }
        }, stepTime);
    });
}

// Service navigation
function goToService(serviceType) {
    // В реальном проекте здесь будет переход на страницу услуги
    window.location.href = `/services/${serviceType}/`;
}

// News navigation
function goToNews(newsId) {
    // В реальном проекте здесь будет переход на страницу новости
    window.location.href = `/news/${newsId}/`;
}

// Initialize animations when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Start counter animation when stats section is visible
    const statsSection = document.querySelector('.stats-section');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounters();
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    if (statsSection) {
        observer.observe(statsSection);
    }

    // Add click events to service cards
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Prevent double click
            if (e.detail === 1) {
                // Add visual feedback
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 150);
            }
        });
    });

    // Add click events to news cards
    const newsCards = document.querySelectorAll('.news-card');
    newsCards.forEach(card => {
        card.addEventListener('click', function() {
            // Add visual feedback
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    });

    // Smooth scrolling for hero button
    const heroButton = document.querySelector('.btn-hero');
    if (heroButton) {
        heroButton.addEventListener('click', function() {
            document.getElementById('services').scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        });
    }
});

// Lazy loading optimization
const images = document.querySelectorAll('img[src]');
const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.classList.add('loaded');
            observer.unobserve(img);
        }
    });
});

images.forEach(img => imageObserver.observe(img));