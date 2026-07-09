from pathlib import Path
import yaml
from src.domain.catalog import CatalogRepository, Category, CarouselSlide

class YamlCatalogRepository(CatalogRepository):
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self._data = self._load_data()

    def _load_data(self) -> dict:
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
        
        results = []
        for cat in self.get_categories():
            if q in cat.name.lower():
                results.append(cat)
        return results
