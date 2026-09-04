import numpy as np
from PIL import Image

# The tooth images in assets/img/secuencia_360/ are 400x400
img = Image.open('assets/img/secuencia_360/paso_1_0deg_frontal_corte.jpg').convert('RGB')
arr = np.asarray(img)

mask = np.any(arr < 240, axis=2)
rows = np.any(mask, axis=1)
cols = np.any(mask, axis=0)

min_y, max_y = np.where(rows)[0][[0, -1]]
min_x, max_x = np.where(cols)[0][[0, -1]]

print(f"Tooth bounding box in 400x400 image:")
print(f"X: {min_x}..{max_x} (center: {(min_x + max_x)/2} px, {(min_x + max_x)/8.0:.1f}%)")
print(f"Y: {min_y}..{max_y} (height: {max_y - min_y} px, {(min_y)/4.0:.1f}% to {(max_y)/4.0:.1f}%)")
print(f"Crown top: {min_y} px ({min_y/4.0:.1f}%)")
print(f"Root apex: {max_y} px ({max_y/4.0:.1f}%)")
