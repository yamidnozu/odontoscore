with open('scratch/sections_extracted.txt', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

parts = content.split("==================== SECTION ")
for p in parts[1:]:
    header = p[:30]
    print(f"Section {header.strip()}: length {len(p)}")
