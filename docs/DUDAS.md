# DUDAS DE ALTO NIVEL — Proyecto EITEC

Este documento recopila exclusivamente las dudas estratégicas, técnicas y de negocio que requieren definición antes de continuar con la implementación. Las certezas confirmadas se encuentran en `docs/CERTEZAS.md`.

---

## DUDAS ESTRATÉGICAS

### [D1] Formato y Transparencia del Logo
**Nivel:** ALTO  
**Área:** Marca / Diseño  
**Contexto:** El logo actual en `static/custom/logo.jpg` es un archivo JPEG con fondo blanco sólido y opaco. Se generó una versión PNG transparente automáticamente como solución temporal, pero puede tener halos o imperfecciones.  
**Pregunta:** ¿Se dispone de una versión del logo EITEC con fondo transparente profesional (en formato SVG o PNG de alta resolución)?  
**Impacto:** Afecta directamente al componente Header, su flexibilidad estética y la capacidad de integrarse con fondos de color.  
**Bloquea propuesta:** No para la paleta general, pero sí bloquea el rediseño del Header con fondo oscuro o degradado.

### [D2] Estética General: Modo Oscuro vs Modo Claro
**Nivel:** ALTO  
**Área:** Diseño / Estrategia UX  
**Contexto:** La imagen oficial de marca (`image.png`) tiene una estética futurista/industrial oscura, con neones cian y magenta sobre fondos azul noche y púrpura profundo. El sitio actual es puramente claro con fondos blancos y grises.  
**Pregunta:** ¿Debemos migrar el sitio web a una estética de modo oscuro (dark mode) por defecto para que coincida con el impacto visual del mapa neón y los rayos magenta, o debemos conservar un esquema claro y usar el cian/magenta neón solo como acentos y hovers?  
**Impacto:** Afecta a la totalidad de las hojas de estilo del sitio (`base.css`, fondos de secciones, textos, inputs).  
**Bloquea propuesta:** Sí. Define la dirección cromática de toda la refactorización visual.

### [D3] Estrategia de Marca: EITEC (Cooperativa) vs EITAR (Histórica)
**Nivel:** ALTO  
**Área:** Estrategia / Marca / SEO  
**Contexto:** EITEC es la cooperativa continuadora de la histórica fábrica EITAR. En el mercado, los clientes siguen buscando activamente "repuestos EITAR" o "válvulas de seguridad EITAR". Si nos enfocamos solo en "EITEC", perderemos el volumen de búsqueda histórica de EITAR. Si nos enfocamos demasiado en "EITAR", podríamos diluir la identidad de la cooperativa.  
**Pregunta:** ¿Cómo priorizar el copy de marca en los textos e introducciones del sitio? ¿Se debe crear contenido específico para búsquedas de reposición EITAR o alcanza con el copy híbrido actual?  
**Impacto:** Afecta los encabezados H1, meta-etiquetas, descripciones en la página de inicio y categorías, y potencialmente la creación de landing pages.  
**Bloquea propuesta:** No. Se puede avanzar con copy híbrico ("EITEC, ex EITAR") de manera segura, pero se necesita definición para una estrategia SEO más agresiva.

### [D4] Modelo de Negocio e Icono de Carrito
**Nivel:** ALTO  
**Área:** Estrategia UX / Negocio  
**Contexto:** El header de la página incluye un ícono de carrito de compras (`/carrito`), pero el sitio es meramente institucional y no tiene base de datos de productos ni pasarela de pago. Se confirmó que el canal es B2B mayorista y que el carrito genera confusión.  
**Pregunta:** ¿Se elimina el ícono de carrito del header completamente, o se reemplaza por un ícono de "solicitud de cotización"? ¿Qué se hace con la página `/carrito`, que hoy funciona como formulario de cotización B2B?  
**Impacto:** Afecta a los componentes Header, Footer, JS de cotización y la ruta `/carrito`.  
**Bloquea propuesta:** No. Se propone eliminar el ícono del header y evaluar renombrar `/carrito` a `/cotizacion`.

### [D5] Certificaciones y Sellos Oficiales
**Nivel:** ALTO  
**Área:** Estrategia UX / Confianza  
**Contexto:** En el sector de gas, la homologación (ENARGAS, IRAM) es vital para la confianza del instalador. Incluir estos logos oficiales en el footer y en páginas de productos aumentaría el E-E-A-T de la web.  
**Pregunta:** ¿Qué certificaciones y sellos vigentes tiene permitido exhibir la cooperativa y se dispone de sus imágenes originales?  
**Impacto:** Afecta la sección inferior del footer y páginas de categorías de productos.  
**Bloquea propuesta:** No. Se puede contemplar un espacio reservado para sellos en la estructura del Footer.

### [D6] Situación legal del dominio EITAR
**Nivel:** ALTO  
**Área:** Legal / SEO / Dominio  
**Contexto:** El dominio `eitar.com.ar` está registrado a nombre de un tercero (titular: GUAZZINI BRUNO DARIO), con fecha de alta 26/02/2021 y vencimiento 26/02/2027. No está caído ni disponible para registro. Sin embargo, `eitar.ar` (TLD directo bajo `.ar`) sí está disponible.  
**Pregunta:** ¿Se conoce al titular de `eitar.com.ar`? ¿Existe posibilidad de negociar la compra/transferencia? ¿Se registra defensivamente `eitar.ar` mientras se decide lo de `.com.ar`? ¿Se registran también variantes como `eitec-eitar.com.ar` o `repuestoseitar.com.ar`?  
**Impacto:** Afecta redirecciones 301, autoridad de dominio, estrategia de backlinks y protección de marca.  
**Bloquea propuesta:** Sí, para decisiones de dominio y redirecciones. No bloquea cambios de copy interno.

### [D7] Definición formal del modelo de negocio
**Nivel:** ALTO  
**Área:** Negocio / UX  
**Contexto:** Se confirmó que el canal es B2B mayorista, pero no se definió si también atienden a instaladores individuales o si hay precios diferenciados por volumen.  
**Pregunta:** ¿Solo mayoristas? ¿También instaladores individuales? ¿Precios diferenciados por volumen? ¿Se requiere login de mayorista o solo formulario de contacto?  
**Impacto:** Define si el sitio necesita área privada de mayorista, formulario B2B segmentado o simplemente contacto general.  
**Bloquea propuesta:** Sí, para cualquier funcionalidad de login o área privada. No bloquea la eliminación del carrito ni ajustes de copy.

### [D8] Nomenclatura del mercado de reposición
**Nivel:** ALTO  
**Área:** SEO / Copy  
**Contexto:** Se sabe que los clientes buscan "repuestos EITAR", pero no se confirmó la nomenclatura exacta que usan ferreteros e instaladores.  
**Pregunta:** ¿Cómo buscan los ferreteros las válvulas? ¿"Repuesto EITAR", "válvula de seguridad EITAR", "termocupla EITAR", "robinete EITAR"?  
**Impacto:** Define el keyword research, el copy de producto, los alt de imágenes y las meta-descripciones de categorías.  
**Bloquea propuesta:** No. Se puede avanzar con keywords obvios, pero se necesita validación para una estrategia completa.

### [D9] Políticas legales y cumplimiento (Privacidad y Cookies) [RESUELTA]
**Nivel:** MEDIO  
**Área:** Legal / SEO E-E-A-T  
**Contexto:** Se confirmó la incorporación de Google Analytics y Microsoft Clarity. Se implementó técnicamente el banner de cookies interactivo y la carga condicional/diferida de scripts de tracking en base al consentimiento. También se actualizaron los borradores del footer y de las políticas.  
**Resolución:** Confirmado el uso de analíticas. Solo resta la validación de la redacción final de los borradores de políticas por parte de la cooperativa.

---

## DUDAS TÉCNICAS

### [DT1] Funcionalidad del cotizador vs. carrito de compras
**Área:** Frontend / UX  
**Contexto:** La página `/carrito` actual funciona como un formulario de solicitud de cotización B2B (usando `localStorage` para recordar productos), pero el ícono en el header es un carrito de compras.  
**Pregunta:** ¿Se elimina toda la lógica de `localStorage` y se simplifica a un formulario de contacto tradicional, o se conserva como "lista de cotización" sin ícono de carrito?  
**Impacto:** Afecta `static/js/modules/cart.js`, `templates/carrito.html`, `templates/index.html` y `templates/partials/header.html`.

### [DT2] Ruta `/carrito` y SEO
**Área:** Backend / SEO  
**Contexto:** La URL `/carrito` tiene semántica de e-commerce minorista. El contenido real es un formulario de cotización mayorista.  
**Pregunta:** ¿Se renombra la ruta a `/cotizacion` o `/solicitud-de-cotizacion` con redirección 301 desde `/carrito`?  
**Impacto:** Afecta `src/infrastructure/fastapi/routers/web.py`, sitemap, internal links y bookmarks existentes.

### [DT3] Landing pages para búsquedas EITAR
**Área:** SEO / Contenido  
**Contexto:** Las categorías actuales ya incluyen "EITAR" en títulos y descripciones, pero no hay páginas específicas orientadas a búsquedas de marca histórica.  
**Pregunta:** ¿Se crean páginas estáticas adicionales como `/repuestos-eitar`, `/valvulas-eitar`, `/termocuplas-eitar` o se optimizan las categorías existentes?  
**Impacto:** Afecta la arquitectura de rutas, el sitemap y la estrategia de contenidos.

### [DT4] Generación de PDF cotizador
**Área:** Frontend / Backend / Funcionalidad B2B  
**Contexto:** Un cotizador mayorista digital a veces requiere la descarga de un comprobante formal en formato PDF para el cliente, mientras que otras veces basta con enviar la solicitud de cotización digital al backend de administración.  
**Pregunta:** ¿El sistema debe generar y permitir la descarga de un presupuesto/cotización en formato PDF para el usuario, o es suficiente con que el formulario envíe la solicitud por correo electrónico/base de datos?  
**Impacto:** Afecta a la implementación de bibliotecas de generación de PDF (ej. ReportLab en Python o jsPDF/html2pdf en JavaScript), diseño de plantilla de presupuesto y flujo de usuario.

---

## RESUMEN DE ESTADO

- **Dudas estratégicas abiertas:** 9 (D1, D2, D3, D4, D5, D6, D7, D8, D10)
- **Dudas técnicas abiertas:** 4 (DT1, DT2, DT3, DT4)
- **Dudas resueltas:** 1 (D9)
- **Certezas confirmadas:** ver `docs/CERTEZAS.md`

### Próximas decisiones críticas para desbloquear
1. **D6** — Dominio EITAR: define estrategia de dominios y redirecciones.
2. **D7** — Modelo de negocio: define si se necesita área privada de mayoristas.
3. **D8** — Nomenclatura: define el keyword research completo.
4. **D10** — Centralización de dominios: define la infraestructura y URL definitiva del sitio.
5. **DT2** — Ruta `/carrito`: define la URL definitiva del formulario de cotización.
6. **DT4** — Generación de PDF cotizador: define si se requiere implementar el generador de PDF.
