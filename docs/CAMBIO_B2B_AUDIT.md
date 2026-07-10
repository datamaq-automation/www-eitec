# AUDITORÍA B2B EITEC — Cambios necesarios post-entrevista con Marcelo

**Fecha:** 2026-07-09  
**Auditor:** Arquitecto de Software + Auditor SEO/UX  
**Contexto:** Se confirmó que EITEC es un negocio B2B mayorista (ferreteros, casas de sanitarios, mayoristas) sin intención de venta directa al público. EITAR es marca histórica muy buscada en reposición. El sitio actual tiene elementos de UI que contradicen este modelo (carrito de compras).

---

## Sección 1: Cambios de UI/UX (B2B)

### 1.1 Eliminar ícono de carrito del Header
- **Archivo:** `templates/partials/header.html`
- **Líneas afectadas:** 12-14
- **Código actual:**
  ```html
  <a href="/carrito" class="icon fa-solid fa-cart-shopping position-relative">
      <span id="cart-badge" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger d-none" style="font-size: 0.55rem; padding: 0.25em 0.4em;">0</span>
  </a>
  ```
- **Problema:** El ícono de carrito de compras sugiere e-commerce minorista. Contradice el modelo B2B confirmado (C7, C9).
- **Cambio requerido:** Eliminar el ícono de carrito y el badge del header. Conservar el buscador.
- **Prioridad:** CRÍTICA
- **Bloqueado por:** No.

### 1.2 Ajustar CTA de categoría de "Agregar a mi cotización" a "Solicitar cotización"
- **Archivo:** `templates/index.html`
- **Líneas afectadas:** 35-42
- **Código actual:** Botón dual: "Agregar a mi cotización" + "Consultar directo".
- **Problema:** El botón con ícono `fa-plus` y la lógica de "agregar" replican un carrito de compras. En B2B, un mayorista no "agrega al carrito"; solicita una cotización por volumen.
- **Cambio requerido:** Reemplazar el botón por un único CTA principal "Solicitar cotización" que navegue a `/carrito#contacto` o directamente a la sección de contacto. Eliminar la lógica de localStorage del botón de categoría.
- **Prioridad:** ALTA
- **Bloqueado por:** No.

### 1.3 Renombrar visualmente "Mi Cotización" a "Solicitud de Cotización Mayorista"
- **Archivo:** `templates/carrito.html`
- **Líneas afectadas:** 21-85
- **Problema:** Aunque el título ya dice "Solicitud de Cotización Mayorista", la ruta `/carrito` y el localStorage mantienen la semántica de carrito.
- **Cambio requerido:**
  - Renombrar ruta `/carrito` → `/cotizacion` con redirección 301 desde `/carrito` (DT2).
  - Revisar copy: "Productos Seleccionados" → "Productos a cotizar".
  - Mantener el formulario B2B intacto.
- **Prioridad:** ALTA
- **Bloqueado por:** DT2 (decisión de ruta).

### 1.4 Actualizar formulario de contacto general para orientación B2B
- **Archivo:** `templates/partials/contact_form.html`
- **Líneas afectadas:** 1-32
- **Problema actual:** El formulario pide "Nombre", no "Nombre / Razón Social"; el textarea dice "¿Querés dejarnos un comentario?", sin orientación a volumen o tipo de cliente.
- **Cambio requerido:**
  - Cambiar label de `nombre` a "Nombre / Razón Social".
  - Cambiar placeholder/label del textarea para inducir a indicar rubro o volumen: "Contanos qué productos necesitás y en qué cantidades".
  - Agregar campo opcional oculto o visible para "Rubro" (mayorista, ferretero, instalador) si se decide más adelante.
- **Prioridad:** MEDIA
- **Bloqueado por:** No.

### 1.5 Eliminar lógica de `localStorage` del cotizador
- **Archivo:** `static/js/modules/cart.js`
- **Líneas afectadas:** 1-138
- **Problema:** Mantiene estado de "carrito" en el navegador, genera badge en header (que se eliminará) y replica UX de e-commerce.
- **Cambio requerido:**
  - Opción A (mínima): eliminar `initCart()` de `main.js` y el badge.
  - Opción B (recomendada): reescribir `cart.js` como `quote.js` que solo maneje el formulario de `/cotizacion`, sin localStorage ni badge.
- **Prioridad:** ALTA
- **Bloqueado por:** DT1.

### 1.6 Revisar Footer (sin cambios críticos detectados)
- **Archivo:** `templates/partials/footer.html`
- **Estado actual:** No contiene ícono de carrito ni CTAs de compra. Solo enlaces a categorías, contacto y redes.
- **Cambio requerido:** Ninguno crítico. A futuro: agregar espacio para certificaciones (D5).
- **Prioridad:** BAJA
- **Bloqueado por:** D5.

---

## Sección 2: Cambios de SEO y Copy

### 2.1 Título y meta descripción de la Home
- **Archivo:** `src/infrastructure/fastapi/routers/web.py`
- **Líneas afectadas:** 21-25
- **Código actual:**
  ```python
  "title": "EITEC - Accesorios y Repuestos para Artefactos a Gas (ex EITAR)",
  "description": "Fábrica cooperativa de accesorios para artefactos a gas en Bernal, Argentina. Válvulas de seguridad, termostatos y quemadores de la línea ex EITAR.",
  ```
- **Cambio requerido:** Incluir palabras clave de búsqueda EITAR: "repuestos EITAR", "válvulas EITAR", "termocuplas EITAR". Mantener EITEC como marca principal.
- **Propuesta:**
  ```python
  "title": "EITEC - Repuestos y Válvulas EITAR para Artefactos a Gas | Cooperativa",
  "description": "Fábrica cooperativa EITEC, continuadora de EITAR. Repuestos EITAR, válvulas de seguridad, termostatos y termocuplas para artefactos a gas en Bernal, Argentina.",
  ```
- **Prioridad:** ALTA
- **Bloqueado por:** No.

### 2.2 H1 de la Home
- **Archivo:** `templates/index.html`
- **Línea afectada:** 69
- **Código actual:**
  ```html
  <h1 class="display-6 fw-bold text-primary mb-3">{{ site_info.intro_title }}</h1>
  ```
- **Problema:** El H1 es genérico ("EITEC Cooperativa de Trabajo"). No capitaliza la búsqueda de EITAR.
- **Cambio requerido:** H1 debe incluir "EITEC" + "EITAR" + palabra clave principal: "Repuestos EITAR y accesorios para artefactos a gas — EITEC Cooperativa".
- **Prioridad:** ALTA
- **Bloqueado por:** No.

### 2.3 Copy de introducción (`site_info.intro_text`)
- **Archivo:** `data/site_data.yml`
- **Líneas afectadas:** 50
- **Código actual:** ya incluye "línea EITAR".
- **Cambio requerido:** Reforzar con términos de búsqueda: "repuestos originales EITAR", "válvulas de seguridad EITAR", "termocuplas", "robinetes". Mantener natural.
- **Prioridad:** MEDIA
- **Bloqueado por:** No.

### 2.4 Títulos y descripciones de categorías
- **Archivo:** `src/infrastructure/fastapi/routers/web.py`
- **Líneas afectadas:** 55-57
- **Código actual:**
  ```python
  "title": f"{active_cat.name} - Repuestos EITAR | EITEC",
  "description": f"Fabricación y provisión de {active_cat.name} de seguridad para artefactos a gas. Componentes originales y homologados por EITEC (ex EITAR) en Argentina.",
  ```
- **Cambio requerido:** Mantener. Es correcto. A futuro, enriquecer con keywords específicas según D8.
- **Prioridad:** MEDIA
- **Bloqueado por:** D8.

### 2.5 Alt de imágenes de categorías
- **Archivo:** `templates/partials/categories_grid.html`
- **Línea afectada:** 7
- **Código actual:**
  ```html
  <img src="/static/img/{{ cat.image }}" alt="{{ cat.name }} - EITEC Cooperativa ex EITAR" ...>
  ```
- **Cambio requerido:** Mejorar alt con keyword EITAR cuando aplique: `"{{ cat.name }} - Repuestos EITAR originales | EITEC"`.
- **Prioridad:** MEDIA
- **Bloqueado por:** No.

### 2.6 Schema.org Organization
- **Archivo:** `templates/partials/schema.html`
- **Líneas afectadas:** 7-26
- **Cambio requerido:** Incluir "EITAR" como `alternateName` adicional. Actualizar `logo` a `.png` si se adopta el logo transparente.
- **Prioridad:** MEDIA
- **Bloqueado por:** D1 (decisión de logo definitivo).

### 2.7 Oportunidad: landing pages para búsquedas EITAR
- **Propuesta:** Crear páginas estáticas o rutas dinámicas para:
  - `/repuestos-eitar`
  - `/valvulas-eitar`
  - `/termocuplas-eitar`
- **Impacto:** Captura búsquedas de marca histórica con intención comercial.
- **Prioridad:** MEDIA
- **Bloqueado por:** DT3, D8.

---

## Sección 3: Cambios de Backend (FastAPI)

### 3.1 Eliminar o redirigir la ruta `/carrito`
- **Archivo:** `src/infrastructure/fastapi/routers/web.py`
- **Líneas afectadas:** 29-39
- **Código actual:**
  ```python
  @router.get("/carrito", response_class=HTMLResponse)
  async def view_cart(...)
  ```
- **Cambio requerido:**
  - Renombrar a `/cotizacion`.
  - Agregar redirección 301 desde `/carrito` a `/cotizacion` para no romper links/indexación.
- **Prioridad:** ALTA
- **Bloqueado por:** DT2.

### 3.2 Actualizar sitemap.xml
- **Archivo:** `src/infrastructure/fastapi/routers/web.py`
- **Líneas afectadas:** 90-118
- **Cambio requerido:** Si se renombra `/carrito` a `/cotizacion`, actualizar sitemap. No incluir `/carrito` (redirección).
- **Prioridad:** MEDIA
- **Bloqueado por:** DT2.

### 3.3 Endpoint de contacto B2B
- **Archivo:** `src/infrastructure/fastapi/routers/contact.py`
- **Estado actual:** El endpoint `/contacto` ya soporta `productos` como campo oculto. Funciona para el flujo B2B.
- **Cambio requerido:** Ninguno estructural. Considerar validación de campos B2B (nombre/razón social, teléfono) más robusta.
- **Prioridad:** BAJA
- **Bloqueado por:** No.

### 3.4 Esquemas Pydantic
- **Archivo:** `src/domain/lead.py`
- **Estado actual:** El modelo `Lead` ya tiene `nombre`, `email`, `telefono`, `mensaje`, `productos`.
- **Cambio requerido:** Ninguno crítico. A futuro podría agregarse `rubro` o `razon_social` si se define en D7.
- **Prioridad:** BAJA
- **Bloqueado por:** D7.

---

## Sección 4: Dudas técnicas descubiertas durante la auditoría

Estas dudas ya fueron incorporadas a `docs/DUDAS.md` con prefijo `[DT]`:

### [DT1] Funcionalidad del cotizador vs. carrito de compras
**Pregunta:** ¿Se elimina toda la lógica de `localStorage` y se simplifica a un formulario de contacto tradicional, o se conserva como "lista de cotización" sin ícono de carrito?  
**Impacto:** `static/js/modules/cart.js`, `templates/carrito.html`, `templates/index.html`, `templates/partials/header.html`.

### [DT2] Ruta `/carrito` y SEO
**Pregunta:** ¿Se renombra la ruta a `/cotizacion` o `/solicitud-de-cotizacion` con redirección 301 desde `/carrito`?  
**Impacto:** `src/infrastructure/fastapi/routers/web.py`, sitemap, internal links.

### [DT3] Landing pages para búsquedas EITAR
**Pregunta:** ¿Se crean páginas estáticas adicionales como `/repuestos-eitar`, `/valvulas-eitar`, `/termocuplas-eitar` o se optimizan las categorías existentes?  
**Impacto:** Arquitectura de rutas, sitemap, estrategia de contenidos.

---

## Resumen de prioridades

| Prioridad | Cambio | Archivos |
|---|---|---|
| CRÍTICA | Eliminar ícono de carrito del header | `templates/partials/header.html`, `static/css/components/header.css` |
| ALTA | Ajustar CTA de categoría | `templates/index.html`, `static/js/modules/cart.js` |
| ALTA | Renombrar `/carrito` → `/cotizacion` | `src/infrastructure/fastapi/routers/web.py`, `templates/carrito.html`, sitemap |
| ALTA | Actualizar título y meta descripción Home | `src/infrastructure/fastapi/routers/web.py` |
| ALTA | Actualizar H1 de Home | `templates/index.html`, `data/site_data.yml` |
| MEDIA | Actualizar formulario de contacto B2B | `templates/partials/contact_form.html` |
| MEDIA | Actualizar alt de imágenes y schema | `templates/partials/categories_grid.html`, `templates/partials/schema.html` |
| BAJA | Revisar footer para certificaciones | `templates/partials/footer.html` |
| BAJA | Validaciones Pydantic B2B | `src/domain/lead.py` |

---

## Recomendación de implementación

Dado que las certezas C6-C9 desbloquean cambios concretos, se propone ejecutar en este orden:

1. **Eliminar carrito del header** (CRÍTICA, desbloqueada).
2. **Actualizar SEO de Home** (ALTA, desbloqueada).
3. **Ajustar CTA de categoría y formulario de contacto** (ALTA/MEDIA, desbloqueada).
4. **Renombrar `/carrito` a `/cotizacion` con 301** (ALTA, bloqueada por DT2 hasta confirmación).

No se recomienda implementar login de mayoristas, pasarela de pago ni cambios de paleta hasta resolver D7, D2 y D5.
