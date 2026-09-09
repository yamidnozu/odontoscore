with open('guias/ejemplos/Longitud-Trabajo-Endodoncia.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

import re
m = re.findall(r'src:\s*([a-zA-Z0-9_$]+)', content)
print("All src bindings:", set(m))
