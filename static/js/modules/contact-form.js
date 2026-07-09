export function initContactForm() {
    // Bind the callback function to window object so Google reCAPTCHA can invoke it globally
    window.onSubmit_contactanos = function (token) {
        const form = document.getElementById("form_contactanos");
        if (form) {
            if (form.checkValidity()) {
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
