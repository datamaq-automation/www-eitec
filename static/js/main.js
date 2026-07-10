import { initHeader } from './modules/header.js';
import { initSearchOverlay } from './modules/search-overlay.js';
import { initContactForm } from './modules/contact-form.js';
import { initCookies } from './modules/cookies.js';

document.addEventListener('DOMContentLoaded', () => {
    initHeader();
    initSearchOverlay();
    initContactForm();
    initCookies();
});
