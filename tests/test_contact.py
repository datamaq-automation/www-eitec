from fastapi.testclient import TestClient

def test_contactanos_redirect(client: TestClient):
    response = client.get("/contactanos", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["location"] == "/#contacto"


def test_contacto_redirect(client: TestClient):
    response = client.get("/contacto", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["location"] == "/#contacto"


def test_thanks_page(client: TestClient):
    response = client.get("/gracias")
    assert response.status_code == 200
    assert "¡Muchas gracias!" in response.text
    assert "Tu mensaje ha sido enviado con éxito" in response.text


def test_contact_form_submission_success(client: TestClient):
    response = client.post(
        "/contacto",
        data={
            "nombre": "Juan Pérez",
            "email": "juan@example.com",
            "telefono": "12345678",
            "mensaje": "Consulta de prueba"
        },
        follow_redirects=False
    )
    assert response.status_code == 303
    assert response.headers["location"] == "/gracias"


def test_contact_form_submission_with_products(client: TestClient):
    response = client.post(
        "/contacto",
        data={
            "nombre": "Juan Pérez",
            "email": "juan@example.com",
            "telefono": "12345678",
            "mensaje": "Consulta de prueba",
            "productos": "Termostatos, Válvulas"
        },
        follow_redirects=False
    )
    assert response.status_code == 303
    assert response.headers["location"] == "/gracias"
