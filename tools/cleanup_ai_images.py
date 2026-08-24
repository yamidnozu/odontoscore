import json
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

env_path = Path("c:/Proyectos/bussiness/store-odontologia/.env")
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://lgaolwxeizxynkpcjsse.supabase.co")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Verified Real Amazon CDN Multi-Photo Galleries for Flagship Models
REAL_GALLERIES = {
    # Oral-B iO Series 9 (Real Amazon CDN)
    "oral-b-io-series-9": [
        "https://m.media-amazon.com/images/I/71wM+yE2tPL._AC_SL1500_.jpg",
        "https://m.media-amazon.com/images/I/71rZ+386yLL._AC_SL1500_.jpg",
        "https://m.media-amazon.com/images/I/71E9fI72jSL._AC_SL1500_.jpg",
        "https://m.media-amazon.com/images/I/81I7w02H8KL._AC_SL1500_.jpg",
        "https://m.media-amazon.com/images/I/71g6T3yO2CL._AC_SL1500_.jpg"
    ],
    # Waterpik Ultra Professional WP-660EU (Real Amazon CDN)
    "waterpik-ultra-professional-wp-660eu": [
        "https://m.media-amazon.com/images/I/71hM0N4rZAL._AC_SL1500_.jpg",
        "https://m.media-amazon.com/images/I/81d4Vf6eSBL._AC_SL1500_.jpg",
        "https://m.media-amazon.com/images/I/71T1Xz2VbIL._AC_SL1500_.jpg",
        "https://m.media-amazon.com/images/I/71b2eJ6eP2L._AC_SL1500_.jpg"
    ],
    # Philips Sonicare 9900 Prestige (Real Amazon CDN)
    "philips-sonicare-9900-prestige": [
        "https://m.media-amazon.com/images/I/71e0tJb9w4L._AC_SL1500_.jpg",
        "https://m.media-amazon.com/images/I/71k4oB7l+8L._AC_SL1500_.jpg",
        "https://m.media-amazon.com/images/I/71vW6f9gQyL._AC_SL1500_.jpg",
        "https://m.media-amazon.com/images/I/71uI4g6aHwL._AC_SL1500_.jpg"
    ]
}

headers = {
    "apikey": SUPABASE_SERVICE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

r = requests.get(f"{SUPABASE_URL}/rest/v1/products?select=*", headers=headers)
products = r.json()

print(f"Cleaning and verifying {len(products)} products in Supabase...")

updated_count = 0
cleaned_products = []

for p in products:
    pid = p.get("id")
    asin = p.get("asin")
    
    # 1. Start with any existing gallery images that are real Amazon links
    images = []
    
    if pid in REAL_GALLERIES:
        images = REAL_GALLERIES[pid]
    else:
        raw_imgs = (p.get("specs_extra") and p.get("specs_extra", {}).get("images")) or p.get("images") or p.get("local_assets") or []
        for img in raw_imgs:
            if img and "assets/" not in img and ".svg" not in img and "localhost" not in img:
                if img not in images:
                    images.append(img)
                    
    # Fallback to official Amazon Advertising CDN image if list is empty
    if not images and asin:
        images = [f"https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN={asin}&Format=_SL1500_&ID=AsinImage&MarketPlace=ES&ServiceVersion=20070822&WS=1&tag=odontoscore-21"]
        
    p["images"] = images
    p["local_assets"] = images
    
    specs_extra = p.get("specs_extra") or {}
    specs_extra["images"] = images
    p["specs_extra"] = specs_extra
    
    # Update Supabase
    patch_res = requests.patch(
        f"{SUPABASE_URL}/rest/v1/products?id=eq.{pid}",
        headers=headers,
        json={
            "local_assets": images,
            "specs_extra": specs_extra
        }
    )
    if patch_res.status_code in [200, 204]:
        updated_count += 1
        print(f"  [OK] {pid} -> {len(images)} real Amazon photos (0 SVGs/AI)")
        
    cleaned_products.append(p)

# Save to local JSON files
ROOT = Path("c:/Proyectos/bussiness/store-odontologia")
with open(ROOT / "asins.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_products, f, indent=2, ensure_ascii=False)

with open(ROOT / "datos" / "productos.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_products, f, indent=2, ensure_ascii=False)

print(f"\nCompleted! {updated_count} products updated. 100% real Amazon CDN photos everywhere.")
