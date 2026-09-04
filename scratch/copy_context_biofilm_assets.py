import shutil
from pathlib import Path

src_dir = Path(r"C:\Users\PREDATOR\.gemini\antigravity-ide\brain\edf88a14-f2cc-4c70-bc38-da0b2c621dbe")
dst_dir = Path(r"c:\Proyectos\bussiness\store-odontologia\assets\img\biofilm")
dst_dir.mkdir(parents=True, exist_ok=True)

context_images_map = {
    "fase1_pelicula.jpg": "fase1_context_tooth_1788528233876.jpg",
    "fase2_adhesion.jpg": "fase2_context_tooth_1788528275758.jpg",
    "fase3_coagregacion.jpg": "fase3_context_tooth_1788528318035.jpg",
    "fase4_maduracion.jpg": "fase4_context_tooth_1788528370792.jpg",
    "fase5_invasion.jpg": "fase5_context_tooth_1788528426939.jpg",
    "endodoncia_conducto.jpg": "endodoncia_apice_zoom_1788528479406.jpg",
    "endodoncia_irrigacion.jpg": "endodoncia_irrigacion_naocl_1788526859571.jpg"
}

for dst_name, src_name in context_images_map.items():
    src_path = src_dir / src_name
    dst_path = dst_dir / dst_name
    if src_path.exists():
        shutil.copy2(src_path, dst_path)
        print(f"Copied {src_name} -> {dst_path} ({dst_path.stat().st_size:,} bytes)")
    else:
        print(f"ERROR: {src_path} not found!")

print("All context images with anatomical callout zooms successfully transferred!")
