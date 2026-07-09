# TODO: Refactorización Frontend

## Estado Actual
El frontend del proyecto está estructurado con Bootstrap 5 y una mezcla de estilos custom en `static/css/styles.css` y jQuery en `static/js/main.js`. 
Presenta los siguientes problemas de deuda técnica:
- **Código CSS Muerto:** Alrededor del 60% del archivo `styles.css` contiene estilos heredados de una plantilla e-commerce (carrito, login, registro, listados de productos detallados) que no se utilizan en absoluto.
- **Acoplamiento de Scripts:** Scripts cargados desde CDNs externos (jQuery, matchHeight, lightGallery) no tienen uso real (las clases/IDs que inicializan no existen en los templates).
- **Estilos Inline:** Tres atributos `style` forzados en los templates.
- **Falta de modularidad:** Un único archivo CSS y JS gigante con selectores aninados complejos o sobre-específicos.

## Objetivo
- Estructurar el CSS bajo la metodología **BEM** (Block-Element-Modifier) con variables nativas de CSS.
- Separar el CSS y JS en módulos específicos de acuerdo a su responsabilidad (componentes independientes).
- Remover dependencias muertas (jQuery, matchHeight, lightGallery).
- Migrar el JS interactivo a ES Modules nativos en JavaScript Vanilla.
- Mantener la UI **estrictamente idéntica** en lo visual y funcional.

## Estrategia CSS Elegida
Utilizaremos **BEM** combinado con una estructura simplificada de **ITCSS** para organizar las hojas de estilo:
1. **Settings / Variables:** Definición de colores, fuentes y espaciados mediante variables nativas CSS (`variables.css`).
2. **Base:** Estilos globales y reset elemental para selectores de etiquetas (`base.css`).
3. **Components:** Archivos CSS separados por bloque BEM para cada componente del sitio (`header.css`, `footer.css`, `carousel.css`, etc.).
4. **Main:** Un archivo `main.css` que reúne todo mediante `@import` para simplificar la carga y escalabilidad.

## Mapa de Carpetas Propuesto
```text
static/
├── css/
│   ├── base.css
│   ├── variables.css
│   ├── components/
│   │   ├── buttons.css
│   │   ├── carousel.css
│   │   ├── categories-grid.css
│   │   ├── category-detail.css
│   │   ├── contact-form.css
│   │   ├── footer.css
│   │   ├── header.css
│   │   └── search-overlay.css
│   └── main.css
├── js/
│   ├── modules/
│   │   ├── contact-form.js
│   │   ├── header.js
│   │   └── search-overlay.js
│   └── main.js
```

## Cambios de Nombres

| Selector/Nombre Viejo | Selector BEM Nuevo | Motivo |
| :--- | :--- | :--- |
| `header` | `.header` | Estandarización a clase BEM. |
| `header .top` | `.header__top` | Elemento top-bar del bloque header. |
| `header .logo` | `.header__logo` | Elemento logo del bloque header. |
| `.hamburger` | `.header__hamburger` | Hamburger menu dentro del header. |
| `header .options` | `.header__menu` | Menú de navegación principal. |
| `header .options > li` | `.header__menu-item` | Ítem del menú. |
| `header .options a` | `.header__menu-link` | Enlace del menú. |
| `header .options p` | `.header__menu-trigger` | Disparador de submenú. |
| `.mask` | `.header__mask` o `.search-overlay__mask` | Desacoplamiento de la máscara de fondo según el bloque. |
| `header + .carousel` | `.carousel-slider` | Bloque independiente para el carrusel de imágenes. |
| `.listadoCategorias` | `.categories-grid` | Bloque contenedor de la grilla de categorías. |
| `.cuadrada` | `.categories-grid__card` | Tarjeta individual de categoría. |
| `.imagenCategoria` | `.categories-grid__image` / `.category-detail__image` | Nombres semánticos según el contexto. |
| `section.intro-eitec` | `.intro-section` | Bloque para la sección de introducción en la Home. |
| `section.producto` | `.category-detail` | Bloque para el detalle de la categoría activa. |
| `section.contacto` | `.contact-section` | Bloque que contiene el formulario de contacto. |
| `form#form_contactanos` | `.contact-form` | Bloque del formulario de contacto. |
| `footer` | `.footer` | Bloque del pie de página. |
| `footer .redes` | `.footer__socials` | Redes sociales del footer. |
| `footer .links` | `.footer__links-column` | Columnas de enlaces del footer. |
| `footer .footReg` | `.footer__copyright` | Derechos de autor del footer. |
| `.buscando` | `.search-overlay` | Bloque del overlay de búsqueda a pantalla completa. |
| `form.busqueda` | `.search-overlay__form` | Formulario del buscador. |

## Componentes Identificados
- **Header:** Menú fijo superior, redes sociales en top-bar, buscador, íconos de acción, y menú hamburguesa en responsive.
- **Carousel:** Carrusel de Bootstrap 5 modificado para slides dinámicos.
- **Categories Grid:** Grilla de 2, 3 o 4 columnas con las categorías traídas del YAML.
- **Category Detail:** Vista del producto/categoría seleccionada con breadcrumbs y CTA.
- **Intro Section:** Bloque de texto con la descripción institucional de EITEC.
- **Contact Form:** Formulario con validaciones nativas HTML5 y reCAPTCHA v2.
- **Footer:** Sección de redes, links rápidos y copyright con año actual dinámico.
- **Search Overlay:** Buscador a pantalla completa con máscara translúcida.

## Riesgos
- **[R1] reCAPTCHA v2 Callback:** reCAPTCHA v2 de Google invoca un callback global definido por `data-callback="onSubmit_contactanos"`. Si encapsulamos este callback dentro de un ES Module sin exponerlo a `window`, la validación de reCAPTCHA fallará.
  - *Mitigación:* Exponer explícitamente `window.onSubmit_contactanos = onSubmit_contactanos;` en el script del formulario.
- **[R2] Pérdida de Estilos Base:** El stylesheet remoto `styles.min.css` define varios estilos estructurales y de íconos. Si modificamos las clases de forma inconsistente, podríamos perder íconos o espaciados.
  - *Mitigación:* Estudiar todas las propiedades aplicadas por `styles.min.css` y asegurar la equivalencia exacta de nombres de clase en el HTML refactorizado.
- **[R3] Efecto Scroll en Navbar:** El cambio de tamaño del header al scrollear depende de la clase `.reduce`.
  - *Mitigación:* Mantener la misma transición CSS y lógica en el JS Vanilla usando `IntersectionObserver` o un handler de `scroll` optimizado.

## Checklist de Verificación Visual
- [ ] **Home Page (`/`):**
  - [ ] El menú de navegación se reduce de tamaño al scrollear más de 50px de altura.
  - [ ] El menú hamburguesa se despliega correctamente en resoluciones menores a 992px y cambia a icono "is-active".
  - [ ] El carrusel se autodesplaza y muestra las imágenes de fondo correctamente adaptadas a pantalla completa.
  - [ ] Las tarjetas de categoría en la grilla se ven alineadas, con el fondo azul en el texto inferior al pasar el mouse, y redireccionan correctamente.
  - [ ] El buscador overlay se despliega a pantalla completa al hacer clic en la lupa, y se cierra al hacer clic fuera del formulario (máscara).
- [ ] **Category Page (`/categoria/{slug}`):**
  - [ ] El breadcrumb superior es visible y el enlace "Inicio" lleva a `/`.
  - [ ] El título principal es el nombre de la categoría en color primario azul y fuente `Bebas Neue`.
  - [ ] La imagen derecha de la categoría se ve redondeada, con sombra ligera (`shadow-sm`) y una altura máxima de 380px.
  - [ ] La sección inferior "Otras Categorías de Productos" carga la grilla correctamente.
- [ ] **Contact Form (`/contacto`):**
  - [ ] El formulario valida campos obligatorios (mínimo de caracteres en nombre, patrón regex en email y largo mínimo en teléfono).
  - [ ] reCAPTCHA funciona y el callback envía el formulario exitosamente al backend FastAPI.
  - [ ] La confirmación muestra el mensaje "Gracias por contactarte" en una caja verde de alerta.
