import logging
from src.domain.lead import Lead, LeadNotifier

# Logger principal del proyecto que hereda el formato y colores de Uvicorn
logger = logging.getLogger("uvicorn.error")

class LoggingLeadNotifier(LeadNotifier):
    async def notify(self, lead: Lead) -> None:
        logger.info(
            "\x1b[1;36mNUEVO LEAD REGISTRADO\x1b[0m -> Nombre: \x1b[1m%s\x1b[0m | Email: \x1b[1m%s\x1b[0m | Teléfono: \x1b[1m%s\x1b[0m | Productos: \x1b[1m%s\x1b[0m | Mensaje: \x1b[1m%s\x1b[0m",
            lead.nombre,
            lead.email,
            lead.telefono,
            lead.productos or "Ninguno",
            lead.mensaje
        )
