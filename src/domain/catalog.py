from typing import Protocol
from pydantic import BaseModel

class Category(BaseModel):
    name: str
    slug: str
    image: str

class CarouselSlide(BaseModel):
    title: str
    image: str
    link: str

class SiteInfo(BaseModel):
    title: str
    subtitle: str
    intro_title: str
    intro_text: str
    category_lead_template: str
    category_description: str
    contact_email: str
    contact_whatsapp: str | None = None
    social_facebook: str
    social_instagram: str
    base_url: str = "https://www.eitec.coop.ar"
    google_analytics_id: str | None = None
    microsoft_clarity_id: str | None = None
    chatwoot_api_url: str = "https://chatwoot.eitec.com.ar"
    chatwoot_account_id: int = 1
    chatwoot_inbox_id: int = 1

class CatalogRepository(Protocol):
    def get_categories(self) -> list[Category]:
        ...

    def get_carousel_slides(self) -> list[CarouselSlide]:
        ...

    def get_category_slugs(self) -> set[str]:
        ...

    def get_category_by_slug(self, slug: str) -> Category | None:
        ...

    def search_categories(self, query: str) -> list[Category]:
        ...

    def get_site_info(self) -> SiteInfo:
        ...

