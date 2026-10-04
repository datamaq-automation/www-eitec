from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse

from src.domain.lead import Lead, LeadNotifier
from src.infrastructure.fastapi.dependencies import (
    get_lead_notifier,
    get_lead_repository,
)
from src.infrastructure.persistence.lead_repository import LeadRepository
from src.infrastructure.services.logger import logger
from src.infrastructure.services.rate_limiter import limiter
from src.infrastructure.services.recaptcha_service import RecaptchaService

router = APIRouter()


@router.get("/contactanos")
@router.get("/contacto")
async def contact_page() -> RedirectResponse:
    return RedirectResponse(url="/#contacto", status_code=301)


@router.post("/contacto")
@limiter.limit("5/hour")
async def contact(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(...),
    mensaje: str = Form(""),
    productos: str | None = Form(None),
    g_recaptcha_response: str = Form(""),
    notifier: LeadNotifier = Depends(get_lead_notifier),
    repo: LeadRepository = Depends(get_lead_repository),
) -> RedirectResponse:
    client_ip = request.client.host if request.client else "Desconocida"
    logger.info(
        "\x1b[1;33mPETICIÓN DE CONTACTO RECIBIDA\x1b[0m -> IP: \x1b[1m%s\x1b[0m",
        client_ip,
    )

    # Validar reCAPTCHA
    if not RecaptchaService.verify_token(g_recaptcha_response, client_ip):
        logger.warning(
            "\x1b[1;31mreCAPTCHA VALIDATION FAILED\x1b[0m -> IP: \x1b[1m%s\x1b[0m",
            client_ip,
        )
        raise HTTPException(status_code=400, detail="reCAPTCHA validation failed")

    lead = Lead(
        nombre=nombre,
        email=email,
        telefono=telefono,
        mensaje=mensaje,
        productos=productos,
    )

    try:
        # Persistir el lead antes de notificar
        lead_id = repo.save(lead)
        logger.info("\x1b[1;32mLEAD PERSISTIDO\x1b[0m -> ID: %d", lead_id)

        # Notificar el lead
        await notifier.notify(lead)

        return RedirectResponse(url="/gracias", status_code=303)
    except Exception as e:
        logger.error("\x1b[1;31mFALLA AL PROCESAR LEAD\x1b[0m -> Error: %s", str(e))
        return RedirectResponse(url="/gracias", status_code=500)
