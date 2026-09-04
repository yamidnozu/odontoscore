from pathlib import Path
import argparse
import shutil
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
Kx,Ky,W0,H0=6,7,400,400
parser=argparse.ArgumentParser(description='Encode the 42-view atlas without changing the image-only viewer.')
parser.add_argument('atlas',nargs='?',type=Path,default=ROOT/'source'/'atlas.png')
source=parser.parse_args().atlas.resolve()
if source != (ROOT/'source'/'atlas.png').resolve():
    shutil.copyfile(source,ROOT/'source'/'atlas.png')
atlas=Image.open(source).convert('RGB')
W,H=atlas.size
tiles=[]
for b in range(Ky):
    for a in range(Kx):
        box=(round(a*W/Kx),round(b*H/Ky),round((a+1)*W/Kx),round((b+1)*H/Ky))
        tile=atlas.crop(box).resize((W0,H0),Image.Resampling.LANCZOS)
        tiles.append(np.asarray(tile))

# Exact vectorized form of enc_np[t*Ky+b,s*Kx+a]=tiles[b*Kx+a][t,s].
# The final two axes are spatial and color; no lossy encoding is involved.
enc_np=np.zeros((H0*Ky,W0*Kx,3),dtype=np.uint8)
for b in range(Ky):
    for a in range(Kx):
        enc_np[b::Ky,a::Kx]=tiles[b*Kx+a]
encoded=ROOT/'dist'/'lightfield_encoded.png'
Image.fromarray(enc_np,'RGB').save(encoded,format='PNG',compress_level=6)
reloaded=np.asarray(Image.open(encoded))
for b in range(Ky):
    for a in range(Kx):
        assert np.array_equal(reloaded[b::Ky,a::Kx],tiles[b*Kx+a])
assert reloaded.shape==(2800,2400,3)
print(f'PASS: 42 exact inverse decodes; encoded PNG {encoded.stat().st_size:,} bytes; source {W}x{H}.')
