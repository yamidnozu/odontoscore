with open('guias/ejemplos/Longitud-Trabajo-Endodoncia.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

import re
matches = re.findall(r'var\s+([a-zA-Z0-9_$]+)\s*=\s*["\'](data:image/[^"\']+)["\']', content)
print(f"Found {len(matches)} data image variables:")
for name, data in matches:
    print(f"- {name}: type {data[:30]}... length {len(data)}")
