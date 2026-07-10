from fastapi.testclient import TestClient

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
    assert "<loc>https://www.eitec.coop.ar/</loc>" in response.text
    assert "<loc>https://www.eitec.coop.ar/categoria/termostatos</loc>" in response.text


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
