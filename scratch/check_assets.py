with open('scratch/line24.js', 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

import re
# Look for img tags or src=
imgs = re.findall(r'src:\s*["\']([^"\']+)["\']', code)
print("Images found:", imgs)

# Look for svg
svgs = re.findall(r'X\("svg"', code)
print("SVG count:", len(svgs))
