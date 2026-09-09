with open('guias/ejemplos/Longitud-Trabajo-Endodoncia.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

print("Line 6 length:", len(lines[6]))
with open('scratch/tailwind_exact.css', 'w', encoding='utf-8') as out:
    out.write(lines[6])

print("Saved line 6 to scratch/tailwind_exact.css!")
