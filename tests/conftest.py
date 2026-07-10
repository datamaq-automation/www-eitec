import pytest
from typing import Generator
from fastapi.testclient import TestClient
from src.infrastructure.fastapi.app import app
from src.infrastructure.config import settings

# Prevent any real HTTP requests to Chatwoot during test suites
settings.CHATWOOT_API_TOKEN = ""
from src.domain.catalog import CatalogRepository, Category, CarouselSlide, SiteInfo, BlogPost
from src.domain.lead import Lead, LeadNotifier
from src.infrastructure.fastapi.dependencies import get_catalog_repository, get_lead_notifier

# Mock data
MOCK_CATEGORIES = [
    Category(name="Termostatos", slug="termostatos", image="termostatos.jpg"),
    Category(name="Válvulas", slug="valvulas", image="valvulas.jpg"),
]

MOCK_SLIDES = [
    CarouselSlide(title="Slide 1", image="slide1.jpg", link="/categoria/termostatos"),
]

MOCK_SITE_INFO = SiteInfo(
    title="EITEC Cooperativa de Trabajo",
    subtitle="Fábrica de accesorios para artefactos a gas",
    intro_title="EITEC Cooperativa de Trabajo",
    intro_text="Fábrica recuperada dedicada a la producción y comercialización de accesorios para artefactos a gas.",
    category_lead_template="Fabricación y venta de <strong>{category_name}</strong> de alta calidad.",
    category_description="Como cooperativa industrial EITEC (anteriormente EITAR), producimos accesorios a gas.",
    contact_email="horacio@eitec.coop.ar",
    social_facebook="https://www.facebook.com/CooperativaEitec",
    social_instagram="https://www.instagram.com/eitec_cooperativa/",
    chatwoot_api_url="https://chatwoot.eitec.com.ar",
    chatwoot_account_id=3,
    chatwoot_inbox_id=13,
    enable_blog=False,
    enable_pdf_generator=False
)

MOCK_BLOG_POSTS = [
    BlogPost(
        title="Test Post",
        slug="test-post",
        date="2026-07-10",
        summary="Summary",
        content="<p>Content</p>",
        image="test.jpg"
    )
]

class MockCatalogRepository(CatalogRepository):
    def get_categories(self) -> list[Category]:
        return MOCK_CATEGORIES

    def get_carousel_slides(self) -> list[CarouselSlide]:
        return MOCK_SLIDES

    def get_category_slugs(self) -> set[str]:
        return {cat.slug for cat in MOCK_CATEGORIES}

    def get_category_by_slug(self, slug: str) -> Category | None:
        for cat in MOCK_CATEGORIES:
            if cat.slug == slug:
                return cat
        return None

    def search_categories(self, query: str) -> list[Category]:
        q = query.lower()
        return [cat for cat in MOCK_CATEGORIES if q in cat.name.lower()]

    def get_site_info(self) -> SiteInfo:
        return MOCK_SITE_INFO

    def get_blog_posts(self) -> list[BlogPost]:
        return MOCK_BLOG_POSTS

    def get_blog_post_by_slug(self, slug: str) -> BlogPost | None:
        for post in MOCK_BLOG_POSTS:
            if post.slug == slug:
                return post
        return None


class MockLeadNotifier(LeadNotifier):
    def __init__(self) -> None:
        self.notified_leads: list[Lead] = []

    async def notify(self, lead: Lead) -> None:
        self.notified_leads.append(lead)


@pytest.fixture
def mock_catalog_repo() -> MockCatalogRepository:
    return MockCatalogRepository()


@pytest.fixture
def mock_lead_notifier() -> MockLeadNotifier:
    return MockLeadNotifier()


@pytest.fixture
def client(
    mock_catalog_repo: MockCatalogRepository,
    mock_lead_notifier: MockLeadNotifier
) -> Generator[TestClient, None, None]:
    # Set up overrides
    app.dependency_overrides[get_catalog_repository] = lambda: mock_catalog_repo
    app.dependency_overrides[get_lead_notifier] = lambda: mock_lead_notifier
    
    with TestClient(app) as test_client:
        yield test_client
        
    # Clean up overrides
    app.dependency_overrides.clear()
