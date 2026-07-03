from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Datamaq SSR")

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
    context.update({"title": "EITEC - Fábrica de accesorios para Artefactos a Gas"})
    return templates.TemplateResponse(request, "index.html", context)


@app.get("/contactanos")
async def contact_page():
    return RedirectResponse(url="/", status_code=307)


@app.get("/categoria/{slug}")
async def category(slug: str):
    if slug not in _get_category_slugs():
        return RedirectResponse(url="/", status_code=307)
    return RedirectResponse(url="/", status_code=307)


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
            "message": "Gracias por contactarte. Te responderemos a la brevedad.",
        }
    )
    return templates.TemplateResponse(request, "index.html", context)


@app.get("/health")
async def health():
    return {"status": "ok"}
