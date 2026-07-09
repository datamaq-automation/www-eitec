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
