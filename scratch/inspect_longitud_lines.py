import re

with open('guias/ejemplos/Longitud-Trabajo-Endodoncia.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Let's find all text inside the bundled React code or find how it's structured
# Search for functions or component definitions
lines = content.splitlines()
print(f"Total lines: {len(lines)}")
for idx, line in enumerate(lines):
    if len(line) < 500:
        print(f"Line {idx}: {line[:120]}")
    else:
        print(f"Line {idx}: length {len(line)}")
