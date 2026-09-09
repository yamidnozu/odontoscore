with open('guias/ejemplos/Longitud-Trabajo-Endodoncia.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

pos_div = content.find('children:[v("style"')
rest = content[pos_div:]

# Let's find each X("section" or v("footer"
import re
items = []
for m in re.finditer(r'(?:X\("section"|v\("footer"|X\("div",\{className:"sticky)', rest):
    items.append((m.start(), m.group(0)))

print(f"Found {len(items)} main blocks in children:")
for idx, (p, tag) in enumerate(items):
    snippet = rest[p:p+80].replace('\n', ' ')
    print(f"Block {idx} at {p}: {tag} -> {snippet}")
