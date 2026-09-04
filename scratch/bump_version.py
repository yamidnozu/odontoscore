import glob
import re

count = 0
for path in glob.glob('**/*.html', recursive=True):
    if 'brain' in path or 'scratch' in path or '.git' in path:
        continue
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    new_c = re.sub(r'styles\.css(\?v=[a-zA-Z0-9_]+)?', 'styles.css?v=20260903_v75', c)
    new_c = re.sub(r'main\.js(\?v=[a-zA-Z0-9_]+)?', 'main.js?v=20260903_v75', new_c)
    if new_c != c:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_c)
        count += 1

print(f'Updated {count} HTML files to version v75')
