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
from src.infrastructure.services.pdf_service import create_pdf_bytes

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
        "canonical_url": f"{context['base_url']}/",
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
        "canonical_url": f"{context['base_url']}/carrito",
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
            "canonical_url": f"{context['base_url']}/",
        })
        return templates.TemplateResponse(request, "index.html", context, status_code=404)
        
    context.update({
        "active_category": active_cat,
        "title": f"{active_cat.name} - Repuestos EITAR | EITEC",
        "description": f"Fabricación y provisión de {active_cat.name} de seguridad para artefactos a gas. Componentes originales y homologados por EITEC (ex EITAR) en Argentina.",
        "canonical_url": f"{context['base_url']}/categoria/{slug}",
    })
    return templates.TemplateResponse(request, "index.html", context)


@router.get("/politica-de-privacidad", response_class=HTMLResponse)
async def privacy_policy(
    request: Request,
    context: dict[str, Any] = Depends(get_common_context),
) -> HTMLResponse:
    context.update({
        "title": "Política de Privacidad - EITEC",
        "description": "Política de privacidad y protección de datos personales de EITEC Cooperativa de Trabajo.",
        "canonical_url": f"{context['base_url']}/politica-de-privacidad",
    })
    return templates.TemplateResponse(request, "politica_privacidad.html", context)


@router.get("/terminos-y-condiciones", response_class=HTMLResponse)
async def terms_and_conditions(
    request: Request,
    context: dict[str, Any] = Depends(get_common_context),
) -> HTMLResponse:
    context.update({
        "title": "Términos y Condiciones de Uso - EITEC",
        "description": "Términos y condiciones de uso del sitio web oficial de la cooperativa metalúrgica EITEC.",
        "canonical_url": f"{context['base_url']}/terminos-y-condiciones",
    })
    return templates.TemplateResponse(request, "terminos_condiciones.html", context)


@router.get("/gracias", response_class=HTMLResponse)
async def thanks_page(
    request: Request,
    context: dict[str, Any] = Depends(get_common_context),
) -> HTMLResponse:
    context.update({
        "title": "¡Gracias por contactarte! - EITEC",
        "description": "Tu mensaje ha sido enviado con éxito a la cooperativa EITEC. Nos comunicaremos a la brevedad.",
        "canonical_url": f"{context['base_url']}/gracias",
        "noindex": True,
    })
    return templates.TemplateResponse(request, "gracias.html", context)


@router.get("/blog", response_class=HTMLResponse)
async def blog_list(
    request: Request,
    repo: CatalogRepository = Depends(get_catalog_repository),
    context: dict[str, Any] = Depends(get_common_context),
) -> Response:
    site_info = repo.get_site_info()
    if not site_info.enable_blog:
        context.update({
            "title": "Página no encontrada - EITEC",
            "description": "La página que buscas no existe o ha sido movida.",
            "canonical_url": f"{context['base_url']}/",
            "noindex": True,
        })
        return templates.TemplateResponse(request, "404.html", context, status_code=404)
        
    posts = repo.get_blog_posts()
    context.update({
        "title": "Novedades y Fichas Técnicas - EITEC",
        "description": "Artículos de interés, novedades institucionales y fichas técnicas de la cooperativa metalúrgica EITEC ex EITAR.",
        "canonical_url": f"{context['base_url']}/blog",
        "blog_posts": posts,
    })
    return templates.TemplateResponse(request, "blog_list.html", context)


@router.get("/blog/{slug}", response_class=HTMLResponse)
async def blog_post(
    request: Request,
    slug: str,
    repo: CatalogRepository = Depends(get_catalog_repository),
    context: dict[str, Any] = Depends(get_common_context),
) -> Response:
    site_info = repo.get_site_info()
    if not site_info.enable_blog:
        context.update({
            "title": "Página no encontrada - EITEC",
            "description": "La página que buscas no existe o ha sido movida.",
            "canonical_url": f"{context['base_url']}/",
            "noindex": True,
        })
        return templates.TemplateResponse(request, "404.html", context, status_code=404)

    post = repo.get_blog_post_by_slug(slug)
    if not post:
        context.update({
            "title": "Artículo no encontrado - EITEC",
            "description": "El artículo o ficha técnica solicitado no existe.",
            "canonical_url": f"{context['base_url']}/blog",
            "noindex": True,
        })
        return templates.TemplateResponse(request, "404.html", context, status_code=404)

    context.update({
        "post": post,
        "title": f"{post.title} - EITEC",
        "description": post.summary,
        "canonical_url": f"{context['base_url']}/blog/{slug}",
    })
    return templates.TemplateResponse(request, "blog_post.html", context)


@router.post("/cotizacion/pdf")
async def generate_pdf(
    nombre: str = Form(...),
    email: str = Form(""),
    telefono: str = Form(""),
    mensaje: str = Form(""),
    productos: str = Form(""),
    repo: CatalogRepository = Depends(get_catalog_repository),
) -> Response:
    site_info = repo.get_site_info()
    if not site_info.enable_pdf_generator:
        return Response(content="PDF generator is disabled", status_code=403)
        
    product_list = [p.strip() for p in productos.split(",") if p.strip()]
    if not product_list:
        return Response(content="No products selected", status_code=400)
        
    pdf_content = create_pdf_bytes(
        nombre=nombre,
        email=email,
        telefono=telefono,
        mensaje=mensaje,
        productos=product_list
    )
    
    filename = f"cotizacion_{nombre.lower().replace(' ', '_')}.pdf"
    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"'
    }
    return Response(content=pdf_content, media_type="application/pdf", headers=headers)




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
async def robots_txt(
    repo: CatalogRepository = Depends(get_catalog_repository),
) -> PlainTextResponse:
    site_info = repo.get_site_info()
    base_url = site_info.base_url.rstrip("/")
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /buscar\n"
        "Disallow: /health\n"
        f"Sitemap: {base_url}/sitemap.xml\n"
    )
    return PlainTextResponse(content=content)


@router.get("/sitemap.xml")
async def sitemap_xml(
    repo: CatalogRepository = Depends(get_catalog_repository),
) -> Response:
    site_info = repo.get_site_info()
    base_url = site_info.base_url.rstrip("/")
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # Home
    url_el = ET.SubElement(urlset, "url")
    loc_el = ET.SubElement(url_el, "loc")
    loc_el.text = f"{base_url}/"
    changefreq_el = ET.SubElement(url_el, "changefreq")
    changefreq_el.text = "weekly"
    priority_el = ET.SubElement(url_el, "priority")
    priority_el.text = "1.0"
    
    # Categorias
    for cat in repo.get_categories():
        url_el = ET.SubElement(urlset, "url")
        loc_el = ET.SubElement(url_el, "loc")
        loc_el.text = f"{base_url}/categoria/{cat.slug}"
        changefreq_el = ET.SubElement(url_el, "changefreq")
        changefreq_el.text = "monthly"
        priority_el = ET.SubElement(url_el, "priority")
        priority_el.text = "0.8"
        
    # Paginas Legales
    for path in ["politica-de-privacidad", "terminos-y-condiciones"]:
        url_el = ET.SubElement(urlset, "url")
        loc_el = ET.SubElement(url_el, "loc")
        loc_el.text = f"{base_url}/{path}"
        changefreq_el = ET.SubElement(url_el, "changefreq")
        changefreq_el.text = "yearly"
        priority_el = ET.SubElement(url_el, "priority")
        priority_el.text = "0.3"

    # Blog posts
    if site_info.enable_blog:
        url_el = ET.SubElement(urlset, "url")
        loc_el = ET.SubElement(url_el, "loc")
        loc_el.text = f"{base_url}/blog"
        changefreq_el = ET.SubElement(url_el, "changefreq")
        changefreq_el.text = "weekly"
        priority_el = ET.SubElement(url_el, "priority")
        priority_el.text = "0.7"

        for post in repo.get_blog_posts():
            url_el = ET.SubElement(urlset, "url")
            loc_el = ET.SubElement(url_el, "loc")
            loc_el.text = f"{base_url}/blog/{post.slug}"
            changefreq_el = ET.SubElement(url_el, "changefreq")
            changefreq_el.text = "monthly"
            priority_el = ET.SubElement(url_el, "priority")
            priority_el.text = "0.6"

        
    xml_str = ET.tostring(urlset, encoding="utf-8")
    parsed_xml = minidom.parseString(xml_str)
    pretty_xml = parsed_xml.toprettyxml(indent="  ", encoding="utf-8")
    
    return Response(content=pretty_xml, media_type="application/xml")


@router.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse(STATIC_DIR / "custom" / "logo.png")
