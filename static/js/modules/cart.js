const STORAGE_KEY = 'eitec_quote_items';

function getCartItems() {
    try {
        return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    } catch (e) {
        return [];
    }
}

function saveCartItems(items) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
}

function updateCartBadge() {
    const badge = document.getElementById('cart-badge');
    if (!badge) return;

    const items = getCartItems();
    badge.textContent = items.length;

    if (items.length > 0) {
        badge.classList.remove('d-none');
    } else {
        badge.classList.add('d-none');
    }
}

export function initCart() {
    // Listen to custom updates to keep badge in sync
    window.addEventListener('cart-updated', updateCartBadge);
    updateCartBadge();

    // 1. Add to quote button logic (on category detail pages)
    const addToQuoteBtn = document.getElementById('add-to-quote-btn');
    if (addToQuoteBtn) {
        const name = addToQuoteBtn.getAttribute('data-name');
        const slug = addToQuoteBtn.getAttribute('data-slug');
        const image = addToQuoteBtn.getAttribute('data-image');

        const updateButtonState = () => {
            const items = getCartItems();
            const exists = items.some(item => item.slug === slug);
            if (exists) {
                addToQuoteBtn.classList.remove('btn-call--secondary');
                addToQuoteBtn.classList.add('btn-success');
                addToQuoteBtn.innerHTML = '<i class="fa-solid fa-check me-2"></i>Ver mi cotización';
            } else {
                addToQuoteBtn.classList.add('btn-call--secondary');
                addToQuoteBtn.classList.remove('btn-success');
                addToQuoteBtn.innerHTML = '<i class="fa-solid fa-plus me-2"></i>Agregar a mi cotización';
            }
        };

        // Initialize state
        updateButtonState();

        addToQuoteBtn.addEventListener('click', () => {
            const items = getCartItems();
            const exists = items.some(item => item.slug === slug);

            if (exists) {
                // If already added, act as a shortcut to view cart
                window.location.href = '/carrito';
            } else {
                // Add item
                items.push({ name, slug, image });
                saveCartItems(items);
                window.dispatchEvent(new Event('cart-updated'));
                updateButtonState();
            }
        });
    }

    // 2. Cart page logic
    const itemsListContainer = document.getElementById('cart-items-list');
    if (itemsListContainer) {
        const renderCartPage = () => {
            const items = getCartItems();
            const emptyView = document.getElementById('cart-empty-view');
            const contentView = document.getElementById('cart-content-view');

            if (items.length === 0) {
                if (emptyView) emptyView.classList.remove('d-none');
                if (contentView) contentView.classList.add('d-none');
                return;
            }

            if (emptyView) emptyView.classList.add('d-none');
            if (contentView) contentView.classList.remove('d-none');

            // Render list
            itemsListContainer.innerHTML = '';
            items.forEach(item => {
                const card = document.createElement('div');
                card.className = 'card shadow-sm border-0 p-3 mb-2';
                card.style.borderRadius = '8px';
                card.innerHTML = `
                    <div class="row align-items-center">
                        <div class="col-3 col-md-2 text-center">
                            <img src="/static/img/${item.image}" class="img-fluid rounded" alt="${item.name}" style="max-height: 60px; object-fit: cover;">
                        </div>
                        <div class="col-6 col-md-8">
                            <h3 class="h6 mb-0 text-dark">${item.name}</h3>
                        </div>
                        <div class="col-3 col-md-2 text-end">
                            <button class="btn btn-outline-danger btn-sm remove-item-btn" data-slug="${item.slug}">
                                <i class="fa-solid fa-trash-can"></i>
                            </button>
                        </div>
                    </div>
                `;
                itemsListContainer.appendChild(card);
            });

            // Set value of hidden input field
            const productsInput = document.getElementById('productos');
            if (productsInput) {
                productsInput.value = items.map(item => item.name).join(', ');
            }

            // Bind remove button events
            const removeButtons = itemsListContainer.querySelectorAll('.remove-item-btn');
            removeButtons.forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const slugToRemove = btn.getAttribute('data-slug');
                    let currentItems = getCartItems();
                    currentItems = currentItems.filter(item => item.slug !== slugToRemove);
                    saveCartItems(currentItems);
                    window.dispatchEvent(new Event('cart-updated'));
                    renderCartPage();
                });
            });
        };

        renderCartPage();
    }
}
