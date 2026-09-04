import zipfile
import os
import datetime
from pathlib import Path

root = Path(__file__).resolve().parents[1]
now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_zip = root / f"odontoscore_{now_str}.zip"

exclude_dirs = {'.git', '.github', '.gemini', 'node_modules', 'scratch', 'tools', '__pycache__'}
exclude_extensions = {'.zip', '.pyc'}

count = 0
with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for foldername, subfolders, filenames in os.walk(root):
        # Filter subfolders in-place
        subfolders[:] = [d for d in subfolders if d not in exclude_dirs]
        for filename in filenames:
            file_path = Path(foldername) / filename
            if file_path == output_zip or file_path.suffix in exclude_extensions:
                continue
            arcname = file_path.relative_to(root)
            zipf.write(file_path, arcname)
            count += 1

print(f"Archive created: {output_zip.name} ({count} files, {output_zip.stat().st_size:,} bytes)")
print(f"PATH:{output_zip.resolve()}")
