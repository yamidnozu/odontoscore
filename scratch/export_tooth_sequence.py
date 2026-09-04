import numpy as np
from PIL import Image
import os

Kx, Ky, W0, H0 = 6, 7, 400, 400
enc = Image.open('assets/img/lightfield_diente_encoded.png').convert('RGB')
enc_np = np.asarray(enc)

os.makedirs('assets/img/secuencia_360', exist_ok=True)

steps = [
    # (col, row, filename)
    (0, 3, 'paso_1_0deg_frontal_corte.jpg'),      # 0 deg Vestibular
    (1, 3, 'paso_2_45deg_vestibular_mesial.jpg'), # 60 deg Vestibular-Mesial
    (2, 3, 'paso_3_90deg_lateral_corte.jpg'),     # 120 deg Mesial-Lingual
    (3, 3, 'paso_4_135deg_lingual_mesial.jpg'),   # 180 deg Lingual
    (4, 3, 'paso_5_180deg_posterior_corte.jpg'),  # 240 deg Lingual-Distal
    (5, 3, 'paso_6_225deg_lingual_distal.jpg'),   # 300 deg Distal-Vestibular
    (0, 0, 'paso_7_270deg_lateral_externo.jpg'),  # +60 deg Cenital Oclusal
    (0, 5, 'paso_8_315deg_hemiseccion_3d.jpg'),   # -40 deg Radicular Apical
]

for col, row, filename in steps:
    tile = enc_np[row::Ky, col::Kx]
    im = Image.fromarray(tile).resize((600, 600), Image.Resampling.LANCZOS)
    out_path = os.path.join('assets/img/secuencia_360', filename)
    im.save(out_path, 'JPEG', quality=94)
    print(f'Saved {filename} from (col={col}, row={row})')

print('All 8 steps replaced with real lightfield tooth images!')
