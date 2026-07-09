from datetime import datetime
from pathlib import Path
from typing import Any
from fastapi import Depends
from fastapi.templating import Jinja2Templates

from src.domain.catalog import CatalogRepository
from src.domain.lead import LeadNotifier
from src.infrastructure.config import settings
from src.infrastructure.repositories.yaml_catalog import YamlCatalogRepository
from src.infrastructure.services.logger import LoggingLeadNotifier
from src.infrastructure.services.smtp_lead_notifier import SmtpLeadNotifier

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
DATA_FILE = BASE_DIR / "data" / "site_data.yml"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

_catalog_repo = YamlCatalogRepository(DATA_FILE)

# Iniciar SmtpLeadNotifier si SMTP_HOST no es 'localhost' y hay usuario configurado.
# De lo contrario, usar LoggingLeadNotifier para pruebas locales sin romper nada.
if settings.SMTP_HOST != "localhost" and settings.SMTP_USERNAME:
    _lead_notifier: LeadNotifier = SmtpLeadNotifier()
else:
    _lead_notifier: LeadNotifier = LoggingLeadNotifier()

def get_catalog_repository() -> CatalogRepository:
    return _catalog_repo

def get_lead_notifier() -> LeadNotifier:
    return _lead_notifier

def get_common_context(
    repo: CatalogRepository = Depends(get_catalog_repository),
) -> dict[str, Any]:
    return {
        "categories": repo.get_categories(),
        "carousel_slides": repo.get_carousel_slides(),
        "site_info": repo.get_site_info(),
        "current_year": datetime.now().year,
    }
