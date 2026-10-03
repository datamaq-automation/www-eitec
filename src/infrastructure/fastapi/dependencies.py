import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import Depends
from fastapi.templating import Jinja2Templates
from src.domain.catalog import CatalogRepository
from src.domain.lead import Lead, LeadNotifier
from src.infrastructure.config import settings
from src.infrastructure.persistence.lead_repository import LeadRepository
from src.infrastructure.repositories.yaml_catalog import YamlCatalogRepository
from src.infrastructure.services.email_lead_notifier import EmailLeadNotifier
from src.infrastructure.services.logger import LoggingLeadNotifier, logger

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
DATA_FILE = BASE_DIR / "data" / "site_data.yml"
LEADS_DB_FILE = BASE_DIR / "data" / "leads.db"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

_catalog_repo = YamlCatalogRepository(DATA_FILE)
_lead_repository = LeadRepository(LEADS_DB_FILE)


class CompositeLeadNotifier(LeadNotifier):
    def __init__(self, notifiers: list[LeadNotifier]):
        self.notifiers = notifiers

    async def notify(self, lead: Lead) -> None:
        for notifier in self.notifiers:
            try:
                await notifier.notify(lead)
            except Exception as e:
                logger.error(
                    "Error al notificar lead con %s: %s",
                    notifier.__class__.__name__,
                    str(e),
                )


# Configurar notificaciones múltiples según variables de entorno
_active_notifiers: list[LeadNotifier] = [LoggingLeadNotifier()]

# Agregar email notifier si SMTP está configurado
site_info = _catalog_repo.get_site_info()
if settings.SMTP_HOST and settings.SMTP_PORT:
    _active_notifiers.append(EmailLeadNotifier(site_info.contact_email))

_lead_notifier: LeadNotifier = CompositeLeadNotifier(_active_notifiers)


def get_catalog_repository() -> CatalogRepository:
    return _catalog_repo


def get_lead_notifier() -> LeadNotifier:
    return _lead_notifier


def get_lead_repository() -> LeadRepository:
    return _lead_repository


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
    site_info = repo.get_site_info()
    return {
        "categories": repo.get_categories(),
        "carousel_slides": repo.get_carousel_slides(),
        "site_info": site_info,
        "static_version": _get_git_version(),
        "current_year": datetime.now().year,
        "google_analytics_id": site_info.google_analytics_id,
        "microsoft_clarity_id": site_info.microsoft_clarity_id,
        "base_url": site_info.base_url.rstrip("/"),
    }
