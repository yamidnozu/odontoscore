with open('guias/ejemplos/Longitud-Trabajo-Endodoncia.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

import re
matches = re.findall(r'img:\s*([a-zA-Z0-9_$]+)', content)
print("img: bindings found:", matches)
