import base64
import os
import re

os.makedirs('public/images/guias/longitud-trabajo', exist_ok=True)

with open('guias/ejemplos/Longitud-Trabajo-Endodoncia.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

var_to_file = {
    'jl': 'lima-k10-sondeo.webp',
    'to': 'regla-milimetrada-endodoncia.webp',
    'or': 'acceso-boca-referencia-incisal.webp',
    'Bl': 'localizador-apical-pantalla.webp',
    'Fl': 'radiografia-conductometria-vertice.webp'
}

for var, filename in var_to_file.items():
    m = re.search(r'var\s+' + var + r'\s*=\s*["\']data:image/webp;base64,([^"\']+)["\']', content)
    if m:
        b64data = m.group(1)
        img_bytes = base64.b64decode(b64data)
        filepath = os.path.join('public/images/guias/longitud-trabajo', filename)
        with open(filepath, 'wb') as img_out:
            img_out.write(img_bytes)
        print(f"Exported {filename}: {len(img_bytes)} bytes")
    else:
        print(f"Failed to find {var}")

print("Image export finished!")
