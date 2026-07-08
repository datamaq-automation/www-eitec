# ESTRATEGIA DE PALABRAS CLAVE Y DECISIONES TÉCNICAS SEO — EITEC

Este documento registra la investigación de palabras clave (keywords) y la justificación técnica de las soluciones implementadas para la optimización en motores de búsqueda (SEO).

---

## 1. INVESTIGACIÓN DE PALABRAS CLAVE (KEYWORDS)

### 10-15 Palabras Clave Principales (Primary Keywords)
1. **termostato para termotanque** / **termostato de termotanque a gas** (Alto volumen en Argentina)
2. **válvula de seguridad para gas** / **válvula de seguridad termoeléctrica** (Componente crítico)
3. **cooperativa eitec** / **eitec bernal** / **eitec cooperativa** (Búsquedas de marca)
4. **termostato eitar** / **repuestos eitar** / **fábrica eitar** (Búsquedas históricas y de reemplazo)
5. **accesorios para artefactos a gas** (Categoría de negocio principal)
6. **robinetes para cocinas** / **robiválvulas** (Componente de cocinas domésticas)
7. **quemadores para cocinas** / **quemadores de gas** (Componente de cocción)
8. **pilotos para gas** / **piloto analizador de gas** (Componente de encendido)
9. **válvulas de seguridad para calefactores** (Seguridad en calefacción)
10. **válvulas de seguridad para hornos** (Seguridad en cocción)
11. **fábrica de repuestos de gas argentina** (B2B mayorista)
12. **repuestos de gas por mayor** (B2B comercial)

### 20-30 Palabras Clave de Cola Larga (Long-Tail Keywords)
1. **termostato eitar para termotanque precio**
2. **repuesto termostato eitar termotanque a gas**
3. **válvula de seguridad termoeléctrica funcionamiento**
4. **fábrica recuperada eitar quilmes**
5. **cooperativa metalúrgica eitec bernal**
6. **robinetes y válvulas de seguridad a gas para cocinas gastronómicas**
7. **robiválvulas para cocinas domésticas alimentadas a gas**
8. **quemadores para cocinas industriales y anafes**
9. **comprar termostato eitar termotanque argentina**
10. **válvula de seguridad calefactor tiro balanceado eitar**
11. **unidad magnética termostato gas**
12. **repuestos de termotanques a gas quilmes**
13. **fábrica de accesorios de gas buenos aires**
14. **termostatos con seguridad termoeléctrica para calentadores de agua**
15. **pilotos analizadores de oxígeno para gas envasado**
16. **válvulas de seguridad para hornos y cocinas domésticas**
17. **tubos de distribución de gas para cocinas**
18. **instalación de termostato termotanque técnico matriculado**
19. **distribuidora de repuestos para artefactos a gas**
20. **repuestos eitar oficiales argentina**
21. **termostato de seguridad termoeléctrica precio**
22. **quemador anafe gas repuesto**
23. **válvula multigas eitar repuesto**
24. **fabricante de componentes de gas B2B**
25. **repuestos de gas aprobados por enargas**

---

## 2. EVALUACIÓN DE ALTERNATIVAS Y DECISIONES TÉCNICAS

### Decisión A: Sitemap.xml dinámico vs. Archivo XML estático
*   **Alternativa A1 (Estática):** Crear un archivo `sitemap.xml` manual en `static/`.
*   **Alternativa A2 (Dinámica):** Servir una ruta `/sitemap.xml` en FastAPI que construya el XML en tiempo real leyendo `data/site_data.yml`.
*   **Elegido: Alternativa A2 (Dinámica).**
*   **Razón:** Reduce a cero el mantenimiento del sitemap para el equipo técnico de la cooperativa. Si en el futuro agregan, eliminan o modifican categorías en el archivo YAML, el sitemap se actualizará de forma instantánea sin necesidad de intervención manual o redespliegue de archivos.

### Decisión B: Robots.txt dinámico vs. Archivo en disco
*   **Alternativa B1 (Estática):** Escribir `static/robots.txt` y redireccionar desde el servidor.
*   **Alternativa B2 (Dinámica):** Servir una ruta `/robots.txt` inline desde FastAPI como respuesta de texto plano.
*   **Elegido: Alternativa B2 (Dinámica).**
*   **Razón:** Evita operaciones de lectura de archivos en disco (E/S) para una petición muy frecuente de crawlers, garantizando un rendimiento óptimo. Además, centraliza el manejo del Sitemap URL en el código de backend.

### Decisión C: SEO de imágenes del carrusel (CSS Background vs. Tag Img)
*   **Alternativa C1 (Rediseño CSS):** Modificar la estructura visual del carrusel para usar `<img>` en lugar de `background-image` en CSS.
*   **Alternativa C2 (Imágenes ocultas para SEO):** Mantener el layout con `background-image` para asegurar que el diseño no sufra regresiones visuales (responsive/recorte de imagen), pero agregar una etiqueta `<img>` oculta con `class="visually-hidden"`, su respectivo atributo `alt` y optimización de carga (`loading="eager"` en el primer slide, `loading="lazy"` en el resto).
*   **Elegido: Alternativa C2 (Imágenes ocultas para SEO).**
*   **Razón:** Protege el diseño del sitio ante regresiones visuales en diferentes resoluciones de pantalla, pero al mismo tiempo permite a los motores de búsqueda indexar los archivos de imagen y sus textos descriptivos (`alt`). También mejora el LCP (Largest Contentful Paint) marcando el primer slide de forma explícita para descarga prioritaria.

### Decisión D: Manejo de URLs de Categorías (Redirección vs. Renderizado Dedicado)
*   **Alternativa D1 (Redirección):** Mantener la redirección temporal 307 de `/categoria/{slug}` hacia `/`.
*   **Alternativa D2 (Renderizado único):** Modificar la ruta en `app.py` para servir la página index actual con el contexto de la categoría activa, y usar condicionales de Jinja2 en `index.html` para mostrar un encabezado de categoría semántico con H1 y ocultar el carrusel de inicio.
*   **Elegido: Alternativa D2 (Renderizado único).**
*   **Razón:** Imprescindible para el SEO. Las redirecciones 307 evitan que Google indexe las categorías individuales y causan errores de contenido duplicado. Con el renderizado condicional, logramos páginas únicas para cada categoría con sus propios metadatos de SEO, jerarquía de encabezados adecuada, y breadcrumbs sin complicar la estructura de plantillas.

### Decisión E: Seguridad (Middlewares de FastAPI vs. Configuración Nginx)
*   **Alternativa E1 (Nginx/Proxy):** Configurar HTTPS, HSTS y CSP a nivel del servidor web reverse proxy.
*   **Alternativa E2 (FastAPI Middleware):** Implementar un middleware HTTP en la aplicación FastAPI que agregue las cabeceras de seguridad (`Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`) a todas las respuestas.
*   **Elegido: Alternativa E2 (FastAPI Middleware).**
*   **Razón:** Hace que la aplicación sea segura por defecto en cualquier entorno (desarrollo local, contenedores, servidores directos). Además, al estar bajo control de versiones en el repositorio del proyecto, no depende de la configuración externa del hosting de la cooperativa.

### Decisión F: Organización de Schema.org JSON-LD
*   **Alternativa F1 (Inline en head.html):** Poner el script de datos estructurados directamente dentro de `head.html`.
*   **Alternativa F2 (Plantilla partial schema.html):** Crear un archivo independiente `templates/partials/schema.html` y cargarlo en `base.html`.
*   **Elegido: Alternativa F2 (Plantilla partial schema.html).**
*   **Razón:** Mejora significativamente la mantenibilidad y legibilidad del código. El JSON-LD suele ser extenso y propenso a errores de sintaxis; tenerlo separado en su propio fragmento facilita su edición futura sin riesgo de dañar la metadata básica de la página.
