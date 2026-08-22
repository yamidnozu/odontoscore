#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OdontoScore Static Site Generator (tools/build_site.py)
Compiles from Supabase (Source of Truth) with fallback to datos/productos.json
into an all-in-one Clinical Portal Landing Page + standalone SEO fichas.
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
VER = "20260822"
BASE_URL = "https://odontoscore.com"
AMAZON_PARTNER_TAG = os.getenv("AMAZON_PARTNER_TAG", "odontoscore-21").strip()
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "").strip()

CATEGORIES = [
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
        "desc": "Kits LED, geles no abrasivos y tiras para eliminar manchas respetando el esmalte.",
        "icon": "✨"
    },
    {
        "id": "ortodoncia_brackets",
        "slug": "ortodoncia-brackets",
        "name": "Ortodoncia y Brackets",
        "desc": "Herramientas especializadas para higiene con brackets, arcos y alineadores transparentes.",
        "icon": "🦷"
    },
    {
        "id": "higiene_infantil",
        "slug": "higiene-infantil",
        "name": "Higiene Infantil",
        "desc": "Cepillos ultrasuaves, temporizadores divertidos y aplicaciones para niños.",
        "icon": "🧸"
    },
    {
        "id": "instrumental_basico",
        "slug": "instrumental-basico",
        "name": "Instrumental Básico Profesional",
        "desc": "Espejos intraorales, lámparas de fotocurado y material esterilizable en autoclave.",
        "icon": "🔬"
    }
]


def load_products():
    """Carga productos intentando Supabase primero, con fallback a datos/productos.json."""
    products = []

    # 1. Intentar Supabase
    if SUPABASE_URL and SUPABASE_SERVICE_KEY:
        try:
            from supabase import create_client
            sb = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
            res = sb.table("products").select("*").execute()
            if res.data and len(res.data) > 0:
                print(f"[Supabase] {len(res.data)} productos recuperados directamente de la base de datos.")
                for row in res.data:
                    asin = row.get("asin")
                    slug = row.get("id")
                    
                    # Local asset check
                    asset_path = f"assets/img/{slug}-1.svg"
                    images = [asset_path] if (ROOT / asset_path).exists() else ["assets/img/hero-dental.svg"]

                    p = {
                        "id": slug,
                        "asin": asin,
                        "name": row.get("name"),
                        "marca": row.get("marca"),
                        "categoria_odontologica": row.get("categoria_odontologica"),
                        "category": row.get("category") or "Odontología",
                        "affiliate_url": f"https://www.amazon.es/dp/{asin}?tag={AMAZON_PARTNER_TAG}",
                        "affiliate_tag": AMAZON_PARTNER_TAG,
                        "canonical_url": row.get("canonical_url") or f"https://www.amazon.es/dp/{asin}",
                        "images": row.get("local_assets") or images,
                        "isFeatured": bool(row.get("is_featured")),
                        "showInTopMenu": bool(row.get("show_in_top_menu")),
                        "retailPrice": float(row.get("retail_price") or 99.99),
                        "discountedPrice": float(row.get("discounted_price") or row.get("retail_price") or 99.99),
                        "rango_precio": row.get("rango_precio") or "medio",
                        "valoracion_media": float(row.get("valoracion_media") or 4.5),
                        "resenas_cantidad": int(row.get("resenas_cantidad") or 0),
                        "precio_fecha": str(row.get("precio_fecha") or "2026-08-22")[:10],
                        "tipo_producto": row.get("tipo_producto") or "dispositivo_dental",
                        "tecnologia": row.get("tecnologia") or "sonico",
                        "modos_limpieza": int(row.get("modos_limpieza") or 1),
                        "presion_agua_psi": row.get("presion_agua_psi"),
                        "capacidad_deposito_ml": row.get("capacidad_deposito_ml"),
                        "pulsaciones_min": row.get("pulsaciones_min"),
                        "autonomia_dias": row.get("autonomia_dias") or 14,
                        "tiempo_carga_h": row.get("tiempo_carga_h") or 3.0,
                        "cabezales_incluidos": row.get("cabezales_incluidos") or 1,
                        "nivel_ruido_db": row.get("nivel_ruido_db") or 60,
                        "resistencia_ipx": row.get("resistencia_ipx") or "IPX7",
                        "app_conectada": bool(row.get("app_conectada")),
                        "material": row.get("material") or "Polímero médico libre de BPA",
                        "esterilizable_autoclave": bool(row.get("esterilizable_autoclave")),
                        "indicado_para": row.get("indicado_para") or [],
                        "specs_extra": row.get("specs_extra") or {},
                        "score_eficacia": float(row.get("score_eficacia") or 8.5),
                        "score_comodidad_encias": float(row.get("score_comodidad_encias") or 8.5),
                        "score_durabilidad": float(row.get("score_durabilidad") or 8.5),
                        "score_facilidad_uso": float(row.get("score_facilidad_uso") or 8.5),
                        "score_silencio": float(row.get("score_silencio") or 8.0),
                        "score_tecnologia": float(row.get("score_tecnologia") or 8.5),
                        "score_calidad_precio": float(row.get("score_calidad_precio") or 8.5),
                        "description": row.get("description") or "",
                        "cuerpo_editorial": row.get("cuerpo_editorial") or "",
                        "pros": row.get("pros") or ["Eficacia probada", "Calidad de materiales", "Garantía oficial"],
                        "contras": row.get("contras") or ["Consultar disponibilidad de recambios"],
                        "ideal_para": row.get("ideal_para") or "Higiene bucal diaria y prevención",
                        "destacado_editorial": row.get("destacado_editorial") or "Producto avalado clínicamente",
                        "resenas_resumen": row.get("resenas_resumen") or "Alta satisfacción de compradores",
                        "geo_faq": row.get("geo_faq") or []
                    }
                    products.append(p)
                return products
        except Exception as e:
            print(f"[Supabase Fallback] Error conectando a Supabase ({e}). Usando datos/productos.json.")

    # 2. Fallback local
    if DATOS_FILE.exists():
        with open(DATOS_FILE, "r", encoding="utf-8") as f:
            products = json.load(f)
            for p in products:
                p["affiliate_tag"] = AMAZON_PARTNER_TAG
                p["affiliate_url"] = f"https://www.amazon.es/dp/{p['asin']}?tag={AMAZON_PARTNER_TAG}"
            return products

    return []


def render_header(active_nav="", root_rel=""):
    return f"""
<header class="site-header">
  <div class="container nav-wrapper">
    <a href="{root_rel}index.html" class="brand-logo">
      <img src="{root_rel}assets/img/logo-odontoscore.svg" alt="OdontoScore Logo" height="38">
    </a>
    <nav class="main-nav">
      <ul class="nav-links">
        <li><a href="{root_rel}index.html#catalogo">Catálogo</a></li>
        <li><a href="{root_rel}index.html#comparador">Comparador</a></li>
        <li><a href="{root_rel}index.html#ofertas">Ofertas</a></li>
        <li><a href="{root_rel}index.html#guias">Guías</a></li>
        <li><a href="{root_rel}index.html#faq">FAQ Clínica</a></li>
      </ul>
      <div class="nav-actions">
        <a href="{root_rel}index.html#comparador" class="btn-nav-compare">
          <span>⚡ Comparar</span>
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
        <h3>Odonto<span style="color:#0EA5E9">Score</span></h3>
        <p style="margin-bottom:1rem;color:#94A3B8;">Plataforma unificada de análisis clínico y comparativas de dispositivos de odontología e higiene bucodental.</p>
        <p style="font-size:0.85rem;color:#64748B;">Evaluación basada en evidencia clínica, presión hidráulica PSI, tecnología sónica y protección gingival.</p>
      </div>
      <div class="footer-col">
        <h4>Especialidades</h4>
        <ul class="footer-links">
          <li><a href="{root_rel}categoria/cepillos-electricos.html">Cepillos Eléctricos</a></li>
          <li><a href="{root_rel}categoria/irrigadores-dentales.html">Irrigadores Dentales</a></li>
          <li><a href="{root_rel}categoria/blanqueamiento-dental.html">Blanqueamiento Dental</a></li>
          <li><a href="{root_rel}categoria/ortodoncia-brackets.html">Ortodoncia y Brackets</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Herramientas</h4>
        <ul class="footer-links">
          <li><a href="{root_rel}comparador.html">Comparador Avanzado</a></li>
          <li><a href="{root_rel}ofertas.html">Ofertas del Día</a></li>
          <li><a href="{root_rel}guias/mejor-irrigador-dental-brackets-2026.html">Guía Irrigadores Brackets</a></li>
          <li><a href="{root_rel}guias/mejor-cepillo-electrico-encias-sensibles-2026.html">Guía Encías Sensibles</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Transparencia Legal</h4>
        <ul class="footer-links">
          <li><a href="{root_rel}aviso-afiliados.html">Aviso de Afiliación</a></li>
          <li><a href="{root_rel}privacidad.html">Privacidad y Cookies</a></li>
          <li><a href="{root_rel}sobre-nosotros.html">Metodología E-E-A-T</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-disclaimers">
      <p><strong>Aviso de Afiliación de Amazon:</strong> En calidad de Afiliado de Amazon, obtenemos ingresos por las compras adscritas que cumplen los requisitos aplicables. «Amazon» y el logotipo de Amazon son marcas comerciales de Amazon.com, Inc. o sus filiales.</p>
      <p><strong>Descargo de Responsabilidad Médica:</strong> Los análisis y comparativas de OdontoScore tienen carácter meramente informativo y divulgativo sobre dispositivos de higiene oral. No constituyen diagnóstico ni recomendación médica personalizada. Ante cualquier patología dental, consulte siempre a su odontólogo colegiado.</p>
    </div>
    <div class="footer-bottom-copy">
      © 2026 OdontoScore (odontoscore.com). Todos los derechos reservados.
    </div>
  </div>
</footer>
"""


def render_product_card(p, root_rel=""):
    discount_pct = round((1 - p["discountedPrice"] / p["retailPrice"]) * 100) if p["discountedPrice"] < p["retailPrice"] else 0
    return f"""
<article class="product-card" data-producto-id="{p['id']}" data-asin="{p['asin']}" data-category="{p['categoria_odontologica']}">
  {'<span class="card-badge-top">Top Clínico</span>' if p.get('isFeatured') else ''}
  {f'<span class="card-badge-offer">-{discount_pct}%</span>' if discount_pct > 0 else ''}
  <div class="card-media">
    <img src="{root_rel}{p['images'][0]}" alt="{p['name']}" loading="lazy">
  </div>
  <div class="card-body">
    <span class="card-brand">{p['marca']}</span>
    <h3 class="card-title">{p['name']}</h3>
    <div class="card-rating">
      <span class="rating-stars">★ {p['valoracion_media']}</span>
      <span class="review-count">({p['resenas_cantidad']:,} valoraciones)</span>
    </div>
    <div class="card-specs-mini">
      <span class="spec-pill">{p['tecnologia'].upper()}</span>
      <span class="spec-pill">{p['modos_limpieza']} Modos</span>
      <span class="spec-pill">{'App IA' if p['app_conectada'] else (f"{p['presion_agua_psi']} PSI" if p.get('presion_agua_psi') else 'Clínico')}</span>
    </div>
    <div class="card-price-box">
      <div>
        <span class="price-current">{p['discountedPrice']} €</span>
        {f'<span class="price-old">{p["retailPrice"]} €</span>' if discount_pct > 0 else ''}
      </div>
      <small class="price-date" style="color:#64748B;font-size:0.75rem;">Sincronizado</small>
    </div>
    <div class="card-cta-group">
      <button type="button" class="btn-card-ficha" data-quick-view="{p['id']}">⚡ Ficha Rápida</button>
      <a href="{p['affiliate_url']}" target="_blank" rel="sponsored nofollow noopener" class="btn-card-amazon">Ver en Amazon</a>
    </div>
  </div>
</article>
"""


def build_home(products):
    cards_html = "\n".join([render_product_card(p, "") for p in products])
    deal_cards_html = "\n".join([render_product_card(p, "") for p in products if p["discountedPrice"] < p["retailPrice"]])
    options_cats = "".join([f'<option value="{c["id"]}">{c["name"]}</option>' for c in CATEGORIES])

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OdontoScore — Portal Unificado de Comparativas Clínicas y Productos de Odontología 2026</title>
  <meta name="description" content="Todo en uno: catálogo clínico, comparador dinámico de 7 ejes, ofertas en tiempo real y fichas técnicas de cepillos eléctricos e irrigadores dentales.">
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
          <span>🩺 Portal Clínico OdontoScore 2026</span>
        </div>
        <h1 class="hero-title">Comparador y Catálogo Dental de <span>Alta Autoridad</span></h1>
        <p class="hero-subtitle">Encuentra y compara los mejores dispositivos de salud bucodental: cepillos sónicos y magnéticos, irrigadores de sobremesa, blanqueamiento e instrumental médico con datos técnicos normalizados.</p>
        <div class="hero-actions">
          <a href="#catalogo" class="btn-primary">🔍 Explorar Catálogo ({len(products)} Productos)</a>
          <a href="#comparador" class="btn-secondary">⚡ Abrir Comparador</a>
        </div>
        <div class="hero-trust-bullets">
          <span>✓ Sellos ADA & SEPA</span>
          <span>✓ Radar Clínico de 7 Ejes</span>
          <span>✓ Precios en Tiempo Real</span>
        </div>
      </div>
      <div class="hero-visual">
        <img src="assets/img/hero-dental.svg" alt="OdontoScore Comparativas Clínicas" fetchpriority="high">
      </div>
    </div>
  </section>

  <!-- 1. Interactive Catalog with Category Filters -->
  <section id="catalogo" class="section-block">
    <div class="container">
      <div class="section-header">
        <div class="hero-badge">📦 Catálogo Normalizado</div>
        <h2 class="section-title">Dispositivos Odontológicos Verificados</h2>
        <p class="section-desc">Filtra por especialidad clínica y haz clic en <strong>⚡ Ficha Rápida</strong> para abrir el análisis técnico instantáneo.</p>
      </div>

      <div class="filter-pills-bar" data-catalog-filters>
        <button type="button" class="filter-pill-btn active" data-filter="all">Todos ({len(products)})</button>
        <button type="button" class="filter-pill-btn" data-filter="cepillos_electricos">🪥 Cepillos Eléctricos</button>
        <button type="button" class="filter-pill-btn" data-filter="irrigadores_dentales">💧 Irrigadores</button>
        <button type="button" class="filter-pill-btn" data-filter="blanqueamiento_dental">✨ Blanqueamiento</button>
        <button type="button" class="filter-pill-btn" data-filter="ortodoncia_brackets">🦷 Ortodoncia</button>
        <button type="button" class="filter-pill-btn" data-filter="higiene_infantil">🧸 Infantil</button>
        <button type="button" class="filter-pill-btn" data-filter="instrumental_basico">🔬 Instrumental</button>
      </div>

      <div class="product-grid">
        {cards_html}
      </div>
    </div>
  </section>

  <!-- 2. Integrated Clinical Comparator -->
  <section id="comparador" class="section-block" style="background-color: var(--color-surface);">
    <div class="container" data-comparator-app>
      <div class="section-header">
        <div class="hero-badge">⚡ Enfrentamiento Lado a Lado</div>
        <h2 class="section-title">Comparador Clínico Integrado</h2>
        <p class="section-desc">Selecciona hasta 4 modelos para ver sus especificaciones técnicas y gráficos radar superpuestos sin cambiar de pantalla.</p>
      </div>

      <div class="comparator-selector-bar" style="background:#FFFFFF;box-shadow:var(--shadow-sm);">
        <div>
          <label for="compCategorySelect" style="font-weight:700;font-size:0.95rem;margin-right:0.75rem;">Filtrar Especialidad:</label>
          <select id="compCategorySelect" style="padding:0.6rem 1rem;border-radius:var(--radius-md);border:1px solid var(--color-border);font-family:var(--font-sans);font-size:0.95rem;">
            <option value="">Todas las Especialidades</option>
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

  <!-- 3. Deals Section -->
  <section id="ofertas" class="section-block">
    <div class="container">
      <div class="section-header">
        <div class="hero-badge">🏷️ Rebajas Verificadas</div>
        <h2 class="section-title">Ofertas y Descuentos Activos</h2>
        <p class="section-desc">Productos odontológicos con precio rebajado respecto al PVP oficial de fabricante.</p>
      </div>
      <div class="product-grid">
        {deal_cards_html}
      </div>
    </div>
  </section>

  <!-- 4. Clinical Buying Guides & Authority Section -->
  <section id="guias" class="section-block" style="background-color: var(--color-surface);">
    <div class="container">
      <div class="section-header">
        <div class="hero-badge">📖 Criterio Clínico</div>
        <h2 class="section-title">Guías Odontológicas Destacadas</h2>
        <p class="section-desc">Artículos técnicos elaborados según consensos periodontales y ortodónticos.</p>
      </div>

      <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(300px, 1fr));gap:1.5rem;">
        <div style="background:#FFFFFF;padding:2rem;border-radius:16px;border:1px solid #E2E8F0;box-shadow:var(--shadow-sm);">
          <span style="font-size:2rem;">💧</span>
          <h3 style="font-size:1.3rem;margin:0.75rem 0 0.5rem;">Mejor Irrigador para Brackets 2026</h3>
          <p style="color:#64748B;font-size:0.95rem;margin-bottom:1.5rem;">Por qué la presión pulsátil de 45-90 PSI es imprescindible para evitar la descalcificación del esmalte con ortodoncia fija.</p>
          <a href="guias/mejor-irrigador-dental-brackets-2026.html" class="category-link">Leer Guía Completa →</a>
        </div>

        <div style="background:#FFFFFF;padding:2rem;border-radius:16px;border:1px solid #E2E8F0;box-shadow:var(--shadow-sm);">
          <span style="font-size:2rem;">🪥</span>
          <h3 style="font-size:1.3rem;margin:0.75rem 0 0.5rem;">Cepillos para Encías Sensibles</h3>
          <p style="color:#64748B;font-size:0.95rem;margin-bottom:1.5rem;">Sónico vs Magnético: comparativa de tecnologías con control activo de fricción y sensores de sobrepresión.</p>
          <a href="guias/mejor-cepillo-electrico-encias-sensibles-2026.html" class="category-link">Leer Guía Completa →</a>
        </div>
      </div>
    </div>
  </section>

  <!-- 5. Clinical FAQ Section (GEO Block for AI) -->
  <section id="faq" class="section-block">
    <div class="container" style="max-width:850px;">
      <div class="section-header">
        <div class="hero-badge">❓ Preguntas Frecuentes</div>
        <h2 class="section-title">Preguntas Frecuentes para Pacientes e IA</h2>
        <p class="section-desc">Respuestas estructuradas a las dudas más comunes sobre higiene bucodental.</p>
      </div>

      <div class="geo-ai-box" style="background:#FFFFFF;border:1px solid #E2E8F0;">
        <div class="geo-qa-item">
          <strong>¿Qué es más recomendable: cepillo sónico o rotatorio magnético?</strong>
          <p>Ambas tecnologías superan ampliamente al cepillado manual. El sistema rotatorio magnético (como Oral-B iO) es excelente para eliminar placa contorneando diente por diente, mientras que el sónico (Philips Sonicare) genera microburbujas hidrodinámicas ideales para encías sensibles y recesión gingival.</p>
        </div>
        <div class="geo-qa-item">
          <strong>¿El irrigador dental sustituye al hilo dental?</strong>
          <p>El irrigador complementa al cepillado. Para pacientes con brackets, implantes o bolsas periodontales, los estudios demuestran que la irrigación con boquillas especializadas elimina significativamente más biofilm y reduce el sangrado gingival.</p>
        </div>
        <div class="geo-qa-item">
          <strong>¿Son seguros los kits de blanqueamiento dental LED caseros?</strong>
          <p>Sí, siempre que no contengan concentraciones de peróxido de hidrógeno superiores al 0.1% permitido en la UE o utilicen agentes no abrasivos con luz fría para evitar quemaduras químicas o hipersensibilidad dental.</p>
        </div>
      </div>
    </div>
  </section>

  {render_footer('')}

  <!-- Interactive Quick-View Modal (Ficha Rápida) -->
  <div class="quick-modal-backdrop" id="quickViewModal">
    <div class="quick-modal-box">
      <button type="button" class="quick-modal-close-btn" aria-label="Cerrar">&times;</button>
      <span id="modalBrand" class="card-brand" style="display:inline-block;margin-bottom:0.25rem;">Marca</span>
      <h2 id="modalTitle" style="font-size:1.5rem;margin-bottom:0.5rem;color:#0F172A;">Nombre del Producto</h2>
      <div style="font-size:1.4rem;font-weight:800;color:#0E76BC;margin-bottom:1rem;" id="modalPrice">0,00 €</div>

      <div class="quick-modal-grid">
        <div>
          <div style="background:#F8FAFC;border-radius:12px;padding:1rem;text-align:center;margin-bottom:1rem;border:1px solid #E2E8F0;">
            <img id="modalImg" src="" alt="Vista previa" style="max-height:220px;margin:0 auto;">
          </div>
          <div class="radar-canvas-container" id="modalRadarCanvas" style="min-height:240px;"></div>
        </div>
        <div>
          <h4 style="margin-bottom:0.5rem;">Ficha Técnica Rápida</h4>
          <table class="specs-table" id="modalSpecsTable" style="margin-bottom:1.5rem;">
            <tbody></tbody>
          </table>
          <div style="display:flex;flex-direction:column;gap:0.75rem;">
            <a id="modalBuyBtn" href="#" target="_blank" rel="sponsored nofollow noopener" class="btn-buy-amazon-large" style="width:100%;text-align:center;justify-content:center;">
              <span>🛒 Ver Oferta en Amazon</span>
            </a>
            <a id="modalFullLink" href="#" target="_blank" class="btn-secondary" style="width:100%;text-align:center;justify-content:center;">
              <span>📄 Ver Ficha Completa y Análisis Editorial</span>
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
    "name": "OdontoScore - Comparador Profesional Dental",
    "url": "{BASE_URL}/",
    "description": "Portal de comparativas y análisis técnicos de productos de odontología e higiene bucodental.",
    "about": {{
      "@type": "MedicalCondition",
      "name": "Higiene Bucodental y Prevención Periodontal"
    }}
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
    thumbs_html = "\n".join([f'<li class="gallery-thumb-btn {"active" if idx==0 else ""}" data-src="../{img}"><img src="../{img}" alt="Miniatura {idx+1}"></li>' for idx, img in enumerate(p["images"])])
    pros_html = "\n".join([f'<li>{pro}</li>' for pro in p["pros"]])
    contras_html = "\n".join([f'<li>{contra}</li>' for contra in p["contras"]])
    badges_ind = " ".join([f'<span class="spec-pill" style="background:#E0F2FE;color:#0369A1;font-weight:700;">{ind.replace("_", " ").upper()}</span>' for ind in p.get("indicado_para", [])])

    extra_specs_rows = ""
    if p.get("specs_extra"):
        for k, v in p["specs_extra"].items():
            extra_specs_rows += f'<tr><th>{k}</th><td>{v}</td></tr>'

    geo_faq_html = ""
    faq_schema_items = []
    if p.get("geo_faq"):
        for item in p["geo_faq"]:
            geo_faq_html += f"""
            <div class="geo-qa-item">
              <strong>{item['q']}</strong>
              <p>{item['a']}</p>
            </div>
            """
            faq_schema_items.append({
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item["a"]
                }
            })

    faq_json_str = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_schema_items
    }, ensure_ascii=False) if faq_schema_items else ""

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{p['name']} — Análisis Técnico, Opiniones y Precio | OdontoScore</title>
  <meta name="description" content="{p['description']}">
  <link rel="canonical" href="{BASE_URL}/producto/{p_id}.html" />
  <link rel="alternate" hreflang="es" href="{BASE_URL}/producto/{p_id}.html" />
  <link rel="alternate" hreflang="x-default" href="{BASE_URL}/producto/{p_id}.html" />
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
      <a href="../categoria/{p['categoria_odontologica'].replace('_', '-')}.html">{p['category']}</a> <span>/</span>
      <span>{p['marca']} {p['name'][:30]}...</span>
    </nav>

    <div class="ficha-hero-grid">
      <!-- Galería WebP -->
      <div class="ficha-gallery-wrapper" data-galeria>
        <div class="gallery-main-view">
          <img class="gallery-main-img" src="../{p['images'][0]}" alt="{p['name']}">
        </div>
        <ul class="gallery-thumbs-list">
          {thumbs_html}
        </ul>
      </div>

      <!-- Cabecera y Compra -->
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
          <p class="ficha-price-note">Precio orientativo · Captura: <span class="price-date">{p['precio_fecha']}</span> · Consúltalo en tiempo real en Amazon</p>
        </div>

        <a href="{p['affiliate_url']}" target="_blank" rel="sponsored nofollow noopener" class="btn-buy-amazon-large">
          <span>🛒 Ver Oferta en Amazon</span>
        </a>

        <div style="display:flex;gap:0.75rem;margin-top:1rem;">
          <a href="../comparador.html" class="btn-secondary" style="width:100%;text-align:center;justify-content:center;">⚡ Comparar este Modelo</a>
        </div>
      </div>
    </div>

    <!-- 3. Radar de 7 Ejes -->
    <section class="radar-section-box">
      <h2 style="font-size:1.5rem;margin-bottom:0.5rem;">Evaluación Clínica OdontoScore (Radar 7 Ejes)</h2>
      <p style="color:#64748B;font-size:0.95rem;margin-bottom:1.5rem;">Puntuaciones objetivas sobre 10 calculadas a partir de especificaciones de laboratorio y fabricante.</p>
      
      <div class="radar-grid-layout">
        <div class="radar-canvas-container" data-radar data-radar-id="{p_id}"></div>
        <div class="radar-scores-breakdown">
          <div class="score-row-item"><span>Eficacia Limpieza Biofilm:</span> <span class="score-val">{p['score_eficacia']} / 10</span></div>
          <div class="score-row-item"><span>Protección y Confort de Encías:</span> <span class="score-val">{p['score_comodidad_encias']} / 10</span></div>
          <div class="score-row-item"><span>Durabilidad y Materiales:</span> <span class="score-val">{p['score_durabilidad']} / 10</span></div>
          <div class="score-row-item"><span>Facilidad de Uso y Batería:</span> <span class="score-val">{p['score_facilidad_uso']} / 10</span></div>
          <div class="score-row-item"><span>Nivel de Silencio (dB):</span> <span class="score-val">{p['score_silencio']} / 10</span></div>
          <div class="score-row-item"><span>Innovación y Tecnología:</span> <span class="score-val">{p['score_tecnologia']} / 10</span></div>
          <div class="score-row-item"><span>Relación Calidad-Precio:</span> <span class="score-val">{p['score_calidad_precio']} / 10</span></div>
        </div>
      </div>
    </section>

    <!-- 4. Tabla de Especificaciones Normalizadas -->
    <section class="dental-specs-table-box">
      <h2 style="font-size:1.5rem;margin-bottom:1rem;">Ficha Técnica Normalizada</h2>
      <table class="specs-table">
        <tbody>
          <tr><th>Marca y Modelo</th><td>{p['marca']} {p['name']}</td></tr>
          <tr><th>Categoría Odontológica</th><td>{p['category']} ({p['tipo_producto']})</td></tr>
          <tr><th>Tecnología Principal</th><td>{p['tecnologia'].upper()}</td></tr>
          <tr><th>Programas / Modos de Limpieza</th><td>{p['modos_limpieza']} modos configurables</td></tr>
          <tr><th>Potencia Hidráulica / Presión</th><td>{f"{p['presion_agua_psi']} PSI (Ajustable)" if p.get('presion_agua_psi') else "—"}</td></tr>
          <tr><th>Capacidad del Depósito</th><td>{f"{p['capacidad_deposito_ml']} ml" if p.get('capacidad_deposito_ml') else "—"}</td></tr>
          <tr><th>Frecuencia de Movimiento / Pulsaciones</th><td>{f"{p['pulsaciones_min']:,} pulsaciones/min" if p.get('pulsaciones_min') else "—"}</td></tr>
          <tr><th>Autonomía de Batería</th><td>{f"{p['autonomia_dias']} días" if p['autonomia_dias'] < 365 else "Conexión a red eléctrica continua"}</td></tr>
          <tr><th>Tiempo de Carga Completa</th><td>{f"{p['tiempo_carga_h']} horas" if p['tiempo_carga_h'] > 0 else "No aplica (AC)"}</td></tr>
          <tr><th>Cabezales / Boquillas Incluidas</th><td>{p['cabezales_incluidos']} unidad(es) de serie</td></tr>
          <tr><th>Nivel Sonoro</th><td>{p['nivel_ruido_db']} dB</td></tr>
          <tr><th>Impermeabilidad</th><td>{p['resistencia_ipx']} (Resistente al agua en ducha/lavabo)</td></tr>
          <tr><th>Conectividad y Sensores</th><td>{'App Bluetooth + Sensores Inteligentes' if p['app_conectada'] else 'Funcionamiento autónomo con temporizador'}</td></tr>
          <tr><th>Materiales y Acabados</th><td>{p['material']}</td></tr>
          <tr><th>Indicaciones Clínicas Específicas</th><td>{', '.join([i.replace('_', ' ').capitalize() for i in p.get('indicado_para', [])])}</td></tr>
          {extra_specs_rows}
        </tbody>
      </table>
    </section>

    <!-- 5. Análisis Editorial, Pros y Contras -->
    <section class="editorial-content-box">
      <h2 style="font-size:1.6rem;margin-bottom:1.5rem;">Veredicto del Especialista Clínico</h2>
      <div class="editorial-body">
        {p['cuerpo_editorial']}
      </div>

      <div class="pros-contras-grid">
        <div class="pros-box">
          <h3>Ventajas Clínicas</h3>
          <ul class="pros-list">
            {pros_html}
          </ul>
        </div>
        <div class="contras-box">
          <h3>A Tener en Cuenta</h3>
          <ul class="contras-list">
            {contras_html}
          </ul>
        </div>
      </div>

      <div class="ideal-para-banner">
        <p><strong>¿Para quién es ideal?</strong> {p['ideal_para']}</p>
      </div>

      <div style="background:#F8FAFC;padding:1.5rem;border-radius:var(--radius-lg);margin-bottom:2rem;border:1px solid #E2E8F0;">
        <h3 style="font-size:1.1rem;margin-bottom:0.5rem;color:#0F172A;">Resumen de Reseñas de Pacientes y Compradores</h3>
        <p style="color:#475569;font-size:0.95rem;">{p['resenas_resumen']}</p>
      </div>

      <!-- 6. Bloque GEO para IA -->
      <div class="geo-ai-box">
        <h3>Preguntas Estructuradas para IA y Pacientes (GEO Block)</h3>
        {geo_faq_html}
      </div>

      <div style="text-align:center;padding-top:1rem;">
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
    "image": ["{BASE_URL}/{p['images'][0]}"],
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
      "priceValidUntil": "2026-12-31",
      "availability": "https://schema.org/InStock"
    }},
    "aggregateRating": {{
      "@type": "AggregateRating",
      "ratingValue": "{p['valoracion_media']}",
      "reviewCount": "{p['resenas_cantidad']}"
    }}
  }}
  </script>

  {f'<script type="application/ld+json">{faq_json_str}</script>' if faq_json_str else ''}
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
  <title>Comparador Profesional Dental — Enfrenta Dispositivos de Odontología | OdontoScore</title>
  <meta name="description" content="Compara hasta 4 dispositivos dentales de la misma categoría lado a lado: presión PSI, pulsaciones, modos, decibelios y radar de 7 ejes superpuesto.">
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
      <div class="hero-badge">⚡ Motor Intra-Categoría</div>
      <h1 style="font-size:2.4rem;margin-bottom:0.75rem;">Comparador Clínico Dental</h1>
      <p style="color:#64748B;font-size:1.1rem;">Selecciona tu categoría y hasta 4 dispositivos para ver especificaciones técnicas lado a lado y sus gráficos radar superpuestos.</p>
    </div>

    <div class="comparator-selector-bar">
      <div>
        <label for="compCategorySelect" style="font-weight:700;font-size:0.95rem;margin-right:0.75rem;">Categoría:</label>
        <select id="compCategorySelect" style="padding:0.6rem 1rem;border-radius:var(--radius-md);border:1px solid var(--color-border);font-family:var(--font-sans);font-size:0.95rem;">
          <option value="">Todas las Categorías</option>
          {options_cats}
        </select>
      </div>
      <div id="compProductChecks" style="display:flex;flex-wrap:wrap;align-items:center;">
        <!-- Checkboxes injected by main.js -->
      </div>
    </div>

    <!-- Superposición de Radares -->
    <div class="radar-section-box" style="margin-bottom:2.5rem;">
      <h2 style="font-size:1.4rem;margin-bottom:0.5rem;">Radar Multiproducto Superpuesto</h2>
      <p style="color:#64748B;font-size:0.9rem;margin-bottom:1rem;">Visualiza fortalezas y debilidades clínicas de cada modelo en los 7 ejes.</p>
      <div id="compRadarLegend" style="margin-bottom:1.5rem;display:flex;flex-wrap:wrap;gap:0.75rem;"></div>
      <div class="radar-canvas-container" id="compRadarCanvas" style="min-height:340px;"></div>
    </div>

    <!-- Tabla Comparativa -->
    <div class="comparator-table-scroll" id="compMatrixContent">
      <!-- Matrix injected by main.js -->
    </div>
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


def build_category_pages(products):
    cat_dir = ROOT / "categoria"
    cat_dir.mkdir(exist_ok=True)

    for c in CATEGORIES:
        cat_id = c["id"]
        cat_slug = c["slug"]
        cat_products = [p for p in products if p["categoria_odontologica"] == cat_id]
        
        cards = "\n".join([render_product_card(p, "../") for p in cat_products]) if cat_products else f"""
        <div style="grid-column:1/-1;padding:3rem;text-align:center;background:#F8FAFC;border-radius:16px;border:1px dashed #CBD5E1;">
          <h3>Próximamente más productos en {c['name']}</h3>
          <p style="color:#64748B;margin-top:0.5rem;">Estamos sincronizando y normalizando nuevos productos dentales para esta categoría.</p>
        </div>
        """

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{c['name']} — Comparativas, Fichas Técnicas y Precios | OdontoScore</title>
  <meta name="description" content="{c['desc']}">
  <link rel="canonical" href="{BASE_URL}/categoria/{cat_slug}.html" />
  <link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css?v={VER}">
</head>
<body>
  {render_header('', '../')}

  <main class="container section-block">
    <nav class="ficha-breadcrumb">
      <a href="../index.html">Inicio</a> <span>/</span>
      <span>Categorías</span> <span>/</span>
      <span>{c['name']}</span>
    </nav>

    <div class="section-header" style="text-align:left;max-width:100%;margin-bottom:2.5rem;">
      <div class="category-icon" style="display:inline-flex;margin-bottom:0.75rem;">{c['icon']}</div>
      <h1 style="font-size:2.4rem;margin-bottom:0.5rem;">{c['name']}</h1>
      <p style="color:#64748B;font-size:1.1rem;max-width:750px;">{c['desc']}</p>
    </div>

    <div class="product-grid">
      {cards}
    </div>
  </main>

  {render_footer('../')}

  <script defer src="../lib/manifest.js"></script>
  <script defer src="../lib/db.js?v={VER}"></script>
  <script defer src="../main.js?v={VER}"></script>
</body>
</html>
"""
        with open(cat_dir / f"{cat_slug}.html", "w", encoding="utf-8") as f:
            f.write(html)


def build_guides(products):
    guias_dir = ROOT / "guias"
    guias_dir.mkdir(exist_ok=True)

    g1_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mejor Irrigador Dental para Brackets y Ortodoncia 2026 — Guía Clínica</title>
  <meta name="description" content="Comparativa clínica de los mejores irrigadores bucales para pacientes con ortodoncia, brackets e implantes. Presión PSI recomendada y boquillas.">
  <link rel="canonical" href="{BASE_URL}/guias/mejor-irrigador-dental-brackets-2026.html" />
  <link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css?v={VER}">
</head>
<body>
  {render_header('guias', '../')}

  <main class="container section-block" style="max-width:900px;">
    <div class="hero-badge">📖 Guía Clínica Especializada 2026</div>
    <h1 style="font-size:2.5rem;margin-bottom:1rem;">Mejor Irrigador Dental para Brackets y Ortodoncia en 2026</h1>
    <p style="color:#64748B;font-size:1.1rem;margin-bottom:2rem;">La acumulación de placa alrededor de los brackets de ortodoncia multiplica por 3 el riesgo de descalcificación del esmalte y gingivitis. Analizamos los requisitos técnicos esenciales para elegir tu irrigador.</p>

    <div class="editorial-content-box">
      <h2>1. Por qué el cepillo no basta con ortodoncia fija</h2>
      <p class="editorial-body">Los arcos y bandas ortodónticas crean áreas de retención mecánica donde los filamentos del cepillo manual o eléctrico convencional no pueden penetrar. Un chorro de agua pulsátil a presión controlada (entre 45 y 90 PSI) logra desorganizar el biofilm bacteriano interdental sin dañar los componentes del bracket.</p>

      <h2>2. El Ganador Clínico: Waterpik Ultra Professional WP-660EU</h2>
      <p class="editorial-body">Gracias a su boquilla <em>Orthodontic Tip</em> con penacho de cerdas cónicas y su presión regulable de 10 a 100 PSI con sello oficial de la ADA, el <strong>Waterpik WP-660EU</strong> se posiciona como la opción de máxima evidencia clínica.</p>
      
      <div style="background:#F8FAFC;padding:1.5rem;border-radius:12px;border:1px solid #CBD5E1;margin:1.5rem 0;">
        <h3>Waterpik WP-660EU (Sobremesa)</h3>
        <p style="margin-bottom:1rem;">Presión: 10-100 PSI · Depósito: 650 ml · Boquillas: 7 incluidas</p>
        <a href="https://www.amazon.es/dp/B00USBV1N8?tag={AMAZON_PARTNER_TAG}" target="_blank" rel="sponsored nofollow noopener" class="btn-card-amazon" style="display:inline-block;padding:0.75rem 1.5rem;">Ver Oferta en Amazon</a>
        <a href="../producto/waterpik-ultra-professional-wp-660eu.html" class="btn-card-ficha" style="display:inline-block;margin-left:0.5rem;padding:0.75rem 1.5rem;">Leer Ficha Técnica</a>
      </div>
    </div>
  </main>

  {render_footer('../')}

  <script defer src="../lib/manifest.js"></script>
  <script defer src="../lib/db.js?v={VER}"></script>
  <script defer src="../main.js?v={VER}"></script>
</body>
</html>
"""
    with open(guias_dir / "mejor-irrigador-dental-brackets-2026.html", "w", encoding="utf-8") as f:
        f.write(g1_html)

    g2_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mejor Cepillo Eléctrico para Encías Sensibles 2026 — Sónico vs Rotatorio</title>
  <meta name="description" content="Análisis de cepillos eléctricos para retracción de encías y gingivitis: Oral-B iO con microvibraciones vs Philips Sonicare con SenseIQ.">
  <link rel="canonical" href="{BASE_URL}/guias/mejor-cepillo-electrico-encias-sensibles-2026.html" />
  <link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css?v={VER}">
</head>
<body>
  {render_header('guias', '../')}

  <main class="container section-block" style="max-width:900px;">
    <div class="hero-badge">📖 Comparativa Clínica 2026</div>
    <h1 style="font-size:2.5rem;margin-bottom:1rem;">Mejor Cepillo Eléctrico para Encías Sensibles y Sangrado</h1>
    <p style="color:#64748B;font-size:1.1rem;margin-bottom:2rem;">El cepillado agresivo es la causa principal de la recesión gingival y abrasión del cuello dental. Analizamos qué tecnología protege mejor tus encías.</p>

    <div class="editorial-content-box">
      <h2>Sónico vs Rotatorio Magnético para Encías Delicadas</h2>
      <p class="editorial-body">Tanto el <strong>Oral-B iO Series 9</strong> como el <strong>Philips Sonicare 9900 Prestige</strong> representan la vanguardia en protección activa de encías.</p>
    </div>
  </main>

  {render_footer('../')}

  <script defer src="../lib/manifest.js"></script>
  <script defer src="../lib/db.js?v={VER}"></script>
  <script defer src="../main.js?v={VER}"></script>
</body>
</html>
"""
    with open(guias_dir / "mejor-cepillo-electrico-encias-sensibles-2026.html", "w", encoding="utf-8") as f:
        f.write(g2_html)


def build_ofertas(products):
    deal_prods = [p for p in products if p["discountedPrice"] < p["retailPrice"]]
    cards = "\n".join([render_product_card(p, "") for p in deal_prods])
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ofertas en Productos de Odontología — Descuentos Activos | OdontoScore</title>
  <meta name="description" content="Listado actualizado de cepillos eléctricos e irrigadores dentales con descuento y precio rebajado en Amazon España.">
  <link rel="canonical" href="{BASE_URL}/ofertas.html" />
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css?v={VER}">
</head>
<body>
  {render_header('ofertas', '')}

  <main class="container section-block">
    <div class="section-header" style="text-align:left;max-width:100%;margin-bottom:2.5rem;">
      <div class="hero-badge">🏷️ Descuentos y Rebajas Activas</div>
      <h1 style="font-size:2.4rem;margin-bottom:0.5rem;">Ofertas en Cuidado Bucal</h1>
      <p style="color:#64748B;font-size:1.1rem;">Dispositivos dentales de alta gama con precio rebajado respecto al PVP oficial de fabricante.</p>
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


def build_legal_pages():
    aviso_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aviso Legal de Afiliados y Descargo Médico | OdontoScore</title>
  <link rel="canonical" href="{BASE_URL}/aviso-afiliados.html" />
  <link rel="stylesheet" href="styles.css?v={VER}">
</head>
<body>
  {render_header('', '')}
  <main class="container section-block" style="max-width:850px;">
    <h1>Aviso de Afiliación y Descargo Médico</h1>
    <div class="editorial-content-box" style="margin-top:2rem;">
      <h2>1. Participación en el Programa de Afiliados de Amazon</h2>
      <p class="editorial-body">OdontoScore (odontoscore.com) participa en el Programa de Afiliados de Amazon EU con el tag <code>odontoscore-21</code>.</p>
      <h2>2. Descargo de Responsabilidad Médica y Odontológica</h2>
      <p class="editorial-body">El contenido publicado en OdontoScore tiene una finalidad exclusivamente informativa y no sustituye el diagnóstico u orientación de un odontólogo colegiado.</p>
    </div>
  </main>
  {render_footer('')}
  <script defer src="lib/manifest.js"></script>
  <script defer src="main.js?v={VER}"></script>
</body>
</html>
"""
    with open(ROOT / "aviso-afiliados.html", "w", encoding="utf-8") as f:
        f.write(aviso_html)

    priv_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Política de Privacidad | OdontoScore</title>
  <link rel="canonical" href="{BASE_URL}/privacidad.html" />
  <link rel="stylesheet" href="styles.css?v={VER}">
</head>
<body>
  {render_header('', '')}
  <main class="container section-block" style="max-width:850px;">
    <h1>Política de Privacidad y Cookies</h1>
    <div class="editorial-content-box" style="margin-top:2rem;">
      <p class="editorial-body">OdontoScore respeta la privacidad de sus visitantes y no recopila datos personales identificables sin consentimiento.</p>
    </div>
  </main>
  {render_footer('')}
  <script defer src="lib/manifest.js"></script>
  <script defer src="main.js?v={VER}"></script>
</body>
</html>
"""
    with open(ROOT / "privacidad.html", "w", encoding="utf-8") as f:
        f.write(priv_html)

    sobre_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Metodología E-E-A-T y Quiénes Somos | OdontoScore</title>
  <link rel="canonical" href="{BASE_URL}/sobre-nosotros.html" />
  <link rel="stylesheet" href="styles.css?v={VER}">
</head>
<body>
  {render_header('', '')}
  <main class="container section-block" style="max-width:850px;">
    <h1>Metodología E-E-A-T y Criterios Clínicos</h1>
    <div class="editorial-content-box" style="margin-top:2rem;">
      <p class="editorial-body">OdontoScore nace con el objetivo de dotar de rigor y transparencia a la elección de productos de salud bucodental evaluando 7 ejes de rendimiento.</p>
    </div>
  </main>
  {render_footer('')}
  <script defer src="lib/manifest.js"></script>
  <script defer src="main.js?v={VER}"></script>
</body>
</html>
"""
    with open(ROOT / "sobre-nosotros.html", "w", encoding="utf-8") as f:
        f.write(sobre_html)


def build_db_js(products):
    db_obj = {
        "productos": products,
        "nichos": ["productos-odontologia"],
        "scoreAxes": ["eficacia", "comodidad_encias", "durabilidad", "facilidad_uso", "silencio", "tecnologia", "calidad_precio"],
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
    for c in CATEGORIES:
        urls.append(f"{BASE_URL}/categoria/{c['slug']}.html")
    for p in products:
        urls.append(f"{BASE_URL}/producto/{p['id']}.html")

    sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sitemap_xml.append(f"  <url><loc>{u}</loc><lastmod>2026-08-22</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>")
    sitemap_xml.append('</urlset>')

    with open(ROOT / "sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(sitemap_xml))

    with open(ROOT / "robots.txt", "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")


def main():
    print("=== OdontoScore Unified Landing & Portal Builder ===")
    products = load_products()
    print(f"Loaded {len(products)} products for compilation")

    build_db_js(products)
    print("[OK] Generated lib/db.js")

    build_home(products)
    print("[OK] Generated all-in-one landing index.html")

    build_comparator(products)
    print("[OK] Generated comparador.html")

    build_category_pages(products)
    print("[OK] Generated category pages in categoria/")

    for p in products:
        build_ficha(p)
    print(f"[OK] Generated {len(products)} product fichas in producto/")

    build_guides(products)
    print("[OK] Generated buying guides in guias/")

    build_ofertas(products)
    print("[OK] Generated ofertas.html")

    build_legal_pages()
    print("[OK] Generated legal pages")

    build_sitemaps_and_robots(products)
    print("[OK] Generated sitemap.xml and robots.txt")

    print(f"\n[OK] Build complete with version: {VER}")


if __name__ == "__main__":
    main()
