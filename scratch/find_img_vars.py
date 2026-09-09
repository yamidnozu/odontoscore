with open('guias/ejemplos/Longitud-Trabajo-Endodoncia.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

import re
for var in ['or', 'jl', 'Bl']:
    m = re.search(r'var\s+' + var + r'\s*=\s*["\']([^"\']+)["\']', content)
    if m:
        val = m.group(1)
        print(f"Var {var}: length {len(val)}, starts with: {val[:60]}")
    else:
        # maybe let var = or const var =
        m2 = re.search(r'(?:let|const|var)\s+' + var + r'\s*=\s*["\']([^"\']+)["\']', content)
        if m2:
            val = m2.group(1)
            print(f"Var {var} (let/const): length {len(val)}, starts with: {val[:60]}")
        else:
            print(f"Var {var} not found directly with quotes")
