export function initHeader() {
    const header = document.getElementById('header');
    const hamburger = document.querySelector('.header__hamburger');
    const menu = document.querySelector('.header__menu');
    const mask = document.querySelector('.header__mask');

    if (hamburger && menu) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('is-active');
            menu.classList.toggle('active');
        });
    }

    // Options dropdown triggers
    const triggers = document.querySelectorAll('.header__menu-trigger');
    triggers.forEach(trigger => {
        trigger.addEventListener('click', (e) => {
            const parent = trigger.parentElement;
            const isActive = parent.classList.contains('active');
            
            // Close all first
            document.querySelectorAll('.header__menu-item').forEach(item => {
                item.classList.remove('active');
            });
            
            if (!isActive) {
                parent.classList.add('active');
                if (mask) mask.classList.add('active');
            } else {
                if (mask) mask.classList.remove('active');
            }
            e.stopPropagation();
        });
    });

    // Close options dropdown when clicking mask
    if (mask) {
        mask.addEventListener('click', () => {
            document.querySelectorAll('.header__menu-item').forEach(item => {
                item.classList.remove('active');
            });
            mask.classList.remove('active');
        });
    }

    // Scroll reduce
    const handleScroll = () => {
        if (!header) return;
        if (window.scrollY > 50) {
            header.classList.add('header--reduce');
            header.classList.add('reduce'); // keep legacy class in case needed
        } else {
            header.classList.remove('header--reduce');
            header.classList.remove('reduce');
        }
    };
    
    window.addEventListener('scroll', handleScroll);
    handleScroll(); // Trigger initially

    // Clean empty menu options
    const menuLinks = document.querySelectorAll('.header__menu-item a');
    menuLinks.forEach(link => {
        if (link.textContent.trim() === '') {
            const item = link.closest('.header__menu-item');
            if (item) item.remove();
        }
    });
}
