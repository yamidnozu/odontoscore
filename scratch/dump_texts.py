import re

with open('scratch/line24.js', 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

texts = re.findall(r'children:\s*["\']([^"\']{4,})["\']', code)
with open('scratch/all_texts.txt', 'w', encoding='utf-8') as f:
    for idx, t in enumerate(texts):
        f.write(f"{idx}: {t}\n")

print(f"Done! Wrote {len(texts)} texts to scratch/all_texts.txt")
