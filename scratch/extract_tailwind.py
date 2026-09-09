with open('guias/ejemplos/Longitud-Trabajo-Endodoncia.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

print("Line 7 length:", len(lines[7]))
with open('scratch/tailwind_exact.css', 'w', encoding='utf-8') as out:
    out.write(lines[7])

print("Saved scratch/tailwind_exact.css!")
