export function initContactForm() {
    const form = document.getElementById("form_contactanos");
    if (form) {
        form.addEventListener("submit", (e) => {
            e.preventDefault();

            const submitBtn = document.getElementById("boton_enviar");
            const recaptchaResponseInput = document.getElementById("g_recaptcha_response");

            // Validar que reCAPTCHA esté completado
            const recaptchaResponse = recaptchaResponseInput?.value;
            if (!recaptchaResponse) {
                alert("Por favor completa el reCAPTCHA");
                return;
            }

            // Mostrar estado de envío
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Enviando...';
            }

            // Enviar el formulario
            form.submit();
        });
    }
}

// Callback global para reCAPTCHA
window.onRecaptchaSuccess = function(token) {
    const recaptchaResponseInput = document.getElementById("g_recaptcha_response");
    if (recaptchaResponseInput) {
        recaptchaResponseInput.value = token;
    }

    const submitBtn = document.getElementById("boton_enviar");
    if (submitBtn) {
        submitBtn.disabled = false;
    }
};

window.onRecaptchaExpired = function() {
    const submitBtn = document.getElementById("boton_enviar");
    if (submitBtn) {
        submitBtn.disabled = true;
    }

    const recaptchaResponseInput = document.getElementById("g_recaptcha_response");
    if (recaptchaResponseInput) {
        recaptchaResponseInput.value = "";
    }
};
