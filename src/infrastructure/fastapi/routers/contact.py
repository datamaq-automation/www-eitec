from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import RedirectResponse

from src.domain.lead import Lead, LeadNotifier
from src.infrastructure.fastapi.dependencies import get_lead_notifier
from src.infrastructure.services.logger import logger

router = APIRouter()


@router.get("/contactanos")
@router.get("/contacto")
async def contact_page() -> RedirectResponse:
    return RedirectResponse(url="/#contacto", status_code=301)


@router.post("/contacto")
async def contact(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(...),
    mensaje: str = Form(""),
    productos: str | None = Form(None),
    notifier: LeadNotifier = Depends(get_lead_notifier),
) -> RedirectResponse:
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

    return RedirectResponse(url="/gracias", status_code=303)
