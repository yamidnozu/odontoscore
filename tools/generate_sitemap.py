import json
import datetime
from pathlib import Path

ROOT = Path("c:/Proyectos/bussiness/store-odontologia")
with open(ROOT / "datos" / "productos.json", "r", encoding="utf-8") as f:
    products = json.load(f)

today = datetime.datetime.now().strftime("%Y-%m-%d")

urls = [
    ("https://odontoscore.com/", "1.0", "daily"),
    ("https://odontoscore.com/comparador.html", "0.9", "weekly"),
    ("https://odontoscore.com/ofertas.html", "0.9", "daily"),
    ("https://odontoscore.com/guias/mejor-irrigador-dental-brackets-2026.html", "0.9", "weekly"),
    ("https://odontoscore.com/guias/mejor-cepillo-electrico-encias-sensibles-2026.html", "0.9", "weekly"),
    ("https://odontoscore.com/guias/anatomia-dental-3d-por-capas.html", "0.9", "weekly"),
    ("https://odontoscore.com/guias/biofilm-microbiologia-endodoncia-3d.html", "0.9", "weekly"),
    ("https://odontoscore.com/guias/semiologia-pares-craneales-odontologia.html", "0.9", "weekly"),
    ("https://odontoscore.com/sobre-nosotros.html", "0.7", "monthly"),
    ("https://odontoscore.com/privacidad.html", "0.5", "monthly"),
    ("https://odontoscore.com/aviso-afiliados.html", "0.5", "monthly")
]

for p in products:
    urls.append((f"https://odontoscore.com/producto/{p.get('id')}.html", "0.8", "weekly"))

sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u, priority, changefreq in urls:
    sitemap_xml.append(f'  <url><loc>{u}</loc><lastmod>{today}</lastmod><changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>')
sitemap_xml.append('</urlset>')

content = "\n".join(sitemap_xml)
with open(ROOT / "sitemap.xml", "w", encoding="utf-8") as f:
    f.write(content)

print(f"[OK] sitemap.xml updated with {len(urls)} URLs on date {today}.")
