#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
OdontoScore (odontoscore.com) — Supabase & Amazon PA-API 5.0 Synchronization
================================================================================
Sincroniza precios, stock, valoraciones y catálogos entre Amazon (PA-API 5.0 /
Rainforest API fallback) y Supabase (Fuente de Verdad).

Regenera automáticamente la caché local datos/productos.json y lib/db.js.

Uso:
    python tools/sync_supabase.py [--dry-run] [--force]
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# Carga de variables de entorno
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

ROOT = Path(__file__).resolve().parent.parent
DATOS_DIR = ROOT / "datos"
DATOS_FILE = DATOS_DIR / "productos.json"
ASINS_FILE = ROOT / "asins.json"
LIB_DB_FILE = ROOT / "lib" / "db.js"

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "").strip()
AMAZON_ACCESS_KEY = os.getenv("AMAZON_ACCESS_KEY", "").strip()
AMAZON_SECRET_KEY = os.getenv("AMAZON_SECRET_KEY", "").strip()
AMAZON_PARTNER_TAG = os.getenv("AMAZON_PARTNER_TAG", "odontoscore-21").strip()
AMAZON_HOST = os.getenv("AMAZON_HOST", "webservices.amazon.es").strip()
AMAZON_REGION = os.getenv("AMAZON_REGION", "eu-west-1").strip()
RAINFOREST_API_KEY = os.getenv("RAINFOREST_API_KEY", "").strip()

# Inicialización cliente Supabase si hay credenciales
supabase_client = None
if SUPABASE_URL and SUPABASE_SERVICE_KEY:
    try:
        from supabase import create_client, Client
        supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        print(f"[Supabase] Conectado exitosamente a {SUPABASE_URL}")
    except Exception as e:
        print(f"[Supabase WARN] No se pudo instanciar cliente oficial: {e}")


def get_asin_list():
    """Lee ASINs desde Supabase y asins.json haciendo merge."""
    asins_map = {}

    # 1. Leer de asins.json
    if ASINS_FILE.exists():
        try:
            with open(ASINS_FILE, "r", encoding="utf-8") as f:
                items = json.load(f)
                for item in items:
                    if isinstance(item, dict) and "asin" in item:
                        asins_map[item["asin"]] = item
                    elif isinstance(item, str):
                        asins_map[item] = {"asin": item}
        except Exception as e:
            print(f"[WARN] Error leyendo asins.json: {e}")

    # 2. Leer de Supabase
    if supabase_client:
        try:
            res = supabase_client.table("products").select("*").execute()
            for row in res.data:
                asin = row.get("asin")
                if asin:
                    if asin not in asins_map:
                        asins_map[asin] = row
                    else:
                        asins_map[asin].update(row)
        except Exception as e:
            print(f"[WARN] No se pudieron leer ASINs de Supabase: {e}")

    # 3. Fallback a datos/productos.json local
    if not asins_map and DATOS_FILE.exists():
        try:
            with open(DATOS_FILE, "r", encoding="utf-8") as f:
                prods = json.load(f)
                for p in prods:
                    if "asin" in p:
                        asins_map[p["asin"]] = p
        except Exception as e:
            print(f"[WARN] Error leyendo datos/productos.json: {e}")

    return list(asins_map.values())


def fetch_paapi(asin):
    """Consulta oficial a Amazon PA-API 5.0 usando paapi5-python-sdk."""
    if not (AMAZON_ACCESS_KEY and AMAZON_SECRET_KEY and AMAZON_PARTNER_TAG):
        return None

    try:
        from paapi5_python_sdk.api.default_api import DefaultApi
        from paapi5_python_sdk.models.get_items_request import GetItemsRequest
        from paapi5_python_sdk.models.get_items_resource import GetItemsResource
        from paapi5_python_sdk.models.partner_type import PartnerType
        from paapi5_python_sdk.rest import ApiException

        api = DefaultApi(
            access_key=AMAZON_ACCESS_KEY,
            secret_key=AMAZON_SECRET_KEY,
            host=AMAZON_HOST,
            region=AMAZON_REGION
        )

        resources = [
            GetItemsResource.ITEMINFO_TITLE,
            GetItemsResource.ITEMINFO_BYLINEINFO,
            GetItemsResource.ITEMINFO_FEATURES,
            GetItemsResource.IMAGES_PRIMARY_LARGE,
            GetItemsResource.OFFERS_LISTINGS_PRICE,
            GetItemsResource.OFFERS_LISTINGS_AVAILABILITY_MESSAGE,
            GetItemsResource.CUSTOMERREVIEWS_COUNT,
            GetItemsResource.CUSTOMERREVIEWS_STARRATING
        ]

        request = GetItemsRequest(
            partner_tag=AMAZON_PARTNER_TAG,
            partner_type=PartnerType.ASSOCIATES,
            marketplace="www.amazon.es",
            item_ids=[asin],
            resources=resources
        )

        response = api.get_items(request)
        if response.items_result and response.items_result.items:
            item = response.items_result.items[0]
            
            # Parsing precio
            price_val = None
            orig_price_val = None
            if item.offers and item.offers.listings:
                listing = item.offers.listings[0]
                if listing.price:
                    price_val = float(listing.price.amount)
                if listing.saving_basis:
                    orig_price_val = float(listing.saving_basis.amount)

            rating_val = None
            reviews_count = 0
            if item.customer_reviews:
                rating_val = float(item.customer_reviews.star_rating.value) if item.customer_reviews.star_rating else None
                reviews_count = int(item.customer_reviews.count) if item.customer_reviews.count else 0

            title_val = item.item_info.title.display_value if item.item_info and item.item_info.title else None
            brand_val = item.item_info.by_line_info.brand.display_value if item.item_info and item.item_info.by_line_info and item.item_info.by_line_info.brand else None

            return {
                "source": "PA-API 5.0",
                "asin": asin,
                "title": title_val,
                "brand": brand_val,
                "discounted_price": price_val,
                "retail_price": orig_price_val or price_val,
                "valoracion_media": rating_val,
                "resenas_cantidad": reviews_count,
                "disponibilidad": "InStock" if price_val else "OutOfStock",
                "currency": "EUR"
            }
    except Exception as e:
        print(f"  [PA-API Fallo para {asin}]: {e}")
        return None


def fetch_rainforest_fallback(asin):
    """Consulta de respaldo a Rainforest API cuando PA-API no está activa."""
    if not RAINFOREST_API_KEY:
        return None

    try:
        import requests
        params = {
            "api_key": RAINFOREST_API_KEY,
            "type": "product",
            "amazon_domain": "amazon.es",
            "asin": asin
        }
        res = requests.get("https://api.rainforestapi.com/request", params=params, timeout=15)
        if res.status_code == 200:
            data = res.json()
            product = data.get("product", {})
            
            price_info = product.get("buybox_winner", {}).get("price", {}) or product.get("price", {})
            price_val = price_info.get("value")
            orig_price_val = product.get("rrp", {}).get("value") or price_val

            return {
                "source": "Rainforest API (Fallback)",
                "asin": asin,
                "title": product.get("title"),
                "brand": product.get("brand"),
                "discounted_price": float(price_val) if price_val else None,
                "retail_price": float(orig_price_val) if orig_price_val else None,
                "valoracion_media": float(product.get("rating", 4.5)),
                "resenas_cantidad": int(product.get("ratings_total", 0)),
                "disponibilidad": "InStock" if product.get("buybox_winner", {}).get("is_in_stock", True) else "OutOfStock",
                "currency": "EUR"
            }
    except Exception as e:
        print(f"  [Rainforest Fallback Fallo para {asin}]: {e}")
        return None


def sync_product(asin_data, dry_run=False, force=False):
    """Obtiene datos frescos de Amazon y actualiza Supabase + Price History."""
    asin = asin_data["asin"]
    print(f"\n--- Procesando ASIN: {asin} ---")

    # 1. Obtener datos de Amazon
    fresh_data = fetch_paapi(asin)
    if not fresh_data:
        fresh_data = fetch_rainforest_fallback(asin)

    if not fresh_data:
        print(f"  [INFO] Sin respuesta de APIs externas para {asin}. Manteniendo datos existentes.")
        fresh_data = {
            "source": "Local Seed / DB Cache",
            "asin": asin,
            "discounted_price": asin_data.get("discountedPrice") or asin_data.get("discounted_price", 99.99),
            "retail_price": asin_data.get("retailPrice") or asin_data.get("retail_price", 99.99),
            "valoracion_media": asin_data.get("valoracion_media", 4.5),
            "resenas_cantidad": asin_data.get("resenas_cantidad", 1000),
            "disponibilidad": asin_data.get("disponibilidad", "InStock"),
            "currency": "EUR"
        }

    print(f"  [Fuente]: {fresh_data['source']}")
    print(f"  [Precio Actual]: {fresh_data['discounted_price']} EUR (PVP: {fresh_data['retail_price']} EUR)")
    print(f"  [Valoración]: {fresh_data['valoracion_media']}★ ({fresh_data['resenas_cantidad']} reviews)")

    if dry_run:
        print("  [DRY-RUN] Modificaciones no persistidas en base de datos.")
        return fresh_data

    # 2. Persistencia en Supabase
    if supabase_client:
        try:
            # Comprobar precio anterior para price_history
            prev_row = supabase_client.table("products").select("discounted_price, id").eq("asin", asin).execute()
            old_price = None
            if prev_row.data:
                old_price = prev_row.data[0].get("discounted_price")
                if old_price:
                    old_price = float(old_price)

            # Comprobar cambio > 5% para loggear en price_history
            new_price = fresh_data["discounted_price"]
            if old_price and new_price and old_price > 0:
                pct_change = abs((new_price - old_price) / old_price) * 100
                if pct_change >= 5.0:
                    print(f"  [PRICE ALERT] Cambio de precio de {old_price} a {new_price} ({pct_change:.1f}%)")
                    supabase_client.table("price_history").insert({
                        "asin": asin,
                        "old_price": old_price,
                        "new_price": new_price,
                        "percentage_change": round(pct_change, 2)
                    }).execute()

            # Upsert en Supabase
            update_payload = {
                "discounted_price": fresh_data["discounted_price"],
                "retail_price": fresh_data["retail_price"],
                "valoracion_media": fresh_data["valoracion_media"],
                "resenas_cantidad": fresh_data["resenas_cantidad"],
                "disponibilidad": fresh_data["disponibilidad"],
                "currency": fresh_data["currency"],
                "precio_fecha": datetime.now(timezone.utc).isoformat(),
                "last_amazon_sync": datetime.now(timezone.utc).isoformat(),
                "affiliate_tag": AMAZON_PARTNER_TAG,
                "affiliate_url": f"https://www.amazon.es/dp/{asin}?tag={AMAZON_PARTNER_TAG}"
            }

            if prev_row.data:
                supabase_client.table("products").update(update_payload).eq("asin", asin).execute()
                print("  [Supabase] Fila actualizada con éxito.")
            else:
                # Nuevo producto no categorizado previamente
                slug = asin_data.get("id") or f"prod-{asin.lower()}"
                new_row = {
                    "id": slug,
                    "asin": asin,
                    "name": fresh_data.get("title") or asin_data.get("name") or f"Producto Dental {asin}",
                    "marca": fresh_data.get("brand") or asin_data.get("marca") or "Dental",
                    "categoria_odontologica": asin_data.get("categoria_odontologica", "cepillos_electricos"),
                    "category": asin_data.get("category", "Cepillos Eléctricos"),
                    "needs_review": True,
                    **update_payload
                }
                supabase_client.table("products").insert(new_row).execute()
                print("  [Supabase] Nuevo producto insertado (needs_review=True).")

        except Exception as e:
            print(f"  [ERROR Supabase Upsert]: {e}")

    return fresh_data


def export_local_cache():
    """Genera datos/productos.json y lib/db.js desde Supabase (o valida local)."""
    products_list = []

    if supabase_client:
        try:
            res = supabase_client.table("products").select("*").execute()
            if res.data:
                for row in res.data:
                    # Mapeo a formato exacto que espera build_site.py
                    p_id = row.get("id")
                    asin = row.get("asin")
                    p = {
                        "id": p_id,
                        "asin": asin,
                        "name": row.get("name"),
                        "marca": row.get("marca"),
                        "categoria_odontologica": row.get("categoria_odontologica"),
                        "category": row.get("category") or "Odontología",
                        "affiliate_url": row.get("affiliate_url") or f"https://www.amazon.es/dp/{asin}?tag={AMAZON_PARTNER_TAG}",
                        "affiliate_tag": AMAZON_PARTNER_TAG,
                        "canonical_url": row.get("canonical_url") or f"https://www.amazon.es/dp/{asin}",
                        "images": row.get("local_assets") or row.get("image_urls") or [f"assets/img/prod-{asin.lower()}-1.svg"],
                        "isFeatured": bool(row.get("is_featured")),
                        "showInTopMenu": bool(row.get("show_in_top_menu")),
                        "retailPrice": float(row.get("retail_price") or 99.99),
                        "discountedPrice": float(row.get("discounted_price") or row.get("retail_price") or 99.99),
                        "rango_precio": row.get("rango_precio") or "medio",
                        "valoracion_media": float(row.get("valoracion_media") or 4.5),
                        "resenas_cantidad": int(row.get("resenas_cantidad") or 0),
                        "precio_fecha": str(row.get("precio_fecha") or datetime.now().strftime("%Y-%m-%d"))[:10],
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
                        "material": row.get("material") or "Material médico",
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
                        "pros": row.get("pros") or [],
                        "contras": row.get("contras") or [],
                        "ideal_para": row.get("ideal_para") or "",
                        "destacado_editorial": row.get("destacado_editorial") or "",
                        "resenas_resumen": row.get("resenas_resumen") or "",
                        "geo_faq": row.get("geo_faq") or []
                    }
                    products_list.append(p)
                print(f"[Export] {len(products_list)} productos leídos de Supabase.")
        except Exception as e:
            print(f"[WARN] Error exportando de Supabase: {e}")

    # Si no hubo conexión a Supabase, usar y normalizar datos/productos.json local
    if not products_list and DATOS_FILE.exists():
        with open(DATOS_FILE, "r", encoding="utf-8") as f:
            products_list = json.load(f)
            # Asegurar tag odontoscore-21 en local
            for p in products_list:
                p["affiliate_tag"] = AMAZON_PARTNER_TAG
                if "voltbike-21" in p.get("affiliate_url", ""):
                    p["affiliate_url"] = f"https://www.amazon.es/dp/{p['asin']}?tag={AMAZON_PARTNER_TAG}"

    # Guardar datos/productos.json
    DATOS_DIR.mkdir(exist_ok=True)
    with open(DATOS_FILE, "w", encoding="utf-8") as f:
        json.dump(products_list, f, indent=2, ensure_ascii=False)
    print(f"[OK] Actualizado caché local: {DATOS_FILE}")

    # Guardar lib/db.js
    db_obj = {
        "productos": products_list,
        "nichos": ["productos-odontologia"],
        "scoreAxes": ["eficacia", "comodidad_encias", "durabilidad", "facilidad_uso", "silencio", "tecnologia", "calidad_precio"],
        "updated": datetime.now().strftime("%Y-%m-%d")
    }
    js_content = f"""(function () {{
  "use strict";
  window.__DB__ = {json.dumps(db_obj, indent=2, ensure_ascii=False)};
}})();
"""
    LIB_DB_FILE.parent.mkdir(exist_ok=True)
    with open(LIB_DB_FILE, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"[OK] Actualizado window.__DB__ en {LIB_DB_FILE}")


def main():
    parser = argparse.ArgumentParser(description="OdontoScore Sync Supabase & PA-API 5.0")
    parser.add_argument("--dry-run", action="store_true", help="Ejecuta comprobaciones sin guardar en Supabase ni escribir archivos")
    parser.add_argument("--force", action="store_true", help="Fuerza actualización aunque los datos sean recientes")
    args = parser.parse_args()

    print("================================================================")
    print("   OdontoScore · Supabase & Amazon PA-API 5.0 Synchronization")
    print(f"   Timestamp: {datetime.now().isoformat()} | Tag: {AMAZON_PARTNER_TAG}")
    print("================================================================")

    asins = get_asin_list()
    print(f"Total ASINs a procesar: {len(asins)}")

    for item in asins:
        sync_product(item, dry_run=args.dry_run, force=args.force)
        time.sleep(1) # Pausa cortés entre llamadas

    if not args.dry_run:
        export_local_cache()

    print("\n✅ Proceso de sincronización finalizado con éxito.")

if __name__ == "__main__":
    main()
