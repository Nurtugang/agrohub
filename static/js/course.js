document.addEventListener('DOMContentLoaded', function() {
    // Section Animation on Scroll
    const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Add fade-in animation to sections
    const sections = document.querySelectorAll('.course-info-section, .learning-section, .curriculum-section, .instructors-section, .reviews-section, .registration-section');
    sections.forEach(section => {
        section.style.opacity = '0';
        observer.observe(section);
    });

    // Expandable Modules
    const moduleHeaders = document.querySelectorAll('.module-header');
    moduleHeaders.forEach(header => {
        header.addEventListener('click', function() {
            // Toggle active class for the header
            this.classList.toggle('active');
            
            // Toggle the content visibility
            const moduleContent = this.nextElementSibling;
            moduleContent.classList.toggle('hidden');
            
            // If module is now active, generate content if empty
            if (!moduleContent.classList.contains('hidden') && moduleContent.innerHTML.trim() === '<!-- Topics will be shown when clicked -->') {
                generateTopics(moduleContent);
            }
        });
    });
    
    // Function to generate topics for modules
    function generateTopics(container) {
        // Sample topics for dynamic generation
        const topicTexts = [
            "Тақырып 1. Duis aute irure dolor in reprehenderit in voluptate velit",
            "Тақырып 2. Lorem ipsum dolor sit amet, consectetur adipiscing elit",
            "Тақырып 3. Ut enim ad minim veniam, quis nostrud exercitation"
        ];
        
        // Clear placeholder content
        container.innerHTML = '';
        
        // Create topics
        topicTexts.forEach(text => {
            const topicDiv = document.createElement('div');
            topicDiv.className = 'topic';
            
            const icon = document.createElement('i');
            icon.className = 'fas fa-play-circle';
            
            const paragraph = document.createElement('p');
            paragraph.textContent = text;
            
            topicDiv.appendChild(icon);
            topicDiv.appendChild(paragraph);
            container.appendChild(topicDiv);
        });
        
        // Add animation to the new content
        container.style.opacity = '0';
        setTimeout(() => {
            container.style.transition = 'opacity 0.5s ease';
            container.style.opacity = '1';
        }, 10);
    }

    // Read More Reviews Button
    const readMoreButton = document.querySelector('.read-more-reviews');
    const hiddenReviews = document.querySelector('.hidden-reviews');
    
    if (readMoreButton && hiddenReviews) {
        readMoreButton.addEventListener('click', function() {
            hiddenReviews.classList.remove('hidden');
            this.style.display = 'none';
            
            // Animate the new reviews
            const newReviews = hiddenReviews.querySelectorAll('.review-card');
            newReviews.forEach((review, index) => {
                review.style.opacity = '0';
                review.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    review.style.transition = 'all 0.5s ease';
                    review.style.opacity = '1';
                    review.style.transform = 'translateY(0)';
                }, 100 * (index + 1));
            });
        });
    }

    // Smooth Scroll to Registration Form
    const registrationLinks = document.querySelectorAll('a[href="#registration-form"]');
    registrationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const registrationForm = document.getElementById('registration-form');
            if (registrationForm) {
                registrationForm.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Form Submission Animation
    const registrationForm = document.querySelector('.registration-form');
    if (registrationForm) {
        registrationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show success message (you could customize this)
            const submitButton = this.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            
            submitButton.disabled = true;
            submitButton.textContent = 'Отправлено ✓';
            submitButton.style.backgroundColor = '#28a745';
            
            // Reset form after delay
            setTimeout(() => {
                this.reset();
                submitButton.disabled = false;
                submitButton.textContent = originalText;
                submitButton.style.backgroundColor = '';
            }, 3000);
        });
    }
});
