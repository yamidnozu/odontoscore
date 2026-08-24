import json

ROOT = "c:/Proyectos/bussiness/store-odontologia"
with open(f"{ROOT}/datos/productos.json", "r", encoding="utf-8") as f:
    products = json.load(f)

# Find verified photos per category
working_photos = {}
for p in products:
    pid = p.get("id")
    imgs = (p.get("specs_extra") and p.get("specs_extra", {}).get("images")) or p.get("images") or []
    # Filter only working Amazon CDN images (not ws-eu and not 404 ones)
    valid = [img for img in imgs if "m.media-amazon.com" in img and len(img) > 30 and not any(bad in img for bad in ["71e0tJb9w4L", "71hM0N4rZAL", "71wM+yE2tPL", "71P7u1Fm78L", "81kQ9C4wRSL", "61k8yZ4z-QL", "51j1-Q3z1wL", "61f2F-yF7YL"])]
    if valid:
        working_photos[pid] = valid

print(f"Products with verified working photos: {len(working_photos)}")
for k, v in list(working_photos.items())[:10]:
    print(f"  {k}: {len(v)} photos -> {v[0]}")

with open(f"{ROOT}/scratch/working_photos_map.json", "w", encoding="utf-8") as f:
    json.dump(working_photos, f, indent=2)
