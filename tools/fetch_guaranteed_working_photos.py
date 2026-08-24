import requests
import json
import re
import os
from PIL import Image
import io
from bs4 import BeautifulSoup
from dotenv import load_dotenv

ROOT = "c:/Proyectos/bussiness/store-odontologia"
load_dotenv(f"{ROOT}/.env")
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://lgaolwxeizxynkpcjsse.supabase.co")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

with open(f"{ROOT}/datos/productos.json", "r", encoding="utf-8") as f:
    products = json.load(f)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"
}

def verify_image(url):
    try:
        r = requests.get(url, headers=headers, timeout=4)
        if r.status_code == 200 and len(r.content) > 5000:
            im = Image.open(io.BytesIO(r.content))
            if im.size[0] > 100 and im.size[1] > 100:
                return True
    except Exception:
        pass
    return False

def get_real_amazon_images(asin, query_name):
    found_urls = []
    
    # 1. Try direct Amazon.es product page
    try:
        url = f"https://www.amazon.es/dp/{asin}"
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            # Extract hiRes images from data-a-dynamic-image or ImageBlockBTF
            matches = re.findall(r'https://m\.media-amazon\.com/images/I/[a-zA-Z0-9%_\+\-]+\.jpg', r.text)
            for m in matches:
                # Filter out thumbnails or tiny icons
                if "._" in m:
                    base = m.split("._")[0] + ".jpg"
                else:
                    base = m
                if base not in found_urls and verify_image(base):
                    found_urls.append(base)
                if len(found_urls) >= 4:
                    break
    except Exception as e:
        print(f"  Amazon page fetch error for {asin}: {e}", flush=True)

    # 2. If not found or < 2 images, search Amazon search results
    if len(found_urls) < 2:
        try:
            s_url = f"https://www.amazon.es/s?k={requests.utils.quote(query_name)}"
            r = requests.get(s_url, headers=headers, timeout=5)
            if r.status_code == 200:
                matches = re.findall(r'https://m\.media-amazon\.com/images/I/[a-zA-Z0-9%_\+\-]+\.jpg', r.text)
                for m in matches:
                    if "._" in m:
                        base = m.split("._")[0] + ".jpg"
                    else:
                        base = m
                    if base not in found_urls and verify_image(base):
                        found_urls.append(base)
                    if len(found_urls) >= 4:
                        break
        except Exception as e:
            print(f"  Amazon search fetch error for {query_name}: {e}", flush=True)

    return found_urls

print(f"Enriching {len(products)} products with 100% verified Amazon images...", flush=True)
updated_products = []

for i, p in enumerate(products):
    pid = p.get("id")
    asin = p.get("asin")
    pname = p.get("name")
    
    # Check currently existing images
    curr_imgs = (p.get("specs_extra") and p.get("specs_extra", {}).get("images")) or p.get("images") or []
    valid_curr = [img for img in curr_imgs if "ws-eu" not in img and verify_image(img)]
    
    if len(valid_curr) >= 2:
        print(f"[{i+1}/{len(products)}] [ALREADY OK] {pid} -> {len(valid_curr)} verified photos", flush=True)
        final_imgs = valid_curr
    else:
        print(f"[{i+1}/{len(products)}] [FETCHING] {pid} ({asin}) - {pname[:40]}...", flush=True)
        fetched = get_real_amazon_images(asin, f"{p.get('marca', '')} {pname}")
        if fetched:
            final_imgs = fetched
            print(f"  -> Found {len(fetched)} working photos!", flush=True)
        else:
            final_imgs = valid_curr
            print(f"  -> WARNING: No new photos found, kept {len(valid_curr)}", flush=True)
            
    p["images"] = final_imgs
    p["local_assets"] = final_imgs
    specs_extra = p.get("specs_extra") or {}
    specs_extra["images"] = final_imgs
    p["specs_extra"] = specs_extra
    
    # Update Supabase
    try:
        supabase_headers = {
            "apikey": SUPABASE_SERVICE_KEY,
            "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        requests.patch(
            f"{SUPABASE_URL}/rest/v1/products?id=eq.{pid}",
            headers=supabase_headers,
            json={"local_assets": final_imgs, "specs_extra": specs_extra},
            timeout=5
        )
    except Exception as e:
        print(f"  Supabase update error: {e}", flush=True)
        
    updated_products.append(p)

with open(f"{ROOT}/datos/productos.json", "w", encoding="utf-8") as f:
    json.dump(updated_products, f, indent=2, ensure_ascii=False)

with open(f"{ROOT}/asins.json", "w", encoding="utf-8") as f:
    json.dump(updated_products, f, indent=2, ensure_ascii=False)

print("\n[COMPLETE] All products processed and synchronized!", flush=True)
