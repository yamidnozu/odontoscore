import math

# Precise 3D coordinates based on the 400x400 atlas measurement:
# Center: X=200, Y=175.
# Crown top: Y=50 (delta = -125 px -> y = +0.83)
# Cusp tips: Y=75 (delta = -100 px -> y = +0.66)
# Cervical line LAC: Y=152 (delta = -23 px -> y = +0.15)
# Furca: Y=210 (delta = +35 px -> y = -0.23)
# Mid-root: Y=275 (delta = +100 px -> y = -0.66)
# Root apex: Y=345 (delta = +170 px -> y = -1.13)

LANDMARKS_3D = [
    {
        "id": "cusp_mv",
        "num": "1",
        "title": "Cúspide Mesiovestibular",
        "desc": "Cúspide de corte con vertientes lisas mesiovestibulares.",
        "pearl": "Contacto céntrico clave contra la fosa central superior.",
        "x": -0.28, "y": 0.68, "z": 0.24
    },
    {
        "id": "cusp_dv",
        "num": "2",
        "title": "Cúspide Distovestibular",
        "desc": "Cúspide redondeada que delimita la tronera distovestibular.",
        "pearl": "Canaliza el bolo alimenticio durante la fase de escape masticatorio.",
        "x": 0.28, "y": 0.66, "z": 0.22
    },
    {
        "id": "surco_v",
        "num": "3",
        "title": "Surco de Desarrollo Vestibular",
        "desc": "Depresión vertical divisoria entre cúspides vestibulares.",
        "pearl": "Zona vulnerable a caries de fisura; sitio diana de sellantes.",
        "x": 0.00, "y": 0.42, "z": 0.32
    },
    {
        "id": "lac",
        "num": "4",
        "title": "Línea Amelocementaria (Cuello)",
        "desc": "Límite cervical entre esmalte coronal y cemento radicular.",
        "pearl": "Referencia biológica para la ubicación del margen de tallado protésico.",
        "x": 0.00, "y": 0.15, "z": 0.26
    },
    {
        "id": "furca",
        "num": "5",
        "title": "Bifurcación Radicular (Furca)",
        "desc": "Punto de divergencia anatómica entre raíces mesial y distal.",
        "pearl": "Sondaje con sonda Nabers para clasificar lesiones de furca (Hamp I a III).",
        "x": 0.00, "y": -0.23, "z": 0.20
    },
    {
        "id": "apex_m",
        "num": "6",
        "title": "Ápice Radicular Mesial",
        "desc": "Vértice apical de la raíz mesial con doble conducto.",
        "pearl": "La longitud de trabajo endodóntica se fija a 0.5 mm del foramen.",
        "x": -0.16, "y": -1.05, "z": 0.05
    },
    {
        "id": "apex_d",
        "num": "7",
        "title": "Ápice Radicular Distal",
        "desc": "Vértice apical de la raíz distal con curvatura fisiológica.",
        "pearl": "Frecuente presencia de delta apical con ramificaciones colaterales.",
        "x": 0.16, "y": -1.02, "z": -0.05
    },
    {
        "id": "cusp_ml",
        "num": "8",
        "title": "Cúspide Mesiolingual",
        "desc": "Cúspide lingual principal de mayor prominencia y volumen.",
        "pearl": "Soporta la carga axial primaria en la masticación y deglución.",
        "x": -0.26, "y": 0.70, "z": -0.24
    },
    {
        "id": "cusp_dl",
        "num": "9",
        "title": "Cúspide Distolingual",
        "desc": "Cúspide lingual funcional con vertientes redondeadas.",
        "pearl": "Guía la desoclusión y protege los tejidos blandos linguales.",
        "x": 0.26, "y": 0.67, "z": -0.22
    },
    {
        "id": "fosa_cen",
        "num": "10",
        "title": "Fosa Central Oclusal",
        "desc": "Depresión oclusal profunda donde convergen los surcos principales.",
        "pearl": "Área de mayor prevalencia de caries dental en dentición permanente.",
        "x": 0.00, "y": 0.58, "z": 0.00
    },
    {
        "id": "cont_m",
        "num": "11",
        "title": "Área de Contacto Mesial",
        "desc": "Zona de contacto proximal con el diente adyacente.",
        "pearl": "Previene el empaquetamiento alimenticio y protege la papila interdental.",
        "x": -0.38, "y": 0.35, "z": 0.00
    },
    {
        "id": "cont_d",
        "num": "12",
        "title": "Área de Contacto Distal",
        "desc": "Punto de contacto posterior amplio hacia la tronera distal.",
        "pearl": "Debe restaurarse con cuña y matriz seccional convexa.",
        "x": 0.38, "y": 0.32, "z": 0.00
    }
]

def get_screen_pos(lm, thetaX, thetaY):
    # thetaX in [0, 5] -> angle from 0 to 300 deg
    azimuth = (thetaX / 5.0) * (300.0 * math.pi / 180.0)
    # thetaY in [0, 6] -> 3 is equator (0 deg), 0 is +60 deg, 6 is -60 deg
    tilt = ((3.0 - thetaY) / 3.0) * (45.0 * math.pi / 180.0)

    x, y, z = lm["x"], lm["y"], lm["z"]

    # 1. Azimuth rotation around Y
    x1 = x * math.cos(azimuth) + z * math.sin(azimuth)
    z1 = -x * math.sin(azimuth) + z * math.cos(azimuth)
    y1 = y

    # 2. Elevation/tilt rotation around X
    y2 = y1 * math.cos(tilt) - z1 * math.sin(tilt)
    z2 = y1 * math.sin(tilt) + z1 * math.cos(tilt)
    x2 = x1

    # Screen coordinates in percentage (0..100)
    # Tooth center in 400x400 is at (50%, 43.75%)
    centerX = 50.0
    centerY = 43.75

    scaleX = 42.0
    scaleY = 38.0

    screenX = centerX + x2 * scaleX
    screenY = centerY - y2 * scaleY

    # Depth test / backface culling
    # Front-facing if z2 > -0.05
    is_front = z2 > -0.05
    opacity = max(0.0, min(1.0, (z2 + 0.05) / 0.12))

    return screenX, screenY, z2, is_front, opacity

for thetaX, label in [(0, "Vestibular (0°)"), (1, "Vesto-Mesial (60°)"), (2.5, "Mesial (150°)"), (3, "Lingual (180°)"), (0, "Oclusal (+45° tilt, thetaY=0)")]:
    tY = 0 if "Oclusal" in label else 3
    print(f"\n=== {label} ===")
    for lm in LANDMARKS_3D:
        sx, sy, z2, is_front, op = get_screen_pos(lm, thetaX, tY)
        if is_front:
            print(f"  [{lm['num']:2s}] {lm['title']:30s} -> ({sx:5.1f}%, {sy:5.1f}%) op={op:4.2f}")
