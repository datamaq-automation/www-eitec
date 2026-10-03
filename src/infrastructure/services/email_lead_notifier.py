import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.domain.lead import Lead, LeadNotifier
from src.infrastructure.config import settings
from src.infrastructure.services.logger import logger


class EmailLeadNotifier(LeadNotifier):
    def __init__(self, recipient_email: str) -> None:
        self.recipient_email = recipient_email

    async def notify(self, lead: Lead) -> None:
        if not settings.SMTP_HOST or not settings.SMTP_PORT:
            logger.warning(
                "Email notifier no está configurado (falta SMTP_HOST o SMTP_PORT)."
            )
            return

        try:
            subject = f"Nuevo lead de contacto: {lead.nombre}"
            body = self._format_email_body(lead)

            msg = MIMEMultipart()
            msg["From"] = settings.SMTP_FROM or "noreply@eitec.coop.ar"
            msg["To"] = self.recipient_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain", "utf-8"))

            with smtplib.SMTP(
                settings.SMTP_HOST, settings.SMTP_PORT, timeout=10
            ) as server:
                if settings.SMTP_TLS:
                    server.starttls()
                if settings.SMTP_USER and settings.SMTP_PASSWORD:
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)

            logger.info(
                "\x1b[1;32mEMAIL DE LEAD ENVIADO\x1b[0m -> %s", self.recipient_email
            )
        except Exception as e:
            logger.error("\x1b[1;31mFALLA AL ENVIAR EMAIL\x1b[0m -> Error: %s", str(e))
            raise

    def _format_email_body(self, lead: Lead) -> str:
        return (
            f"Nuevo lead recibido en el formulario de contacto:\n\n"
            f"Nombre: {lead.nombre}\n"
            f"Email: {lead.email}\n"
            f"Teléfono: {lead.telefono}\n"
            f"Productos de interés: {lead.productos or 'Ninguno'}\n\n"
            f"Mensaje:\n{lead.mensaje}"
        )
