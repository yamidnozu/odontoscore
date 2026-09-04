import math

landmarks = [
    { 'id': 'cusp_mv',  'num': '1',  'title': 'Cúspide Mesiovestibular',       'x': -0.47, 'y': 0.82,  'z': 0.35 },
    { 'id': 'cusp_dv',  'num': '2',  'title': 'Cúspide Distovestibular',       'x':  0.47, 'y': 0.80,  'z': 0.35 },
    { 'id': 'surco_v',  'num': '3',  'title': 'Surco de Desarrollo Vestibular','x':  0.00, 'y': 0.57,  'z': 0.48 },
    { 'id': 'lac',      'num': '4',  'title': 'Línea Amelocementaria (Cuello)','x':  0.00, 'y': 0.16,  'z': 0.42 },
    { 'id': 'furca',    'num': '5',  'title': 'Bifurcación Radicular (Furca)', 'x':  0.00, 'y': -0.15, 'z': 0.35 },
    { 'id': 'apex_m',   'num': '6',  'title': 'Ápice Radicular Mesial',        'x': -0.35, 'y': -0.99, 'z': 0.08 },
    { 'id': 'apex_d',   'num': '7',  'title': 'Ápice Radicular Distal',        'x':  0.35, 'y': -0.99, 'z': -0.08 },
    { 'id': 'cusp_ml',  'num': '8',  'title': 'Cúspide Mesiolingual',          'x': -0.47, 'y': 0.82,  'z': -0.35 },
    { 'id': 'cusp_dl',  'num': '9',  'title': 'Cúspide Distolingual',          'x':  0.47, 'y': 0.80,  'z': -0.35 },
    { 'id': 'surco_l',  'num': '10', 'title': 'Surco Lingual de Desarrollo',   'x':  0.00, 'y': 0.57,  'z': -0.48 },
    { 'id': 'fosa_cen', 'num': '11', 'title': 'Fosa Central Oclusal',          'x':  0.00, 'y': 0.75,  'z': 0.00 },
    { 'id': 'cont_m',   'num': '12', 'title': 'Área de Contacto Mesial',       'x': -0.62, 'y': 0.45,  'z': 0.00 },
    { 'id': 'cont_d',   'num': '13', 'title': 'Área de Contacto Distal',       'x':  0.62, 'y': 0.42,  'z': 0.00 },
]

def project(lm, tx, ty):
    azimuth = (tx / 6.0) * 2 * math.pi
    elevation = ((3.0 - ty) / 3.0) * (math.pi / 3.6)
    x, y, z = lm['x'], lm['y'], lm['z']
    x1 = x * math.cos(azimuth) + z * math.sin(azimuth)
    z1 = -x * math.sin(azimuth) + z * math.cos(azimuth)
    y1 = y
    y2 = y1 * math.cos(elevation) - z1 * math.sin(elevation)
    z2 = y1 * math.sin(elevation) + z1 * math.cos(elevation)
    x2 = x1
    centerX = 50.0
    centerY = 48.0
    scaleX = 20.0
    scaleY = 38.0
    screenX = centerX + x2 * scaleX
    screenY = centerY - y2 * scaleY
    is_front = z2 > -0.08
    opacity = max(0.0, min(1.0, (z2 + 0.08) / 0.18))
    return screenX, screenY, z2, is_front, opacity

print('=== Vestibular (tx=0, ty=3) ===')
for lm in landmarks[:7]:
    sx, sy, z2, is_front, op = project(lm, 0, 3)
    print(f"{lm['title']:32s}: ({sx:5.1f}%, {sy:5.1f}%) op={op:.2f} z={z2:+.2f}")

print('\n=== Oclusal (tx=0, ty=0) ===')
for lm in [landmarks[0], landmarks[1], landmarks[7], landmarks[8], landmarks[10]]:
    sx, sy, z2, is_front, op = project(lm, 0, 0)
    print(f"{lm['title']:32s}: ({sx:5.1f}%, {sy:5.1f}%) op={op:.2f} z={z2:+.2f}")
