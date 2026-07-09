import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.domain.lead import Lead, LeadNotifier
from src.infrastructure.config import settings
from src.infrastructure.services.logger import logger

class SmtpLeadNotifier(LeadNotifier):
    async def notify(self, lead: Lead) -> None:
        try:
            # Ejecutar el proceso síncrono de smtplib en un thread pool asíncrono
            await asyncio.to_thread(self._send_email, lead)
            logger.info("\x1b[1;32mNOTIFICACIÓN SMTP EXITOSA\x1b[0m -> Lead notificado correctamente por correo")
        except Exception as e:
            logger.error(
                "\x1b[1;31mFALLA EN NOTIFICACIÓN SMTP\x1b[0m -> No se pudo enviar el correo del lead: %s",
                str(e)
            )

    def _send_email(self, lead: Lead) -> None:
        msg = MIMEMultipart()
        msg["From"] = settings.CONTACT_SENDER_EMAIL
        msg["To"] = settings.CONTACT_RECIPIENT_EMAIL
        msg["Subject"] = f"Nuevo contacto desde el sitio web - {lead.nombre}"

        body = (
            f"Se ha registrado un nuevo contacto en el sitio web de EITEC:\n\n"
            f"Nombre: {lead.nombre}\n"
            f"Email: {lead.email}\n"
            f"Teléfono: {lead.telefono}\n\n"
            f"Mensaje:\n{lead.mensaje}\n"
        )
        msg.attach(MIMEText(body, "plain", "utf-8"))

        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10)
        
        if settings.SMTP_USE_TLS:
            server.starttls()
        
        if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            
        server.sendmail(settings.CONTACT_SENDER_EMAIL, settings.CONTACT_RECIPIENT_EMAIL, msg.as_string())
        server.quit()
