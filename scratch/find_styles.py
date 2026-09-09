with open('guias/ejemplos/Longitud-Trabajo-Endodoncia.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

import re
styles = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
print(f"Found {len(styles)} style tags:")
for idx, s in enumerate(styles):
    print(f"Style {idx}: length {len(s)}")
    print(s[:200])
    print("...")
    print(s[-200:])
