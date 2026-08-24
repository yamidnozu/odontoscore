import json
from pathlib import Path

ROOT = Path("c:/Proyectos/bussiness/store-odontologia")
with open(ROOT / "datos" / "productos.json", "r", encoding="utf-8") as f:
    products = json.load(f)

# Build ItemList Schema for all 50 products
item_list_elements = []
for idx, p in enumerate(products):
    img = p.get("images", [""])[0] if p.get("images") else ""
    item_list_elements.append({
        "@type": "ListItem",
        "position": idx + 1,
        "item": {
            "@type": "Product",
            "name": p.get("name"),
            "image": img,
            "description": p.get("description", p.get("name")),
            "brand": {
                "@type": "Brand",
                "name": p.get("marca", "OdontoScore")
            },
            "offers": {
                "@type": "Offer",
                "priceCurrency": "EUR",
                "price": str(p.get("precio", "0.00")),
                "availability": "https://schema.org/InStock",
                "url": f"https://odontoscore.com/producto/{p.get('id')}.html"
            }
        }
    })

item_list_schema = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "itemListElement": item_list_elements
}

# Generate semantic noscript catalogue for search bots
noscript_items = []
for p in products:
    noscript_items.append(f"""
      <article class="bot-product-item" style="margin-bottom:1rem;">
        <h3><a href="producto/{p.get('id')}.html">{p.get('name')}</a></h3>
        <p><strong>Marca:</strong> {p.get('marca')} | <strong>Precio:</strong> {p.get('precio')} € | <strong>Categoría:</strong> {p.get('categoria')}</p>
        <p>{p.get('description', '')}</p>
      </article>""")

noscript_html = "\n".join(noscript_items)

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <!-- Primary SEO Meta Tags -->
  <title>OdontoScore — Portal Odontológico 2026: Catálogo Clínico, Estudiantes y Comparador</title>
  <meta name="title" content="OdontoScore — Portal Odontológico 2026: Catálogo Clínico, Estudiantes y Comparador">
  <meta name="description" content="Catálogo y comparativa de material odontológico 2026: tipodontos para estudiantes, cepillos eléctricos Oral-B iO y Philips Sonicare, irrigadores dentales Waterpik, kits de sutura y lámparas LED al mejor precio internacional.">
  <meta name="keywords" content="odontologia, tipodonto dental, kit sutura odontologia, cepillos electricos oral-b io, philips sonicare, irrigador dental waterpik, blanqueamiento dental led, cera ortodoncia brackets, instrumental dental autoclave">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="author" content="OdontoScore">

  <!-- Canonical & Geo Hreflang Tags for Multi-Country Indexing -->
  <link rel="canonical" href="https://odontoscore.com/" />
  <link rel="alternate" hreflang="es" href="https://odontoscore.com/" />
  <link rel="alternate" hreflang="es-ES" href="https://odontoscore.com/" />
  <link rel="alternate" hreflang="es-CO" href="https://odontoscore.com/" />
  <link rel="alternate" hreflang="es-MX" href="https://odontoscore.com/" />
  <link rel="alternate" hreflang="es-AR" href="https://odontoscore.com/" />
  <link rel="alternate" hreflang="es-PE" href="https://odontoscore.com/" />
  <link rel="alternate" hreflang="es-CL" href="https://odontoscore.com/" />
  <link rel="alternate" hreflang="es-US" href="https://odontoscore.com/" />
  <link rel="alternate" hreflang="x-default" href="https://odontoscore.com/" />

  <!-- Geographic Meta Tags -->
  <meta name="geo.region" content="ES;CO;MX;AR;PE;CL;US">
  <meta name="geo.position" content="40.4168;-3.7038">
  <meta name="ICBM" content="40.4168, -3.7038">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://odontoscore.com/">
  <meta property="og:title" content="OdontoScore — Portal Odontológico 2026: Catálogo Clínico y Comparador">
  <meta property="og:description" content="Análisis técnico, precios multi-tienda y comparativas en 7 ejes de equipamiento dental y preclínico universitario.">
  <meta property="og:image" content="https://odontoscore.com/assets/img/logo-odontoscore.svg">
  <meta property="og:locale" content="es_ES">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:url" content="https://odontoscore.com/">
  <meta name="twitter:title" content="OdontoScore — Portal Odontológico 2026">
  <meta name="twitter:description" content="Portal especializado en dispositivos odontológicos, zona universitaria y comparador en 7 ejes.">
  <meta name="twitter:image" content="https://odontoscore.com/assets/img/logo-odontoscore.svg">

  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css?v=20260823_v53">

  <!-- Structured Data: WebSite & SearchAction -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "OdontoScore",
    "url": "https://odontoscore.com/",
    "potentialAction": {{
      "@type": "SearchAction",
      "target": "https://odontoscore.com/#catalogo?q={{search_term_string}}",
      "query-input": "required name=search_term_string"
    }}
  }}
  </script>

  <!-- Structured Data: Organization -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "OdontoScore",
    "url": "https://odontoscore.com",
    "logo": "https://odontoscore.com/assets/img/logo-odontoscore.svg",
    "description": "Portal odontológico independiente de análisis técnico, catálogo clínico y comparativas en 7 ejes."
  }}
  </script>

  <!-- Structured Data: ItemList (50 Verified Products) -->
  <script type="application/ld+json">
  {json.dumps(item_list_schema, indent=2, ensure_ascii=False)}
  </script>

  <!-- Structured Data: FAQPage -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {{
        "@type": "Question",
        "name": "¿Qué tipodonto se recomienda para prácticas universitarias de odontología?",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "Para prácticas preclínicas se recomiendan modelos con 28 o 32 dientes anatómicos atornillables con encía blanda de silicona, compatibles con articuladores estándar."
        }}
      }},
      {{
        "@type": "Question",
        "name": "¿Qué es más recomendable: cepillo sónico o rotatorio magnético?",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "El sistema rotatorio magnético (Oral-B iO) destaca por su precisión diente a diente, mientras que el sónico (Philips Sonicare) es el más suave para encías sensibles y recesión periodontal."
        }}
      }},
      {{
        "@type": "Question",
        "name": "¿Los productos tienen garantía oficial?",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "Sí, todos los productos enlazados cuentan con garantía oficial europea de 3 años y devoluciones seguras a través de distribuidores oficiales y Amazon Prime."
        }}
      }},
      {{
        "@type": "Question",
        "name": "¿Cómo comparar precios de material dental entre Amazon, Mercado Libre y AliExpress?",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "OdontoScore ofrece un comparador multi-tienda automático que cotiza en tiempo real en Amazon España, Amazon USA, Mercado Libre regional y AliExpress, convirtiendo los precios a tu moneda local."
        }}
      }}
    ]
  }}
  </script>
</head>
<body>

<!-- Header -->
<header class="site-header" id="siteHeader">
  <div class="container nav-wrapper">
    <a href="index.html" class="brand-logo" title="OdontoScore - Portal Odontológico">
      <img src="assets/img/logo-odontoscore.svg" alt="OdontoScore" height="40">
    </a>
    <button type="button" class="mobile-menu-toggle" id="mobileMenuBtn" aria-label="Menú">
      <span></span><span></span><span></span>
    </button>
    <nav class="main-nav" id="mainNav">
      <ul class="nav-links">
        <li><a href="#catalogo" data-nav="catalogo">Catálogo</a></li>
        <li><a href="#estudiantes" data-nav="estudiantes">Estudiantes</a></li>
        <li><a href="#comparador" data-nav="comparador">Comparador</a></li>
        <li><a href="#ofertas" data-nav="ofertas">Ofertas</a></li>
        <li><a href="#faq" data-nav="faq">FAQ</a></li>
      </ul>
      <div class="nav-actions">
        <div class="currency-selector-wrapper">
          <select id="globalCurrencySelect" class="currency-select" aria-label="Seleccionar País y Moneda">
            <option value="EUR" data-symbol="€" data-flag="🇪🇸">🇪🇸 EUR (€)</option>
            <option value="COP" data-symbol="$" data-flag="🇨🇴">🇨🇴 COP ($)</option>
            <option value="MXN" data-symbol="$" data-flag="🇲🇽">🇲🇽 MXN ($)</option>
            <option value="USD" data-symbol="$" data-flag="🇺🇸">🇺🇸 USD ($)</option>
            <option value="PEN" data-symbol="S/." data-flag="🇵🇪">🇵🇪 PEN (S/.)</option>
            <option value="ARS" data-symbol="$" data-flag="🇦🇷">🇦🇷 ARS ($)</option>
            <option value="CLP" data-symbol="$" data-flag="🇨🇱">🇨🇱 CLP ($)</option>
            <option value="GBP" data-symbol="£" data-flag="🇬🇧">🇬🇧 GBP (£)</option>
          </select>
        </div>
        <a href="#comparador" class="btn-nav-compare">
          <span>Comparar Modelos</span>
        </a>
      </div>
    </nav>
  </div>
</header>

<!-- Hero Section -->
<section class="hero-section">
  <div class="container hero-grid">
    <div class="hero-content">
      <div class="hero-badge">Panel Odontológico Independiente 2026</div>
      <h1 class="hero-title">Análisis Técnico y Catálogo Odontológico <span>Profesional</span></h1>
      <p class="hero-subtitle">Dispositivos de higiene bucodental, equipamiento preclínico para estudiantes universitarios e instrumental médico evaluados bajo criterios objetivos de rendimiento y precio.</p>
      <div class="hero-actions">
        <a href="#catalogo" class="btn-primary">Ver Catálogo Completo</a>
        <a href="#estudiantes" class="btn-secondary">Zona Estudiantes</a>
      </div>
      <div class="hero-trust-bullets">
        <span>✓ Enlaces y fotos reales verificadas</span>
        <span>✓ Radar de rendimiento en 7 ejes</span>
        <span>✓ Vídeos oficiales de fabricantes</span>
      </div>
    </div>
    <div class="hero-visual">
      <img src="assets/img/hero-dental.svg" alt="OdontoScore Portal Odontológico" fetchpriority="high">
    </div>
  </div>
</section>

<!-- 1. Catálogo Unificado -->
<section id="catalogo" class="section-block">
  <div class="container">
    <div class="section-header">
      <div class="hero-badge">Catálogo Clínico y Académico</div>
      <h2 class="section-title">Dispositivos y Material Odontológico</h2>
      <p class="section-desc">Filtra por especialidad, busca por palabra clave o consulta el análisis técnico detallado con comparativa multi-tienda.</p>
    </div>

    <div class="catalog-toolbar-wrapper">
      <div class="catalog-search-row">
        <input type="text" id="catalogSearchInput" class="catalog-search-input" placeholder="Buscar por producto, marca o especificación (ej: tipodonto, Oral-B, sutura, Waterpik)...">
        <select id="catalogSortSelect" class="catalog-sort-select" aria-label="Ordenar productos">
          <option value="has-video">🎬 Con Vídeo Primero</option>
          <option value="featured">Ordenar: Más Recomendados</option>
          <option value="price-asc">Precio: Menor a Mayor</option>
          <option value="price-desc">Precio: Mayor a Menor</option>
          <option value="score">Mayor Puntuación Clínica</option>
        </select>
        <div class="view-toggle-group">
          <button type="button" class="view-toggle-btn active" id="btnViewGrid">Cuadrícula</button>
          <button type="button" class="view-toggle-btn" id="btnViewList">Lista</button>
        </div>
      </div>

      <div class="filter-pills-bar" id="filterPillsBar" data-catalog-filters>
        <!-- Dynamic Filter Pills -->
      </div>
    </div>

    <div class="product-grid" id="mainProductGrid">
      <div class="skeleton-card"></div>
      <div class="skeleton-card"></div>
      <div class="skeleton-card"></div>
      <div class="skeleton-card"></div>
      <div class="skeleton-card"></div>
      <div class="skeleton-card"></div>
    </div>

    <noscript>
      <div class="noscript-catalog-seo" style="margin-top:2rem;">
        <h2>Catálogo de Productos Odontológicos Disponibles</h2>
        {noscript_html}
      </div>
    </noscript>
  </div>
</section>

<!-- 2. Zona Estudiantes -->
<section id="estudiantes" class="section-block section-alt">
  <div class="container">
    <div class="section-header">
      <div class="hero-badge">Grado en Odontología</div>
      <h2 class="section-title">Zona Estudiantes y Prácticas Preclínicas</h2>
      <p class="section-desc">Modelos anatómicos de tipodonto, kits de sutura con almohadilla de silicona e instrumental básico para laboratorio.</p>
    </div>
    <div class="product-grid" id="studentGrid">
      <div class="skeleton-card"></div>
      <div class="skeleton-card"></div>
      <div class="skeleton-card"></div>
    </div>
  </div>
</section>

<!-- 3. Comparador Clínico -->
<section id="comparador" class="section-block" data-comparator-app>
  <div class="container">
    <div class="section-header">
      <div class="hero-badge">Herramienta Técnica</div>
      <h2 class="section-title">Comparador de Rendimiento en 7 Ejes</h2>
      <p class="section-desc">Compara métricas objetivas de potencia, autonomía, ergonomía y relación calidad-precio entre hasta 4 modelos.</p>
    </div>

    <div class="comparator-controls">
      <div class="comparator-select-row">
        <label for="compCategorySelect">Categoría a comparar:</label>
        <select id="compCategorySelect">
          <option value="cepillos_electricos">Cepillos Eléctricos</option>
          <option value="irrigadores_dentales">Irrigadores Dentales</option>
          <option value="estudiantes_practicas">Estudiantes y Prácticas</option>
          <option value="blanqueamiento_dental">Blanqueamiento Dental</option>
          <option value="ortodoncia_brackets">Ortodoncia y Brackets</option>
          <option value="instrumental_basico">Instrumental y Clínica</option>
        </select>
      </div>
      <div class="comparator-checks" id="compProductChecks"></div>
    </div>

    <div class="radar-section-box">
      <h3>Evaluación Comparativa Multidimensional</h3>
      <div class="radar-legend" id="compRadarLegend"></div>
      <div class="radar-canvas-container" id="compRadarCanvas"></div>
    </div>

    <div class="matrix-wrapper" id="compMatrixContent"></div>
  </div>
</section>

<!-- 4. Ofertas y Oportunidades -->
<section id="ofertas" class="section-block section-alt">
  <div class="container">
    <div class="section-header">
      <div class="hero-badge">Descuentos Verificados</div>
      <h2 class="section-title">Ofertas y Oportunidades de Compra</h2>
      <p class="section-desc">Dispositivos y equipamiento con bajadas de precio respecto a su PVP de referencia.</p>
    </div>
    <div class="product-grid" id="dealsGrid">
      <div class="skeleton-card"></div>
      <div class="skeleton-card"></div>
      <div class="skeleton-card"></div>
    </div>
  </div>
</section>

<!-- 5. FAQ -->
<section id="faq" class="section-block">
  <div class="container">
    <div class="section-header">
      <div class="hero-badge">Guía y Soporte Clínico</div>
      <h2 class="section-title">Preguntas Frecuentes de la Comunidad</h2>
      <p class="section-desc">Respuestas basadas en evidencia clínica sobre elección de material y dispositivos.</p>
    </div>

    <div class="faq-accordion" style="max-width:860px;margin:0 auto;">
      <details class="faq-item">
        <summary class="faq-question">¿Qué tipodonto se recomienda para prácticas universitarias de odontología?</summary>
        <div class="faq-answer">
          <p>Para prácticas preclínicas se recomiendan modelos con 28 o 32 dientes anatómicos atornillables con encía blanda de silicona, compatibles con articuladores estándar (como Nissin o Frasaco).</p>
        </div>
      </details>
      <details class="faq-item">
        <summary class="faq-question">¿Qué es más recomendable: cepillo sónico o rotatorio magnético?</summary>
        <div class="faq-answer">
          <p>El sistema rotatorio magnético (Oral-B iO) destaca por su precisión diente a diente y eliminación de placa por microvibraciones, mientras que el sónico (Philips Sonicare) es el más suave para encías sensibles y recesión periodontal.</p>
        </div>
      </details>
      <details class="faq-item">
        <summary class="faq-question">¿Los productos tienen garantía oficial?</summary>
        <div class="faq-answer">
          <p>Sí, todos los productos enlazados cuentan con garantía oficial europea de 3 años y devoluciones seguras a través de Amazon Prime y distribuidores certificados.</p>
        </div>
      </details>
      <details class="faq-item">
        <summary class="faq-question">¿Cómo se calculan las puntuaciones del radar de 7 ejes?</summary>
        <div class="faq-answer">
          <p>Las puntuaciones se basan en especificaciones técnicas de laboratorio: presión en PSI, oscilaciones/minuto, decibelios de ruido, autonomía de batería y certificaciones de biocompatibilidad.</p>
        </div>
      </details>
      <details class="faq-item">
        <summary class="faq-question">¿Cómo comparar precios entre Amazon, Mercado Libre y AliExpress?</summary>
        <div class="faq-answer">
          <p>OdontoScore cuenta con un motor multi-tienda integrado que calcula la equivalencia en divisas en tiempo real (EUR, COP, MXN, USD, PEN, ARS, CLP) y resalta el mejor precio con enlace directo de compra segura.</p>
        </div>
      </details>
    </div>
  </div>
</section>

<!-- Footer -->
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col">
        <div class="brand-logo" style="margin-bottom:0.75rem;">
          <img src="assets/img/logo-odontoscore.svg" alt="OdontoScore" height="36">
        </div>
        <p style="font-size:0.85rem;color:#64748B;line-height:1.6;">Portal técnico odontológico independiente. Análisis de equipamiento clínico, material preclínico para estudiantes y dispositivos de salud bucodental.</p>
      </div>
      <div class="footer-col">
        <h4>Especialidades</h4>
        <ul class="footer-links">
          <li><a href="#catalogo">Estudiantes y Prácticas</a></li>
          <li><a href="#catalogo">Cepillos Eléctricos</a></li>
          <li><a href="#catalogo">Irrigadores Dentales</a></li>
          <li><a href="#catalogo">Blanqueamiento Dental</a></li>
          <li><a href="#catalogo">Ortodoncia y Brackets</a></li>
          <li><a href="#catalogo">Instrumental Clínico</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Herramientas</h4>
        <ul class="footer-links">
          <li><a href="#comparador">Comparador de 7 Ejes</a></li>
          <li><a href="#ofertas">Ofertas y Descuentos</a></li>
          <li><a href="guias/mejor-irrigador-dental-brackets-2026.html">Guía Irrigadores</a></li>
          <li><a href="guias/mejor-cepillo-electrico-encias-sensibles-2026.html">Guía Encías Sensibles</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Transparencia</h4>
        <ul class="footer-links">
          <li><a href="aviso-afiliados.html">Aviso de Afiliación</a></li>
          <li><a href="privacidad.html">Privacidad y Cookies</a></li>
          <li><a href="sobre-nosotros.html">Metodología OdontoScore</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-disclaimers">
      <p><strong>Aviso de Afiliación:</strong> En calidad de Afiliado de Amazon y plataformas asociadas, obtenemos ingresos por las compras adscritas que cumplen los requisitos aplicables.</p>
      <p><strong>Descargo de Responsabilidad Médica:</strong> Los análisis y comparativas de OdontoScore tienen carácter informativo y divulgativo. No constituyen diagnóstico ni prescripción médica individualizada.</p>
    </div>
    <div class="footer-bottom-copy">
      © 2026 OdontoScore (odontoscore.com). Todos los derechos reservados.
    </div>
  </div>
</footer>

<!-- Quick-View Modal with Video & Multi-Store -->
<div class="quick-modal-backdrop" id="quickViewModal">
  <div class="quick-modal-box">
    <button type="button" class="quick-modal-close-btn" aria-label="Cerrar">&times;</button>
    <span id="modalBrand" class="card-brand-tag" style="display:inline-block;margin-bottom:0.25rem;">Marca</span>
    <h2 id="modalTitle" class="modal-title">Nombre del Producto</h2>
    <div class="modal-price" id="modalPrice">0,00 €</div>

    <div class="quick-modal-grid">
      <div>
        <div id="modalVideoWrapper" class="modal-video-wrapper"></div>
        <div class="modal-gallery-main">
          <img id="modalImg" src="" alt="Vista previa">
        </div>
        <div class="modal-thumbs-row" id="modalThumbsRow"></div>
        <div class="radar-canvas-container" id="modalRadarCanvas"></div>
      </div>
      <div>
        <h4 class="modal-specs-heading">Ficha Técnica y Prestaciones</h4>
        <table class="specs-table" id="modalSpecsTable">
          <tbody></tbody>
        </table>
        <div class="modal-actions">
          <a id="modalBuyBtn" href="#" target="_blank" rel="sponsored nofollow noopener" class="btn-buy-amazon-large">
            <span>Ver Oferta en Amazon</span>
          </a>
          <a id="modalFullLink" href="#" target="_blank" class="btn-secondary modal-full-link">
            <span>Ver Ficha Completa</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

<script defer src="main.js?v=20260823_v53"></script>
</body>
</html>
"""

with open(ROOT / "index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[OK] index.html written with rich ItemList Schema ({len(products)} products), GEO hreflangs, and noscript feed.")
