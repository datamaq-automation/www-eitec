from typing import Any, cast
import httpx
from src.domain.catalog import CatalogRepository
from src.domain.lead import Lead, LeadNotifier
from src.infrastructure.config import settings
from src.infrastructure.services.logger import logger

class ChatwootLeadNotifier(LeadNotifier):
    def __init__(self, repo: CatalogRepository | None = None) -> None:
        self.repo = repo

    def _format_phone(self, phone: str) -> str:
        cleaned = phone.strip()
        if cleaned and not cleaned.startswith("+") and cleaned.isdigit():
            return f"+{cleaned}"
        return cleaned

    async def _search_contact(
        self, client: httpx.AsyncClient, api_url: str, account_id: int, query: str, headers: dict[str, str]
    ) -> int | None:
        # El search endpoint de Chatwoot busca por email o por telefono
        if "/api/v1" not in api_url:
            url = f"{api_url}/api/v1/accounts/{account_id}/contacts/search"
        else:
            url = f"{api_url}/accounts/{account_id}/contacts/search"

        try:
            response = await client.get(url, headers=headers, params={"q": query})
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict):
                    data_dict = cast(dict[str, Any], data)
                    contacts = cast(list[Any], data_dict.get("payload", []))
                    if contacts:
                        first_contact = contacts[0]
                        if isinstance(first_contact, dict):
                            first_contact_dict = cast(dict[str, Any], first_contact)
                            val = cast(Any, first_contact_dict.get("id"))
                            if val is not None:
                                return int(val)
        except Exception as e:
            logger.error("Error al buscar contacto en Chatwoot: %s", str(e))
        return None

    async def _update_contact(
        self, client: httpx.AsyncClient, api_url: str, account_id: int, contact_id: int, lead: Lead, headers: dict[str, str]
    ) -> None:
        if "/api/v1" not in api_url:
            url = f"{api_url}/api/v1/accounts/{account_id}/contacts/{contact_id}"
        else:
            url = f"{api_url}/accounts/{account_id}/contacts/{contact_id}"

        payload: dict[str, Any] = {
            "name": lead.nombre,
            "email": lead.email,
            "custom_attributes": {
                "mensaje": lead.mensaje,
                "productos": lead.productos or ""
            }
        }
        try:
            response = await client.put(url, headers=headers, json=payload)
            if response.status_code == 200:
                logger.info("Contacto %d actualizado en Chatwoot.", contact_id)
            else:
                logger.error("Falla al actualizar contacto en Chatwoot: Código %d: %s", response.status_code, response.text)
        except Exception as e:
            logger.error("Excepción al actualizar contacto en Chatwoot: %s", str(e))

    async def _create_contact(
        self, client: httpx.AsyncClient, api_url: str, account_id: int, phone: str, lead: Lead, headers: dict[str, str]
    ) -> int | None:
        if "/api/v1" not in api_url:
            url = f"{api_url}/api/v1/accounts/{account_id}/contacts"
        else:
            url = f"{api_url}/accounts/{account_id}/contacts"

        payload: dict[str, Any] = {
            "name": lead.nombre,
            "email": lead.email,
            "phone_number": phone,
            "custom_attributes": {
                "mensaje": lead.mensaje,
                "productos": lead.productos or ""
            }
        }
        try:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code in (200, 201):
                data = response.json()
                if isinstance(data, dict):
                    data_dict = cast(dict[str, Any], data)
                    contact_data = cast(dict[str, Any], data_dict.get("payload", {}))
                    contact = cast(dict[str, Any], contact_data.get("contact", {}))
                    if "id" in contact:
                        val = cast(Any, contact.get("id"))
                        if val is not None:
                            return int(val)
                    val2 = cast(Any, contact_data.get("id"))
                    if val2 is not None:
                        return int(val2)
            else:
                logger.error("Falla al crear contacto en Chatwoot: Código %d: %s", response.status_code, response.text)
        except Exception as e:
            logger.error("Excepción al crear contacto en Chatwoot: %s", str(e))
        return None

    async def _create_conversation(
        self, client: httpx.AsyncClient, api_url: str, account_id: int, inbox_id: int, contact_id: int, headers: dict[str, str]
    ) -> int | None:
        if "/api/v1" not in api_url:
            url = f"{api_url}/api/v1/accounts/{account_id}/conversations"
        else:
            url = f"{api_url}/accounts/{account_id}/conversations"

        payload = {
            "inbox_id": inbox_id,
            "contact_id": contact_id
        }
        try:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code in (200, 201):
                data = response.json()
                if isinstance(data, dict):
                    data_dict = cast(dict[str, Any], data)
                    if "id" in data_dict:
                        val = cast(Any, data_dict.get("id"))
                        if val is not None:
                            return int(val)
                    payload_data = cast(dict[str, Any], data_dict.get("payload", {}))
                    val2 = cast(Any, payload_data.get("id"))
                    if val2 is not None:
                        return int(val2)
            else:
                logger.error("Falla al crear conversación en Chatwoot: Código %d: %s", response.status_code, response.text)
        except Exception as e:
            logger.error("Excepción al crear conversación en Chatwoot: %s", str(e))
        return None

    async def _send_message(
        self, client: httpx.AsyncClient, api_url: str, account_id: int, conversation_id: int, lead: Lead, headers: dict[str, str]
    ) -> None:
        if "/api/v1" not in api_url:
            url = f"{api_url}/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages"
        else:
            url = f"{api_url}/accounts/{account_id}/conversations/{conversation_id}/messages"

        # Mensaje formateado para que sea fácilmente legible por los agentes
        content = (
            f"Consulta Web de EITEC\n\n"
            f"*Nombre:* {lead.nombre}\n"
            f"*Email:* {lead.email}\n"
            f"*Teléfono:* {lead.telefono}\n"
            f"*Productos de interés:* {lead.productos or 'Ninguno'}\n\n"
            f"*Mensaje:*\n{lead.mensaje}"
        )
        payload = {
            "content": content,
            "message_type": "incoming"
        }
        try:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code in (200, 201):
                logger.info("Mensaje enviado con éxito a la conversación de Chatwoot.")
            else:
                logger.error("Falla al enviar mensaje en Chatwoot: Código %d: %s", response.status_code, response.text)
        except Exception as e:
            logger.error("Excepción al enviar mensaje en Chatwoot: %s", str(e))

    async def notify(self, lead: Lead) -> None:
        if not settings.CHATWOOT_API_TOKEN:
            logger.warning("Chatwoot no está configurado (falta CHATWOOT_API_TOKEN).")
            return

        if self.repo:
            site_info = self.repo.get_site_info()
            api_url = site_info.chatwoot_api_url
            account_id = site_info.chatwoot_account_id
            inbox_id = site_info.chatwoot_inbox_id
        else:
            # Fallback para pruebas que no inyectan el repo
            api_url = "https://chatwoot.eitec.com.ar"
            account_id = 1
            inbox_id = 1

        if not api_url:
            logger.warning("Chatwoot no está configurado (falta chatwoot_api_url).")
            return

        headers = {
            "Content-Type": "application/json",
            "api_access_token": settings.CHATWOOT_API_TOKEN
        }

        phone = self._format_phone(lead.telefono)

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                # 1. Buscar si el contacto ya existe por su teléfono
                contact_id = await self._search_contact(client, api_url, account_id, phone, headers)

                # Si no se encontró por teléfono, intentar buscar por email (para robustez del Upsert)
                if not contact_id and lead.email:
                    contact_id = await self._search_contact(client, api_url, account_id, lead.email.strip(), headers)

                # 2. Registrar el contacto (Upsert)
                if contact_id:
                    await self._update_contact(client, api_url, account_id, contact_id, lead, headers)
                else:
                    contact_id = await self._create_contact(client, api_url, account_id, phone, lead, headers)

                # 3. Habilitar la conversación y el envío de mensaje
                if contact_id:
                    conversation_id = await self._create_conversation(client, api_url, account_id, inbox_id, contact_id, headers)
                    if conversation_id:
                        await self._send_message(client, api_url, account_id, conversation_id, lead, headers)
                        logger.info("\x1b[1;32mINTEGRACIÓN CHATWOOT EXITOSA\x1b[0m -> Contacto, conversación y mensaje sincronizados.")
                else:
                    logger.error("No se pudo obtener o crear el contact_id en Chatwoot.")
        except Exception as e:
            logger.error("\x1b[1;31mFALLA EN CHATWOOT INTEGRATION\x1b[0m -> Error general: %s", str(e))
