document.addEventListener('DOMContentLoaded', function() {
    // Handle thumbnail click
    initThumbnailGallery();
    
    // Initialize image zoom modal
    initImageZoomModal();
});

/**
 * Initialize the thumbnail gallery functionality
 */
function initThumbnailGallery() {
    const thumbnails = document.querySelectorAll('.thumbnail');
    const mainImage = document.getElementById('mainImage');
    
    if (!thumbnails.length || !mainImage) return;
    
    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            // Update active thumbnail
            thumbnails.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            // Update main image
            const imgSrc = this.getAttribute('data-img');
            mainImage.src = imgSrc;
            
            // Add animation effect
            mainImage.classList.add('changing');
            setTimeout(() => {
                mainImage.classList.remove('changing');
            }, 300);
        });
    });
}

/**
 * Initialize the image zoom modal functionality
 */
function initImageZoomModal() {
    const mainImage = document.getElementById('mainImage');
    const modal = document.querySelector('.image-viewer-modal');
    const zoomedImage = document.getElementById('zoomed-image');
    const closeBtn = document.querySelector('.close-viewer');
    
    if (!mainImage || !modal || !zoomedImage || !closeBtn) return;
    
    // Open modal when clicking on main image
    mainImage.addEventListener('click', function() {
        zoomedImage.src = this.src;
        modal.classList.add('show');
        
        // Add animation after small delay
        setTimeout(() => {
            zoomedImage.classList.add('zoomed-in');
        }, 100);
        
        // Prevent scrolling of background content
        document.body.style.overflow = 'hidden';
    });
    
    // Close modal when clicking the close button
    closeBtn.addEventListener('click', closeModal);
    
    // Close modal when clicking outside the image
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });
    
    // Handle ESC key to close modal
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('show')) {
            closeModal();
        }
    });
    
    function closeModal() {
        zoomedImage.classList.remove('zoomed-in');
        
        // Delay the modal hiding to allow for animation
        setTimeout(() => {
            modal.classList.remove('show');
            document.body.style.overflow = '';
        }, 300);
    }
    
    // Add additional zoom functionality within the modal
    let isZoomedIn = false;
    zoomedImage.addEventListener('click', function(e) {
        e.stopPropagation();
        
        if (!isZoomedIn) {
            this.style.transform = 'scale(1.5)';
            isZoomedIn = true;
        } else {
            this.style.transform = 'scale(1)';
            isZoomedIn = false;
        }
    });
}

// Add animation to elements when they come into view
document.addEventListener('DOMContentLoaded', function() {
    // Optional: Add intersection observer for additional animations if needed
    if ('IntersectionObserver' in window) {
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animated');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);
        
        // Example: observe elements with .animate-on-scroll class if you add any
        document.querySelectorAll('.animate-on-scroll').forEach(item => {
            observer.observe(item);
        });
    }
});
