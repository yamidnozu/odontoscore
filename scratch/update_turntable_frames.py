import numpy as np
from PIL import Image
import os

Kx, Ky, W0, H0 = 6, 7, 400, 400
enc = Image.open('assets/img/lightfield_diente_encoded.png').convert('RGB')
enc_np = np.asarray(enc)

os.makedirs('assets/img/turntable', exist_ok=True)

# 8 frames around the equator (row 3 = elevation 0)
# We have 6 exact azimuth columns: 0, 1, 2, 3, 4, 5
# For frames 0..7:
# 0 -> col 0 (0 deg)
# 1 -> col 1 (60 deg)
# 2 -> 50% col 1 + 50% col 2 (90 deg)
# 3 -> col 2 (120 deg)
# 4 -> col 3 (180 deg)
# 5 -> col 4 (240 deg)
# 6 -> 50% col 4 + 50% col 5 (270 deg)
# 7 -> col 5 (300 deg)

frames = [
    enc_np[3::Ky, 0::Kx],
    enc_np[3::Ky, 1::Kx],
    ((enc_np[3::Ky, 1::Kx].astype(np.float32) + enc_np[3::Ky, 2::Kx].astype(np.float32)) * 0.5).astype(np.uint8),
    enc_np[3::Ky, 2::Kx],
    enc_np[3::Ky, 3::Kx],
    enc_np[3::Ky, 4::Kx],
    ((enc_np[3::Ky, 4::Kx].astype(np.float32) + enc_np[3::Ky, 5::Kx].astype(np.float32)) * 0.5).astype(np.uint8),
    enc_np[3::Ky, 5::Kx]
]

for idx, f in enumerate(frames):
    im = Image.fromarray(f).resize((512, 512), Image.Resampling.LANCZOS)
    im.save(f'assets/img/turntable/frame_{idx}.jpg', 'JPEG', quality=95)
    print(f'Saved assets/img/turntable/frame_{idx}.jpg')

print('Turntable frames updated successfully!')
