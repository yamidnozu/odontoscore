with open('guias/ejemplos/Longitud-Trabajo-Endodoncia.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

import re
img_vars = ['jl', 'to', 'or', 'Bl', 'Fl']
for v in img_vars:
    # search where v is used as src: v or src={v}
    occurrences = [m.start() for m in re.finditer(r'src:\s*' + v + r'\b', content)]
    print(f"Var {v} used {len(occurrences)} times at:", occurrences)
    # print snippet around it
    for idx in occurrences:
        print(f"  Snippet for {v}:", content[idx-50:idx+150])
