export function initContactForm() {
    const form = document.getElementById("form_contactanos");
    if (form) {
        form.addEventListener("submit", () => {
            const submitBtn = document.getElementById("boton_enviar");
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Enviando...';
            }
        });
    }
}
