// Cookie Consent Manager for EITEC (Google Analytics & Microsoft Clarity)

function loadGoogleAnalytics(gaId) {
    if (!gaId || document.getElementById('gtm-script')) return;

    // Load gtag script
    const script = document.createElement('script');
    script.id = 'gtm-script';
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${gaId}`;
    document.head.appendChild(script);

    // Initialize gtag
    const initScript = document.createElement('script');
    initScript.id = 'gtm-init';
    initScript.innerHTML = `
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', '${gaId}', { 'anonymize_ip': true });
    `;
    document.head.appendChild(initScript);
    console.log('[Analytics] Google Analytics loaded successfully.');
}

function loadMicrosoftClarity(clarityId) {
    if (!clarityId || document.getElementById('clarity-script')) return;

    const script = document.createElement('script');
    script.id = 'clarity-script';
    script.type = 'text/javascript';
    script.innerHTML = `
        (function(c,l,a,r,i,t,y){
            c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
            t=l.createElement(i);t.async=1;t.src="https://www.clarity.ms/tag/"+r;
            y=l.getElementsByTagName(i)[0];y.parentNode.insertBefore(t,y);
        })(window, document, "clarity", "script", "${clarityId}");
    `;
    document.head.appendChild(script);
    console.log('[Analytics] Microsoft Clarity loaded successfully.');
}

function enableTracking() {
    const gaId = window.EITEC_GA_ID;
    const clarityId = window.EITEC_CLARITY_ID;

    if (gaId) {
        loadGoogleAnalytics(gaId);
    }
    if (clarityId) {
        loadMicrosoftClarity(clarityId);
    }
}

export function initCookies() {
    const banner = document.getElementById('cookie-banner');
    if (!banner) return;

    const consent = localStorage.getItem('eitec_cookies_consent');
    const whatsappBtn = document.querySelector('.whatsapp-btn');
    
    // Evitar solapamientos informativos en páginas de contenido legal
    const isLegalPage = window.location.pathname === '/politica-de-privacidad' || 
                        window.location.pathname === '/terminos-y-condiciones';

    if (consent === 'accepted') {
        enableTracking();
    } else if (consent === 'rejected') {
        console.log('[Analytics] Tracking cookies rejected by user preference.');
    } else if (!isLegalPage) {
        // Show banner
        banner.classList.remove('d-none');
        if (whatsappBtn) {
            whatsappBtn.classList.add('whatsapp-btn--elevated');
        }

        const btnAccept = document.getElementById('btn-accept-cookies');
        const btnReject = document.getElementById('btn-reject-cookies');

        if (btnAccept) {
            btnAccept.addEventListener('click', () => {
                localStorage.setItem('eitec_cookies_consent', 'accepted');
                banner.classList.add('d-none');
                if (whatsappBtn) {
                    whatsappBtn.classList.remove('whatsapp-btn--elevated');
                }
                enableTracking();
            });
        }

        if (btnReject) {
            btnReject.addEventListener('click', () => {
                localStorage.setItem('eitec_cookies_consent', 'rejected');
                banner.classList.add('d-none');
                if (whatsappBtn) {
                    whatsappBtn.classList.remove('whatsapp-btn--elevated');
                }
                console.log('[Analytics] Tracking cookies rejected.');
            });
        }
    }
}
