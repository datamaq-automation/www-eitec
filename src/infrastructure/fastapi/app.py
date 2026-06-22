from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Datamaq SSR")

STATIC_DIR = BASE_DIR / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

CUSTOM_DIR = STATIC_DIR / "custom"
if CUSTOM_DIR.exists():
    app.mount("/custom", StaticFiles(directory=str(CUSTOM_DIR)), name="custom")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Starlette 0.21-0.27: request va primero, luego name, luego context
    return templates.TemplateResponse(
        request,           # <-- 1er arg: el objeto Request
        "index.html",      # <-- 2do arg: nombre del template
        {"title": "Inicio"}  # <-- 3er arg: contexto (sin repetir request)
    )

@app.get("/health")
async def health():
    return {"status": "ok"}