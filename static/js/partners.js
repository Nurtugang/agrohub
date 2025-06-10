document.addEventListener('DOMContentLoaded', function() {
    // Initialize testimonial carousel
    initTestimonialCarousel();

    // Handle partner form submissions
    const partnerForm = document.getElementById('partnerForm');
    if (partnerForm) {
        partnerForm.addEventListener('submit', handleFormSubmit);
    }

    // Initialize partner card hover effects
    initPartnerCards();
    
    // Add smooth scroll functionality for "Become a Partner" button
    const scrollToFormBtn = document.getElementById('scrollToFormBtn');
    const formSection = document.querySelector('.partner-form-section');
    
    if (scrollToFormBtn && formSection) {
        scrollToFormBtn.addEventListener('click', function() {
            formSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        });
    }
});

/**
 * Initialize the testimonial carousel
 */
function initTestimonialCarousel() {
    // Store the testimonial data
    const cards = [
        {
            name: "Билл Гейтс1",
            position: "Генеральный директор\nТОО \"Микрософт\"",
            text: "Сотрудничество с университетом стало для нас ценным опытом. Мы высоко оцениваем профессионализм команды и открытость к совместным инновационным проектам в аграрной сфере.",
            avatar: "images/h=174.png"
        },
        {
            name: "Билл Гейтс2",
            position: "Генеральный директор\nТОО \"Микрософт\"",
            text: "Сотрудничество с университетом стало для нас ценным опытом. Мы высоко оцениваем профессионализм команды и открытость к совместным инновационным проектам в аграрной сфере.",
            avatar: "images/h=174.png"
        },
        {
            name: "Билл Гейтс3",
            position: "Генеральный директор\nТОО \"Микрософт\"",
            text: "Сотрудничество с университетом стало для нас ценным опытом. Мы высоко оцениваем профессионализм команды и открытость к совместным инновационным проектам в аграрной сфере.",
            avatar: "images/h=174.png"
        },
        {
            name: "Билл Гейтс4",
            position: "Генеральный директор\nТОО \"Микрософт\"",
            text: "Сотрудничество с университетом стало для нас ценным опытом. Мы высоко оцениваем профессионализм команды и открытость к совместным инновационным проектам в аграрной сфере.",
            avatar: "images/h=174.png"
        },
        {
            name: "Билл Гейтс5",
            position: "Генеральный директор\nТОО \"Микрософт\"",
            text: "Сотрудничество с университетом стало для нас ценным опытом. Мы высоко оцениваем профессионализм команды и открытость к совместным инновационным проектам в аграрной сфере.",
            avatar: "images/h=174.png"
        },
        {
            name: "Билл Гейтс6",
            position: "Генеральный директор\nТОО \"Микрософт\"",
            text: "Сотрудничество с университетом стало для нас ценным опытом. Мы высоко оцениваем профессионализм команды и открытость к совместным инновационным проектам в аграрной сфере.",
            avatar: "images/h=174.png"
        },
        {
            name: "Билл Гейтс7",
            position: "Генеральный директор\nТОО \"Микрософт\"",
            text: "Сотрудничество с университетом стало для нас ценным опытом. Мы высоко оцениваем профессионализм команды и открытость к совместным инновационным проектам в аграрной сфере.",
            avatar: "images/h=174.png"
        }
    ];

    // Create a deep copy of the cards with processed avatars
    const processedCards = cards.map(card => {
        return {
            ...card,
            avatar: `/static/${card.avatar}` // Add static base URL once
        };
    });

    let currentIndex = 0;
    let isAnimating = false;
    
    const container = document.querySelector('.carousel-container');
    if (!container) return;

    const prevButton = container.querySelector('.nav-button.prev');
    const nextButton = container.querySelector('.nav-button.next');
    const indicators = container.querySelectorAll('.indicator');

    function createCard(data, index) {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <div class="card-header">
                <img src="${data.avatar}" alt="${data.name}" class="avatar">
                <div class="person-info">
                    <h3>${data.name}</h3>
                    <p>${data.position.replace('\n', '<br>')}</p>
                </div>
            </div>
            <div class="card-content">
                ${data.text}
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

        updateIndicators();
    }

    function updateIndicators() {
        indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === currentIndex);
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
            updateIndicators();
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
            updateIndicators();
            isAnimating = false;
        }, 100);
    }

    function goToCard(index) {
        if (isAnimating || index === currentIndex) return;
        
        const difference = index - currentIndex;
        const steps = Math.abs(difference);
        const direction = difference > 0 ? 'next' : 'prev';
        
        for (let i = 0; i < steps; i++) {
            setTimeout(() => {
                if (direction === 'next') nextCard();
                else prevCard();
            }, i * 700);
        }
    }

    // Setup event listeners
    if (prevButton) {
        prevButton.addEventListener('click', prevCard);
    }
    
    if (nextButton) {
        nextButton.addEventListener('click', nextCard);
    }
    
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => {
            goToCard(index);
        });
    });

    // Initialize
    renderCards();
}

/**
 * Handle form submission for partner forms
 */
function handleFormSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.textContent;
    
    // Set button to loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Жіберілуде...';
    
    // Simulate form submission (replace with actual API call)
    setTimeout(() => {
        // Reset form and button
        form.reset();
        submitBtn.disabled = false;
        submitBtn.textContent = originalBtnText;
        
        // Show success notification
        showNotification('Сіздің өтінішіңіз сәтті жіберілді!', 'success');
    }, 1500);
}

/**
 * Initialize partner card hover animations
 */
function initPartnerCards() {
    const partnerCards = document.querySelectorAll('.partner-card');
    
    partnerCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.classList.add('partner-card-hover');
        });
        
        card.addEventListener('mouseleave', () => {
            card.classList.remove('partner-card-hover');
        });
    });
}

/**
 * Show notification message
 */
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add to document
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Automatically remove after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}
