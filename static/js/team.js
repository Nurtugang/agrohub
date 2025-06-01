document.addEventListener('DOMContentLoaded', function() {
    // Animation on scroll using Intersection Observer
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Initialize animations for team cards
    const teamCards = document.querySelectorAll('.team-card');
    teamCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(card);
    });

    // Initialize animations for circle avatars
    const circles = document.querySelectorAll('.circle-avatar');
    circles.forEach((circle, index) => {
        const parent = circle.closest('.col-lg-3, .col-md-6');
        parent.style.opacity = '0';
        parent.style.transform = 'scale(0.8)';
        parent.style.transition = `opacity 0.6s ease ${index * 0.15}s, transform 0.6s ease ${index * 0.15}s`;
        observer.observe(parent);
    });

    // Parallax effect for hero
    let ticking = false;
    function updateParallax() {
        const hero = document.querySelector('.team-hero');
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
});