import urllib.request
import urllib.parse
import json
from typing import Any
from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.concurrency import run_in_threadpool

from src.domain.lead import Lead, LeadNotifier
from src.infrastructure.config import settings
from src.infrastructure.fastapi.dependencies import (
    templates,
    get_lead_notifier,
    get_common_context,
)
from src.infrastructure.services.logger import logger

router = APIRouter()

def verify_recaptcha_sync(token: str | None, secret_key: str) -> bool:
    if not token:
        return False
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = urllib.parse.urlencode({
        "secret": secret_key,
        "response": token
    }).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data.get("success", False)
    except Exception as e:
        logger.error("Error al verificar reCAPTCHA en el servidor: %s", str(e))
        return False


@router.get("/contactanos")
async def contact_page() -> RedirectResponse:
    return RedirectResponse(url="/", status_code=307)


@router.post("/contacto", response_class=HTMLResponse)
async def contact(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(...),
    mensaje: str = Form(""),
    g_recaptcha_response: str = Form(None, alias="g-recaptcha-response"),
    productos: str | None = Form(None),
    notifier: LeadNotifier = Depends(get_lead_notifier),
    context: dict[str, Any] = Depends(get_common_context),
) -> HTMLResponse:
    # Depurar petición entrante
    client_ip = request.client.host if request.client else "Desconocida"
    logger.info(
        "\x1b[1;33mPETICIÓN DE CONTACTO RECIBIDA\x1b[0m -> IP: \x1b[1m%s\x1b[0m | Nombre: '%s' | Email: '%s' | Teléfono: '%s' | Productos: '%s'",
        client_ip,
        nombre,
        email,
        telefono,
        productos
    )

    # Validar reCAPTCHA si hay una clave secreta configurada
    if settings.RECAPTCHA_SECRET_KEY:
        if settings.RECAPTCHA_SECRET_KEY.startswith("6LcPPAwqAAAAALh_legacy_placeholder"):
            logger.warning("reCAPTCHA omitido: usando clave de prueba/marcador de posición.")
        else:
            is_valid = await run_in_threadpool(
                verify_recaptcha_sync, g_recaptcha_response, settings.RECAPTCHA_SECRET_KEY
            )
            if not is_valid:
                logger.warning(
                    "Intento de envío de formulario de contacto bloqueado por reCAPTCHA de IP: %s",
                    client_ip
                )
                context.update(
                    {
                        "title": "Verificación fallida - EITEC",
                        "description": "Error al verificar reCAPTCHA.",
                        "canonical_url": "https://www.eitec.coop.ar/",
                        "noindex": True,
                        "message": "Error de verificación de seguridad (reCAPTCHA). Por favor, intenta de nuevo.",
                        "message_type": "danger",
                    }
                )
                return templates.TemplateResponse(request, "index.html", context)

    # Registrar y notificar el lead
    lead = Lead(nombre=nombre, email=email, telefono=telefono, mensaje=mensaje, productos=productos)
    await notifier.notify(lead)

    context.update(
        {
            "title": "Mensaje enviado - EITEC",
            "description": "Formulario de contacto de EITEC Cooperativa Bernal. Contactate por repuestos de gas EITAR.",
            "canonical_url": "https://www.eitec.coop.ar/",
            "noindex": True,
            "message": "Gracias por contactarte. Te responderemos a la brevedad.",
            "message_type": "success",
        }
    )
    return templates.TemplateResponse(request, "index.html", context)
