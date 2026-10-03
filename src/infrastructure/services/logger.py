import logging

from src.domain.lead import Lead, LeadNotifier

logger = logging.getLogger("uvicorn.error")


class LoggingLeadNotifier(LeadNotifier):
    async def notify(self, lead: Lead) -> None:
        logger.info(
            "\x1b[1;36mNUEVO LEAD NOTIFICADO A LOG\x1b[0m -> Email: %s",
            lead.email,
        )
