import zipfile
import os
import datetime
from pathlib import Path

ROOT = Path("c:/Proyectos/bussiness/store-odontologia")
now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
zip_name = f"odontoscore_{now_str}.zip"
zip_path = ROOT / zip_name

files_to_include = [
    "index.html",
    "styles.css",
    "main.js",
    "robots.txt",
    "sitemap.xml",
    ".htaccess",
    "_redirects",
    "aviso-afiliados.html",
    "privacidad.html",
    "sobre-nosotros.html",
    "comparador.html",
    "ofertas.html"
]

dirs_to_include = [
    "assets",
    "datos",
    "lib",
    "producto",
    "guias"
]

print(f"Creating deploy archive: {zip_path}")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for f in files_to_include:
        fp = ROOT / f
        if fp.exists():
            zipf.write(fp, arcname=f)
            print(f"  + file: {f}")
            
    for d in dirs_to_include:
        dp = ROOT / d
        if dp.exists():
            for root, _, files in os.walk(dp):
                for file in files:
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(ROOT)
                    zipf.write(file_path, arcname=str(rel_path).replace("\\", "/"))
                    print(f"  + dir file: {rel_path}")

print(f"\n[OK] Archive created: {zip_path} (Size: {os.path.getsize(zip_path)} bytes)")
