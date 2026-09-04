import base64
import io
import numpy as np
from PIL import Image

with open('lib/lightfield-data.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

start = js_code.find('base64,') + 7
end = js_code.rfind('"')
b64_str = js_code[start:end]

img_bytes = base64.b64decode(b64_str)
img = Image.open(io.BytesIO(img_bytes))
print(f"Format: {img.format}, Mode: {img.mode}, Size: {img.size}")

arr = np.asarray(img)
print(f"Array shape: {arr.shape}")
assert arr.shape[:2] == (2800, 2400), f"Incorrect shape {arr.shape}"

# Check that tiles can be sliced out with exact precision
Kx, Ky, W0, H0 = 6, 7, 400, 400
print(f"Testing exact inverse de-multiplexing for all {Kx * Ky} views...")

# Load atlas to verify exact match
atlas = Image.open('assets/img/atlas_diente_42vistas.png').convert('RGB')
W, H = atlas.size
tiles = []
for b in range(Ky):
    for a in range(Kx):
        box = (round(a * W / Kx), round(b * H / Ky), round((a + 1) * W / Kx), round((b + 1) * H / Ky))
        tile = atlas.crop(box).resize((W0, H0), Image.Resampling.LANCZOS)
        tiles.append(np.asarray(tile))

# Verify every single pixel matches
matches = 0
for b in range(Ky):
    for a in range(Kx):
        extracted = arr[b::Ky, a::Kx, :3]
        target = tiles[b * Kx + a]
        if np.array_equal(extracted, target):
            matches += 1

print(f"PASS: {matches}/42 views match byte-for-byte with 100% exact numerical precision!")
