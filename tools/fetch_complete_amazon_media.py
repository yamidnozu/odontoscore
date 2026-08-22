#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetch complete Amazon image galleries, high-res photos, and real videos for each product
using Rainforest API type=product, and update Supabase.
"""

import json
import os
import time
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

import requests
from supabase import create_client

ROOT = Path(__file__).resolve().parent.parent
ASINS_FILE = ROOT / "asins.json"
API_KEY = os.getenv("RAINFOREST_API_KEY", "95BD9468E3AD4623B3ABCEBA747D32A2").strip()

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "").strip()

if not (SUPABASE_URL and SUPABASE_SERVICE_KEY):
    print("Faltan credenciales de Supabase")
    exit(1)

sb = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

with open(ASINS_FILE, "r", encoding="utf-8") as f:
    products = json.load(f)

print(f"=== Obteniendo Galerías Completas de Amazon para {len(products)} Productos ===")

updated_products = []

for idx, p in enumerate(products):
    asin = p["asin"]
    slug = p["id"]
    print(f"\n[{idx+1}/{len(products)}] Consultando Amazon.es para ASIN {asin}...")

    params = {
        "api_key": API_KEY,
        "type": "product",
        "amazon_domain": "amazon.es",
        "asin": asin
    }

    try:
        res = requests.get("https://api.rainforestapi.com/request", params=params, timeout=25)
        if res.status_code == 200:
            data = res.json()
            prod = data.get("product", {})
            
            # 1. Full Gallery of Images
            raw_images = prod.get("images", [])
            image_links = [img.get("link") for img in raw_images if img.get("link")]
            
            # If empty, fallback to main_image
            if not image_links and prod.get("main_image", {}).get("link"):
                image_links = [prod["main_image"]["link"]]
            elif not image_links:
                image_links = [f"https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN={asin}&Format=_SL1500_&ID=AsinImage&MarketPlace=ES&ServiceVersion=20070822&WS=1&tag=odontoscore-21"]

            # 2. Real Amazon Videos
            raw_videos = prod.get("videos", [])
            videos_list = []
            for v in raw_videos:
                if v.get("url") or v.get("link"):
                    videos_list.append({
                        "title": v.get("title") or f"Demostración de {p['name'][:30]}",
                        "url": v.get("url") or v.get("link"),
                        "thumbnail": v.get("preview_image") or image_links[0]
                    })

            # 3. Bullets / Features
            bullets = prod.get("feature_bullets", [])
            
            # 4. Prices
            price_val = prod.get("price", {}).get("value")
            retail_val = prod.get("buybox_winner", {}).get("rrp", {}).get("value") or (round(price_val * 1.25, 2) if price_val else p.get("retailPrice", 49.99))
            discounted_val = float(price_val) if price_val else float(p.get("discountedPrice", 39.99))

            p["name"] = prod.get("title") or p["name"]
            p["images"] = image_links
            p["local_assets"] = image_links
            p["videos"] = videos_list
            p["feature_bullets"] = bullets
            p["retailPrice"] = retail_val
            p["discountedPrice"] = discounted_val
            p["valoracion_media"] = float(prod.get("rating", p.get("valoracion_media", 4.5)))
            p["resenas_cantidad"] = int(prod.get("ratings_total", p.get("resenas_cantidad", 500)))

            print(f"  -> Título: {p['name'][:40]}...")
            print(f"  -> {len(image_links)} fotos de Amazon encontradas.")
            print(f"  -> {len(videos_list)} vídeos oficiales de Amazon.")

            # Update Supabase row
            update_data = {
                "name": p["name"],
                "local_assets": image_links,
                "retail_price": retail_val,
                "discounted_price": discounted_val,
                "valoracion_media": p["valoracion_media"],
                "resenas_cantidad": p["resenas_cantidad"],
                "specs_extra": {
                    "images": image_links,
                    "videos": videos_list,
                    "bullets": bullets
                }
            }
            sb.table("products").update(update_data).eq("asin", asin).execute()
            print(f"  -> Supabase actualizado para {asin}")

        else:
            print(f"  [!] Falló petición ({res.status_code}), manteniendo enlaces directos de Amazon.")
            img_cdn = f"https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN={asin}&Format=_SL1500_&ID=AsinImage&MarketPlace=ES&ServiceVersion=20070822&WS=1&tag=odontoscore-21"
            p["images"] = [img_cdn]
            p["local_assets"] = [img_cdn]

    except Exception as e:
        print(f"  [!] Error para ASIN {asin}: {e}")
        img_cdn = f"https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN={asin}&Format=_SL1500_&ID=AsinImage&MarketPlace=ES&ServiceVersion=20070822&WS=1&tag=odontoscore-21"
        p["images"] = [img_cdn]
        p["local_assets"] = [img_cdn]

    updated_products.append(p)
    time.sleep(0.3)

# Save to asins.json and datos/productos.json
with open(ASINS_FILE, "w", encoding="utf-8") as f:
    json.dump(updated_products, f, indent=2, ensure_ascii=False)

with open(ROOT / "datos" / "productos.json", "w", encoding="utf-8") as f:
    json.dump(updated_products, f, indent=2, ensure_ascii=False)

print("\n=== Todas las galerías y vídeos de Amazon sincronizados en Supabase ===")
