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

