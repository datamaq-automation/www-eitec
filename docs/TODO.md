# TODO: Modernización UI/UX — Identidad Visual EITEC

## Estado Actual
La identidad visual actual del sitio web es minimalista y muy plana. Está construida sobre Bootstrap 5 con estilos custom en `static/css/` que fueron refactorizados de un único archivo gigante. 
- **Paleta**: Usa un azul celeste primario (`#00a6ed`), un verde oliva para hovers (`#8aae4e`) y un azul marino oscuro (`#040734`) para el texto de menús o detalles. Los fondos son predominantemente claros (`#f8f9fa` y `#ffffff`).
- **Tipografía**: La fuente de títulos es `Bebas Neue` (adecuada e industrial, pero mal integrada con recuadros de fondo rígidos en H2), y la de cuerpo es `Roboto`. Hay una tipografía importada (`Varela Round`) que no se utiliza en ningún componente.
- **Componentes**: Botones con esquinas completamente rectas (`border-radius: 0`), sin transiciones en hover. Tarjetas de categorías estáticas, sin animaciones ni feedback al pasar el cursor. El header tiene un fondo blanco sólido obligado por el fondo blanco del logo JPG.
- **Responsive**: Se apoya en una hoja de estilos externa (`styles.min.css`) que implementa un sistema legacy de posicionamiento con floats, clearfixes y múltiples media queries con márgenes fijos en píxeles para compensar la barra de navegación en distintas resoluciones.
- **Accesibilidad**: Presenta fallas críticas. El contraste de texto blanco sobre el azul primario `#00a6ed` es de solo `2.43:1` (falla WCAG AA). En el overlay del buscador, el texto escrito por el usuario es blanco sobre fondo blanco (contraste 1:1), haciéndolo completamente invisible.

## Desalineaciones con la marca
La imagen oficial de marca de EITEC (representada en `image.png`) transmite una estética moderna, tecnológica e industrial de alto impacto. Sin embargo, el sitio web actual no refleja esto:
- **Colores ausentes**: La marca oficial se destaca por colores de alta saturación / neón sobre fondos oscuros:
  - **Cian neón** (`#00d4ff` / `#0ce9fc`): En el mapa de Argentina y logo. En el sitio se usa un azul celeste estándar (`#00a6ed`).
  - **Magenta neón** (`#c026d3` / `#ad02e3`): En los rayos de fondo. Está totalmente ausente del sitio.
  - **Verde lima** (`#50ae4e`): En el aro del logo. En el sitio se usa un verde oliva apagado (`#8aae4e`) para hover.
  - **Azul noche / Púrpura oscuro** (`#0a0a2e` / `#1c0b4e`): El fondo oscuro del logo y mapa. El sitio usa blanco y gris claro como fondos principales.
- **Atmósfera visual**: La marca es vibrante, con brillo ("glow"), gradientes y profundidad. El sitio es plano, sin sombras modernas ni transiciones.
- **Logo deformado**: El logo JPG se fuerza en proporciones rectangulares estáticas (86x116px), rompiendo su forma circular nativa.

## Oportunidades de modernización
Es posible rejuvenecer y alinear estéticamente el sitio web de EITEC sin alterar la estructura lógica de FastAPI o los datos del YAML:
1. **Paleta de Colores Coherente**: Reemplazar las variables de color por tonos extraídos directamente de la imagen oficial de marca (Cian y Magenta neón como acentos, Azul Noche y Gris Azulado para fondos y textos).
2. **Interactividad Premium (Microinteracciones)**: Añadir transiciones suaves (`transition: all 0.3s ease`) en todos los botones, enlaces y tarjetas.
3. **Efectos de Hover Modernos**: Implementar zooms suaves (`transform: scale(1.03)`) y efectos de resplandor ("box-shadow glow" cian/magenta) en botones y tarjetas al pasar el cursor.
4. **Layout Moderno (Flexbox / Grid)**: Deshacerse del float legacy y los clearfixes en la grilla de categorías y footer, adoptando Flexbox y CSS Grid.
5. **Tipografía Optimizada**: Remover la importación de `Varela Round` para mejorar el rendimiento de carga y pulir los tamaños de fuente en `rem`.

## Propuesta de paleta (bajo nivel)

| Variable actual | Valor propuesto | Justificación con la imagen de marca |
| :--- | :--- | :--- |
| `--color-primary: #00a6ed` | `#00d4ff` (Cian Neón) | El cian brillante que delimita el mapa de Argentina y destaca el fuego del logo. |
| `--color-primary-hover: #8aae4e` | `#7df9ff` (Glow Cian) | Versión luminosa del cian de marca para estados hover y activos con efecto de luz. |
| `--color-dark: #040734` | `#0a0a2e` (Azul Noche) | El azul profundo del fondo espacial/grilla del logo. Brinda una base oscura y tecnológica. |
| `--color-text: #414141` | `#1a1a2e` (Negro Azulado) | Tono oscuro casi negro con tinte azulado para mejorar el contraste de lectura sobre fondos claros. |
| `--color-text-muted: #808080` | `#5a6e85` (Gris Pizarra) | Tono grisáceo azulado para descripciones secundarias, mejorando el contraste a 4.7:1. |
| `--color-bg-light: #f8f9fa` | `#f0f4f8` (Gris Azulado Claro)| Fondo claro suave con tinte azul para mantener la armonía fría de la paleta. |
| (Nueva variable acento) | `#c026d3` (Magenta Neón) | Representa los rayos de luz verticales del fondo. Ideal para llamadas a la acción secundarias y CTAs. |
| (Nueva variable acento) | `#50ae4e` (Verde Lima) | Saca el verde exacto del anillo del logo para usarlo en alertas de éxito, confirmaciones o detalles puntuales. |

## Propuesta de componentes (bajo nivel)

- **Header**:
  - Cambiar la sombra `.header` por una más suave y moderna (`box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05)`).
  - Corregir el dimensionamiento del logo (`.header__logo`) usando `background-size: contain`, `background-repeat: no-repeat` y una proporción cuadrada balanceada (ej. `80px` por `80px`) para evitar que el círculo del logo se aplaste.
  - Añadir un efecto de subrayado dinámico en hover en los enlaces de navegación usando pseudo-elementos (`::after`) con transición de ancho.

- **Carousel**:
  - Aplicar un degradado de color (overlay) de azul noche profundo a magenta translúcido sobre las imágenes de fondo en lugar del gris plano actual (`background-color: rgb(0 0 0 / .25)`), dando un look integrado con la marca.
  - Modificar las tipografías del carrusel para que utilicen la escala tipográfica correcta y tengan sombras de texto sutiles que faciliten la lectura sobre fondos dinámicos.

- **Grilla de Categorías**:
  - Modificar `.categories-grid` para usar `display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px;` eliminando las reglas fijas de float y márgenes manuales.
  - En las tarjetas (`.categories-grid__card`), sustituir las esquinas rectas por bordes ligeramente redondeados (`border-radius: 8px`).
  - Añadir transiciones suaves: al hacer hover, la tarjeta debe elevarse ligeramente (`transform: translateY(-5px)`) y la imagen debe hacer un zoom suave (`transform: scale(1.05)`). El texto de fondo debe cambiar de color con una transición gradual de cian neón a un brillo más claro.

- **Botones (`.btn-call`)**:
  - Añadir `border-radius: 4px` (esquinas suavizadas, mantienen el look industrial pero no son toscas).
  - Añadir `transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);`.
  - El hover debe cambiar de cian neón a glow cian, y el borde debe acompañar este cambio.

- **Formulario de Contacto**:
  - Retirar el `!important` de `.contact-form__input` y sustituirlo por bordes con variables CSS.
  - Añadir estado `:focus-visible` que resalte el borde del input en cian neón con un suave resplandor (`box-shadow: 0 0 0 3px rgba(0, 212, 255, 0.25)`).

- **Footer**:
  - Cambiar el fondo de negro puro a azul noche profundo (`--color-dark`).
  - Alinear los enlaces de categorías en columnas limpias sin usar botones gigantes `.btn-call`, mejorando el aspecto editorial e institucional.

- **Search Overlay**:
  - **Corrección de Bug**: Establecer el color del texto del input a `#ffffff` y asegurar que el placeholder tenga contraste adecuado.
  - Usar un fondo translúcido oscuro (`rgba(10, 10, 46, 0.95)`) en lugar de blanco translúcido, imitando la estética oscura del mapa de Argentina de la marca oficial.

## Jerarquía visual propuesta
- **Contraste**: Reemplazar los colores que fallan accesibilidad para que todos los textos principales tengan al menos `4.5:1` de contraste relativo contra sus respectivos fondos (WCAG AA).
- **Titulares de sección (H2)**: El actual recuadro azul sólido alrededor de los H2 se ve tosco y confuso. Se propone eliminar el fondo azul completo de los H2, usar una tipografía limpia en color azul noche con un subrayado decorativo corto y centrado en cian neón (`border-bottom` o pseudo-elemento). Esto aclara que es un título y no un botón interactivo.
- **CTA Principal**: Utilizar el color de acento Magenta Neón (`#c026d3`) en los botones de "Consultar por esta categoría" y "Enviar" para crear una clara llamada a la acción secundaria que llame la atención de inmediato frente al cian predominante.

## Responsive y accesibilidad
- **Eliminar Floats**: Reemplazar el layout basado en floats de la grilla de categorías y footer por CSS Flexbox y CSS Grid. Esto garantiza una adaptabilidad fluida sin necesidad de hackear con clearfixes en resoluciones intermedias (como tablets).
- **Compensación del Header**: Reemplazar los márgenes estáticos en px de compensación del header por una variable CSS dinámica de altura de cabecera (`--header-height`), controlada en el CSS o a través de un pequeño script JS que mida la altura real del header.
- **Accesibilidad**: Asegurar que todos los botones y campos tengan `:focus-visible` claramente visible (borde cian o magenta neón) y añadir atributos `aria-expanded` y roles semánticos correspondientes en el menú hamburguesa.

## Riesgos de regresión visual
- **Hojas de estilo externas**: La dependencia actual de `styles.min.css` puede provocar que algunas clases legacy dejen de funcionar si se cambian los nombres de clase.
  - *Mitigación*: Mantener el acoplamiento controlado o, idealmente, copiar las reglas estructurales indispensables de `styles.min.css` a nuestro `base.css` local para independizarnos del archivo remoto.
- **Imágenes del carrusel**: Las imágenes de productos provistas por la cooperativa tienen proporciones muy diversas. Al modernizar el carrusel, debemos garantizar que el recorte vía `background-size: cover` no corte textos o partes fundamentales del producto.
  - *Mitigación*: Asegurar que el overlay oscuro del carrusel mantenga un contraste de texto óptimo en todas las imágenes.

## Checklist de verificación

### Home Page (`/`)
- [ ] El menú de navegación se reduce suavemente al scrollear sin saltos visuales bruscos.
- [ ] El menú hamburguesa cambia a "is-active" y abre el menú cubriendo la pantalla correctamente en móviles.
- [ ] El logo de EITEC no se ve aplastado ni pixelado en desktop ni en móvil.
- [ ] Las tarjetas de categoría en la grilla se adaptan fluidamente de 4 columnas (desktop) a 2 columnas (tablet) y 1 columna (móvil) sin salirse de la pantalla.
- [ ] Al hacer hover sobre una tarjeta de categoría, se visualiza la transición de zoom en la imagen y el sombreado suave de la tarjeta.
- [ ] El buscador overlay se abre con fondo azul noche oscuro translúcido y permite leer el texto ingresado en blanco perfectamente.

### Página de Categoría (`/categoria/{slug}`)
- [ ] El breadcrumb superior es visible e indica la categoría activa sobre un fondo gris azulado suave.
- [ ] El título principal (H1) se muestra en el color de marca cian o azul noche sin recuadros toscos.
- [ ] El botón de cotización resalta con la variable Magenta Neón y tiene transición de hover a un tono más claro.
- [ ] La sección de "Otras Categorías" renderiza la grilla modernizada sin errores.

### Formulario de Contacto y Footer
- [ ] Los campos de entrada (inputs) cambian su borde a cian neón al hacer foco y muestran un resplandor suave.
- [ ] El botón de enviar tiene el contraste correcto de texto y funciona con la validación de reCAPTCHA.
- [ ] El footer muestra los links alineados en columnas ordenadas, usando tipografía de tamaño adecuado en lugar de botones gigantes.
- [ ] El copyright del footer muestra el año actual de forma correcta y tiene buen contraste de lectura.
