import base64
import os

src_path = r'C:\Users\PREDATOR\Downloads\visor-una-png-codigo-y-prompts\visor-una-png\dist\lightfield_encoded.png'
with open(src_path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('ascii')

out_path = 'lib/lightfield-data.js'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('window.LIGHTFIELD_DATA_URI = "data:image/png;base64,' + b64 + '";\n')

print('Generated lib/lightfield-data.js with size:', os.path.getsize(out_path), 'bytes')
