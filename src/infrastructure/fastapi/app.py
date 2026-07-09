from datetime import datetime
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET
from xml.dom import minidom

import yaml
from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import RequestResponseEndpoint


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Datamaq SSR")

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
        "script-src 'self' 'unsafe-inline' https://code.jquery.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://www.google.com/recaptcha/ https://www.gstatic.com/recaptcha/; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net https://default.contactopuro.com https://cdnjs.cloudflare.com; "
        "font-src 'self' https://fonts.gstatic.com https://default.contactopuro.com; "
        "img-src 'self' data: https://default.contactopuro.com; "
        "frame-src 'self' https://www.google.com/recaptcha/ https://recaptcha.google.com/;"
    )
    response.headers["Content-Security-Policy"] = csp
    
    # Cabeceras de seguridad adicionales
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    
    return response

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

CUSTOM_DIR = STATIC_DIR / "custom"
if CUSTOM_DIR.exists():
    app.mount("/custom", StaticFiles(directory=str(CUSTOM_DIR)), name="custom")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

DATA_FILE = BASE_DIR / "data" / "site_data.yml"


def _load_site_data() -> dict[str, Any]:
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {"categories": [], "carousel_slides": []}
    return {"categories": [], "carousel_slides": []}


SITE_DATA: dict[str, Any] = _load_site_data()


def _get_category_slugs() -> set[str]:
    return {cat["slug"] for cat in SITE_DATA.get("categories", [])}


def _common_context() -> dict[str, Any]:
    return {
        "categories": SITE_DATA.get("categories", []),
        "carousel_slides": SITE_DATA.get("carousel_slides", []),
        "current_year": datetime.now().year,
    }


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = _common_context()
    context.update({
        "title": "EITEC - Accesorios y Repuestos para Artefactos a Gas (ex EITAR)",
        "description": "Fábrica cooperativa de accesorios para artefactos a gas en Bernal, Argentina. Válvulas de seguridad, termostatos y quemadores de la línea ex EITAR.",
        "canonical_url": "https://www.eitec.coop.ar/",
    })
    return templates.TemplateResponse(request, "index.html", context)


@app.get("/contactanos")
async def contact_page():
    return RedirectResponse(url="/", status_code=307)


@app.get("/categoria/{slug}", response_class=HTMLResponse)
async def category(request: Request, slug: str):
    if slug not in _get_category_slugs():
        return RedirectResponse(url="/", status_code=307)
    
    context = _common_context()
    # Buscar la categoría activa
    active_cat = next((cat for cat in SITE_DATA.get("categories", []) if cat["slug"] == slug), None)
    
    if not active_cat:
        return RedirectResponse(url="/", status_code=307)
        
    context.update({
        "active_category": active_cat,
        "title": f"{active_cat['name']} - Repuestos EITAR | EITEC",
        "description": f"Fabricación y provisión de {active_cat['name']} de seguridad para artefactos a gas. Componentes originales y homologados por EITEC (ex EITAR) en Argentina.",
        "canonical_url": f"https://www.eitec.coop.ar/categoria/{slug}",
    })
    return templates.TemplateResponse(request, "index.html", context)


@app.post("/buscar")
async def search(busqueda: str = Form("")):
    query = busqueda.strip().lower()
    if not query:
        return RedirectResponse(url="/", status_code=307)

    for cat in SITE_DATA.get("categories", []):
        if query in cat["name"].lower():
            return RedirectResponse(url=f"/categoria/{cat['slug']}", status_code=307)

    return RedirectResponse(url="/", status_code=307)


@app.post("/contacto", response_class=HTMLResponse)
async def contact(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(...),
    mensaje: str = Form(""),
):
    # TODO: agregar envío de email o persistencia real.
    # Por ahora solo confirmamos recepción.
    context = _common_context()
    context.update(
        {
            "title": "Mensaje enviado - EITEC",
            "description": "Formulario de contacto de EITEC Cooperativa Bernal. Contactate por repuestos de gas EITAR.",
            "canonical_url": "https://www.eitec.coop.ar/",
            "noindex": True,
            "message": "Gracias por contactarte. Te responderemos a la brevedad.",
        }
    )
    return templates.TemplateResponse(request, "index.html", context)


@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots_txt():
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /buscar\n"
        "Disallow: /health\n"
        "Sitemap: https://www.eitec.coop.ar/sitemap.xml\n"
    )
    return PlainTextResponse(content=content)


@app.get("/sitemap.xml")
async def sitemap_xml():
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # Home
    url_el = ET.SubElement(urlset, "url")
    loc_el = ET.SubElement(url_el, "loc")
    loc_el.text = "https://www.eitec.coop.ar/"
    changefreq_el = ET.SubElement(url_el, "changefreq")
    changefreq_el.text = "weekly"
    priority_el = ET.SubElement(url_el, "priority")
    priority_el.text = "1.0"
    
    # Categorias
    for cat in SITE_DATA.get("categories", []):
        url_el = ET.SubElement(urlset, "url")
        loc_el = ET.SubElement(url_el, "loc")
        loc_el.text = f"https://www.eitec.coop.ar/categoria/{cat['slug']}"
        changefreq_el = ET.SubElement(url_el, "changefreq")
        changefreq_el.text = "monthly"
        priority_el = ET.SubElement(url_el, "priority")
        priority_el.text = "0.8"
        
    xml_str = ET.tostring(urlset, encoding="utf-8")
    parsed_xml = minidom.parseString(xml_str)
    pretty_xml = parsed_xml.toprettyxml(indent="  ", encoding="utf-8")
    
    return Response(content=pretty_xml, media_type="application/xml")


@app.get("/health")
async def health():
    return {"status": "ok"}
