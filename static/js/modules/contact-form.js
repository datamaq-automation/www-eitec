export function initContactForm() {
    // Bind the callback function to window object so Google reCAPTCHA can invoke it globally
    window.onSubmit_contactanos = function (token) {
        const form = document.getElementById("form_contactanos");
        const submitBtn = document.getElementById("boton_enviar");
        if (form) {
            if (form.checkValidity()) {
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Enviando...';
                }
                form.submit();
            } else {
                if (typeof grecaptcha !== 'undefined') {
                    grecaptcha.reset();
                }
                form.reportValidity();
            }
        }
    };
}
