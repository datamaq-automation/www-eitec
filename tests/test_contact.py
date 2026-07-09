import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.infrastructure.config import settings

def test_contactanos_redirect(client: TestClient):
    response = client.get("/contactanos", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/"


def test_contact_form_submission_no_recaptcha(client: TestClient):
    # Test submission when RECAPTCHA_SECRET_KEY is empty (should skip validation)
    original_secret = settings.RECAPTCHA_SECRET_KEY
    settings.RECAPTCHA_SECRET_KEY = ""
    try:
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
    finally:
        settings.RECAPTCHA_SECRET_KEY = original_secret


def test_contact_form_submission_placeholder_recaptcha(client: TestClient):
    # Test submission when RECAPTCHA_SECRET_KEY is a placeholder
    original_secret = settings.RECAPTCHA_SECRET_KEY
    settings.RECAPTCHA_SECRET_KEY = "6LcPPAwqAAAAALh_legacy_placeholder_key_change_me"
    try:
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
    finally:
        settings.RECAPTCHA_SECRET_KEY = original_secret


@patch("urllib.request.urlopen")
def test_contact_form_submission_recaptcha_success(mock_urlopen, client: TestClient):
    # Mocking successful reCAPTCHA verification
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"success": true}'
    mock_response.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_response

    original_secret = settings.RECAPTCHA_SECRET_KEY
    settings.RECAPTCHA_SECRET_KEY = "real_secret_key"
    try:
        response = client.post(
            "/contacto",
            data={
                "nombre": "Juan Pérez",
                "email": "juan@example.com",
                "telefono": "12345678",
                "mensaje": "Consulta de prueba",
                "g-recaptcha-response": "valid_token"
            }
        )
        assert response.status_code == 200
        assert "Gracias por contactarte" in response.text
    finally:
        settings.RECAPTCHA_SECRET_KEY = original_secret


@patch("urllib.request.urlopen")
def test_contact_form_submission_recaptcha_failure(mock_urlopen, client: TestClient):
    # Mocking failed reCAPTCHA verification
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"success": false}'
    mock_response.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_response

    original_secret = settings.RECAPTCHA_SECRET_KEY
    settings.RECAPTCHA_SECRET_KEY = "real_secret_key"
    try:
        response = client.post(
            "/contacto",
            data={
                "nombre": "Juan Pérez",
                "email": "juan@example.com",
                "telefono": "12345678",
                "mensaje": "Consulta de prueba",
                "g-recaptcha-response": "invalid_token"
            }
        )
        assert response.status_code == 200
        assert "Error de verificación de seguridad" in response.text
    finally:
        settings.RECAPTCHA_SECRET_KEY = original_secret


@patch("urllib.request.urlopen")
def test_contact_form_submission_recaptcha_exception(mock_urlopen, client: TestClient):
    # Mocking a network exception during reCAPTCHA verification
    mock_urlopen.side_effect = Exception("Connection error")

    original_secret = settings.RECAPTCHA_SECRET_KEY
    settings.RECAPTCHA_SECRET_KEY = "real_secret_key"
    try:
        response = client.post(
            "/contacto",
            data={
                "nombre": "Juan Pérez",
                "email": "juan@example.com",
                "telefono": "12345678",
                "mensaje": "Consulta de prueba",
                "g-recaptcha-response": "some_token"
            }
        )
        assert response.status_code == 200
        assert "Error de verificación de seguridad" in response.text
    finally:
        settings.RECAPTCHA_SECRET_KEY = original_secret
