# DUDAS DE ALTO NIVEL — Identidad Visual EITEC

Este documento recopila las dudas estratégicas de negocio, marca y diseño identificadas durante la auditoría de identidad visual y UI/UX. Estas decisiones requieren definiciones de la cooperativa antes de ser codificadas.

## [D1] Formato y Transparencia del Logo
**Nivel:** ALTO  
**Área:** Marca / Diseño  
**Contexto:** El logo actual en `static/custom/logo.jpg` es un archivo JPEG con fondo blanco sólido y opaco. Esto imposibilita el uso de cabeceras oscuras, translúcidas o con efectos de desenfoque modernos (glassmorphism), obligando a mantener un header blanco plano para evitar un recuadro blanco antiestético.  
**Pregunta:** ¿Se dispone de una versión del logo EITEC con fondo transparente (en formato SVG o PNG de alta resolución)?  
**Impacto:** Afecta directamente al componente Header, su flexibilidad estética y la capacidad de integrarse con fondos de color.  
**Bloquea propuesta:** No para la paleta general, pero sí bloquea el rediseño del Header con fondo oscuro o degradado.

## [D2] Estética General: Modo Oscuro vs Modo Claro
**Nivel:** ALTO  
**Área:** Diseño / Estrategia UX  
**Contexto:** La imagen oficial de marca (`image.png`) tiene una estética futurista/industrial oscura, con neones cian y magenta sobre fondos azul noche y púrpura profundo. El sitio actual es puramente claro con fondos blancos y grises.  
**Pregunta:** ¿Debemos migrar el sitio web a una estética de modo oscuro (dark mode) por defecto para que coincida con el impacto visual del mapa neón y los rayos magenta, o debemos conservar un esquema claro y usar el cian/magenta neón solo como acentos y hovers?  
**Impacto:** Afecta a la totalidad de las hojas de estilo del sitio (`base.css`, fondos de secciones, textos, inputs).  
**Bloquea propuesta:** Sí. Define la dirección cromática de toda la refactorización visual.

## [D3] Estrategia de Marca: EITEC (Cooperativa) vs EITAR (Histórica)
**Nivel:** ALTO  
**Área:** Estrategia / Marca  
**Contexto:** EITEC es la cooperativa continuadora de la histórica fábrica EITAR. En el mercado, los clientes siguen buscando activamente "repuestos EITAR" o "válvulas de seguridad EITAR". Si nos enfocamos solo en "EITEC", perderemos el volumen de búsqueda histórica de EITAR. Si nos enfocamos demasiado en "EITAR", podríamos diluir la identidad de la cooperativa.  
**Pregunta:** ¿Cómo priorizar el copy de marca en los textos e introducciones del sitio?  
**Impacto:** Afecta los encabezados H1, meta-etiquetas y descripciones en la página de inicio y categorías.  
**Bloquea propuesta:** No. Se puede avanzar con copy híbrido ("EITEC, ex EITAR") de manera segura.

## [D4] Modelo de Negocio e Icono de Carrito
**Nivel:** ALTO  
**Área:** Estrategia UX / Negocio  
**Contexto:** El header de la página incluye un ícono de carrito de compras (`/carrito`), pero el sitio es meramente institucional y no tiene base de datos de productos ni pasarela de pago. Se requiere definir si se mantendrá como fabricante B2B, en cuyo caso se debería remover el carrito y optimizar para generación de clientes potenciales mayoristas.  
**Pregunta:** ¿Se debe eliminar el ícono de carrito de compras del header y footer para clarificar que el sitio es de catálogo industrial y contacto B2B?  
**Impacto:** Afecta a los componentes Header y Footer.  
**Bloquea propuesta:** No. Se puede proponer su remoción temporal en el plan visual.

## [D5] Certificaciones y Sellos Oficiales
**Nivel:** ALTO  
**Área:** Estrategia UX / Confianza  
**Contexto:** En el sector de gas, la homologación (ENARGAS, IRAM) es vital para la confianza del instalador. Incluir estos logos oficiales en el footer y en páginas de productos aumentaría el E-E-A-T de la web.  
**Pregunta:** ¿Qué certificaciones y sellos vigentes tiene permitido exhibir la cooperativa y se dispone de sus imágenes originales?  
**Impacto:** Afecta la sección inferior del footer y páginas de categorías de productos.  
**Bloquea propuesta:** No. Se puede contemplar un espacio reservado para sellos en la estructura del Footer.
