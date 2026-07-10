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
def test_chatwoot_notifier_success(mock_post):
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 201
    mock_response.text = '{"status":"success"}'
    mock_post.return_value = mock_response

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
        
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert args[0] == "https://chatwoot.eitec.com.ar/api/v1/accounts/1/contacts"
        assert kwargs["headers"]["api_access_token"] == "test_token"
        assert kwargs["json"]["name"] == "Test User"
        assert kwargs["json"]["phone_number"] == "+12345678"
    finally:
        settings.CHATWOOT_API_TOKEN = original_token


@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
def test_chatwoot_notifier_failure(mock_post):
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
        
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert args[0] == "https://chatwoot.eitec.com.ar/api/v1/accounts/1/contacts"
    finally:
        settings.CHATWOOT_API_TOKEN = original_token


@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
def test_chatwoot_notifier_exception(mock_post):
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
        
        mock_post.assert_called_once()
    finally:
        settings.CHATWOOT_API_TOKEN = original_token
