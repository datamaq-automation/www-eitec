from pathlib import Path
from typing import Any
import yaml
from src.domain.catalog import CatalogRepository, Category, CarouselSlide, SiteInfo, BlogPost

from src.infrastructure.config import settings

class YamlCatalogRepository(CatalogRepository):
    _data: dict[str, Any]

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self._data = self._load_data()

    def _load_data(self) -> dict[str, Any]:
        if self.file_path.exists():
            with open(self.file_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        return {}

    def get_categories(self) -> list[Category]:
        return [Category(**cat) for cat in self._data.get("categories", [])]

    def get_carousel_slides(self) -> list[CarouselSlide]:
        return [CarouselSlide(**slide) for slide in self._data.get("carousel_slides", [])]

    def get_category_slugs(self) -> set[str]:
        return {cat.slug for cat in self.get_categories()}

    def get_category_by_slug(self, slug: str) -> Category | None:
        for cat in self.get_categories():
            if cat.slug == slug:
                return cat
        return None

    def search_categories(self, query: str) -> list[Category]:
        q = query.strip().lower()
        if not q:
            return []
        
        results: list[Category] = []
        for cat in self.get_categories():
            if q in cat.name.lower():
                results.append(cat)
        return results

    def get_site_info(self) -> SiteInfo:
        info = SiteInfo(**self._data.get("site_info", {}))
        info.enable_pdf_generator = settings.ENABLE_PDF_GENERATOR
        info.enable_blog = settings.ENABLE_BLOG
        return info

    def get_blog_posts(self) -> list[BlogPost]:
        return [BlogPost(**post) for post in self._data.get("blog_posts", [])]

    def get_blog_post_by_slug(self, slug: str) -> BlogPost | None:
        for post in self.get_blog_posts():
            if post.slug == slug:
                return post
        return None

