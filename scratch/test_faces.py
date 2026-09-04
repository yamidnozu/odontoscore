import math

LANDMARKS = [
    { 'id': 'cusp_mv',  'num': '1',  'title': 'Cúspide Mesiovestibular',       'x': -0.48, 'y': 0.82,  'z': 0.42,  'face': 'vestibular' },
    { 'id': 'cusp_dv',  'num': '2',  'title': 'Cúspide Distovestibular',       'x':  0.48, 'y': 0.80,  'z': 0.42,  'face': 'vestibular' },
    { 'id': 'surco_v',  'num': '3',  'title': 'Surco de Desarrollo Vestibular','x':  0.00, 'y': 0.48,  'z': 0.58,  'face': 'vestibular' },
    { 'id': 'lac_v',    'num': '4',  'title': 'Línea Amelocementaria (Cuello)','x':  0.00, 'y': 0.12,  'z': 0.52,  'face': 'vestibular' },
    { 'id': 'furca',    'num': '5',  'title': 'Bifurcación Radicular (Furca)', 'x':  0.00, 'y': -0.22, 'z': 0.42,  'face': 'vestibular' },
    { 'id': 'apex_m',   'num': '6',  'title': 'Ápice Radicular Mesial',        'x': -0.30, 'y': -1.02, 'z': 0.08,  'face': 'apices' },
    { 'id': 'apex_d',   'num': '7',  'title': 'Ápice Radicular Distal',        'x':  0.30, 'y': -1.00, 'z': -0.08, 'face': 'apices' },
    { 'id': 'cusp_ml',  'num': '8',  'title': 'Cúspide Mesiolingual',          'x': -0.48, 'y': 0.82,  'z': -0.42, 'face': 'lingual' },
    { 'id': 'cusp_dl',  'num': '9',  'title': 'Cúspide Distolingual',          'x':  0.48, 'y': 0.80,  'z': -0.42, 'face': 'lingual' },
    { 'id': 'surco_l',  'num': '10', 'title': 'Surco Lingual de Desarrollo',   'x':  0.00, 'y': 0.48,  'z': -0.58, 'face': 'lingual' },
    { 'id': 'fosa_cen', 'num': '11', 'title': 'Fosa Central Oclusal',          'x':  0.00, 'y': 0.74,  'z': 0.00,  'face': 'oclusal' },
    { 'id': 'cont_m',   'num': '12', 'title': 'Área de Contacto Mesial',       'x': -0.68, 'y': 0.40,  'z': 0.00,  'face': 'mesial' },
    { 'id': 'cont_d',   'num': '13', 'title': 'Área de Contacto Distal',       'x':  0.68, 'y': 0.36,  'z': 0.00,  'face': 'distal' },
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
    centerX, centerY = 50.0, 44.0
    scaleX, scaleY = 25.0, 38.0
    screenX = centerX + x2 * scaleX
    screenY = centerY - y2 * scaleY
    is_front = z2 > -0.12
    opacity = max(0.0, min(1.0, (z2 + 0.12) / 0.22))
    return screenX, screenY, z2, is_front, opacity

faces = [
    ('Vestibular', 0, 3),
    ('Mesial', 1.5, 3),
    ('Lingual', 3, 3),
    ('Distal', 4.5, 3),
    ('Oclusal', 0, 0),
    ('Ápices', 0, 6)
]

for name, tx, ty in faces:
    print(f'=== Face: {name} ===')
    for lm in LANDMARKS:
        sx, sy, z2, is_front, op = project(lm, tx, ty)
        if is_front:
            print(f'  [{lm["num"]:>2}] {lm["title"]:32s}: ({sx:5.1f}%, {sy:5.1f}%) op={op:.2f} z={z2:+.2f}')
