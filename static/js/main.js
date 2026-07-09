import { initHeader } from './modules/header.js';
import { initSearchOverlay } from './modules/search-overlay.js';
import { initContactForm } from './modules/contact-form.js';
import { initCart } from './modules/cart.js';

document.addEventListener('DOMContentLoaded', () => {
    initHeader();
    initSearchOverlay();
    initContactForm();
    initCart();
});
