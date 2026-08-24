import requests
import json
import concurrent.futures

ROOT = "c:/Proyectos/bussiness/store-odontologia"
with open(f"{ROOT}/datos/productos.json", "r", encoding="utf-8") as f:
    products = json.load(f)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def check_product(p):
    pid = p.get("id")
    asin = p.get("asin")
    imgs = (p.get("specs_extra") and p.get("specs_extra", {}).get("images")) or p.get("images") or []
    
    valid_imgs = []
    for img in imgs:
        try:
            r = requests.head(img, headers=headers, timeout=4)
            if r.status_code == 200:
                valid_imgs.append(img)
        except Exception:
            pass
    return pid, asin, len(valid_imgs), valid_imgs

print(f"Checking {len(products)} products with 10 threads...", flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(check_product, p) for p in products]
    
    valid_count = 0
    broken_count = 0
    broken_list = []
    
    for f in concurrent.futures.as_completed(futures):
        pid, asin, count, vimgs = f.result()
        if count > 0:
            valid_count += 1
            print(f"[OK] {pid} ({asin}) -> {count} valid images", flush=True)
        else:
            broken_count += 1
            broken_list.append((pid, asin))
            print(f"[BROKEN] {pid} ({asin}) -> 0 valid images!", flush=True)

print(f"\nRESULTS: {valid_count} VALID, {broken_count} BROKEN", flush=True)
with open(f"{ROOT}/scratch/broken_list.json", "w", encoding="utf-8") as f:
    json.dump(broken_list, f, indent=2)
