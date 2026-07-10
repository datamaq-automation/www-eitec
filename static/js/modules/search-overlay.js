export function initSearchOverlay() {
    const searchTriggers = document.querySelectorAll('.buscar');
    const searchOverlay = document.querySelector('.search-overlay');
    const searchMask = document.querySelector('.search-overlay__mask');
    const hamburger = document.querySelector('.header__hamburger');
    const menu = document.querySelector('.header__menu');

    if (searchTriggers.length > 0 && searchOverlay) {
        searchTriggers.forEach(trigger => {
            trigger.addEventListener('click', () => {
                searchOverlay.classList.toggle('active');
                
                // Si se activa el buscador, cerrar el menú móvil automáticamente
                if (searchOverlay.classList.contains('active')) {
                    if (hamburger && hamburger.classList.contains('is-active')) {
                        hamburger.classList.remove('is-active');
                        hamburger.setAttribute('aria-expanded', 'false');
                    }
                    if (menu && menu.classList.contains('active')) {
                        menu.classList.remove('active');
                    }
                }
            });
        });
    }

    if (searchMask && searchOverlay) {
        searchMask.addEventListener('click', () => {
            searchOverlay.classList.remove('active');
        });
    }
}
