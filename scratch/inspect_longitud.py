import re

with open('guias/ejemplos/Longitud-Trabajo-Endodoncia.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

print('File length:', len(content))
title_match = re.search(r'<title>(.*?)</title>', content)
print('Title:', title_match.group(1) if title_match else 'None')

# Look for text strings in the bundle
matches = re.findall(r'["\']([^"\']{20,120})["\']', content)
endodoncia_matches = [m for m in matches if any(k in m.lower() for k in ['longitud', 'ápice', 'apice', 'conducto', 'endodoncia', 'lima', 'trabajo', 'constricción', 'foramen'])]
print(f'Found {len(endodoncia_matches)} relevant strings. Samples:')
for m in endodoncia_matches[:30]:
    print('-', m)
