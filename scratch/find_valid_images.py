import requests
import json

ROOT = "c:/Proyectos/bussiness/store-odontologia"
with open(f"{ROOT}/datos/productos.json", "r", encoding="utf-8") as f:
    products = json.load(f)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

print("Inspecting all image URLs across all products...")
good_products = []
bad_products = []

for p in products:
    pid = p.get("id")
    asin = p.get("asin")
    imgs = (p.get("specs_extra") and p.get("specs_extra", {}).get("images")) or p.get("images") or []
    
    good_imgs = []
    for img in imgs:
        try:
            r = requests.head(img, headers=headers, timeout=5)
            if r.status_code == 200:
                good_imgs.append(img)
        except Exception:
            pass
            
    if good_imgs:
        good_products.append((pid, asin, good_imgs))
        print(f"[VALID] {pid} ({asin}) -> {len(good_imgs)} working photos (e.g. {good_imgs[0][:60]}...)")
    else:
        bad_products.append((pid, asin))
        print(f"[BROKEN] {pid} ({asin}) -> 0 working photos!")

print(f"\nSummary: {len(good_products)} VALID, {len(bad_products)} BROKEN.")
