import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any
from fastapi import Depends
from fastapi.templating import Jinja2Templates

from src.domain.catalog import CatalogRepository
from src.domain.lead import Lead, LeadNotifier
from src.infrastructure.config import settings
from src.infrastructure.repositories.yaml_catalog import YamlCatalogRepository
from src.infrastructure.services.logger import logger, LoggingLeadNotifier
from src.infrastructure.services.chatwoot_lead_notifier import ChatwootLeadNotifier

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
DATA_FILE = BASE_DIR / "data" / "site_data.yml"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

_catalog_repo = YamlCatalogRepository(DATA_FILE)

class CompositeLeadNotifier(LeadNotifier):
    def __init__(self, notifiers: list[LeadNotifier]):
        self.notifiers = notifiers

    async def notify(self, lead: Lead) -> None:
        for notifier in self.notifiers:
            try:
                await notifier.notify(lead)
            except Exception as e:
                logger.error("Error al notificar lead con %s: %s", notifier.__class__.__name__, str(e))

# Configurar notificaciones múltiples según variables de entorno
_active_notifiers: list[LeadNotifier] = [LoggingLeadNotifier()]

if settings.CHATWOOT_API_TOKEN:
    _active_notifiers.append(ChatwootLeadNotifier())

_lead_notifier: LeadNotifier = CompositeLeadNotifier(_active_notifiers)

def get_catalog_repository() -> CatalogRepository:
    return _catalog_repo

def get_lead_notifier() -> LeadNotifier:
    return _lead_notifier


def _get_git_version() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=BASE_DIR,
            text=True,
        ).strip()
    except Exception:
        return "dev"


def get_common_context(
    repo: CatalogRepository = Depends(get_catalog_repository),
) -> dict[str, Any]:
    return {
        "categories": repo.get_categories(),
        "carousel_slides": repo.get_carousel_slides(),
        "site_info": repo.get_site_info(),
        "static_version": _get_git_version(),
        "current_year": datetime.now().year,
        "google_analytics_id": settings.GOOGLE_ANALYTICS_ID,
        "microsoft_clarity_id": settings.MICROSOFT_CLARITY_ID,
    }
