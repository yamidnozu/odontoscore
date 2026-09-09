with open('scratch/line24.js', 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

# Let's slice the code into the sections
# Let's find each section's start and content
import re
sections = [m.start() for m in re.finditer(r'X\("section"', code)]
sections.append(len(code))

with open('scratch/sections_extracted.txt', 'w', encoding='utf-8') as out:
    for i in range(len(sections)-1):
        out.write(f"\n\n==================== SECTION {i+1} ====================\n")
        out.write(code[sections[i]:sections[i+1]])

print("Sections extracted!")
