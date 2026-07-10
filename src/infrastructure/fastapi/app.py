from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import RequestResponseEndpoint

from src.infrastructure.fastapi.dependencies import (
    STATIC_DIR,
    templates,
    get_common_context,
    get_catalog_repository,
)
from src.infrastructure.fastapi.routers.web import router as web_router
from src.infrastructure.fastapi.routers.contact import router as contact_router

from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI(title="Datamaq SSR")
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Middleware para inyectar cabeceras de seguridad (HSTS, CSP, etc.)
@app.middleware("http")
async def add_security_headers(
    request: Request, call_next: RequestResponseEndpoint
) -> Response:
    response = await call_next(request)
    # HSTS (Strict-Transport-Security)
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
    
    # CSP (Content-Security-Policy)
    csp = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://code.jquery.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://static.cloudflareinsights.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net https://default.contactopuro.com https://cdnjs.cloudflare.com; "
        "font-src 'self' https://fonts.gstatic.com https://default.contactopuro.com https://cdnjs.cloudflare.com; "
        "img-src 'self' data: https://default.contactopuro.com; "
        "connect-src 'self' https://cdn.jsdelivr.net; "
        "frame-src 'self';"
    )
    response.headers["Content-Security-Policy"] = csp
    
    # Cabeceras de seguridad adicionales
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    
    return response

# Montar archivos estáticos
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

CUSTOM_DIR = STATIC_DIR / "custom"
if CUSTOM_DIR.exists():
    app.mount("/custom", StaticFiles(directory=str(CUSTOM_DIR)), name="custom")

# Registrar Routers
app.include_router(web_router)
app.include_router(contact_router)

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: Exception) -> Response:
    repo = get_catalog_repository()
    context = get_common_context(repo=repo)
    context.update({
        "title": "Página no encontrada - EITEC",
        "description": "La página que buscas no existe o ha sido movida.",
        "canonical_url": "https://www.eitec.coop.ar/",
        "noindex": True,
    })
    return templates.TemplateResponse(request, "404.html", context, status_code=404)
