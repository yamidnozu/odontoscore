import re

with open('scratch/line24.js', 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

# Replace common JS patterns with newlines
formatted = code
formatted = formatted.replace('X("', '\nX("')
formatted = formatted.replace('v("', '\nv("')
formatted = formatted.replace('{children:', '\n  {children:')
formatted = formatted.replace(',className:', '\n  ,className:')

with open('scratch/component_formatted.txt', 'w', encoding='utf-8') as f:
    f.write(formatted)

print("Formatted length:", len(formatted))
# Print all text content found in children strings
texts = re.findall(r'children:\s*["\']([^"\']{4,})["\']', code)
print(f"Total text blocks: {len(texts)}")
for idx, t in enumerate(texts):
    print(f"{idx}: {t[:100]}")
