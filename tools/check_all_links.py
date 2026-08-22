import urllib.request
import re

base = "https://odontoscore.com/"
req = urllib.request.Request(base, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req).read().decode("utf-8")

hrefs = re.findall(r'href=["\']([^"\'#]+)["\']', html)
print(f"Total hrefs encontradas en Home: {len(set(hrefs))}")

broken = []
for h in set(hrefs):
    if h.startswith("http") and "odontoscore.com" not in h:
        # Check external amazon links
        continue
    if h.startswith("mailto:") or h.startswith("tel:"):
        continue
    test_url = h if h.startswith("http") else (base + h.lstrip("/"))
    try:
        r = urllib.request.urlopen(urllib.request.Request(test_url, headers={"User-Agent": "Mozilla/5.0"}), timeout=8)
        if r.getcode() != 200:
            broken.append((h, r.getcode()))
    except Exception as e:
        broken.append((h, str(e)))

print(f"\nEnlaces rotos encontrados: {len(broken)}")
for b in broken:
    print(f"  [BROKEN] {b[0]} -> {b[1]}")
