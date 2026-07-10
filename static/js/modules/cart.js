// Cart/Quote Manager for EITEC

const STORAGE_KEY = 'eitec_quote_items';

export function getQuoteItems() {
    try {
        const items = localStorage.getItem(STORAGE_KEY);
        return items ? JSON.parse(items) : [];
    } catch (e) {
        console.error('Error reading quote items from localStorage', e);
        return [];
    }
}

export function saveQuoteItems(items) {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
        // Disparar evento para que otros componentes (como el badge) se enteren
        window.dispatchEvent(new Event('cart-updated'));
    } catch (e) {
        console.error('Error saving quote items to localStorage', e);
    }
}

export function addQuoteItem(slug, name, image) {
    const items = getQuoteItems();
    if (!items.some(item => item.slug === slug)) {
        items.push({ slug, name, image });
        saveQuoteItems(items);
    }
}

export function removeQuoteItem(slug) {
    let items = getQuoteItems();
    items = items.filter(item => item.slug !== slug);
    saveQuoteItems(items);
}

export function updateCartBadge() {
    const badge = document.getElementById('cart-badge');
    if (!badge) return;

    const items = getQuoteItems();
    const count = items.length;

    badge.textContent = count;
    if (count > 0) {
        badge.classList.remove('d-none');
    } else {
        badge.classList.add('d-none');
    }
}

function updateAddToQuoteButton() {
    const btn = document.getElementById('btn-add-to-quote');
    if (!btn) return;

    const slug = btn.getAttribute('data-slug');
    const items = getQuoteItems();
    const isAdded = items.some(item => item.slug === slug);

    if (isAdded) {
        btn.innerHTML = '<i class="fa-solid fa-circle-check me-2"></i>Quitar de mi cotización';
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-danger');
    } else {
        btn.innerHTML = '<i class="fa-solid fa-file-invoice-dollar me-2"></i>Agregar a mi cotización';
        btn.classList.remove('btn-danger');
        btn.classList.add('btn-primary');
    }
}

function renderCartPage() {
    const emptyView = document.getElementById('cart-empty-view');
    const contentView = document.getElementById('cart-content-view');
    const listContainer = document.getElementById('cart-items-list');
    const inputProductos = document.getElementById('productos');

    if (!emptyView || !contentView || !listContainer) return;

    const items = getQuoteItems();

    if (items.length === 0) {
        emptyView.classList.remove('d-none');
        contentView.classList.add('d-none');
        if (inputProductos) inputProductos.value = '';
    } else {
        emptyView.classList.add('d-none');
        contentView.classList.remove('d-none');

        // Generar HTML de la lista
        listContainer.innerHTML = items.map(item => `
            <div class="card border-0 shadow-sm p-3 mb-2 d-flex flex-row align-items-center justify-content-between" style="border-radius: 8px; background: #fff;">
                <div class="d-flex align-items-center gap-3">
                    <img src="/static/img/${item.image}" alt="${item.name}" class="rounded" style="width: 60px; height: 60px; object-fit: cover;">
                    <div>
                        <h3 class="h6 mb-0 text-dark fw-bold">${item.name}</h3>
                        <span class="text-muted" style="font-size: 0.8rem;">Repuesto original EITAR</span>
                    </div>
                </div>
                <button class="btn btn-outline-danger btn-sm border-0 btn-remove-item" data-slug="${item.slug}" aria-label="Quitar ${item.name} de la lista">
                    <i class="fa-solid fa-trash-can" style="font-size: 1.1rem;"></i>
                </button>
            </div>
        `).join('');

        // Agregar listeners para el botón de eliminar
        listContainer.querySelectorAll('.btn-remove-item').forEach(button => {
            button.addEventListener('click', (e) => {
                const btn = e.currentTarget;
                const slug = btn.getAttribute('data-slug');
                removeQuoteItem(slug);
                renderCartPage();
            });
        });

        // Actualizar el input de productos para el envío del formulario
        if (inputProductos) {
            const productNames = items.map(item => item.name).join(', ');
            inputProductos.value = productNames;
        }
    }
}

export function initCart() {
    // 1. Escuchar actualizaciones y sincronizar el badge
    window.addEventListener('cart-updated', () => {
        updateCartBadge();
        updateAddToQuoteButton();
    });

    // 2. Inicializar badge al cargar
    updateCartBadge();

    // 3. Listener para el botón en la página de categoría
    const btnAddToQuote = document.getElementById('btn-add-to-quote');
    if (btnAddToQuote) {
        updateAddToQuoteButton();
        
        btnAddToQuote.addEventListener('click', () => {
            const slug = btnAddToQuote.getAttribute('data-slug');
            const name = btnAddToQuote.getAttribute('data-name');
            const image = btnAddToQuote.getAttribute('data-image');
            
            const items = getQuoteItems();
            const isAdded = items.some(item => item.slug === slug);
            
            if (isAdded) {
                removeQuoteItem(slug);
            } else {
                addQuoteItem(slug, name, image);
            }
        });
    }

    // 4. Renderizar página del carrito si estamos en ella
    if (window.location.pathname === '/carrito') {
        renderCartPage();
        
        // Escuchar por si se limpia el carrito en otro componente
        window.addEventListener('cart-updated', renderCartPage);
    }
}
