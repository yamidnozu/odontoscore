#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OdontoScore Static Site Generator (tools/build_site.py)
Generates high-converting clinical landing with 7 segmented categories (including Students),
live search, high-res Amazon images, dual grid/list view, rich specs matrix, and interactive quick modal.
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
VER = "20260822_v3"
BASE_URL = "https://odontoscore.com"
AMAZON_PARTNER_TAG = os.getenv("AMAZON_PARTNER_TAG", "odontoscore-21").strip()
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "").strip()

CATEGORIES = [
    {
        "id": "estudiantes_practicas",
        "slug": "estudiantes-odontologia",
        "name": "Estudiantes y Prácticas",
        "desc": "Tipodontos anatómicos con dientes atornillables, kits de sutura oral, lámparas LED y modelos de simulación.",
        "icon": "🎓"
    },
    {
        "id": "cepillos_electricos",
        "slug": "cepillos-electricos",
        "name": "Cepillos Eléctricos",
        "desc": "Tecnología sónica, magnética y rotatoria para una eliminación superior de placa bacteriana.",
        "icon": "🪥"
    },
    {
        "id": "irrigadores_dentales",
        "slug": "irrigadores-dentales",
        "name": "Irrigadores Dentales",
        "desc": "Limpieza interdental profunda y masaje gingival avalado clínicamente por la ADA.",
        "icon": "💧"
    },
    {
        "id": "blanqueamiento_dental",
        "slug": "blanqueamiento-dental",
        "name": "Blanqueamiento Dental",
        "desc": "Kits LED profesionales, geles no abrasivos y tiras para eliminar manchas respetando el esmalte.",
        "icon": "✨"
    },
    {
        "id": "ortodoncia_brackets",
        "slug": "ortodoncia-brackets",
        "name": "Ortodoncia y Brackets",
        "desc": "Ceras protectoras, cepillos interdentales y kits de higiene para brackets y alineadores.",
        "icon": "🦷"
    },
    {
        "id": "higiene_infantil",
        "slug": "higiene-infantil",
        "name": "Higiene Infantil y Odontopediatría",
        "desc": "Cepillos ultrasuaves, temporizadores y kits diseñados para el cuidado dental infantil.",
        "icon": "🧸"
    },
    {
        "id": "instrumental_basico",
        "slug": "instrumental-clinica",
        "name": "Instrumental y Clínica",
        "desc": "Bandejas quirúrgicas, cestas de autoclave y material de acero inoxidable para clínica dental.",
        "icon": "🔬"
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
                    
                    local_prod_img = f"assets/img/products/{asin}.jpg"
                    if (ROOT / local_prod_img).exists():
                        img_path = local_prod_img
                    elif row.get("local_assets") and row["local_assets"][0] != "assets/img/hero-dental.svg":
                        img_path = row["local_assets"][0]
                    else:
                        img_path = "assets/img/hero-dental.svg"
                    
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
                        "images": [img_path],
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
                        "capacidad_deposito_ml": row.get("capacidad_deposito_ml"),
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
                        "pros": row.get("pros") or ["Eficacia clínica verificada", "Garantía oficial y envío Prime", "Excelente relación calidad-precio"],
                        "contras": row.get("contras") or ["Consultar disponibilidad de recambios"],
                        "ideal_para": row.get("ideal_para") or "Estudiantes, pacientes y profesionales odontológicos.",
                        "destacado_editorial": row.get("destacado_editorial") or "Producto verificado por OdontoScore 2026.",
                        "resenas_resumen": row.get("resenas_resumen") or "Alta satisfacción de compradores.",
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
      <img src="{root_rel}assets/img/logo-odontoscore.svg" alt="OdontoScore" height="42">
    </a>
    <nav class="main-nav">
      <ul class="nav-links">
        <li><a href="{root_rel}index.html#catalogo">Catálogo</a></li>
        <li><a href="{root_rel}index.html#estudiantes">Zona Estudiantes</a></li>
        <li><a href="{root_rel}index.html#comparador">Comparador Radar</a></li>
        <li><a href="{root_rel}index.html#ofertas">Ofertas</a></li>
        <li><a href="{root_rel}index.html#faq">FAQ Clínica</a></li>
      </ul>
      <div class="nav-actions">
        <a href="{root_rel}index.html#comparador" class="btn-nav-compare">
          <span>⚡ Comparar Modelos</span>
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
        <img src="{root_rel}assets/img/logo-odontoscore.svg" alt="OdontoScore" height="38" style="filter: brightness(0) invert(1); margin-bottom:1rem;">
        <p style="margin-bottom:1rem;color:#94A3B8;">Portal odontológico independiente de comparativas técnicas, guías clínicas y catálogo para estudiantes, profesionales y pacientes.</p>
        <p style="font-size:0.85rem;color:#64748B;">Evaluación de rendimiento en 7 ejes: bio-eficacia, ergonomía, confort gingival, decibelios y presión hidráulica.</p>
      </div>
      <div class="footer-col">
        <h4>Especialidades</h4>
        <ul class="footer-links">
          <li><a href="{root_rel}index.html#catalogo">🎓 Estudiantes y Prácticas</a></li>
          <li><a href="{root_rel}index.html#catalogo">🪥 Cepillos Eléctricos</a></li>
          <li><a href="{root_rel}index.html#catalogo">💧 Irrigadores Dentales</a></li>
          <li><a href="{root_rel}index.html#catalogo">✨ Blanqueamiento Dental</a></li>
          <li><a href="{root_rel}index.html#catalogo">🦷 Ortodoncia y Brackets</a></li>
          <li><a href="{root_rel}index.html#catalogo">🔬 Instrumental y Clínica</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Herramientas</h4>
        <ul class="footer-links">
          <li><a href="{root_rel}comparador.html">Comparador de 7 Ejes</a></li>
          <li><a href="{root_rel}ofertas.html">Ofertas y Descuentos</a></li>
          <li><a href="{root_rel}guias/mejor-irrigador-dental-brackets-2026.html">Guía Irrigadores Brackets</a></li>
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
    img_url = p['images'][0] if p.get('images') else f"{root_rel}assets/img/hero-dental.svg"
    
    # Tech and specs details
    tech_str = p.get('tecnologia', 'sonico').replace('_', ' ').upper()
    potencia_str = f"{p['presion_agua_psi']} PSI" if p.get('presion_agua_psi') else (f"{p['pulsaciones_min']:,} puls/min" if p.get('pulsaciones_min') else ("Autoclave 134°C" if p.get('esterilizable_autoclave') else "Clínico"))
    autonomia_str = f"{p['autonomia_dias']} días" if p.get('autonomia_dias', 14) < 365 else "Red Eléctrica / AC"
    ruido_str = f"{p['nivel_ruido_db']} dB" if p.get('nivel_ruido_db') and p.get('nivel_ruido_db') > 0 else "Silencioso"

    return f"""
<article class="product-card" data-producto-id="{p['id']}" data-asin="{p['asin']}" data-category="{p['categoria_odontologica']}" data-brand="{p['marca'].lower()}" data-title="{p['name'].lower()}" data-price="{p['discountedPrice']}" data-score="{p['score_eficacia']}">
  {'<span class="card-badge-top" style="position:absolute;top:1rem;left:1rem;z-index:10;background:#0F172A;color:#FFF;font-size:0.75rem;font-weight:700;padding:3px 10px;border-radius:999px;">★ Top Recomendado</span>' if p.get('isFeatured') else ''}
  {f'<span class="price-discount-pill" style="position:absolute;top:1rem;right:1rem;z-index:10;">-{discount_pct}%</span>' if discount_pct > 0 else ''}
  
  <div class="card-media">
    <img src="{img_url}" alt="{p['name']}" loading="lazy" onerror="this.onerror=null;this.src='{root_rel}assets/img/hero-dental.svg';">
  </div>
  
  <div class="card-body">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.35rem;">
      <span style="font-size:0.75rem;font-weight:800;color:#0E76BC;letter-spacing:0.05em;text-transform:uppercase;">{p['marca']}</span>
      <span style="font-size:0.7rem;color:#475569;font-weight:700;background:#F1F5F9;padding:2px 8px;border-radius:999px;">{p['category']}</span>
    </div>
    
    <h3 class="card-title" title="{p['name']}">{p['name']}</h3>
    
    <div class="card-rating-box">
      <span class="rating-badge">★ {p['valoracion_media']}</span>
      <span style="font-size:0.8rem;color:#64748B;">({p['resenas_cantidad']:,} valoraciones)</span>
    </div>
    
    <!-- Rich Clinical Specs Matrix -->
    <div class="card-specs-matrix">
      <div class="spec-cell">⚙️ <strong>{tech_str}</strong></div>
      <div class="spec-cell">🎛️ <strong>{p['modos_limpieza']} Modos</strong></div>
      <div class="spec-cell">⚡ <strong>{potencia_str}</strong></div>
      <div class="spec-cell">🔋 <strong>{autonomia_str}</strong></div>
    </div>
    
    <div class="card-price-row">
      <div>
        <span class="price-main-val">{p['discountedPrice']} €</span>
        {f'<span class="price-strike-val">{p["retailPrice"]} €</span>' if discount_pct > 0 else ''}
      </div>
      <span style="font-size:0.75rem;font-weight:700;color:#16A34A;display:flex;align-items:center;gap:0.25rem;">✓ Prime 24/48h</span>
    </div>
    
    <div class="card-actions-grid">
      <button type="button" class="btn-card-quick" data-quick-view="{p['id']}">
        <span>⚡ Ficha &amp; Radar</span>
      </button>
      <a href="{p['affiliate_url']}" target="_blank" rel="sponsored nofollow noopener" class="btn-card-prime">
        <span>🛒 Ver en Amazon</span>
      </a>
    </div>

    <!-- Intra-Page Compare Checkbox -->
    <div style="margin-top:0.75rem;padding-top:0.5rem;border-top:1px dashed #E2E8F0;display:flex;align-items:center;justify-content:center;">
      <label style="font-size:0.8rem;font-weight:600;color:#64748B;cursor:pointer;display:inline-flex;align-items:center;gap:0.35rem;">
        <input type="checkbox" class="product-compare-checkbox" value="{p['id']}" data-name="{p['name'][:25]}...">
        <span>⚖️ Añadir al Comparador</span>
      </label>
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

    # Category counters
    cat_counts = {}
    for p in products:
        c_id = p.get("categoria_odontologica", "otros")
        cat_counts[c_id] = cat_counts.get(c_id, 0) + 1

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OdontoScore — Portal Odontológico Integral: Catálogo Clínico, Estudiantes y Comparador 2026</title>
  <meta name="description" content="Catálogo completo de odontología: tipodontos anatómicos, kits de sutura para estudiantes, cepillos sónicos y rotatorios, irrigadores y material de clínica con comparador de 7 ejes.">
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
        <div class="hero-badge">
          <span>🩺 OdontoScore 2026 · Portal Clínico, Académico &amp; Pacientes</span>
        </div>
        <h1 class="hero-title">El Catálogo Odontológico más <span>Completo y Riguroso</span></h1>
        <p class="hero-subtitle">Material docente para estudiantes universitarios, equipamiento de clínica y dispositivos de higiene oral: tipodontos, kits de sutura, lámparas LED, cepillos iO e irrigadores con análisis técnico normalizado.</p>
        <div class="hero-actions">
          <a href="#catalogo" class="btn-primary">🔍 Ver Catálogo Completo ({len(products)} Productos)</a>
          <a href="#estudiantes" class="btn-secondary">🎓 Material para Estudiantes</a>
        </div>
        <div class="hero-trust-bullets">
          <span>✓ Enlaces Verificados Amazon Prime</span>
          <span>✓ Radar Clínico de 7 Ejes</span>
          <span>✓ Sincronización Automática</span>
        </div>
      </div>
      <div class="hero-visual">
        <img src="assets/img/hero-dental.svg" alt="OdontoScore Portal Odontológico" fetchpriority="high">
      </div>
    </div>
  </section>

  <!-- 1. Interactive Catalog with Advanced Toolbar -->
  <section id="catalogo" class="section-block">
    <div class="container">
      <div class="section-header">
        <div class="hero-badge">📦 Catálogo Clínico &amp; Universitario</div>
        <h2 class="section-title">Explora Todos los Dispositivos y Materiales</h2>
        <p class="section-desc">Filtra por especialidad, busca en tiempo real o abre la <strong>⚡ Ficha Rápida</strong> para ver el radar de 7 ejes.</p>
      </div>

      <!-- Advanced Catalog Toolbar -->
      <div class="catalog-toolbar-wrapper">
        <div class="catalog-search-row">
          <input type="text" id="catalogSearchInput" class="catalog-search-input" placeholder="🔎 Buscar por producto, marca o palabra clave (ej: tipodonto, Oral-B, sutura, Waterpik, LED)...">
          
          <select id="catalogSortSelect" class="catalog-sort-select" aria-label="Ordenar productos">
            <option value="featured">Ordenar: Más Recomendados</option>
            <option value="price-asc">Precio: Menor a Mayor</option>
            <option value="price-desc">Precio: Mayor a Menor</option>
            <option value="score">Mayor Puntuación Clínica</option>
          </select>

          <div class="view-toggle-group">
            <button type="button" class="view-toggle-btn active" id="btnViewGrid" title="Vista Cuadrícula">⊞ Cuadrícula</button>
            <button type="button" class="view-toggle-btn" id="btnViewList" title="Vista Lista">☰ Lista</button>
          </div>
        </div>

        <!-- Category Pills Bar -->
        <div class="filter-pills-bar" data-catalog-filters style="margin-bottom:0;">
          <button type="button" class="filter-pill-btn active" data-filter="all">Todos ({len(products)})</button>
          <button type="button" class="filter-pill-btn" data-filter="estudiantes_practicas">🎓 Estudiantes ({cat_counts.get('estudiantes_practicas', 0)})</button>
          <button type="button" class="filter-pill-btn" data-filter="cepillos_electricos">🪥 Cepillos ({cat_counts.get('cepillos_electricos', 0)})</button>
          <button type="button" class="filter-pill-btn" data-filter="irrigadores_dentales">💧 Irrigadores ({cat_counts.get('irrigadores_dentales', 0)})</button>
          <button type="button" class="filter-pill-btn" data-filter="blanqueamiento_dental">✨ Blanqueamiento ({cat_counts.get('blanqueamiento_dental', 0)})</button>
          <button type="button" class="filter-pill-btn" data-filter="ortodoncia_brackets">🦷 Ortodoncia ({cat_counts.get('ortodoncia_brackets', 0)})</button>
          <button type="button" class="filter-pill-btn" data-filter="higiene_infantil">🧸 Infantil ({cat_counts.get('higiene_infantil', 0)})</button>
          <button type="button" class="filter-pill-btn" data-filter="instrumental_basico">🔬 Instrumental ({cat_counts.get('instrumental_basico', 0)})</button>
        </div>
      </div>

      <!-- Main Product Grid -->
      <div class="product-grid" id="mainProductGrid">
        {cards_html}
      </div>
    </div>
  </section>

  <!-- 2. Specialized University Student Zone -->
  <section id="estudiantes" class="section-block" style="background: linear-gradient(180deg, #F8FAFC 0%, #EFF6FF 100%);">
    <div class="container">
      <div class="section-header">
        <div class="hero-badge">🎓 Prácticas Universitarias &amp; Laboratorio</div>
        <h2 class="section-title">Zona Estudiantes de Odontología</h2>
        <p class="section-desc">Guía de material didáctico imprescindible para prácticas de grado en odontología, preclínica y simulación.</p>
      </div>

      <!-- University Essentials Banner -->
      <div style="background:#FFFFFF;border:1px solid #BFDBFE;border-radius:16px;padding:1.75rem;margin-bottom:2.5rem;box-shadow:var(--shadow-sm);display:grid;grid-template-columns:repeat(auto-fit, minmax(240px, 1fr));gap:1.5rem;">
        <div style="display:flex;gap:0.75rem;align-items:flex-start;">
          <span style="font-size:2rem;">🦷</span>
          <div>
            <h4 style="font-size:1.05rem;margin-bottom:0.25rem;">Tipodontos Anatómicos</h4>
            <p style="font-size:0.85rem;color:#64748B;">Modelos de 28/32 dientes con encía blanda de silicona para prácticas de operatoria y prótesis fija.</p>
          </div>
        </div>
        <div style="display:flex;gap:0.75rem;align-items:flex-start;">
          <span style="font-size:2rem;">🪡</span>
          <div>
            <h4 style="font-size:1.05rem;margin-bottom:0.25rem;">Kits de Sutura Oral</h4>
            <p style="font-size:0.85rem;color:#64748B;">Almohadillas multicapa con encías y dientes simulados para prácticas de cirugía bucal.</p>
          </div>
        </div>
        <div style="display:flex;gap:0.75rem;align-items:flex-start;">
          <span style="font-size:2rem;">💡</span>
          <div>
            <h4 style="font-size:1.05rem;margin-bottom:0.25rem;">Lámparas LED Polimerización</h4>
            <p style="font-size:0.85rem;color:#64748B;">Fotocurado de composites de 36W con longitud de onda calibrada para clínica docente.</p>
          </div>
        </div>
      </div>

      <div class="product-grid">
        {students_cards if students_cards else '<p style="text-align:center;grid-column:1/-1;">Cargando material docente...</p>'}
      </div>
    </div>
  </section>

  <!-- 3. Integrated Multi-Product Radar Comparator -->
  <section id="comparador" class="section-block">
    <div class="container" data-comparator-app>
      <div class="section-header">
        <div class="hero-badge">⚡ Enfrentamiento Lado a Lado</div>
        <h2 class="section-title">Comparador Clínico OdontoScore (7 Ejes)</h2>
        <p class="section-desc">Selecciona hasta 4 modelos para ver especificaciones y superposición de polígonos de radar sin salir de la página.</p>
      </div>

      <div class="comparator-selector-bar" style="background:#FFFFFF;box-shadow:var(--shadow-sm);border:1px solid var(--color-border);">
        <div>
          <label for="compCategorySelect" style="font-weight:700;font-size:0.95rem;margin-right:0.75rem;">Especialidad:</label>
          <select id="compCategorySelect" style="padding:0.6rem 1rem;border-radius:var(--radius-md);border:1px solid var(--color-border);font-family:var(--font-sans);font-size:0.95rem;">
            <option value="">Todas las Categorías</option>
            {options_cats}
          </select>
        </div>
        <div id="compProductChecks" style="display:flex;flex-wrap:wrap;align-items:center;"></div>
      </div>

      <div class="radar-section-box" style="margin-bottom:2rem;background:#FFFFFF;">
        <h3 style="font-size:1.3rem;margin-bottom:0.5rem;">Superposición de Radares Clínicos (7 Ejes)</h3>
        <div id="compRadarLegend" style="margin-bottom:1rem;display:flex;flex-wrap:wrap;gap:0.75rem;"></div>
        <div class="radar-canvas-container" id="compRadarCanvas" style="min-height:340px;"></div>
      </div>

      <div class="comparator-table-scroll" id="compMatrixContent"></div>
    </div>
  </section>

  <!-- 4. Deals & Offers Section -->
  <section id="ofertas" class="section-block" style="background-color: var(--color-surface);">
    <div class="container">
      <div class="section-header">
        <div class="hero-badge">🏷️ Descuentos Verificados</div>
        <h2 class="section-title">Ofertas Activas en Cuidado Bucal</h2>
        <p class="section-desc">Dispositivos y materiales odontológicos con precio rebajado en Amazon España.</p>
      </div>
      <div class="product-grid">
        {deal_cards_html}
      </div>
    </div>
  </section>

  <!-- 5. Clinical FAQ Section -->
  <section id="faq" class="section-block">
    <div class="container" style="max-width:850px;">
      <div class="section-header">
        <div class="hero-badge">❓ Preguntas Frecuentes</div>
        <h2 class="section-title">Preguntas Frecuentes OdontoScore</h2>
        <p class="section-desc">Criterios técnicos para estudiantes, pacientes y profesionales.</p>
      </div>

      <div class="geo-ai-box" style="background:#FFFFFF;border:1px solid #E2E8F0;">
        <div class="geo-qa-item">
          <strong>¿Qué tipodonto se recomienda para prácticas universitarias de odontología?</strong>
          <p>Para prácticas preclínicas se recomiendan modelos con 28 o 32 dientes anatómicos atornillables con encía blanda de silicona (tipo Frasaco o Nissin), compatibles con articuladores estándar.</p>
        </div>
        <div class="geo-qa-item">
          <strong>¿Qué es más recomendable: cepillo sónico o rotatorio magnético?</strong>
          <p>El sistema rotatorio magnético (Oral-B iO) destaca por su precisión diente a diente, mientras que el sónico (Philips Sonicare) es el más suave para encías sensibles y recesión periodontal.</p>
        </div>
        <div class="geo-qa-item">
          <strong>¿Los productos tienen garantía en España?</strong>
          <p>Sí, todos los productos enlazados cuentan con garantía oficial europea de 3 años y devoluciones seguras a través de Amazon Prime.</p>
        </div>
      </div>
    </div>
  </section>

  {render_footer('')}

  <!-- Floating Comparison Dock -->
  <div class="floating-compare-dock" id="floatingCompareDock">
    <div class="floating-compare-count">
      <span>⚖️</span>
      <span id="floatingCompareCountText">0 productos seleccionados</span>
    </div>
    <a href="#comparador" class="btn-floating-action" id="btnFloatingCompareNow">Ver Comparativa →</a>
  </div>

  <!-- Interactive Quick-View Modal -->
  <div class="quick-modal-backdrop" id="quickViewModal">
    <div class="quick-modal-box">
      <button type="button" class="quick-modal-close-btn" aria-label="Cerrar">&times;</button>
      <span id="modalBrand" class="card-brand" style="display:inline-block;margin-bottom:0.25rem;">Marca</span>
      <h2 id="modalTitle" style="font-size:1.4rem;margin-bottom:0.5rem;color:#0F172A;line-height:1.3;">Nombre del Producto</h2>
      <div style="font-size:1.4rem;font-weight:800;color:#0E76BC;margin-bottom:1rem;" id="modalPrice">0,00 €</div>

      <div class="quick-modal-grid">
        <div>
          <div style="background:#F8FAFC;border-radius:12px;padding:1rem;text-align:center;margin-bottom:1rem;border:1px solid #E2E8F0;">
            <img id="modalImg" src="" alt="Vista previa" style="max-height:220px;margin:0 auto;object-fit:contain;">
          </div>
          <div class="radar-canvas-container" id="modalRadarCanvas" style="min-height:240px;"></div>
        </div>
        <div>
          <h4 style="margin-bottom:0.5rem;">Ficha Técnica de Laboratorio</h4>
          <table class="specs-table" id="modalSpecsTable" style="margin-bottom:1.5rem;">
            <tbody></tbody>
          </table>
          <div style="display:flex;flex-direction:column;gap:0.75rem;">
            <a id="modalBuyBtn" href="#" target="_blank" rel="sponsored nofollow noopener" class="btn-buy-amazon-large" style="width:100%;text-align:center;justify-content:center;">
              <span>🛒 Ver Oferta en Amazon</span>
            </a>
            <a id="modalFullLink" href="#" target="_blank" class="btn-secondary" style="width:100%;text-align:center;justify-content:center;">
              <span>📄 Ver Ficha Completa y Análisis</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script defer src="lib/manifest.js"></script>
  <script defer src="lib/db.js?v={VER}"></script>
  <script defer src="main.js?v={VER}"></script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "MedicalWebPage",
    "name": "OdontoScore - Portal Odontológico Integral",
    "url": "{BASE_URL}/",
    "description": "Portal de odontología con productos para estudiantes, profesionales y pacientes con comparador radar."
  }}
  </script>
</body>
</html>
"""
    with open(ROOT / "index.html", "w", encoding="utf-8") as f:
        f.write(html)


def build_ficha(p):
    p_id = p["id"]
    discount_pct = round((1 - p["discountedPrice"] / p["retailPrice"]) * 100) if p["discountedPrice"] < p["retailPrice"] else 0
    img_url = p["images"][0] if p.get("images") else "../assets/img/hero-dental.svg"
    pros_html = "\n".join([f'<li>{pro}</li>' for pro in p["pros"]])
    contras_html = "\n".join([f'<li>{contra}</li>' for contra in p["contras"]])
    badges_ind = " ".join([f'<span class="spec-pill" style="background:#E0F2FE;color:#0369A1;font-weight:700;">{ind.replace("_", " ").upper()}</span>' for ind in p.get("indicado_para", [])])

    geo_faq_html = ""
    if p.get("geo_faq"):
        for item in p["geo_faq"]:
            geo_faq_html += f"""
            <div class="geo-qa-item">
              <strong>{item['q']}</strong>
              <p>{item['a']}</p>
            </div>
            """

    video_html = ""
    if p.get("video_demo"):
        v = p["video_demo"]
        video_html = f"""
    <section class="video-demo-box" style="margin-bottom:2rem;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:16px;padding:1.75rem;box-shadow:var(--shadow-sm);">
      <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
        <span style="font-size:1.25rem;">🎥</span>
        <h2 style="font-size:1.35rem;color:#0F172A;">Demostración Clínica en Vídeo</h2>
        <span style="font-size:0.75rem;font-weight:700;background:#E0F2FE;color:#0369A1;padding:2px 8px;border-radius:999px;margin-left:auto;">{v.get('duracion', '3 min')}</span>
      </div>
      <p style="color:#64748B;font-size:0.9rem;margin-bottom:1.25rem;">{v.get('title', 'Técnica y manejo clínico')}</p>
      <div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:12px;background:#0F172A;">
        <iframe src="{v.get('video_url')}" title="{v.get('title')}" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>
      </div>
      <p style="font-size:0.75rem;color:#94A3B8;margin-top:0.75rem;text-align:right;">Fuente: {v.get('autor', 'Panel Clínico OdontoScore')}</p>
    </section>
        """

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

  <main class="container ficha-layout" data-producto-id="{p_id}" data-asin="{p['asin']}">
    <nav class="ficha-breadcrumb">
      <a href="../index.html">Inicio</a> <span>/</span>
      <a href="../index.html#catalogo">{p['category']}</a> <span>/</span>
      <span>{p['marca']} {p['name'][:30]}...</span>
    </nav>

    <div class="ficha-hero-grid">
      <div class="ficha-gallery-wrapper">
        <div class="gallery-main-view" style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:16px;padding:2rem;text-align:center;">
          <img class="gallery-main-img" src="../{img_url}" alt="{p['name']}" style="max-height:350px;margin:0 auto;object-fit:contain;" onerror="this.onerror=null;this.src='../assets/img/hero-dental.svg';">
        </div>
      </div>

      <div class="ficha-info-head">
        <span class="ficha-brand-tag">{p['marca']}</span>
        <h1 class="ficha-title">{p['name']}</h1>
        
        <div class="ficha-meta-row">
          <div class="ficha-rating" style="color:#D97706;font-weight:700;">★ {p['valoracion_media']} / 5</div>
          <div class="ficha-reviews-count" style="color:#64748B;">({p['resenas_cantidad']:,} valoraciones verificadas)</div>
          <div>{badges_ind}</div>
        </div>

        <div class="ficha-price-container">
          <div class="ficha-price-main">
            <span class="current price-current">{p['discountedPrice']} €</span>
            {f'<span class="old price-old">{p["retailPrice"]} €</span>' if discount_pct > 0 else ''}
            {f'<span class="discount-badge" style="background:#EF4444;color:#FFF;padding:2px 8px;border-radius:999px;font-size:0.8rem;font-weight:800;">-{discount_pct}%</span>' if discount_pct > 0 else ''}
          </div>
          <p class="ficha-price-note">Precio orientativo · Actualizado en tiempo real · Amazon Prime</p>
        </div>

        <a href="{p['affiliate_url']}" target="_blank" rel="sponsored nofollow noopener" class="btn-buy-amazon-large">
          <span>🛒 Ver Oferta en Amazon</span>
        </a>

        <div style="display:flex;gap:0.75rem;margin-top:1rem;">
          <a href="../comparador.html" class="btn-secondary" style="width:100%;text-align:center;justify-content:center;">⚡ Comparar este Modelo</a>
        </div>
      </div>
    </div>

    <!-- Video Demo Section -->
    {video_html}

    <section class="radar-section-box">
      <h2 style="font-size:1.5rem;margin-bottom:0.5rem;">Evaluación OdontoScore (Radar 7 Ejes)</h2>
      <div class="radar-grid-layout">
        <div class="radar-canvas-container" data-radar data-radar-id="{p_id}"></div>
        <div class="radar-scores-breakdown">
          <div class="score-row-item"><span>Eficacia y Desempeño:</span> <span class="score-val">{p['score_eficacia']} / 10</span></div>
          <div class="score-row-item"><span>Protección Gingival / Tejidos:</span> <span class="score-val">{p['score_comodidad_encias']} / 10</span></div>
          <div class="score-row-item"><span>Durabilidad y Materiales:</span> <span class="score-val">{p['score_durabilidad']} / 10</span></div>
          <div class="score-row-item"><span>Ergonomía y Uso:</span> <span class="score-val">{p['score_facilidad_uso']} / 10</span></div>
          <div class="score-row-item"><span>Nivel Sonoro (Silencio):</span> <span class="score-val">{p['score_silencio']} / 10</span></div>
          <div class="score-row-item"><span>Tecnología e Innovación:</span> <span class="score-val">{p['score_tecnologia']} / 10</span></div>
          <div class="score-row-item"><span>Relación Calidad-Precio:</span> <span class="score-val">{p['score_calidad_precio']} / 10</span></div>
        </div>
      </div>
    </section>

    <section class="dental-specs-table-box">
      <h2 style="font-size:1.5rem;margin-bottom:1rem;">Ficha Técnica de Fabricante</h2>
      <table class="specs-table">
        <tbody>
          <tr><th>Marca y Modelo</th><td>{p['marca']} {p['name']}</td></tr>
          <tr><th>Categoría</th><td>{p['category']}</td></tr>
          <tr><th>Tecnología</th><td>{p['tecnologia'].upper()}</td></tr>
          <tr><th>Modos / Ajustes</th><td>{p['modos_limpieza']} configuraciones</td></tr>
          <tr><th>Presión / Potencia</th><td>{f"{p['presion_agua_psi']} PSI" if p.get('presion_agua_psi') else "—"}</td></tr>
          <tr><th>Autonomía</th><td>{f"{p['autonomia_dias']} días" if p['autonomia_dias'] < 365 else "Uso continuo / No aplica batería"}</td></tr>
          <tr><th>Nivel Sonoro</th><td>{p['nivel_ruido_db']} dB</td></tr>
          <tr><th>App / Conectividad</th><td>{'Sí, conectividad Bluetooth' if p['app_conectada'] else 'No aplica'}</td></tr>
          <tr><th>Esterilización</th><td>{'Apto para autoclave' if p['esterilizable_autoclave'] else 'Limpieza convencional'}</td></tr>
        </tbody>
      </table>
    </section>

    <section class="editorial-content-box">
      <h2 style="font-size:1.6rem;margin-bottom:1.5rem;">Análisis Editorial OdontoScore</h2>
      <div class="editorial-body">
        {p['cuerpo_editorial']}
      </div>

      <div class="pros-contras-grid">
        <div class="pros-box">
          <h3>Puntos Fuertes</h3>
          <ul class="pros-list">{pros_html}</ul>
        </div>
        <div class="contras-box">
          <h3>A Considerar</h3>
          <ul class="contras-list">{contras_html}</ul>
        </div>
      </div>

      <div class="ideal-para-banner">
        <p><strong>Recomendación:</strong> {p['ideal_para']}</p>
      </div>

      <div class="geo-ai-box">
        <h3>Preguntas Estructuradas (GEO Block)</h3>
        {geo_faq_html}
      </div>

      <div style="text-align:center;padding-top:1.5rem;">
        <a href="{p['affiliate_url']}" target="_blank" rel="sponsored nofollow noopener" class="btn-buy-amazon-large" style="display:inline-flex;">
          <span>🛒 Comprar {p['name'][:35]} en Amazon</span>
        </a>
      </div>
    </section>
  </main>

  {render_footer('../')}

  <script defer src="../lib/manifest.js"></script>
  <script defer src="../lib/db.js?v={VER}"></script>
  <script defer src="../main.js?v={VER}"></script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "{p['name']}",
    "image": ["{img_url}"],
    "description": "{p['description']}",
    "brand": {{
      "@type": "Brand",
      "name": "{p['marca']}"
    }},
    "offers": {{
      "@type": "Offer",
      "url": "{p['affiliate_url']}",
      "priceCurrency": "EUR",
      "price": "{p['discountedPrice']}",
      "availability": "https://schema.org/InStock"
    }}
  }}
  </script>
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
  <title>Comparador Odontológico — Enfrenta Dispositivos y Material Dental | OdontoScore</title>
  <meta name="description" content="Comparador de 7 ejes de rendimiento odontológico: cepillos sónicos, irrigadores, kits de sutura y tipodontos.">
  <link rel="canonical" href="{BASE_URL}/comparador.html" />
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css?v={VER}">
</head>
<body>
  {render_header('', '')}

  <main class="container comparator-page-wrapper" data-comparator-app>
    <div class="section-header" style="text-align:left;max-width:100%;">
      <div class="hero-badge">⚡ Comparativa Multiproducto</div>
      <h1 style="font-size:2.4rem;margin-bottom:0.75rem;">Comparador Clínico OdontoScore</h1>
      <p style="color:#64748B;font-size:1.1rem;">Selecciona una categoría y compara hasta 4 productos simultáneamente en los 7 ejes de rendimiento.</p>
    </div>

    <div class="comparator-selector-bar">
      <div>
        <label for="compCategorySelect" style="font-weight:700;font-size:0.95rem;margin-right:0.75rem;">Especialidad:</label>
        <select id="compCategorySelect" style="padding:0.6rem 1rem;border-radius:var(--radius-md);border:1px solid var(--color-border);font-family:var(--font-sans);font-size:0.95rem;">
          <option value="">Todas las Especialidades</option>
          {options_cats}
        </select>
      </div>
      <div id="compProductChecks" style="display:flex;flex-wrap:wrap;align-items:center;"></div>
    </div>

    <div class="radar-section-box" style="margin-bottom:2.5rem;">
      <h2 style="font-size:1.4rem;margin-bottom:0.5rem;">Radares Clínicos Superpuestos</h2>
      <div id="compRadarLegend" style="margin-bottom:1.5rem;display:flex;flex-wrap:wrap;gap:0.75rem;"></div>
      <div class="radar-canvas-container" id="compRadarCanvas" style="min-height:340px;"></div>
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
  <title>Ofertas en Odontología — Descuentos en Material y Cepillos | OdontoScore</title>
  <link rel="canonical" href="{BASE_URL}/ofertas.html" />
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
  <link rel="stylesheet" href="styles.css?v={VER}">
</head>
<body>
  {render_header('ofertas', '')}

  <main class="container section-block">
    <div class="section-header" style="text-align:left;max-width:100%;margin-bottom:2.5rem;">
      <div class="hero-badge">🏷️ Descuentos Activos</div>
      <h1 style="font-size:2.4rem;margin-bottom:0.5rem;">Ofertas en Material y Cuidado Bucal</h1>
      <p style="color:#64748B;font-size:1.1rem;">Precios rebajados respecto al PVP oficial en Amazon España.</p>
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
    print("=== OdontoScore Ultra-Rich UI/UX Builder ===")
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
