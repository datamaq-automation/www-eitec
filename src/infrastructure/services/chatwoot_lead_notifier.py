from typing import Any
import httpx
from src.domain.lead import Lead, LeadNotifier
from src.infrastructure.config import settings
from src.infrastructure.services.logger import logger

class ChatwootLeadNotifier(LeadNotifier):
    async def notify(self, lead: Lead) -> None:
        if not settings.CHATWOOT_API_TOKEN or not settings.CHATWOOT_API_URL:
            logger.warning("Chatwoot no está configurado (falta CHATWOOT_API_TOKEN o CHATWOOT_API_URL).")
            return

        base_url = settings.CHATWOOT_API_URL.rstrip("/")
        if "/api/v1" not in base_url:
            url = f"{base_url}/api/v1/accounts/{settings.CHATWOOT_ACCOUNT_ID}/contacts"
        else:
            url = f"{base_url}/accounts/{settings.CHATWOOT_ACCOUNT_ID}/contacts"

        headers = {
            "Content-Type": "application/json",
            "api_access_token": settings.CHATWOOT_API_TOKEN
        }

        # Process phone number formatting for Chatwoot (E.164 expected)
        phone = lead.telefono.strip()
        if phone and not phone.startswith("+") and phone.isdigit():
            # Standard formatting assumption: prepend a plus sign
            phone = f"+{phone}"

        payload: dict[str, Any] = {
            "inbox_id": settings.CHATWOOT_INBOX_ID,
            "name": lead.nombre,
            "email": lead.email,
            "phone_number": phone,
            "custom_attributes": {
                "mensaje": lead.mensaje,
                "productos": lead.productos or ""
            }
        }

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(url, headers=headers, json=payload)
                if response.status_code in (200, 201):
                    logger.info("\x1b[1;32mCONTACTO CREADO EN CHATWOOT\x1b[0m -> Lead creado correctamente en Chatwoot API")
                else:
                    logger.error(
                        "\x1b[1;31mFALLA EN CHATWOOT API\x1b[0m -> Código de estado %d: %s",
                        response.status_code,
                        response.text
                    )
        except Exception as e:
            logger.error("\x1b[1;31mFALLA EN CHATWOOT API\x1b[0m -> Error de conexión: %s", str(e))
