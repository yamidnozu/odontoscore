with open('guias/anatomia-dental-3d-por-capas.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove any existing lightfield-viewer.js tags
content = content.replace('<script src="../lib/lightfield-viewer.js?v=20260903_v75"></script>', '')

# Place it right before the inline script
target = '<script>\n  (function () {\n    "use strict";'
replacement = '<script src="../lib/lightfield-viewer.js?v=20260903_v75"></script>\n  <script>\n  (function () {\n    "use strict";'

if target in content:
    content = content.replace(target, replacement)
    print("Placed lightfield-viewer.js before inline script!")
else:
    print("Target inline script pattern not found, checking alternatives...")

with open('guias/anatomia-dental-3d-por-capas.html', 'w', encoding='utf-8') as f:
    f.write(content)
