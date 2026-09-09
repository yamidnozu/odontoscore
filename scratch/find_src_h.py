with open('guias/ejemplos/Longitud-Trabajo-Endodoncia.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

import re
occurrences = [m.start() for m in re.finditer(r'src:\s*h\b', content)]
for idx in occurrences:
    print("Snippet for src:h:", content[idx-100:idx+150])
