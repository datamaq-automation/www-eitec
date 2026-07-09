export function initSearchOverlay() {
    const searchTrigger = document.querySelector('.buscar');
    const searchOverlay = document.querySelector('.search-overlay');
    const searchMask = document.querySelector('.search-overlay__mask');

    if (searchTrigger && searchOverlay) {
        searchTrigger.addEventListener('click', () => {
            searchOverlay.classList.toggle('active');
        });
    }

    if (searchMask && searchOverlay) {
        searchMask.addEventListener('click', () => {
            searchOverlay.classList.remove('active');
        });
    }
}
