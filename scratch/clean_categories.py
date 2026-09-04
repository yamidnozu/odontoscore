import glob
import re

for path in glob.glob('categoria/*.html'):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove category-icon with emoji
    content = re.sub(r'<div class="category-icon"[^>]*>.*?</div>\s*', '', content)
    # Compact heading
    content = content.replace('font-size:2.4rem;', 'font-size:1.65rem;')
    content = content.replace('font-size:1.1rem;', 'font-size:0.92rem;')
    content = content.replace('margin-bottom:2.5rem;', 'margin-bottom:1.5rem;')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Category headers cleaned and compacted successfully!')
