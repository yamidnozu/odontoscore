with open('guias/ejemplos/Longitud-Trabajo-Endodoncia.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

import re
# Find objects with title:, img:, etc.
pattern = r'\{[^{}]*title:[^{}]*\}'
matches = re.findall(pattern, content)
print(f"Found {len(matches)} item objects:")
for idx, m in enumerate(matches):
    print(f"--- Item {idx} ---")
    print(m)
