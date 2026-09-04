import math

# Define 3D anatomical landmarks of the molar: (x, y, z)
# +Y = Occlusal (up), -Y = Apical (down)
# +Z = Vestibular (front), -Z = Lingual (back)
# -X = Mesial (left), +X = Distal (right)

LANDMARKS = [
    {"id": "cusp_mv", "name": "Cúspide Mesiovestibular", "pos": (-0.18, 0.48, 0.22)},
    {"id": "cusp_dv", "name": "Cúspide Distovestibular", "pos": (0.18, 0.46, 0.20)},
    {"id": "cusp_ml", "name": "Cúspide Mesiolingual",    "pos": (-0.16, 0.50, -0.22)},
    {"id": "cusp_dl", "name": "Cúspide Distolingual",    "pos": (0.16, 0.48, -0.20)},
    {"id": "fosa_cen", "name": "Fosa Central Oclusal",   "pos": (0.00, 0.42, 0.00)},
    {"id": "surco_v", "name": "Surco Vestibular",       "pos": (0.00, 0.28, 0.26)},
    {"id": "lac_v", "name": "Cuello Cervical LAC",      "pos": (0.00, 0.02, 0.23)},
    {"id": "furca_v", "name": "Furca Radicular",        "pos": (0.00, -0.25, 0.16)},
    {"id": "apex_m", "name": "Ápice Mesial",            "pos": (-0.12, -0.78, 0.04)},
    {"id": "apex_d", "name": "Ápice Distal",            "pos": (0.12, -0.76, -0.02)},
    {"id": "cont_m", "name": "Área de Contacto Mesial",  "pos": (-0.28, 0.22, 0.00)},
    {"id": "cont_d", "name": "Área de Contacto Distal",  "pos": (0.28, 0.20, 0.00)},
    {"id": "surco_l", "name": "Surco Lingual",          "pos": (0.00, 0.26, -0.24)},
]

def project(pos, thetaX, thetaY):
    # thetaX: 0..5.9 (horizontal rotation)
    # thetaY: 0..6.9 (vertical tilt, 3 is equator)
    # The lightfield covers 0°..300° across thetaX 0..5
    azimuth = (thetaX / 5.0) * (300.0 * math.pi / 180.0)
    # vertical tilt: 0 is +60° (looking from top), 3 is 0°, 6 is -60° (looking from bottom)
    elevation = ((3.0 - thetaY) / 3.0) * (45.0 * math.pi / 180.0)

    x, y, z = pos

    # 1. Rotate around Y axis (azimuth)
    x1 = x * math.cos(azimuth) + z * math.sin(azimuth)
    z1 = -x * math.sin(azimuth) + z * math.cos(azimuth)
    y1 = y

    # 2. Rotate around X axis (elevation/tilt)
    y2 = y1 * math.cos(elevation) - z1 * math.sin(elevation)
    z2 = y1 * math.sin(elevation) + z1 * math.cos(elevation)
    x2 = x1

    # Screen projection
    # Tooth center in viewport is (50%, 52%)
    screenX = 50.0 + x2 * 75.0
    screenY = 52.0 - y2 * 50.0

    # Visibility: z2 > 0 is facing the camera. z2 < -0.1 is hidden on back.
    visible = z2 > -0.08
    opacity = max(0.0, min(1.0, (z2 + 0.08) / 0.15))

    return screenX, screenY, z2, visible, opacity

# Test at Front view (thetaX=0, thetaY=3)
print("--- FRONT VIEW (thetaX=0, thetaY=3) ---")
for lm in LANDMARKS:
    sx, sy, z2, vis, op = project(lm["pos"], 0, 3)
    if vis:
        print(f"{lm['name']:30s}: screen=({sx:5.1f}%, {sy:5.1f}%), z={z2:5.2f}, opacity={op:4.2f}")

# Test at 180 deg (thetaX=3, thetaY=3)
print("\n--- LINGUAL VIEW (thetaX=3, thetaY=3) ---")
for lm in LANDMARKS:
    sx, sy, z2, vis, op = project(lm["pos"], 3, 3)
    if vis:
        print(f"{lm['name']:30s}: screen=({sx:5.1f}%, {sy:5.1f}%), z={z2:5.2f}, opacity={op:4.2f}")

# Test at Top/Occlusal view (thetaX=0, thetaY=0)
print("\n--- OCCLUSAL VIEW (thetaX=0, thetaY=0) ---")
for lm in LANDMARKS:
    sx, sy, z2, vis, op = project(lm["pos"], 0, 0)
    if vis:
        print(f"{lm['name']:30s}: screen=({sx:5.1f}%, {sy:5.1f}%), z={z2:5.2f}, opacity={op:4.2f}")
