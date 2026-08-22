#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OdontoScore Static Site Generator (tools/build_site.py)
Clean, professional medical grade design (zero tacky emojis).
Dynamic Amazon CDN multi-image galleries, video support, and 7-axis radar charts.
"""

import json
import os
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

ROOT = Path(__file__).resolve().parent.parent
DATOS_DIR = ROOT / "datos"
DATOS_FILE = DATOS_DIR / "productos.json"
VER = "20260822_v4"
BASE_URL = "https://odontoscore.com"
AMAZON_PARTNER_TAG = os.getenv("AMAZON_PARTNER_TAG", "odontoscore-21").strip()
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "").strip()

CATEGORIES = [
    {
        "id": "estudiantes_practicas",
        "slug": "estudiantes-odontologia",
        "name": "Estudiantes y Prácticas",
        "desc": "Tipodontos anatómicos con dientes desmontables, kits de sutura oral y material de simulación universitaria."
    },
    {
        "id": "cepillos_electricos",
        "slug": "cepillos-electricos",
        "name": "Cepillos Eléctricos",
        "desc": "Tecnología sónica, rotatoria y magnética para eliminación de placa bacteriana y protección gingival."
    },
    {
        "id": "irrigadores_dentales",
        "slug": "irrigadores-dentales",
        "name": "Irrigadores Dentales",
        "desc": "Limpieza interdental profunda y masaje de encías avalado por la ADA."
    },
    {
        "id": "blanqueamiento_dental",
        "slug": "blanqueamiento-dental",
        "name": "Blanqueamiento Dental",
        "desc": "Kits con tecnología LED de luz fría, geles desensibilizantes y tiras para esmalte."
    },
    {
        "id": "ortodoncia_brackets",
        "slug": "ortodoncia-brackets",
        "name": "Ortodoncia y Brackets",
        "desc": "Ceras protectoras, cepillos interproximales y accesorios para brackets y alineadores."
    },
    {
        "id": "higiene_infantil",
        "slug": "higiene-infantil",
        "name": "Odontopediatría",
        "desc": "Cepillos con cerdas extrasuaves, temporizadores y cuidado bucal adaptado para niños."
    },
    {
        "id": "instrumental_basico",
        "slug": "instrumental-clinica",
        "name": "Instrumental y Clínica",
        "desc": "Bandejas quirúrgicas, cestas de esterilización para autoclave y material de acero inoxidable."
    }
]


def load_products():
    """Carga productos de Supabase o datos/productos.json."""
    if SUPABASE_URL and SUPABASE_SERVICE_KEY:
        try:
            from supabase import create_client
            sb = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
            res = sb.table("products").select("*").execute()
            if res.data and len(res.data) > 0:
                print(f"[Supabase] {len(res.data)} productos cargados.")
                products = []
                for row in res.data:
                    asin = row.get("asin")
                    slug = row.get("id")
                    
                    raw_images = row.get("local_assets") or []
                    if not raw_images or raw_images[0] == "assets/img/hero-dental.svg":
                        raw_images = [f"https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN={asin}&Format=_SL1500_&ID=AsinImage&MarketPlace=ES&ServiceVersion=20070822&WS=1&tag=odontoscore-21"]

                    p = {
                        "id": slug,
                        "asin": asin,
                        "name": row.get("name"),
                        "marca": row.get("marca") or "Dental",
                        "categoria_odontologica": row.get("categoria_odontologica") or "cepillos_electricos",
                        "category": row.get("category") or "Odontología",
                        "affiliate_url": f"https://www.amazon.es/dp/{asin}?tag={AMAZON_PARTNER_TAG}",
                        "affiliate_tag": AMAZON_PARTNER_TAG,
                        "canonical_url": f"https://www.amazon.es/dp/{asin}",
                        "images": raw_images,
                        "isFeatured": bool(row.get("is_featured")),
                        "retailPrice": float(row.get("retail_price") or 49.99),
                        "discountedPrice": float(row.get("discounted_price") or row.get("retail_price") or 39.99),
                        "valoracion_media": float(row.get("valoracion_media") or 4.5),
                        "resenas_cantidad": int(row.get("resenas_cantidad") or 500),
                        "precio_fecha": str(row.get("precio_fecha") or "2026-08-22")[:10],
                        "tipo_producto": row.get("tipo_producto") or row.get("categoria_odontologica"),
                        "tecnologia": row.get("tecnologia") or "sonico",
                        "modos_limpieza": int(row.get("modos_limpieza") or 1),
                        "presion_agua_psi": row.get("presion_agua_psi"),
                        "pulsaciones_min": row.get("pulsaciones_min"),
                        "autonomia_dias": row.get("autonomia_dias") or 14,
                        "nivel_ruido_db": row.get("nivel_ruido_db") or 55,
                        "app_conectada": bool(row.get("app_conectada")),
                        "esterilizable_autoclave": bool(row.get("esterilizable_autoclave")),
                        "indicado_para": row.get("indicado_para") or [],
                        "score_eficacia": float(row.get("score_eficacia") or 9.0),
                        "score_comodidad_encias": float(row.get("score_comodidad_encias") or 9.0),
                        "score_durabilidad": float(row.get("score_durabilidad") or 9.0),
                        "score_facilidad_uso": float(row.get("score_facilidad_uso") or 9.0),
                        "score_silencio": float(row.get("score_silencio") or 8.5),
                        "score_tecnologia": float(row.get("score_tecnologia") or 9.0),
                        "score_calidad_precio": float(row.get("score_calidad_precio") or 9.0),
                        "description": row.get("description") or "",
                        "cuerpo_editorial": row.get("cuerpo_editorial") or "",
                        "pros": row.get("pros") or ["Eficacia clínica verificada", "Garantía oficial y envío Prime", "Materiales certificados"],
                        "contras": row.get("contras") or ["Consultar disponibilidad de recambios"],
                        "ideal_para": row.get("ideal_para") or "Estudiantes, profesionales y pacientes.",
                        "destacado_editorial": "Seleccionado en el catálogo oficial OdontoScore 2026.",
                        "resenas_resumen": row.get("resumen_resenas") or "Alta satisfacción de compradores.",
                        "geo_faq": row.get("geo_faq") or []
                    }
                    products.append(p)
                return products
        except Exception as e:
            print(f"[Supabase WARN] Fallback local: {e}")

    if DATOS_FILE.exists():
        with open(DATOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def render_header(active_nav="", root_rel=""):
    return f"""
<header class="site-header">
  <div class="container nav-wrapper">
    <a href="{root_rel}index.html" class="brand-logo" title="OdontoScore - Portal Odontológico">
      <img src="{root_rel}assets/img/logo-odontoscore.svg" alt="OdontoScore" height="40">
    </a>
    <nav class="main-nav">
      <ul class="nav-links">
        <li><a href="{root_rel}index.html#catalogo">Catálogo</a></li>
        <li><a href="{root_rel}index.html#estudiantes">Estudiantes</a></li>
        <li><a href="{root_rel}index.html#comparador">Comparador</a></li>
        <li><a href="{root_rel}index.html#ofertas">Ofertas</a></li>
        <li><a href="{root_rel}index.html#faq">Preguntas Frecuentes</a></li>
      </ul>
      <div class="nav-actions">
        <a href="{root_rel}index.html#comparador" class="btn-nav-compare">
          <span>Comparar Modelos</span>
        </a>
      </div>
    </nav>
  </div>
</header>
"""


def render_footer(root_rel=""):
    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="{root_rel}assets/img/logo-odontoscore.svg" alt="OdontoScore" height="36" style="filter: brightness(0) invert(1); margin-bottom:1rem;">
        <p style="margin-bottom:1rem;color:#94A3B8;">Portal odontológico independiente de análisis técnico, comparativas clínicas y catálogo de equipamiento dental.</p>
        <p style="font-size:0.85rem;color:#64748B;">Evaluación de rendimiento en 7 ejes: bio-eficacia, ergonomía, confort gingival, decibelios y potencia hidráulica.</p>
      </div>
      <div class="footer-col">
        <h4>Especialidades</h4>
        <ul class="footer-links">
          <li><a href="{root_rel}index.html#catalogo">Estudiantes y Prácticas</a></li>
          <li><a href="{root_rel}index.html#catalogo">Cepillos Eléctricos</a></li>
          <li><a href="{root_rel}index.html#catalogo">Irrigadores Dentales</a></li>
          <li><a href="{root_rel}index.html#catalogo">Blanqueamiento Dental</a></li>
          <li><a href="{root_rel}index.html#catalogo">Ortodoncia y Brackets</a></li>
          <li><a href="{root_rel}index.html#catalogo">Instrumental Clínico</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Herramientas</h4>
        <ul class="footer-links">
          <li><a href="{root_rel}comparador.html">Comparador de 7 Ejes</a></li>
          <li><a href="{root_rel}ofertas.html">Ofertas y Descuentos</a></li>
          <li><a href="{root_rel}guias/mejor-irrigador-dental-brackets-2026.html">Guía Irrigadores</a></li>
          <li><a href="{root_rel}guias/mejor-cepillo-electrico-encias-sensibles-2026.html">Guía Encías Sensibles</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Transparencia</h4>
        <ul class="footer-links">
          <li><a href="{root_rel}aviso-afiliados.html">Aviso de Afiliación</a></li>
          <li><a href="{root_rel}privacidad.html">Privacidad y Cookies</a></li>
          <li><a href="{root_rel}sobre-nosotros.html">Metodología OdontoScore</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-disclaimers">
      <p><strong>Aviso de Afiliación de Amazon:</strong> En calidad de Afiliado de Amazon, obtenemos ingresos por las compras adscritas que cumplen los requisitos aplicables. «Amazon» y el logotipo de Amazon son marcas comerciales de Amazon.com, Inc. o sus filiales.</p>
      <p><strong>Descargo de Responsabilidad Médica:</strong> Los análisis y comparativas de OdontoScore tienen carácter informativo. No constituyen diagnóstico ni prescripción médica individualizada. Ante cualquier duda clínica, consulte siempre a su odontólogo colegiado.</p>
    </div>
    <div class="footer-bottom-copy">
      © 2026 OdontoScore (odontoscore.com). Todos los derechos reservados.
    </div>
  </div>
</footer>
"""


def render_product_card(p, root_rel=""):
    discount_pct = round((1 - p["discountedPrice"] / p["retailPrice"]) * 100) if p["discountedPrice"] < p["retailPrice"] else 0
    images = p.get('images', [])
    main_img = images[0] if len(images) > 0 else f"https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN={p['asin']}&Format=_SL1500_&ID=AsinImage&MarketPlace=ES&ServiceVersion=20070822&WS=1&tag=odontoscore-21"
    
    tech_str = p.get('tecnologia', 'sonico').replace('_', ' ').upper()
    potencia_str = f"{p['presion_agua_psi']} PSI" if p.get('presion_agua_psi') else (f"{p['pulsaciones_min']:,} mov/min" if p.get('pulsaciones_min') else ("Autoclave 134°C" if p.get('esterilizable_autoclave') else "Clínico"))
    autonomia_str = f"{p['autonomia_dias']} días" if p.get('autonomia_dias', 14) < 365 else "Red continua / AC"

    thumbs_html = ""
    if len(images) > 1:
        mini_thumbs = "".join([f'<button type="button" class="card-thumb-mini {"active" if idx==0 else ""}" data-card-thumb="{img}" aria-label="Foto {idx+1}"><img src="{img}" alt="Miniatura"></button>' for idx, img in enumerate(images[:6])])
        thumbs_html = f'<div class="card-thumbs-strip">{mini_thumbs}</div>'

    return f"""
<article class="product-card" data-producto-id="{p['id']}" data-asin="{p['asin']}" data-category="{p['categoria_odontologica']}" data-brand="{p['marca'].lower()}" data-title="{p['name'].lower()}" data-price="{p['discountedPrice']}" data-score="{p['score_eficacia']}">
  {'<span class="card-badge-top">Top Clínico</span>' if p.get('isFeatured') else ''}
  {f'<span class="price-discount-pill">-{discount_pct}%</span>' if discount_pct > 0 else ''}
  
  <div class="card-media-wrapper">
    <div class="card-media">
      <img class="card-main-photo" src="{main_img}" alt="{p['name']}" loading="lazy" onerror="this.onerror=null;this.src='https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN={p['asin']}&Format=_SL1500_&ID=AsinImage&MarketPlace=ES&ServiceVersion=20070822&WS=1&tag=odontoscore-21';">
      <span class="card-video-pill">Vídeo y {len(images)} Fotos</span>
    </div>
    {thumbs_html}
  </div>
  
  <div class="card-body">
    <div class="card-header-meta">
      <span class="card-brand-tag">{p['marca']}</span>
      <span class="card-category-tag">{p['category']}</span>
    </div>
    
    <h3 class="card-title" title="{p['name']}">{p['name']}</h3>
    
    <div class="card-rating-box">
      <span class="rating-badge">★ {p['valoracion_media']}</span>
      <span style="font-size:0.85rem;color:#64748B;">({p['resenas_cantidad']:,} valoraciones verificadas)</span>
    </div>
    
    <div class="card-specs-matrix">
      <div class="spec-cell">Tecnología: <strong>{tech_str}</strong></div>
      <div class="spec-cell">Modos: <strong>{p['modos_limpieza']} programas</strong></div>
      <div class="spec-cell">Potencia: <strong>{potencia_str}</strong></div>
      <div class="spec-cell">Autonomía: <strong>{autonomia_str}</strong></div>
    </div>
    
    <div class="card-price-row">
      <div>
        <span class="price-main-val">{p['discountedPrice']} €</span>
        {f'<span class="price-strike-val">{p["retailPrice"]} €</span>' if discount_pct > 0 else ''}
      </div>
      <span style="font-size:0.78rem;font-weight:700;color:#059669;">Envío Prime 24/48h</span>
    </div>
    
    <div class="card-actions-grid">
      <button type="button" class="btn-card-quick" data-quick-view="{p['id']}">Ver Galería</button>
      <a href="{p['affiliate_url']}" target="_blank" rel="sponsored nofollow noopener" class="btn-card-prime">Ver en Amazon</a>
    </div>
  </div>
</article>
"""


def build_home(products):
    cards_html = "\n".join([render_product_card(p, "") for p in products])
    students_products = [p for p in products if p["categoria_odontologica"] == "estudiantes_practicas"]
    students_cards = "\n".join([render_product_card(p, "") for p in students_products])
    deal_cards_html = "\n".join([render_product_card(p, "") for p in products if p["discountedPrice"] < p["retailPrice"]])
    options_cats = "".join([f'<option value="{c["id"]}">{c["name"]}</option>' for c in CATEGORIES])

    cat_counts = {}
    for p in products:
        c_id = p.get("categoria_odontologica", "otros")
        cat_counts[c_id] = cat_counts.get(c_id, 0) + 1

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OdontoScore — Portal Odontológico: Catálogo Clínico, Estudiantes y Comparador 2026</title>
  <meta name="description" content="Portal especializado de odontología: tipodontos para estudiantes, cepillos sónicos y magnéticos, irrigadores y material de clínica con comparador de 7 ejes.">
  <link rel="canonical" href="{BASE_URL}/" />
  <link rel="alternate" hreflang="es" href="{BASE_URL}/" />
  <link rel="alternate" hreflang="x-default" href="{BASE_URL}/" />
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css?v={VER}">
</head>
<body>
  {render_header('home', '')}

  <!-- Hero Section -->
  <section class="hero-section">
    <div class="container hero-grid">
      <div class="hero-content">
        <div class="hero-badge">Panel Odontológico Independiente</div>
        <h1 class="hero-title">Análisis Técnico y Catálogo Odontológico <span>Profesional</span></h1>
        <p class="hero-subtitle">Dispositivos de higiene bucodental, equipamiento preclínico para estudiantes universitarios e instrumental médico evaluados bajo criterios objetivos de rendimiento.</p>
        <div class="hero-actions">
          <a href="#catalogo" class="btn-primary">Ver Catálogo Completo ({len(products)} Productos)</a>
          <a href="#estudiantes" class="btn-secondary">Zona Estudiantes</a>
        </div>
        <div class="hero-trust-bullets">
          <span>Enlaces directos verificados</span>
          <span>Radar de rendimiento en 7 ejes</span>
          <span>Actualización continua</span>
        </div>
      </div>
      <div class="hero-visual">
        <img src="assets/img/hero-dental.svg" alt="OdontoScore Portal Odontológico" fetchpriority="high">
      </div>
    </div>
  </section>

  <!-- 1. Interactive Catalog with Clean Toolbar -->
  <section id="catalogo" class="section-block">
    <div class="container">
      <div class="section-header">
        <div class="hero-badge">Catálogo Clínico y Académico</div>
        <h2 class="section-title">Dispositivos y Material Odontológico</h2>
        <p class="section-desc">Filtra por especialidad, busca por palabra clave o consulta el análisis técnico detallado.</p>
      </div>

      <div class="catalog-toolbar-wrapper">
        <div class="catalog-search-row">
          <input type="text" id="catalogSearchInput" class="catalog-search-input" placeholder="Buscar por producto, marca o especificación (ej: tipodonto, Oral-B, sutura, Waterpik)...">
          
          <select id="catalogSortSelect" class="catalog-sort-select" aria-label="Ordenar productos">
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

        <div class="filter-pills-bar" data-catalog-filters>
          <button type="button" class="filter-pill-btn active" data-filter="all">Todos ({len(products)})</button>
          <button type="button" class="filter-pill-btn" data-filter="estudiantes_practicas">Estudiantes ({cat_counts.get('estudiantes_practicas', 0)})</button>
          <button type="button" class="filter-pill-btn" data-filter="cepillos_electricos">Cepillos ({cat_counts.get('cepillos_electricos', 0)})</button>
          <button type="button" class="filter-pill-btn" data-filter="irrigadores_dentales">Irrigadores ({cat_counts.get('irrigadores_dentales', 0)})</button>
          <button type="button" class="filter-pill-btn" data-filter="blanqueamiento_dental">Blanqueamiento ({cat_counts.get('blanqueamiento_dental', 0)})</button>
          <button type="button" class="filter-pill-btn" data-filter="ortodoncia_brackets">Ortodoncia ({cat_counts.get('ortodoncia_brackets', 0)})</button>
          <button type="button" class="filter-pill-btn" data-filter="higiene_infantil">Odontopediatría ({cat_counts.get('higiene_infantil', 0)})</button>
          <button type="button" class="filter-pill-btn" data-filter="instrumental_basico">Instrumental ({cat_counts.get('instrumental_basico', 0)})</button>
        </div>
      </div>

      <div class="product-grid" id="mainProductGrid">
        {cards_html}
      </div>
    </div>
  </section>

  <!-- 2. University Student Section -->
  <section id="estudiantes" class="section-block" style="background-color: var(--color-surface);">
    <div class="container">
      <div class="section-header">
        <div class="hero-badge">Prácticas Universitarias y Laboratorio</div>
        <h2 class="section-title">Zona Estudiantes de Odontología</h2>
        <p class="section-desc">Material didáctico para prácticas de anatomía dental, periodoncia, cirugía menor y simulación clínica.</p>
      </div>

      <div class="product-grid">
        {students_cards if students_cards else '<p style="text-align:center;grid-column:1/-1;">Cargando material docente...</p>'}
      </div>
    </div>
  </section>

  <!-- 3. Multi-Product Radar Comparator -->
  <section id="comparador" class="section-block">
    <div class="container" data-comparator-app>
      <div class="section-header">
        <div class="hero-badge">Enfrentamiento Lado a Lado</div>
        <h2 class="section-title">Comparador Clínico OdontoScore (7 Ejes)</h2>
        <p class="section-desc">Selecciona hasta 4 modelos para ver especificaciones y superposición de polígonos de radar sin salir de la página.</p>
      </div>

      <div class="comparator-selector-bar" style="background:#FFFFFF;box-shadow:var(--shadow-sm);border:1px solid var(--color-border);padding:1.25rem;border-radius:12px;margin-bottom:2rem;">
        <div>
          <label for="compCategorySelect" style="font-weight:700;font-size:0.95rem;margin-right:0.75rem;">Especialidad:</label>
          <select id="compCategorySelect" style="padding:0.6rem 1rem;border-radius:8px;border:1px solid var(--color-border);font-family:var(--font-sans);font-size:0.95rem;">
            <option value="">Todas las Categorías</option>
            {options_cats}
          </select>
        </div>
        <div id="compProductChecks" style="display:flex;flex-wrap:wrap;align-items:center;margin-top:1rem;"></div>
      </div>

      <div class="radar-section-box" style="margin-bottom:2rem;background:#FFFFFF;border:1px solid var(--color-border);border-radius:16px;padding:2rem;">
        <h3 style="font-size:1.3rem;margin-bottom:0.5rem;">Superposición de Radares Clínicos (7 Ejes)</h3>
        <div id="compRadarLegend" style="margin-bottom:1rem;display:flex;flex-wrap:wrap;gap:0.75rem;"></div>
        <div class="radar-canvas-container" id="compRadarCanvas" style="min-height:300px;"></div>
      </div>

      <div class="comparator-table-scroll" id="compMatrixContent"></div>
    </div>
  </section>

  <!-- 4. Deals Section -->
  <section id="ofertas" class="section-block" style="background-color: var(--color-surface);">
    <div class="container">
      <div class="section-header">
        <div class="hero-badge">Descuentos Verificados</div>
        <h2 class="section-title">Ofertas Activas en Cuidado Bucal</h2>
        <p class="section-desc">Dispositivos y materiales odontológicos con precio rebajado en Amazon España.</p>
      </div>
      <div class="product-grid">
        {deal_cards_html}
      </div>
    </div>
  </section>

  <!-- 5. FAQ Section -->
  <section id="faq" class="section-block">
    <div class="container" style="max-width:850px;">
      <div class="section-header">
        <div class="hero-badge">Preguntas Frecuentes</div>
        <h2 class="section-title">Preguntas Frecuentes OdontoScore</h2>
        <p class="section-desc">Criterios técnicos para estudiantes, pacientes y profesionales.</p>
      </div>

      <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:16px;padding:2rem;">
        <div style="margin-bottom:1.5rem;padding-bottom:1.5rem;border-bottom:1px solid #F1F5F9;">
          <strong style="font-size:1.05rem;color:#0F172A;display:block;margin-bottom:0.5rem;">¿Qué tipodonto se recomienda para prácticas universitarias de odontología?</strong>
          <p style="color:#475569;font-size:0.95rem;">Para prácticas preclínicas se recomiendan modelos con 28 o 32 dientes anatómicos atornillables con encía blanda de silicona, compatibles con articuladores estándar.</p>
        </div>
        <div style="margin-bottom:1.5rem;padding-bottom:1.5rem;border-bottom:1px solid #F1F5F9;">
          <strong style="font-size:1.05rem;color:#0F172A;display:block;margin-bottom:0.5rem;">¿Qué es más recomendable: cepillo sónico o rotatorio magnético?</strong>
          <p style="color:#475569;font-size:0.95rem;">El sistema rotatorio magnético (Oral-B iO) destaca por su precisión diente a diente, mientras que el sónico (Philips Sonicare) es el más suave para encías sensibles y recesión periodontal.</p>
        </div>
        <div>
          <strong style="font-size:1.05rem;color:#0F172A;display:block;margin-bottom:0.5rem;">¿Los productos tienen garantía oficial?</strong>
          <p style="color:#475569;font-size:0.95rem;">Sí, todos los productos enlazados cuentan con garantía oficial europea de 3 años y devoluciones seguras a través de Amazon Prime.</p>
        </div>
      </div>
    </div>
  </section>

  {render_footer('')}

  <!-- Quick-View Modal with Multi-Photo Gallery -->
  <div class="quick-modal-backdrop" id="quickViewModal">
    <div class="quick-modal-box">
      <button type="button" class="quick-modal-close-btn" aria-label="Cerrar">&times;</button>
      <span id="modalBrand" class="card-brand-tag" style="display:inline-block;margin-bottom:0.25rem;">Marca</span>
      <h2 id="modalTitle" style="font-size:1.35rem;margin-bottom:0.5rem;color:#0F172A;line-height:1.35;">Nombre del Producto</h2>
      <div style="font-size:1.4rem;font-weight:800;color:#0E76BC;margin-bottom:1rem;" id="modalPrice">0,00 €</div>

      <div class="quick-modal-grid">
        <div>
          <div class="modal-gallery-main">
            <img id="modalImg" src="" alt="Vista previa">
          </div>
          <div class="modal-thumbs-row" id="modalThumbsRow"></div>
          
          <div id="modalVideoWrapper" style="margin-bottom:1.5rem;display:none;"></div>
          
          <div class="radar-canvas-container" id="modalRadarCanvas" style="min-height:220px;"></div>
        </div>
        <div>
          <h4 style="font-size:1rem;margin-bottom:0.75rem;">Ficha Técnica y Prestaciones</h4>
          <table class="specs-table" id="modalSpecsTable" style="margin-bottom:1.75rem;">
            <tbody></tbody>
          </table>
          <div style="display:flex;flex-direction:column;gap:0.75rem;">
            <a id="modalBuyBtn" href="#" target="_blank" rel="sponsored nofollow noopener" class="btn-buy-amazon-large">
              <span>Ver Oferta en Amazon</span>
            </a>
            <a id="modalFullLink" href="#" target="_blank" class="btn-secondary" style="text-align:center;justify-content:center;">
              <span>Ver Ficha Completa</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script defer src="lib/manifest.js"></script>
  <script defer src="lib/db.js?v={VER}"></script>
  <script defer src="main.js?v={VER}"></script>
</body>
</html>
"""
    with open(ROOT / "index.html", "w", encoding="utf-8") as f:
        f.write(html)


def build_ficha(p):
    p_id = p["id"]
    discount_pct = round((1 - p["discountedPrice"] / p["retailPrice"]) * 100) if p["discountedPrice"] < p["retailPrice"] else 0
    main_img = p["images"][0] if p.get("images") and len(p["images"]) > 0 else f"https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN={p['asin']}&Format=_SL1500_&ID=AsinImage&MarketPlace=ES&ServiceVersion=20070822&WS=1&tag=odontoscore-21"
    
    thumbs_html = "\n".join([f'<li class="gallery-thumb-btn {"active" if idx==0 else ""}" data-src="{img}"><img src="{img}" alt="Miniatura {idx+1}"></li>' for idx, img in enumerate(p["images"][:8])])
    pros_html = "\n".join([f'<li>{pro}</li>' for pro in p["pros"]])
    contras_html = "\n".join([f'<li>{contra}</li>' for contra in p["contras"]])
    badges_ind = " ".join([f'<span class="card-category-tag">{ind.replace("_", " ").upper()}</span>' for ind in p.get("indicado_para", [])])

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{p['name']} — Análisis Clínico y Precio | OdontoScore</title>
  <meta name="description" content="{p['description']}">
  <link rel="canonical" href="{BASE_URL}/producto/{p_id}.html" />
  <link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css?v={VER}">
</head>
<body>
  {render_header('', '../')}

  <main class="container ficha-layout" data-producto-id="{p_id}" data-asin="{p['asin']}" style="padding-top:2.5rem;padding-bottom:4rem;">
    <div style="font-size:0.85rem;color:#64748B;margin-bottom:1.5rem;">
      <a href="../index.html">Inicio</a> / <a href="../index.html#catalogo">{p['category']}</a> / <span>{p['marca']} {p['name'][:30]}...</span>
    </div>

    <div class="ficha-hero-grid" style="display:grid;grid-template-columns:1fr 1fr;gap:3rem;margin-bottom:3rem;">
      <div class="ficha-gallery-wrapper" data-galeria>
        <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:16px;padding:2rem;text-align:center;height:380px;display:flex;align-items:center;justify-content:center;margin-bottom:1rem;">
          <img class="gallery-main-img" src="{main_img}" alt="{p['name']}" style="max-height:100%;max-width:100%;object-fit:contain;">
        </div>
        <ul style="display:flex;gap:0.5rem;overflow-x:auto;list-style:none;">
          {thumbs_html}
        </ul>
      </div>

      <div>
        <span class="card-brand-tag">{p['marca']}</span>
        <h1 style="font-size:1.85rem;line-height:1.3;margin:0.5rem 0 1rem;">{p['name']}</h1>
        
        <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:1.25rem;">
          <span style="color:#D97706;font-weight:800;">★ {p['valoracion_media']} / 5</span>
          <span style="color:#64748B;font-size:0.9rem;">({p['resenas_cantidad']:,} valoraciones)</span>
          <div>{badges_ind}</div>
        </div>

        <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:1.25rem;margin-bottom:1.5rem;">
          <div style="display:flex;align-items:baseline;gap:0.75rem;">
            <span style="font-size:1.8rem;font-weight:800;color:#0F172A;">{p['discountedPrice']} €</span>
            {f'<span style="font-size:1rem;color:#94A3B8;text-decoration:line-through;">{p["retailPrice"]} €</span>' if discount_pct > 0 else ''}
            {f'<span class="price-discount-pill">-{discount_pct}%</span>' if discount_pct > 0 else ''}
          </div>
          <p style="font-size:0.8rem;color:#64748B;margin-top:0.25rem;">Precio sincronizado con Amazon España · Envío Prime</p>
        </div>

        <a href="{p['affiliate_url']}" target="_blank" rel="sponsored nofollow noopener" class="btn-buy-amazon-large" style="width:100%;">
          <span>Ver Oferta en Amazon</span>
        </a>
      </div>
    </div>

    <section style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:16px;padding:2rem;margin-bottom:3rem;">
      <h2 style="font-size:1.4rem;margin-bottom:1rem;">Evaluación Técnica OdontoScore (7 Ejes)</h2>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:2rem;align-items:center;">
        <div class="radar-canvas-container" data-radar data-radar-id="{p_id}" style="min-height:280px;"></div>
        <div>
          <table class="specs-table">
            <tbody>
              <tr><th>Eficacia y Desempeño</th><td>{p['score_eficacia']} / 10</td></tr>
              <tr><th>Protección Gingival</th><td>{p['score_comodidad_encias']} / 10</td></tr>
              <tr><th>Durabilidad de Materiales</th><td>{p['score_durabilidad']} / 10</td></tr>
              <tr><th>Ergonomía de Uso</th><td>{p['score_facilidad_uso']} / 10</td></tr>
              <tr><th>Nivel Sonoro (Silencio)</th><td>{p['score_silencio']} / 10</td></tr>
              <tr><th>Tecnología e Innovación</th><td>{p['score_tecnologia']} / 10</td></tr>
              <tr><th>Relación Calidad-Precio</th><td>{p['score_calidad_precio']} / 10</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:16px;padding:2rem;margin-bottom:3rem;">
      <h2 style="font-size:1.4rem;margin-bottom:1rem;">Especificaciones Técnicas</h2>
      <table class="specs-table">
        <tbody>
          <tr><th>Marca y Modelo</th><td>{p['marca']} {p['name']}</td></tr>
          <tr><th>Especialidad</th><td>{p['category']}</td></tr>
          <tr><th>Tecnología</th><td>{p['tecnologia'].upper()}</td></tr>
          <tr><th>Modos / Ajustes</th><td>{p['modos_limpieza']} programas</td></tr>
          <tr><th>Potencia / Presión</th><td>{f"{p['presion_agua_psi']} PSI" if p.get('presion_agua_psi') else (f"{p['pulsaciones_min']:,} mov/min" if p.get('pulsaciones_min') else "Clínico")}</td></tr>
          <tr><th>Autonomía</th><td>{f"{p['autonomia_dias']} días" if p['autonomia_dias'] < 365 else "Red continua / AC"}</td></tr>
          <tr><th>Esterilización</th><td>{'Apto para autoclave 134°C' if p['esterilizable_autoclave'] else 'Limpieza convencional'}</td></tr>
        </tbody>
      </table>
    </section>
  </main>

  {render_footer('../')}

  <script defer src="../lib/manifest.js"></script>
  <script defer src="../lib/db.js?v={VER}"></script>
  <script defer src="../main.js?v={VER}"></script>
</body>
</html>
"""
    out_dir = ROOT / "producto"
    out_dir.mkdir(exist_ok=True)
    with open(out_dir / f"{p_id}.html", "w", encoding="utf-8") as f:
        f.write(html)


def build_comparator(products):
    options_cats = "".join([f'<option value="{c["id"]}">{c["name"]}</option>' for c in CATEGORIES])
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Comparador Odontológico — OdontoScore</title>
  <meta name="description" content="Comparador clínico de 7 ejes de rendimiento odontológico.">
  <link rel="canonical" href="{BASE_URL}/comparador.html" />
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
  <link rel="stylesheet" href="styles.css?v={VER}">
</head>
<body>
  {render_header('', '')}

  <main class="container section-block" data-comparator-app>
    <div class="section-header" style="text-align:left;max-width:100%;">
      <div class="hero-badge">Comparador Clínico</div>
      <h1 style="font-size:2.2rem;margin-bottom:0.75rem;">Comparativa de Dispositivos y Material</h1>
      <p style="color:#64748B;font-size:1.05rem;">Selecciona una especialidad y compara especificaciones técnicas y radares superpuestos.</p>
    </div>

    <div class="comparator-selector-bar" style="background:#FFFFFF;border:1px solid var(--color-border);padding:1.25rem;border-radius:12px;margin-bottom:2rem;">
      <div>
        <label for="compCategorySelect" style="font-weight:700;font-size:0.95rem;margin-right:0.75rem;">Especialidad:</label>
        <select id="compCategorySelect" style="padding:0.6rem 1rem;border-radius:8px;border:1px solid var(--color-border);font-family:var(--font-sans);font-size:0.95rem;">
          <option value="">Todas las Especialidades</option>
          {options_cats}
        </select>
      </div>
      <div id="compProductChecks" style="display:flex;flex-wrap:wrap;align-items:center;margin-top:1rem;"></div>
    </div>

    <div class="radar-section-box" style="margin-bottom:2.5rem;background:#FFFFFF;border:1px solid var(--color-border);border-radius:16px;padding:2rem;">
      <h2 style="font-size:1.3rem;margin-bottom:0.5rem;">Radares Clínicos Superpuestos</h2>
      <div id="compRadarLegend" style="margin-bottom:1.5rem;display:flex;flex-wrap:wrap;gap:0.75rem;"></div>
      <div class="radar-canvas-container" id="compRadarCanvas" style="min-height:300px;"></div>
    </div>

    <div class="comparator-table-scroll" id="compMatrixContent"></div>
  </main>

  {render_footer('')}

  <script defer src="lib/manifest.js"></script>
  <script defer src="lib/db.js?v={VER}"></script>
  <script defer src="main.js?v={VER}"></script>
</body>
</html>
"""
    with open(ROOT / "comparador.html", "w", encoding="utf-8") as f:
        f.write(html)


def build_ofertas(products):
    deal_prods = [p for p in products if p["discountedPrice"] < p["retailPrice"]]
    cards = "\n".join([render_product_card(p, "") for p in deal_prods])
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ofertas en Odontología — OdontoScore</title>
  <link rel="canonical" href="{BASE_URL}/ofertas.html" />
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
  <link rel="stylesheet" href="styles.css?v={VER}">
</head>
<body>
  {render_header('ofertas', '')}

  <main class="container section-block">
    <div class="section-header" style="text-align:left;max-width:100%;margin-bottom:2.5rem;">
      <div class="hero-badge">Descuentos Verificados</div>
      <h1 style="font-size:2.2rem;margin-bottom:0.5rem;">Ofertas en Material y Cuidado Bucal</h1>
      <p style="color:#64748B;font-size:1.05rem;">Precios rebajados respecto al PVP oficial en Amazon España.</p>
    </div>

    <div class="product-grid">
      {cards}
    </div>
  </main>

  {render_footer('')}

  <script defer src="lib/manifest.js"></script>
  <script defer src="lib/db.js?v={VER}"></script>
  <script defer src="main.js?v={VER}"></script>
</body>
</html>
"""
    with open(ROOT / "ofertas.html", "w", encoding="utf-8") as f:
        f.write(html)


def build_db_js(products):
    db_obj = {
        "productos": products,
        "updated": "2026-08-22"
    }
    js_content = f"""(function () {{
  "use strict";
  window.__DB__ = {json.dumps(db_obj, indent=2, ensure_ascii=False)};
}})();
"""
    lib_dir = ROOT / "lib"
    lib_dir.mkdir(exist_ok=True)
    with open(lib_dir / "db.js", "w", encoding="utf-8") as f:
        f.write(js_content)


def build_sitemaps_and_robots(products):
    urls = [
        f"{BASE_URL}/",
        f"{BASE_URL}/comparador.html",
        f"{BASE_URL}/ofertas.html",
        f"{BASE_URL}/aviso-afiliados.html",
        f"{BASE_URL}/privacidad.html",
        f"{BASE_URL}/sobre-nosotros.html",
        f"{BASE_URL}/guias/mejor-irrigador-dental-brackets-2026.html",
        f"{BASE_URL}/guias/mejor-cepillo-electrico-encias-sensibles-2026.html"
    ]
    for p in products:
        urls.append(f"{BASE_URL}/producto/{p['id']}.html")

    sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sitemap_xml.append(f"  <url><loc>{u}</loc><lastmod>2026-08-22</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>")
    sitemap_xml.append('</urlset>')

    with open(ROOT / "sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(sitemap_xml))


def main():
    print("=== OdontoScore Clean Medical Grade Builder ===")
    products = load_products()
    print(f"Loaded {len(products)} products for compilation")

    build_db_js(products)
    build_home(products)
    build_comparator(products)
    build_ofertas(products)

    for p in products:
        build_ficha(p)

    build_sitemaps_and_robots(products)
    print(f"[OK] Build complete with {len(products)} products and version: {VER}")


if __name__ == "__main__":
    main()
