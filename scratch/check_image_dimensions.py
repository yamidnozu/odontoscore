import requests
import json
from PIL import Image
import io

ROOT = "c:/Proyectos/bussiness/store-odontologia"
with open(f"{ROOT}/datos/productos.json", "r", encoding="utf-8") as f:
    products = json.load(f)

print(f"Testing {len(products)} products for valid image size > 50x50...")
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

invalid_products = []
for p in products:
    pid = p.get("id")
    asin = p.get("asin")
    imgs = (p.get("specs_extra") and p.get("specs_extra", {}).get("images")) or p.get("images") or []
    
    valid_imgs = []
    for img in imgs:
        try:
            r = requests.get(img, headers=headers, timeout=5)
            if r.status_code == 200:
                im = Image.open(io.BytesIO(r.content))
                w, h = im.size
                if w > 50 and h > 50:
                    valid_imgs.append((img, w, h))
                else:
                    print(f"  [1x1 BLANK IMAGE DETECTED] {pid} ({asin}) -> {w}x{h} on {img}")
        except Exception as e:
            print(f"  [ERROR] {pid} -> {e}")
            
    if not valid_imgs:
        invalid_products.append((pid, asin, p.get("name")))
        print(f"[NO VALID IMAGES] {pid} | ASIN: {asin} | Name: {p.get('name')}")
    else:
        print(f"[OK] {pid} -> {len(valid_imgs)} valid photos (first: {valid_imgs[0][1]}x{valid_imgs[0][2]})")

print(f"\nSummary: {len(invalid_products)} products have NO valid image.")
with open(f"{ROOT}/scratch/invalid_image_products.json", "w", encoding="utf-8") as f:
    json.dump(invalid_products, f, indent=2)
