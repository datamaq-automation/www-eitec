from fastapi.testclient import TestClient

def test_contactanos_redirect(client: TestClient):
    response = client.get("/contactanos", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/#contacto"


def test_contact_form_submission_success(client: TestClient):
    response = client.post(
        "/contacto",
        data={
            "nombre": "Juan Pérez",
            "email": "juan@example.com",
            "telefono": "12345678",
            "mensaje": "Consulta de prueba"
        }
    )
    assert response.status_code == 200
    assert "Gracias por contactarte" in response.text


def test_contact_form_submission_with_products(client: TestClient):
    response = client.post(
        "/contacto",
        data={
            "nombre": "Juan Pérez",
            "email": "juan@example.com",
            "telefono": "12345678",
            "mensaje": "Consulta de prueba",
            "productos": "Termostatos, Válvulas"
        }
    )
    assert response.status_code == 200
    assert "Gracias por contactarte" in response.text
