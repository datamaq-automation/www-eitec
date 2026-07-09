from typing import Any
from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from src.domain.lead import Lead, LeadNotifier
from src.infrastructure.fastapi.dependencies import (
    templates,
    get_lead_notifier,
    get_common_context,
)

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
    notifier: LeadNotifier = Depends(get_lead_notifier),
    context: dict[str, Any] = Depends(get_common_context),
) -> HTMLResponse:
    # Registrar y notificar el lead
    lead = Lead(nombre=nombre, email=email, telefono=telefono, mensaje=mensaje)
    await notifier.notify(lead)

    context.update(
        {
            "title": "Mensaje enviado - EITEC",
            "description": "Formulario de contacto de EITEC Cooperativa Bernal. Contactate por repuestos de gas EITAR.",
            "canonical_url": "https://www.eitec.coop.ar/",
            "noindex": True,
            "message": "Gracias por contactarte. Te responderemos a la brevedad.",
        }
    )
    return templates.TemplateResponse(request, "index.html", context)
