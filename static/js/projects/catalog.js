// Filter animations
document.addEventListener('DOMContentLoaded', function() {
    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);

    // Observe all elements with fade-in-up class
    document.querySelectorAll('.fade-in-up').forEach(el => {
        observer.observe(el);
    });

    // Filter button animations
    const filterBtns = document.querySelectorAll('.filter-btn, .direction-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            this.classList.add('loading');
        });
    });

    // Smooth page transitions
    const links = document.querySelectorAll('a[href*="?"]');
    links.forEach(link => {
        link.addEventListener('click', function() {
            document.body.style.opacity = '0.8';
        });
    });
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
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