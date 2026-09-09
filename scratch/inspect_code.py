with open('guias/ejemplos/Longitud-Trabajo-Endodoncia.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

print("Line 24 preview:", lines[24][:300])
print("Line 26 preview:", lines[26][:300])
# Let's inspect the end of line 18
print("Line 18 end preview:", lines[18][-500:])

# Search where component is in line 18
import re
pos = lines[18].find("function")
print("First function pos in line 18:", pos)
