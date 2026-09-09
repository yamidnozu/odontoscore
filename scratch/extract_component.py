with open('guias/ejemplos/Longitud-Trabajo-Endodoncia.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

# Let's inspect where the main component starts in line 18
# It probably starts somewhere near the end of line 18
line18 = lines[18]
# Search backwards for component definition like function App or similar
pos = line18.rfind("function ")
print("Last function in line 18 at:", pos)
print("Content around that function:", line18[pos:pos+1500])

with open('scratch/line24.js', 'w', encoding='utf-8') as out:
    out.write(line18[pos:] + '\n' + lines[24])

print("Wrote component code to scratch/line24.js")
