from fastapi.testclient import TestClient
from tests.conftest import MOCK_SITE_INFO

def test_health(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_robots_txt(client: TestClient):
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert "User-agent: *" in response.text
    assert "Disallow: /health" in response.text


def test_sitemap_xml(client: TestClient):
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    assert "application/xml" in response.headers["content-type"]
    assert f"<loc>{MOCK_SITE_INFO.base_url}/</loc>" in response.text
    assert f"<loc>{MOCK_SITE_INFO.base_url}/categoria/termostatos</loc>" in response.text


def test_index_page(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    # Check that security headers are present
    assert "Strict-Transport-Security" in response.headers
    assert "Content-Security-Policy" in response.headers
    assert "X-Frame-Options" in response.headers


def test_view_cart(client: TestClient):
    response = client.get("/carrito")
    assert response.status_code == 200
    assert "Solicitud de Cotización Mayorista" in response.text



def test_category_page_success(client: TestClient):
    response = client.get("/categoria/termostatos")
    assert response.status_code == 200


def test_category_page_not_found(client: TestClient):
    response = client.get("/categoria/nonexistent-category")
    assert response.status_code == 404
    assert "La categoría solicitada no existe o ha sido movida" in response.text


def test_search_success(client: TestClient):
    response = client.post("/buscar", data={"busqueda": "termo"}, follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/categoria/termostatos"


def test_search_empty(client: TestClient):
    response = client.post("/buscar", data={"busqueda": ""}, follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/"


def test_search_no_results(client: TestClient):
    response = client.post("/buscar", data={"busqueda": "xyz"}, follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/"


def test_custom_404_page(client: TestClient):
    response = client.get("/algun-path-invalido")
    assert response.status_code == 404
    assert "404 - Página no encontrada" in response.text
    assert "Lo sentimos, la página que estás buscando" in response.text


def test_blog_disabled(client: TestClient):
    # Por defecto, en MOCK_SITE_INFO, enable_blog es False
    response = client.get("/blog")
    assert response.status_code == 404
    
    response = client.get("/blog/test-post")
    assert response.status_code == 404


def test_blog_enabled(client: TestClient):
    # Habilitamos el blog obteniendo el repo del mock
    from src.infrastructure.fastapi.dependencies import get_catalog_repository
    repo = client.app.dependency_overrides[get_catalog_repository]()
    site_info = repo.get_site_info()
    site_info.enable_blog = True
    try:
        response = client.get("/blog")
        assert response.status_code == 200
        assert "Novedades y Fichas Técnicas" in response.text
        assert "Test Post" in response.text
        
        response = client.get("/blog/test-post")
        assert response.status_code == 200
        assert "Test Post" in response.text
        assert "Content" in response.text
        
        response = client.get("/blog/nonexistent-post")
        assert response.status_code == 404
    finally:
        # Restauramos el estado del mock
        site_info.enable_blog = False


def test_pdf_generator_disabled(client: TestClient):
    # Por defecto, enable_pdf_generator es False
    response = client.post(
        "/cotizacion/pdf",
        data={
            "nombre": "Agustin",
            "email": "test@test.com",
            "telefono": "12345678",
            "mensaje": "test message",
            "productos": "Producto A, Producto B"
        }
    )
    assert response.status_code == 403


def test_pdf_generator_enabled(client: TestClient):
    # Habilitamos el PDF generator
    from src.infrastructure.fastapi.dependencies import get_catalog_repository
    repo = client.app.dependency_overrides[get_catalog_repository]()
    site_info = repo.get_site_info()
    site_info.enable_pdf_generator = True
    try:
        # Petición exitosa
        response = client.post(
            "/cotizacion/pdf",
            data={
                "nombre": "Agustin",
                "email": "test@test.com",
                "telefono": "12345678",
                "mensaje": "test message",
                "productos": "Producto A, Producto B"
            }
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert "attachment; filename=" in response.headers["content-disposition"]
        assert len(response.content) > 0
        
        # Petición sin productos
        response = client.post(
            "/cotizacion/pdf",
            data={
                "nombre": "Agustin",
                "email": "test@test.com",
                "telefono": "12345678",
                "mensaje": "test message",
                "productos": ""
            }
        )
        assert response.status_code == 400
    finally:
        site_info.enable_pdf_generator = False

