import re
from pathlib import Path

root = Path('.')

# 1. Update sitemap.xml
sitemap_path = root / 'sitemap.xml'
if sitemap_path.exists():
    text = sitemap_path.read_text(encoding='utf-8')
    biofilm_entry = '  <url><loc>https://odontoscore.com/guias/biofilm-microbiologia-endodoncia-3d.html</loc><lastmod>2026-09-04</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>\n'
    if 'biofilm-microbiologia-endodoncia-3d.html' not in text:
        text = text.replace(
            '<url><loc>https://odontoscore.com/guias/anatomia-dental-3d-por-capas.html</loc><lastmod>2026-09-03</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>',
            '<url><loc>https://odontoscore.com/guias/anatomia-dental-3d-por-capas.html</loc><lastmod>2026-09-04</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>\n' + biofilm_entry.strip()
        )
        sitemap_path.write_text(text, encoding='utf-8')
        print("Updated sitemap.xml")

# 2. Update tools/generate_sitemap.py
gen_sitemap = root / 'tools' / 'generate_sitemap.py'
if gen_sitemap.exists():
    txt = gen_sitemap.read_text(encoding='utf-8')
    if 'biofilm-microbiologia-endodoncia-3d.html' not in txt:
        old_str = '    ("https://odontoscore.com/guias/mejor-cepillo-electrico-encias-sensibles-2026.html", "0.9", "weekly"),'
        new_str = old_str + '\n    ("https://odontoscore.com/guias/anatomia-dental-3d-por-capas.html", "0.9", "weekly"),\n    ("https://odontoscore.com/guias/biofilm-microbiologia-endodoncia-3d.html", "0.9", "weekly"),\n    ("https://odontoscore.com/guias/semiologia-pares-craneales-odontologia.html", "0.9", "weekly"),'
        txt = txt.replace(old_str, new_str)
        gen_sitemap.write_text(txt, encoding='utf-8')
        print("Updated tools/generate_sitemap.py")

# 3. Update index.html
index_path = root / 'index.html'
if index_path.exists():
    t = index_path.read_text(encoding='utf-8')
    # Update dropdown
    old_dd = '<a href="guias/anatomia-dental-3d-por-capas.html" class="dropdown-link">Atlas Anatómico Dental</a>'
    new_dd = '<a href="guias/anatomia-dental-3d-por-capas.html" class="dropdown-link">Atlas Anatómico Dental 360°</a>\n            <a href="guias/biofilm-microbiologia-endodoncia-3d.html" class="dropdown-link">Biofilm y Endodoncia 3D</a>'
    if old_dd in t:
        t = t.replace(old_dd, new_dd)
    
    # Update footer
    old_ft = '<li><a href="guias/semiologia-pares-craneales-odontologia.html" style="font-weight:700;color:var(--color-primary);">Semiología Pares Craneales</a></li>'
    new_ft = '<li><a href="guias/anatomia-dental-3d-por-capas.html">Atlas Anatómico Dental 360°</a></li>\n          <li><a href="guias/biofilm-microbiologia-endodoncia-3d.html">Biofilm y Endodoncia 3D</a></li>\n          ' + old_ft
    if old_ft in t and 'biofilm-microbiologia-endodoncia-3d.html' not in t[t.find('Herramientas & Academia'):t.find('Herramientas & Academia')+500]:
        t = t.replace(old_ft, new_ft)
    
    index_path.write_text(t, encoding='utf-8')
    print("Updated index.html")

# 4. Update sobre-nosotros.html
sobre_path = root / 'sobre-nosotros.html'
if sobre_path.exists():
    st = sobre_path.read_text(encoding='utf-8')
    old_s_dd = '<a href="guias/anatomia-dental-3d-por-capas.html" class="dropdown-link">Atlas Anatómico Dental 360°</a>'
    new_s_dd = old_s_dd + '\n            <a href="guias/biofilm-microbiologia-endodoncia-3d.html" class="dropdown-link">Biofilm y Endodoncia 3D</a>'
    if old_s_dd in st and 'biofilm-microbiologia-endodoncia-3d.html' not in st:
        st = st.replace(old_s_dd, new_s_dd)
        # Update footer
        st = st.replace(
            '<li><a href="guias/mejor-irrigador-dental-brackets-2026.html">Guía Irrigadores Brackets</a></li>',
            '<li><a href="guias/anatomia-dental-3d-por-capas.html">Atlas Anatómico Dental 360°</a></li>\n          <li><a href="guias/biofilm-microbiologia-endodoncia-3d.html">Biofilm y Endodoncia 3D</a></li>\n          <li><a href="guias/semiologia-pares-craneales-odontologia.html">Semiología y Pares Craneales</a></li>\n          <li><a href="guias/mejor-irrigador-dental-brackets-2026.html">Guía Irrigadores Brackets</a></li>'
        )
        sobre_path.write_text(st, encoding='utf-8')
        print("Updated sobre-nosotros.html")

# 5. Update guias/*.html dropdowns
for gpath in root.glob('guias/*.html'):
    if gpath.name == 'biofilm-microbiologia-endodoncia-3d.html':
        continue
    gtxt = gpath.read_text(encoding='utf-8')
    old_g_dd = '<a href="../guias/anatomia-dental-3d-por-capas.html" class="dropdown-link">Atlas Anatómico Dental 360°</a>'
    new_g_dd = old_g_dd + '\n            <a href="../guias/biofilm-microbiologia-endodoncia-3d.html" class="dropdown-link">Biofilm y Endodoncia 3D</a>'
    if old_g_dd in gtxt and 'biofilm-microbiologia-endodoncia-3d.html' not in gtxt:
        gtxt = gtxt.replace(old_g_dd, new_g_dd)
        gpath.write_text(gtxt, encoding='utf-8')
        print(f"Updated {gpath.name}")

print("All navigation synchronization finished successfully.")
