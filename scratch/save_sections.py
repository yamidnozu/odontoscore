with open('scratch/sections_extracted.txt', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

parts = content.split("==================== SECTION ")
with open('scratch/section5.txt', 'w', encoding='utf-8') as out:
    out.write(parts[5])

with open('scratch/section1.txt', 'w', encoding='utf-8') as out:
    out.write(parts[1])

with open('scratch/section2.txt', 'w', encoding='utf-8') as out:
    out.write(parts[2])

with open('scratch/section3.txt', 'w', encoding='utf-8') as out:
    out.write(parts[3])

with open('scratch/section4.txt', 'w', encoding='utf-8') as out:
    out.write(parts[4])

print("Saved section files individually!")
