document.addEventListener('DOMContentLoaded', function() {
    // Add animation classes to elements
    const animateElements = () => {
        const elements = document.querySelectorAll('.article-card');
        elements.forEach((element, index) => {
            setTimeout(() => {
                element.classList.add('animate');
            }, index * 100);
        });
    };
    
    // Animate elements when page loads
    animateElements();
    
    // Smooth scrolling for pagination
    const paginationLinks = document.querySelectorAll('.pagination a');
    paginationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            // In a real application, this would load the next page
            // For this demo, we just scroll to the top
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    });
    
    // Category filter button effects
    const selectAllBtn = document.querySelector('.btn-all-categories');
    const clearAllBtn = document.querySelector('.btn-clear-categories');
    const checkboxes = document.querySelectorAll('.category-checkbox');
    
    if (selectAllBtn) {
        selectAllBtn.addEventListener('click', function() {
            checkboxes.forEach(checkbox => {
                checkbox.checked = true;
            });
        });
    }
    
    if (clearAllBtn) {
        clearAllBtn.addEventListener('click', function() {
            checkboxes.forEach(checkbox => {
                checkbox.checked = false;
            });
        });
    }
});
