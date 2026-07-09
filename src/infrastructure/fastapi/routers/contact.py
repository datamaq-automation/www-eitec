from typing import Any
from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from src.domain.lead import Lead, LeadNotifier
from src.infrastructure.fastapi.dependencies import (
    templates,
    get_lead_notifier,
    get_common_context,
)
from src.infrastructure.services.logger import logger

router = APIRouter()


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
