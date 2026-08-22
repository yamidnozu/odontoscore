# Niche & Architecture — DentaRank Global (Odontología)

The core principle remains absolute: **one normalized database, many generated pages**.
In the dental niche (**Productos de Odontología**), comparison is highly technical and spec-driven (pulsations, water pressure, sterilization, battery life, noise levels, clinical indications). Users make high-intent purchasing decisions based on oral health needs (brackets, implants, sensitive gums, pediatric care, professional clinics).

---

## The principle (repeat it until it's reflex)

> A product is a **record**, not a page. Pages are **views** over records.
> Adding a product means adding a record — never writing HTML.

Consequences that must hold:
- The comparator, radar charts, category lists, buying guides, and fichas all read the same `productos.json` (or `window.__DB__`).
- Design lives in CSS + templates, applied uniformly to every record with clinical authority and trust (clean medical aesthetic: #FFFFFF white + #0E76BC trust blue).
- The user (or AI) grows the site by pasting Amazon affiliate links (`amazon.es`, `amazon.com`, `amazon.com.mx`), not by editing pages.

If you ever find yourself writing `<h1>Oral-B iO Series 9</h1>` by hand, stop — that belongs in the data.

---

## Dental Categories & Segments

The site structures dental products into 6 core clinical and consumer categories:

1. **Cepillos Eléctricos** (Sónicos, Rotatorios-Oscilantes, Magnéticos iO)
2. **Irrigadores Dentales** (Sobremesa, Portátiles/Inalámbricos, Conexión a Grifo)
3. **Blanqueamiento Dental** (Kits LED, Tiras Blanqueadoras, Geles de Peróxido/PAP+)
4. **Ortodoncia & Brackets** (Irrigadores específicos, Cepillos interdentales, Ceras y Protectores)
5. **Higiene Infantil** (Cepillos con app lúdica, Cabezales ultrasuaves, Temporizadores)
6. **Instrumental Básico Profesional** (Lámparas de fotocurado, Espejos intraorales, Localizadores de ápices, Esterilizables en autoclave)

---

## Page map (what a complete site has)

| Page | Generated from | Purpose |
|---|---|---|
| **Home** (`/` o `/{lang}/`) | featured + newest records | Hero clínico con autoridad E-E-A-T, top picks, categorías directas, "Cómo evaluamos" |
| **Category pages** (`/categoria/{slug}/`) | records filtered by `categoria_odontologica` | Páginas silo por categoría con filtros dinámicos (tecnología, presión PSI, modos) |
| **Product ficha** (`/producto/{id}.html`) | one record | Ficha técnica dental: galería WebP + tabla técnica + radar 0-10 + editorial 300 palabras + pros/contras + ideal para + resumen reseñas + CTA afiliado |
| **Comparator** (`/comparador.html`) | 2-4 records (intra-categoría) | Tabla lado a lado de specs dentales + radares superpuestos |
| **Buying guides / Blog** (`/guias/{slug}.html`) | records + editorial clínico | "Mejor irrigador dental para brackets 2026", "Guía cepillos sónicos vs rotatorios" — imán SEO/GEO |
| **Rankings / "Los mejores X"** | records sorted by scores | "Top 5 irrigadores por presión PSI", "Mejores cepillos para encías sensibles" |
| **Ofertas** (`/ofertas.html`) | records where `discountedPrice < retailPrice` | Descuentos activos en productos dentales con badge de oferta |
| **Metodología / E-E-A-T** | static | Quiénes somos, fuentes clínicas consultadas, criterios de puntuación |
| **Aviso de afiliados + legal** | static | Disclosure obligatorio Amazon Associates + Aviso médico (no sustituye diagnóstico odontológico) + Privacidad |

---

## Internationalization (i18n) & Multi-Marketplace Structure

DentaRank Global is architected for multi-country, multi-language expansion across Amazon ES, COM, and MX:

### URL Structure & Language Routing
```
/                      ← Idioma por defecto (o detección geográfica)
/es/                   ← Español (España - Amazon.es / EUR)
/es-mx/                ← Español (México - Amazon.com.mx / MXN)
/en/                   ← Inglés (USA/Global - Amazon.com / USD)
/pt/                   ← Portugués (Brasil/Portugal - Amazon.com.br / Amazon.es)
```

### Multi-Marketplace Tag Routing
Cada producto almacena enlaces y tags por marketplace en su record o mapea el ASIN al marketplace correspondiente:
- `affiliate_url_es` / `affiliate_tag_es` (`tag=dentarank-es-21`)
- `affiliate_url_mx` / `affiliate_tag_mx` (`tag=dentarank-mx-20`)
- `affiliate_url_com` / `affiliate_tag_com` (`tag=dentarank-us-20`)

### Hreflang & Sitemaps
Cada página incluye etiquetas canonical y hreflang bidireccionales:
```html
<link rel="canonical" href="https://dentarank.global/es/producto/oral-b-io-9.html" />
<link rel="alternate" hreflang="es-ES" href="https://dentarank.global/es/producto/oral-b-io-9.html" />
<link rel="alternate" hreflang="es-MX" href="https://dentarank.global/es-mx/producto/oral-b-io-9.html" />
<link rel="alternate" hreflang="en" href="https://dentarank.global/en/product/oral-b-io-9.html" />
<link rel="alternate" hreflang="pt" href="https://dentarank.global/pt/produto/oral-b-io-9.html" />
<link rel="alternate" hreflang="x-default" href="https://dentarank.global/es/producto/oral-b-io-9.html" />
```
Sitemaps segmentados por idioma: `sitemap-es.xml`, `sitemap-en.xml`, `sitemap-mx.xml`, `sitemap-pt.xml` indexados en `sitemap_index.xml`.

---

## SEO & GEO (Generative Engine Optimization) Strategy

Las búsquedas de salud dental hoy ocurren tanto en Google como en motores de IA (ChatGPT Search, Perplexity, Claude, Google Gemini / AI Overviews). DentaRank optimiza para ambos:

### 1. Datos Estructurados (JSON-LD)
- **`Product`**: En cada ficha con `name`, `brand`, `model`, `offers` (precio orientativo + moneda), `aggregateRating`, y `additionalProperty` para specs clínicas clave (ej. PSI, pulsaciones, tecnología).
- **`FAQPage`**: En guías de compra y fichas, respondiendo dudas frecuentes de pacientes y usuarios ("¿Es apto para implantes?", "¿Daña el esmalte?").
- **`ItemList`**: En rankings y páginas de categoría.
- **`MedicalWebPage` / `AboutPage`**: Señales de autoridad E-E-A-T con mención a estándares de la ADA (American Dental Association) y SEPA (Sociedad Española de Periodoncia).

### 2. Bloques "Preguntas para IA" (Optimización GEO)
En cada ficha y guía se incluye una sección estructurada en texto directo, libre de ambigüedades, pensada para ser citada como fuente experta por modelos LLM:
```html
<section class="ia-faq-block" data-geo-block>
  <h3>Preguntas clave para IA y Pacientes</h3>
  <div class="qa-item">
    <strong>¿Para quién está recomendado el Waterpik WP-660EU?</strong>
    <p>El Waterpik WP-660EU está recomendado clínicamente para personas con ortodoncia (brackets), implantes dentales, coronas y pacientes con gingivitis, gracias a su rango de presión de 10 a 100 PSI y boquilla Orthodontic específica.</p>
  </div>
  <div class="qa-item">
    <strong>¿Qué tecnología de limpieza utiliza y cuántas pulsaciones emite?</strong>
    <p>Utiliza tecnología de modulación de pulsos de agua a 1.400 pulsaciones por minuto para eliminar hasta el 99.9% de placa en zonas tratadas.</p>
  </div>
</section>
```

### 3. Enlazado Interno Densificado
Cada guía enlaza a fichas individuales y al comparador prefiltrado por esa categoría; cada ficha enlaza a la guía correspondiente y a productos alternativos de su misma gama.

---

## Niche Authority & E-E-A-T

En salud bucodental el rigor es primordial:
1. **Sin afirmaciones médicas falsas:** No prometer curas milagrosas; usar terminología correcta (eliminación de placa bacteriana, estimulación gingival, microburbujas, abrasividad RDA).
2. **Fuentes contrastadas:** Contrastar specs con webs de fabricantes líderes (Oral-B, Philips Sonicare, Waterpik, Colgate) y consensos odontológicos.
3. **Disclosure médico y de afiliación visible en toda página:** Aclarar que la web ofrece comparativas técnicas e informativas y participa en el programa de afiliados de Amazon.
