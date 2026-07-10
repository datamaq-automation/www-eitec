import asyncio
import httpx
from unittest.mock import patch, AsyncMock, MagicMock
from src.domain.lead import Lead
from src.domain.catalog import CatalogRepository
from src.infrastructure.services.chatwoot_lead_notifier import ChatwootLeadNotifier
from src.infrastructure.config import settings

def test_chatwoot_notifier_no_token():
    # If no token is set, it should exit early
    original_token = settings.CHATWOOT_API_TOKEN
    settings.CHATWOOT_API_TOKEN = ""
    try:
        notifier = ChatwootLeadNotifier()
        lead = Lead(nombre="Test", email="test@example.com", telefono="12345678", mensaje="Hola")
        
        with patch("httpx.AsyncClient.post") as mock_post:
            asyncio.run(notifier.notify(lead))
            mock_post.assert_not_called()
    finally:
        settings.CHATWOOT_API_TOKEN = original_token


@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
@patch("httpx.AsyncClient.get", new_callable=AsyncMock)
def test_chatwoot_notifier_success(mock_get, mock_post):
    # Mock de búsqueda (GET): no encuentra contacto
    mock_get_response = MagicMock(spec=httpx.Response)
    mock_get_response.status_code = 200
    mock_get_response.json.return_value = {"payload": []}
    mock_get.return_value = mock_get_response

    # Mocks de creación (POST):
    # 1. Crear contacto: retorna contact id 123
    mock_post_contact = MagicMock(spec=httpx.Response)
    mock_post_contact.status_code = 201
    mock_post_contact.json.return_value = {"payload": {"contact": {"id": 123}}}

    # 2. Crear conversación: retorna conversation id 456
    mock_post_conv = MagicMock(spec=httpx.Response)
    mock_post_conv.status_code = 201
    mock_post_conv.json.return_value = {"id": 456}

    # 3. Enviar mensaje: retorna 201
    mock_post_msg = MagicMock(spec=httpx.Response)
    mock_post_msg.status_code = 201
    mock_post_msg.json.return_value = {"id": 789}

    # Asignamos efectos secundarios para las llamadas secuenciales a post
    mock_post.side_effect = [mock_post_contact, mock_post_conv, mock_post_msg]

    original_token = settings.CHATWOOT_API_TOKEN
    settings.CHATWOOT_API_TOKEN = "test_token"
    
    mock_site_info = MagicMock()
    mock_site_info.chatwoot_api_url = "https://chatwoot.eitec.com.ar"
    mock_site_info.chatwoot_account_id = 1
    mock_site_info.chatwoot_inbox_id = 1
    
    mock_repo = MagicMock(spec=CatalogRepository)
    mock_repo.get_site_info.return_value = mock_site_info
    
    try:
        notifier = ChatwootLeadNotifier(repo=mock_repo)
        lead = Lead(nombre="Test User", email="test@example.com", telefono="12345678", mensaje="Hola", productos="Termostatos")
        asyncio.run(notifier.notify(lead))
        
        # Debe haber hecho 2 consultas GET (teléfono y email) y 3 llamadas POST
        assert mock_get.call_count == 2
        assert mock_post.call_count == 3
        
        # Validar primer POST (creación de contacto)
        first_call_args = mock_post.call_args_list[0]
        assert first_call_args[0][0] == "https://chatwoot.eitec.com.ar/api/v1/accounts/1/contacts"
        assert first_call_args[1]["json"]["name"] == "Test User"
        assert first_call_args[1]["json"]["phone_number"] == "+12345678"
        
        # Validar segundo POST (creación de conversación)
        second_call_args = mock_post.call_args_list[1]
        assert second_call_args[0][0] == "https://chatwoot.eitec.com.ar/api/v1/accounts/1/conversations"
        assert second_call_args[1]["json"]["contact_id"] == 123
        
        # Validar tercer POST (envío de mensaje)
        third_call_args = mock_post.call_args_list[2]
        assert third_call_args[0][0] == "https://chatwoot.eitec.com.ar/api/v1/accounts/1/conversations/456/messages"
        assert "Consulta Web de EITEC" in third_call_args[1]["json"]["content"]
    finally:
        settings.CHATWOOT_API_TOKEN = original_token


@patch("httpx.AsyncClient.put", new_callable=AsyncMock)
@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
@patch("httpx.AsyncClient.get", new_callable=AsyncMock)
def test_chatwoot_notifier_upsert_existing(mock_get, mock_post, mock_put):
    # Mock de búsqueda (GET): encuentra al contacto con ID 777
    mock_get_response = MagicMock(spec=httpx.Response)
    mock_get_response.status_code = 200
    mock_get_response.json.return_value = {"payload": [{"id": 777, "name": "Test User"}]}
    mock_get.return_value = mock_get_response

    # Mock de actualización (PUT): retorna 200
    mock_put_response = MagicMock(spec=httpx.Response)
    mock_put_response.status_code = 200
    mock_put.return_value = mock_put_response

    # Mocks de creación (POST):
    # 1. Crear conversación: retorna conversación id 888
    mock_post_conv = MagicMock(spec=httpx.Response)
    mock_post_conv.status_code = 201
    mock_post_conv.json.return_value = {"id": 888}

    # 2. Enviar mensaje: retorna 201
    mock_post_msg = MagicMock(spec=httpx.Response)
    mock_post_msg.status_code = 201
    mock_post_msg.json.return_value = {"id": 999}

    mock_post.side_effect = [mock_post_conv, mock_post_msg]

    original_token = settings.CHATWOOT_API_TOKEN
    settings.CHATWOOT_API_TOKEN = "test_token"
    
    mock_site_info = MagicMock()
    mock_site_info.chatwoot_api_url = "https://chatwoot.eitec.com.ar"
    mock_site_info.chatwoot_account_id = 1
    mock_site_info.chatwoot_inbox_id = 1
    
    mock_repo = MagicMock(spec=CatalogRepository)
    mock_repo.get_site_info.return_value = mock_site_info
    
    try:
        notifier = ChatwootLeadNotifier(repo=mock_repo)
        lead = Lead(nombre="Test User", email="test@example.com", telefono="12345678", mensaje="Hola")
        asyncio.run(notifier.notify(lead))
        
        # Debe buscar, luego actualizar (PUT), luego crear conversación (POST) y enviar mensaje (POST)
        mock_get.assert_called_once()
        mock_put.assert_called_once()
        assert mock_post.call_count == 2
        
        # Validar actualización (PUT)
        put_call_args = mock_put.call_args
        assert put_call_args[0][0] == "https://chatwoot.eitec.com.ar/api/v1/accounts/1/contacts/777"
        assert put_call_args[1]["json"]["name"] == "Test User"
    finally:
        settings.CHATWOOT_API_TOKEN = original_token


@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
@patch("httpx.AsyncClient.get", new_callable=AsyncMock)
def test_chatwoot_notifier_failure(mock_get, mock_post):
    mock_get_response = MagicMock(spec=httpx.Response)
    mock_get_response.status_code = 200
    mock_get_response.json.return_value = {"payload": []}
    mock_get.return_value = mock_get_response

    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 404
    mock_response.text = '{"error":"Account not found"}'
    mock_post.return_value = mock_response

    original_token = settings.CHATWOOT_API_TOKEN
    settings.CHATWOOT_API_TOKEN = "test_token"
    
    mock_site_info = MagicMock()
    mock_site_info.chatwoot_api_url = "https://chatwoot.eitec.com.ar/api/v1"
    mock_site_info.chatwoot_account_id = 1
    mock_site_info.chatwoot_inbox_id = 1
    
    mock_repo = MagicMock(spec=CatalogRepository)
    mock_repo.get_site_info.return_value = mock_site_info
    
    try:
        notifier = ChatwootLeadNotifier(repo=mock_repo)
        lead = Lead(nombre="Test User", email="test@example.com", telefono="12345678", mensaje="Hola")
        asyncio.run(notifier.notify(lead))
        
        assert mock_get.call_count == 2
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert args[0] == "https://chatwoot.eitec.com.ar/api/v1/accounts/1/contacts"
    finally:
        settings.CHATWOOT_API_TOKEN = original_token


@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
@patch("httpx.AsyncClient.get", new_callable=AsyncMock)
def test_chatwoot_notifier_exception(mock_get, mock_post):
    mock_get_response = MagicMock(spec=httpx.Response)
    mock_get_response.status_code = 200
    mock_get_response.json.return_value = {"payload": []}
    mock_get.return_value = mock_get_response
    
    mock_post.side_effect = httpx.RequestError("Connection timeout")

    original_token = settings.CHATWOOT_API_TOKEN
    settings.CHATWOOT_API_TOKEN = "test_token"
    
    mock_site_info = MagicMock()
    mock_site_info.chatwoot_api_url = "https://chatwoot.eitec.com.ar"
    mock_site_info.chatwoot_account_id = 1
    mock_site_info.chatwoot_inbox_id = 1
    
    mock_repo = MagicMock(spec=CatalogRepository)
    mock_repo.get_site_info.return_value = mock_site_info
    
    try:
        notifier = ChatwootLeadNotifier(repo=mock_repo)
        lead = Lead(nombre="Test User", email="test@example.com", telefono="12345678", mensaje="Hola")
        asyncio.run(notifier.notify(lead))
        
        assert mock_get.call_count == 2
        mock_post.assert_called_once()
    finally:
        settings.CHATWOOT_API_TOKEN = original_token
