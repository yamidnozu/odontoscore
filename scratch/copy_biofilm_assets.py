import shutil
from pathlib import Path

src_dir = Path(r"C:\Users\PREDATOR\.gemini\antigravity-ide\brain\edf88a14-f2cc-4c70-bc38-da0b2c621dbe")
dst_dir = Path(r"c:\Proyectos\bussiness\store-odontologia\assets\img\biofilm")
dst_dir.mkdir(parents=True, exist_ok=True)

images_map = {
    "fase1_pelicula.jpg": "biofilm_fase1_pelicula_1788526690867.jpg",
    "fase2_adhesion.jpg": "biofilm_fase2_adhesion_1788526711478.jpg",
    "fase3_coagregacion.jpg": "biofilm_fase3_coagregacion_1788526734887.jpg",
    "fase4_maduracion.jpg": "biofilm_fase4_maduracion_1788526763032.jpg",
    "fase5_invasion.jpg": "biofilm_fase5_invasion_1788526792536.jpg",
    "endodoncia_conducto.jpg": "endodoncia_conducto_biofilm_1788526827063.jpg",
    "endodoncia_irrigacion.jpg": "endodoncia_irrigacion_naocl_1788526859571.jpg"
}

for dst_name, src_name in images_map.items():
    src_path = src_dir / src_name
    dst_path = dst_dir / dst_name
    if src_path.exists():
        shutil.copy2(src_path, dst_path)
        print(f"Copied {src_name} -> {dst_path} ({dst_path.stat().st_size:,} bytes)")
    else:
        print(f"ERROR: {src_path} not found!")

print("All biofilm image assets successfully transferred to assets/img/biofilm/")
