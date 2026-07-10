# AGENTS.md — Guía para agentes de código

Este documento resume la arquitectura, el stack tecnológico, la organización del código, las convenciones de desarrollo y las consideraciones de seguridad del proyecto. Está escrito en español porque ese es el idioma que se usa en los comentarios, plantillas y datos del proyecto.

> **Nota:** Al momento de crear este archivo, `AGENTS.md` estaba vacío. Esta guía se redactó a partir del contenido real del repositorio, sin suposiciones.

---

## 1. Visión general del proyecto

Este es un sitio web estático renderizado en servidor (SSR) para la cooperativa **EITEC** (fábrica de accesorios para artefactos a gas). No es una aplicación con base de datos ni API REST compleja; se trata de una página de presentación corporativa con:

- Una página de inicio (`/`).
- Un carrusel de productos/servicios.
- Una grilla de categorías de productos.
- Un formulario de contacto (solo confirma recepción; no envía ni persiste datos aún).
- Una búsqueda simple de categorías.

El contenido editable (categorías y slides del carrusel) se carga desde un archivo YAML (`data/site_data.yml`), lo que permite modificar la información del sitio sin tocar código.

---

## 2. Stack tecnológico

### Backend

- **Python 3.12.3** (según `venv/pyvenv.cfg`).
- **FastAPI 0.138.0** como framework web.
- **Uvicorn 0.49.0** como servidor ASGI.
- **Jinja2 3.1.6** para plantillas HTML.
- **PyYAML 6.0.2** para leer la configuración del sitio.
- **Pydantic 2.13.4** (dependencia de FastAPI).

### Frontend

- **Bootstrap 5.0.0** (CSS y JS desde CDN).
- **jQuery 3.6.0** desde CDN.
- **Font Awesome**, **lightGallery**, **tiny-slider**, **Hamburgers** desde CDNs externos.
- Hoja de estilos propia en `static/css/styles.css`.
- Scripts propios en `static/js/main.js`.

### Otros

- **Google reCAPTCHA v2** incluido en el formulario de contacto (solo del lado cliente; el servidor no valida el token).
- No hay framework de JavaScript compilado (React, Vue, etc.) ni `package.json`.

---

## 3. Estructura del proyecto

```text
www-eitec/
├── data/
│   └── site_data.yml          # Datos de categorías y carrusel
├── src/
│   └── infrastructure/
│       └── fastapi/
│           ├── __init__.py
│           └── app.py         # Aplicación FastAPI (único módulo Python)
├── static/
│   ├── css/styles.css         # Estilos propios
│   ├── custom/
│   │   ├── favicon/           # Vacío al momento de la revisión
│   │   └── logo.png           # Logo usado en header, favicon y meta tags
│   ├── img/                   # Imágenes de categorías y carrusel
│   └── js/main.js             # Scripts propios
├── templates/
│   ├── base.html              # Layout base
│   ├── index.html             # Página de inicio
│   └── partials/              # Fragmentos reutilizables
│       ├── carousel.html
│       ├── categories_grid.html
│       ├── contact_form.html
│       ├── footer.html
│       ├── head.html
│       ├── header.html
│       ├── scripts.html
│       └── search_overlay.html
├── .gitignore                 # Ignora venv/, .env y __pycache__/
├── .vscode/settings.json      # Configura intérprete de venv y PYTHONPATH extra
├── requirements.txt           # Dependencias de Python
└── run.sh                     # Script para levantar Uvicorn en desarrollo
```

### Observaciones importantes

- **No existe** `pyproject.toml`, `setup.py`, `setup.cfg`, `package.json`, `Cargo.toml`, `tox.ini`, `pytest.ini`, `Makefile`, `Dockerfile`, ni configuración de CI/CD.
- **No hay tests** automatizados (ni `tests/`, ni `*_test.py`, ni configuración de pytest).
- El único módulo Python con lógica de negocio es `src/infrastructure/fastapi/app.py`.

---

## 4. Arquitectura y funcionamiento

### Aplicación FastAPI

- El punto de entrada es `src/infrastructure/fastapi/app.py`.
- Se crea una instancia `app = FastAPI(title="Datamaq SSR")`.
- Se montan dos directorios como archivos estáticos:
  - `/static` → `static/`
  - `/custom` → `static/custom/`
- Se configura Jinja2 con `templates = Jinja2Templates(directory="templates")`.
- Los datos del sitio se cargan una sola vez al importar el módulo, desde `data/site_data.yml`.

### Rutas definidas

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Página de inicio. Renderiza `index.html` con categorías, carrusel y año actual. |
| GET | `/contactanos` | Redirección temporal (307) a `/`. |
| GET | `/categoria/{slug}` | Verifica que el slug exista; de momento también redirige a `/`. |
| POST | `/buscar` | Recibe `busqueda`, busca coincidencias en nombres de categoría y redirige a `/categoria/{slug}` o `/`. |
| POST | `/contacto` | Recibe `nombre`, `email`, `telefono` y `mensaje`. Muestra mensaje de confirmación pero no envía/persiste datos. |
| GET | `/health` | Endpoint de salud: devuelve `{"status": "ok"}`. |

### Contexto común de plantillas

La función `_common_context()` inyecta en todas las renderizaciones:

- `categories`: lista de categorías desde YAML.
- `carousel_slides`: lista de slides desde YAML.
- `current_year`: año actual (usado en el copyright del footer).

### Datos (`data/site_data.yml`)

El archivo tiene dos claves principales:

- `categories`: cada categoría tiene `name`, `slug` e `image`.
- `carousel_slides`: cada slide tiene `title`, `image` y `link`.

Cambiar este archivo actualiza el sitio sin reiniciar el servidor en modo `--reload`.

---

## 5. Cómo construir y ejecutar

### Requisitos previos

- Python 3.9 o superior (recomendado 3.12.3, el que usa el entorno actual).
- `pip` disponible.

### Pasos

```bash
# 1. Crear entorno virtual (si no existe)
python3 -m venv venv

# 2. Activar entorno virtual
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar el servidor de desarrollo
./run.sh
```

### Qué hace `run.sh`

- Detecta el directorio del proyecto.
- Activa `venv/` si existe; si no, intenta con `.venv/`.
- Agrega `src/` a `PYTHONPATH` para que el import `infrastructure.fastapi.app` funcione.
- Ejecuta Uvicorn con recarga automática:

```bash
uvicorn infrastructure.fastapi.app:app --host 0.0.0.0 --port 8000 --reload
```

La aplicación queda disponible en `http://localhost:8000`.

---

## 6. Instrucciones de testing

No hay tests automatizados. Para verificar el funcionamiento manualmente:

```bash
# Verificar que el servidor responde
curl http://localhost:8000/health

# Ver la página de inicio
curl http://localhost:8000/

# Probar la búsqueda
curl -X POST -d "busqueda=pilotos" http://localhost:8000/buscar

# Probar el formulario de contacto
curl -X POST \
  -d "nombre=Juan Perez" \
  -d "email=juan@example.com" \
  -d "telefono=12345678" \
  -d "mensaje=Consulta de prueba" \
  http://localhost:8000/contacto
```

### Verificaciones visuales recomendadas

- Carga correcta de Bootstrap y otros recursos CDN.
- Menú hamburguesa en móviles.
- Overlay de búsqueda.
- Carrusel de inicio.
- Renderizado de categorías desde YAML.
- Footer con año actual.

---

## 7. Convenciones de código

### Python

- Se usa **snake_case** para funciones y variables (`_load_site_data`, `_common_context`, `busqueda`).
- Los nombres de variables y endpoints están en **español** (`categoria`, `contacto`, `buscar`).
- Las constantes de configuración se definen a nivel de módulo (`BASE_DIR`, `TEMPLATES_DIR`, etc.).
- Los datos del sitio se cargan en una constante global `SITE_DATA` al importar el módulo.
- Los endpoints son funciones `async`.
- Se usa anotación de tipos básica (`dict[str, Any]`).

### Plantillas Jinja2

- `base.html` define el layout con bloques `content`, `head_extra` y `scripts_extra`.
- Las páginas extienden `base.html`.
- Los fragmentos reutilizables están en `templates/partials/`.
- Las variables esperadas en el contexto son `categories`, `carousel_slides`, `current_year`, `title`, `description` y `message`.

### CSS

- El archivo `static/css/styles.css` es un CSS plano, sin preprocesadores.
- Existe una mezcla de clases en español e inglés.
- Algunas reglas hacen referencia a recursos que no existen en el repositorio, por ejemplo `url(../files/logo.png)` en el footer, mientras que el logo real está en `static/custom/logo.png`.

---

## 8. Consideraciones de seguridad

- **reCAPTCHA no validado en el servidor:** el formulario incluye una clave de sitio (`data-sitekey`) y un callback de JavaScript, pero `app.py` no verifica el token con Google. Cualquier petición POST a `/contacto` será aceptada.
- **Sin validación/sanitización de datos:** el endpoint `/contacto` recibe los campos y solo los muestra de vuelta en la plantilla. No hay sanitización de HTML, validación de longitudes ni de formato en el backend.
- **Sin CSRF token:** el formulario no incluye protección contra CSRF.
- **Sin rate limiting:** no hay límite de peticiones, lo que puede facilitar spam o fuerza bruta.
- **Sin persistencia ni envío real de emails:** el TODO en `app.py` indica que falta implementar el envío/persistencia. Mientras tanto, los datos del contacto se pierden.
- **Sin variables de entorno para secretos:** no existe `.env` ni configuración de secretos; la clave de reCAPTCHA está hardcodeada en la plantilla.
- **Archivos estáticos expuestos:** todo el contenido de `static/` y `static/custom/` es accesible públicamente.
- **Modo desarrollo:** `run.sh` usa `--reload`, que nunca debe usarse en producción.

### Recomendaciones antes de publicar

1. Implementar la validación del token de reCAPTCHA en el backend.
2. Validar y sanitizar todos los campos del formulario de contacto.
3. Agregar un mecanismo de envío de correos o persistencia segura.
4. Usar variables de entorno para secretos y configuraciones sensibles.
5. Ejecutar Uvicorn sin `--reload` y detrás de un reverse proxy (por ejemplo, Nginx).
6. Considerar agregar headers de seguridad básicos (HSTS, CSP, X-Frame-Options, etc.).

---

## 9. Despliegue

Actualmente el proyecto no tiene configuración de despliegue automatizado. Para producción, una opción mínima sería:

```bash
source venv/bin/activate
export PYTHONPATH="/ruta/al/proyecto/src:${PYTHONPATH}"
uvicorn infrastructure.fastapi.app:app --host 0.0.0.0 --port 8000 --workers 4
```

Luego exponer el puerto a través de un reverse proxy con HTTPS.

---

## 10. Configuración del entorno de desarrollo

El archivo `.vscode/settings.json` indica:

- Intérprete por defecto: `${workspaceFolder}/venv/bin/python`.
- `python.analysis.extraPaths` incluye `${workspaceFolder}/src`.

Esto permite que VS Code resuelva correctamente el import `infrastructure.fastapi.app`.

---

## 11. Resumen de archivos clave

| Archivo | Propósito |
|---------|-----------|
| `requirements.txt` | Dependencias de Python. |
| `run.sh` | Script de arranque para desarrollo. |
| `src/infrastructure/fastapi/app.py` | Aplicación FastAPI, rutas y lógica de renderizado. |
| `data/site_data.yml` | Contenido editable del sitio. |
| `templates/` | Plantillas Jinja2. |
| `static/` | CSS, JS, imágenes y logo. |
| `.vscode/settings.json` | Configuración del entorno de trabajo en VS Code. |

---

*Última actualización: 2026-07-03*
