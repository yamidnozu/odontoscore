import json
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

env_path = Path("c:/Proyectos/bussiness/store-odontologia/.env")
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://lgaolwxeizxynkpcjsse.supabase.co")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

VIDEO_MAPPING = {
    # Tipodontos
    "tipodonto": {"url": "https://www.youtube.com/embed/JG_5smgkAts", "title": "Práctica Clínica en Tipodonto Dental"},
    # Suturas
    "sutura": {"url": "https://www.youtube.com/embed/IHg8PcnLeFk", "title": "Técnica de Sutura Quirúrgica Dental"},
    # Lámparas LED
    "l-mpara": {"url": "https://www.youtube.com/embed/Njkm70cZDpo", "title": "Demostración Lámpara LED de Fotocurado"},
    "luz": {"url": "https://www.youtube.com/embed/Njkm70cZDpo", "title": "Demostración Luz Fotográfica y Lámpara LED"},
    # Oral-B iO
    "oral-b-io": {"url": "https://www.youtube.com/embed/8eu8xQF6RZ8", "title": "Tecnología Magnética Oral-B iO en Acción"},
    # Philips Sonicare
    "sonicare": {"url": "https://www.youtube.com/embed/kbpoJY0sHOo", "title": "Tecnología Sónica Philips Sonicare"},
    # Waterpik
    "waterpik": {"url": "https://www.youtube.com/embed/KnNuSvIx-6I", "title": "Uso y Funcionamiento Waterpik Flosser"},
    # Irrigador Portátil
    "irrigador": {"url": "https://www.youtube.com/embed/ERP84DYT47A", "title": "Demostración Irrigador Dental Inalámbrico"},
    "usmile": {"url": "https://www.youtube.com/embed/ERP84DYT47A", "title": "Demostración Irrigador Dental de Viaje"},
    "jtf": {"url": "https://www.youtube.com/embed/ERP84DYT47A", "title": "Demostración Irrigador Bucal Portátil"},
    # Blanqueamiento
    "blanquea": {"url": "https://www.youtube.com/embed/v92t-2p4Qdw", "title": "Guía de Aplicación Kit Blanqueamiento LED"},
    "bledras": {"url": "https://www.youtube.com/embed/v92t-2p4Qdw", "title": "Demostración Kit Blanqueamiento Profesional"},
    "ipo": {"url": "https://www.youtube.com/embed/v92t-2p4Qdw", "title": "Tratamiento de Blanqueamiento Dental"},
    # Ortodoncia Cera
    "cera": {"url": "https://www.youtube.com/embed/svTG_jDhqdI", "title": "Cómo Aplicar Cera Dental de Ortodoncia"},
    "yuzna": {"url": "https://www.youtube.com/embed/svTG_jDhqdI", "title": "Alivio y Protección con Cera Ortodóntica"},
    "lacer": {"url": "https://www.youtube.com/embed/svTG_jDhqdI", "title": "Protección para Brackets y Alineadores"},
    # Interdentales
    "interdental": {"url": "https://www.youtube.com/embed/77lgpUf4_qY", "title": "Técnica de Limpieza con Cepillos Interdentales"},
    "picks": {"url": "https://www.youtube.com/embed/77lgpUf4_qY", "title": "Higiene Interproximal para Brackets"},
    # Kids
    "kids": {"url": "https://www.youtube.com/embed/b0alKWNrp3w", "title": "Demostración Cepillo Eléctrico Infantil"},
    "frozen": {"url": "https://www.youtube.com/embed/b0alKWNrp3w", "title": "Cepillado Divertido Oral-B Pro Kids"},
    # Instrumental
    "piezas": {"url": "https://www.youtube.com/embed/TK3sKmgQL2c", "title": "Instrumental y Bandejas de Acero Inoxidable"},
    "bandeja": {"url": "https://www.youtube.com/embed/TK3sKmgQL2c", "title": "Esterilización y Uso de Bandejas Clínicas"},
    "cesta": {"url": "https://www.youtube.com/embed/TK3sKmgQL2c", "title": "Esterilización de Instrumental en Autoclave"},
    "gima": {"url": "https://www.youtube.com/embed/TK3sKmgQL2c", "title": "Material Instrumental Clínico y Quirúrgico"}
}

def get_video_for_prod(prod_id, prod_name, cat):
    key_str = f"{prod_id} {prod_name}".lower()
    for pattern, vdata in VIDEO_MAPPING.items():
        if pattern in key_str:
            return [{
                "title": vdata["title"],
                "url": vdata["url"],
                "thumbnail": "https://img.youtube.com/vi/" + vdata["url"].split("/")[-1] + "/hqdefault.jpg"
            }]
    return None

# Update Supabase
headers = {
    "apikey": SUPABASE_SERVICE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

# Fetch all
r = requests.get(f"{SUPABASE_URL}/rest/v1/products?select=*", headers=headers)
products = r.json()
print(f"Updating {len(products)} products in Supabase with verified working videos...")

updated_count = 0
for p in products:
    pid = p.get("id")
    pname = p.get("name", "")
    pcat = p.get("categoria_odontologica", "")
    
    vid = get_video_for_prod(pid, pname, pcat)
    if vid:
        specs_extra = p.get("specs_extra") or {}
        specs_extra["videos"] = vid
        
        patch_res = requests.patch(
            f"{SUPABASE_URL}/rest/v1/products?id=eq.{pid}",
            headers=headers,
            json={"specs_extra": specs_extra}
        )
        if patch_res.status_code in [200, 204]:
            updated_count += 1
            print(f"  [OK] {pid} -> {vid[0]['title']} ({vid[0]['url']})")
        else:
            print(f"  [ERROR] {pid}: {patch_res.text}")

print(f"\nSuccessfully updated {updated_count} products in Supabase with working videos!")
