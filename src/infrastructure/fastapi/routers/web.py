import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Any
from fastapi import APIRouter, Request, Depends, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse, FileResponse

from src.domain.catalog import CatalogRepository
from src.infrastructure.fastapi.dependencies import (
    templates,
    get_catalog_repository,
    get_common_context,
    STATIC_DIR,
)

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    context: dict[str, Any] = Depends(get_common_context),
) -> HTMLResponse:
    context.update({
        # B2B-REFACTOR: se priorizan keywords de búsqueda orgánica por marca histórica EITAR
        "title": "EITEC - Repuestos y Válvulas EITAR para Artefactos a Gas | Cooperativa",
        "description": "Fábrica cooperativa EITEC, continuadora de EITAR. Repuestos EITAR, válvulas de seguridad, termostatos y termocuplas para artefactos a gas en Bernal, Argentina.",
        "canonical_url": "https://www.eitec.coop.ar/",
    })
    return templates.TemplateResponse(request, "index.html", context)


@router.get("/carrito", response_class=HTMLResponse)
async def view_cart(
    request: Request,
    context: dict[str, Any] = Depends(get_common_context),
) -> HTMLResponse:
    context.update({
        "title": "Mi Solicitud de Cotización - EITEC",
        "description": "Revisa los productos seleccionados para tu solicitud de cotización mayorista a la cooperativa EITEC.",
        "canonical_url": "https://www.eitec.coop.ar/carrito",
    })
    return templates.TemplateResponse(request, "carrito.html", context)


@router.get("/categoria/{slug}", response_class=HTMLResponse)
async def category(
    request: Request,
    slug: str,
    repo: CatalogRepository = Depends(get_catalog_repository),
    context: dict[str, Any] = Depends(get_common_context),
) -> Response:
    active_cat = repo.get_category_by_slug(slug)
    if not active_cat:
        context.update({
            "title": "Categoría no encontrada - EITEC",
            "description": "La categoría de repuestos o accesorios para artefactos a gas solicitada no existe.",
            "message": "La categoría solicitada no existe o ha sido movida.",
            "message_type": "danger",
            "canonical_url": "https://www.eitec.coop.ar/",
        })
        return templates.TemplateResponse(request, "index.html", context, status_code=404)
        
    context.update({
        "active_category": active_cat,
        "title": f"{active_cat.name} - Repuestos EITAR | EITEC",
        "description": f"Fabricación y provisión de {active_cat.name} de seguridad para artefactos a gas. Componentes originales y homologados por EITEC (ex EITAR) en Argentina.",
        "canonical_url": f"https://www.eitec.coop.ar/categoria/{slug}",
    })
    return templates.TemplateResponse(request, "index.html", context)


@router.get("/buscar")
async def search_get(
    s: str = "",
    repo: CatalogRepository = Depends(get_catalog_repository),
) -> RedirectResponse:
    query = s.strip().lower()
    if not query:
        return RedirectResponse(url="/", status_code=301)

    results = repo.search_categories(query)
    if results:
        return RedirectResponse(url=f"/categoria/{results[0].slug}", status_code=301)

    return RedirectResponse(url="/", status_code=302)


@router.post("/buscar")
async def search(
    busqueda: str = Form(""),
    repo: CatalogRepository = Depends(get_catalog_repository),
) -> RedirectResponse:
    query = busqueda.strip().lower()
    if not query:
        return RedirectResponse(url="/", status_code=307)

    results = repo.search_categories(query)
    if results:
        return RedirectResponse(url=f"/categoria/{results[0].slug}", status_code=307)

    return RedirectResponse(url="/", status_code=307)


@router.get("/robots.txt", response_class=PlainTextResponse)
async def robots_txt() -> PlainTextResponse:
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /buscar\n"
        "Disallow: /health\n"
        "Sitemap: https://www.eitec.coop.ar/sitemap.xml\n"
    )
    return PlainTextResponse(content=content)


@router.get("/sitemap.xml")
async def sitemap_xml(
    repo: CatalogRepository = Depends(get_catalog_repository),
) -> Response:
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
    for cat in repo.get_categories():
        url_el = ET.SubElement(urlset, "url")
        loc_el = ET.SubElement(url_el, "loc")
        loc_el.text = f"https://www.eitec.coop.ar/categoria/{cat.slug}"
        changefreq_el = ET.SubElement(url_el, "changefreq")
        changefreq_el.text = "monthly"
        priority_el = ET.SubElement(url_el, "priority")
        priority_el.text = "0.8"
        
    xml_str = ET.tostring(urlset, encoding="utf-8")
    parsed_xml = minidom.parseString(xml_str)
    pretty_xml = parsed_xml.toprettyxml(indent="  ", encoding="utf-8")
    
    return Response(content=pretty_xml, media_type="application/xml")


@router.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse(STATIC_DIR / "custom" / "logo.png")
