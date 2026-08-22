#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Populate all ASINs into Supabase database."""

import json
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from supabase import create_client

ROOT = Path(__file__).resolve().parent.parent
ASINS_FILE = ROOT / "asins.json"

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "").strip()

if not (SUPABASE_URL and SUPABASE_SERVICE_KEY):
    print("Missing Supabase credentials in .env")
    exit(1)

sb = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

with open(ASINS_FILE, "r", encoding="utf-8") as f:
    items = json.load(f)

print(f"Upserting {len(items)} products into Supabase...")

for p in items:
    asin = p["asin"]
    slug = p.get("id", f"prod-{asin.lower()}")
    
    # Check if local asset exists
    asset_path = f"assets/img/{slug}-1.svg"
    images = [asset_path] if (ROOT / asset_path).exists() else ["assets/img/hero-dental.svg"]

    row = {
        "id": slug,
        "asin": asin,
        "name": p["name"],
        "marca": p.get("marca", "Dental"),
        "categoria_odontologica": p.get("categoria_odontologica", "cepillos_electricos"),
        "category": p.get("category", "Cepillos Eléctricos"),
        "tipo_producto": p.get("tipo_producto", p.get("categoria_odontologica")),
        "tecnologia": p.get("tecnologia", "rotatorio"),
        "affiliate_url": f"https://www.amazon.es/dp/{asin}?tag=odontoscore-21",
        "affiliate_tag": "odontoscore-21",
        "canonical_url": f"https://www.amazon.es/dp/{asin}",
        "retail_price": p.get("retailPrice", 99.99),
        "discounted_price": p.get("discountedPrice", p.get("retailPrice", 99.99)),
        "valoracion_media": p.get("valoracion_media", 4.5),
        "resenas_cantidad": p.get("resenas_cantidad", 1000),
        "modos_limpieza": p.get("modos_limpieza", 2),
        "presion_agua_psi": p.get("presion_agua_psi"),
        "pulsaciones_min": p.get("pulsaciones_min"),
        "capacidad_deposito_ml": p.get("capacidad_deposito_ml"),
        "autonomia_dias": p.get("autonomia_dias", 14),
        "nivel_ruido_db": p.get("nivel_ruido_db", 60),
        "app_conectada": p.get("app_conectada", False),
        "esterilizable_autoclave": p.get("esterilizable_autoclave", False),
        "indicado_para": p.get("indicado_para", ["limpieza_general"]),
        "score_eficacia": p.get("score_eficacia", 8.8),
        "score_comodidad_encias": p.get("score_comodidad_encias", 8.8),
        "score_durabilidad": p.get("score_durabilidad", 8.8),
        "score_facilidad_uso": p.get("score_facilidad_uso", 9.0),
        "score_silencio": p.get("score_silencio", 8.0),
        "score_tecnologia": p.get("score_tecnologia", 8.5),
        "score_calidad_precio": p.get("score_calidad_precio", 9.0),
        "is_featured": p.get("isFeatured", False),
        "local_assets": images,
        "description": f"Análisis clínico y especificaciones técnicas completas de {p['name']}.",
        "cuerpo_editorial": f"<p>El dispositivo <strong>{p['name']}</strong> ofrece una respuesta técnica excelente para la higiene bucal diaria con tecnología {p.get('tecnologia', 'avanzada')}.</p>",
        "pros": ["Eficacia clínica probada", "Excelente relación calidad-precio", "Ergonomía optimizada"],
        "contras": ["Consultar disponibilidad de recambios"],
        "ideal_para": "Pacientes que buscan máxima higiene interdental y protección gingival.",
        "destacado_editorial": "Recomendado por nuestro panel odontológico 2026.",
        "resumen_resenas": "Alta satisfacción entre usuarios por su durabilidad y facilidad de uso.",
        "geo_faq": [
            {"q": f"¿Para qué está indicado {p['name']}?", "a": f"Está especialmente diseñado para {', '.join(p.get('indicado_para', ['higiene bucal']))}."},
            {"q": "¿Tiene garantía oficial?", "a": "Sí, cuenta con garantía directa de fabricante y envío protegido por Amazon Prime."}
        ]
    }
    
    # Do not overwrite rich editorial on the 3 seed products
    if slug in ["oral-b-io-series-9", "waterpik-ultra-professional-wp-660eu", "philips-sonicare-9900-prestige"]:
        row.pop("cuerpo_editorial", None)
        row.pop("pros", None)
        row.pop("contras", None)
        row.pop("geo_faq", None)
        row.pop("local_assets", None)

    sb.table("products").upsert(row, on_conflict="asin").execute()
    print(f"[OK] Upserted {slug} ({asin})")

print("\nAll products populated into Supabase successfully!")
