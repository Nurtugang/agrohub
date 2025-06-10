// Image gallery functionality
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for internal links
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

    // Gallery image click functionality
    const galleryItems = document.querySelectorAll('.gallery-item img');
    galleryItems.forEach(img => {
        img.addEventListener('click', function() {
            // Create modal or lightbox here if needed
            window.open(this.src, '_blank');
        });
        img.style.cursor = 'pointer';
    });

    // Reading progress indicator (for long descriptions)
    window.addEventListener('scroll', function() {
        const content = document.querySelector('.project-content');
        if (content) {
            const contentTop = content.offsetTop;
            const contentHeight = content.offsetHeight;
            const windowHeight = window.innerHeight;
            const scrollTop = window.pageYOffset;
            
            const progress = Math.min(100, Math.max(0, 
                ((scrollTop - contentTop + windowHeight) / contentHeight) * 100
            ));
            
        }
    });
});