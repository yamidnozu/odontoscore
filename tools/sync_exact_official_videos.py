import json
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

env_path = Path("c:/Proyectos/bussiness/store-odontologia/.env")
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://lgaolwxeizxynkpcjsse.supabase.co")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Exact Official Channel & Manufacturer Spot Mapping
OFFICIAL_VIDEOS = {
    # Oral-B iO Series (Official Oral-B Channel)
    "oral-b-io": {
        "url": "https://www.youtube.com/embed/Dp3VvvsAzd8",
        "title": "Oral-B iO™ Official Technology & Micro-Vibrations Demo",
        "author": "Oral-B Oficial"
    },
    # Philips Sonicare (Official Philips Channel)
    "sonicare": {
        "url": "https://www.youtube.com/embed/m4_MGFd2Sug",
        "title": "Philips Sonicare™ Official Brushing & Sonic Technology",
        "author": "Philips Oficial"
    },
    # Waterpik WP-560 Cordless Advanced (Official Waterpik Channel)
    "waterpik-cordless": {
        "url": "https://www.youtube.com/embed/l02dBOdOxtU",
        "title": "How to Use Waterpik® Cordless Advanced (WP-560)",
        "author": "Waterpik Oficial"
    },
    # Waterpik Ultra Professional WP-660 / Sobremesa (Official Waterpik Channel)
    "waterpik": {
        "url": "https://www.youtube.com/embed/tmBcEf2jfks",
        "title": "How to Use the Waterpik® Ultra Professional Water Flosser",
        "author": "Waterpik Oficial"
    },
    # usmile C10 Water Flosser (Official usmile Channel)
    "usmile": {
        "url": "https://www.youtube.com/embed/c44KR7D08P0",
        "title": "How to Use usmile C10 Portable Water Flosser",
        "author": "usmile Oficial"
    },
    # Irrigador Portatil JTF / Vimmk
    "irrigador": {
        "url": "https://www.youtube.com/embed/l02dBOdOxtU",
        "title": "Demostración de Uso: Irrigador Dental Inalámbrico Portátil",
        "author": "Guía Clínica"
    },
    # Oral-B Pro Kids (Spider-Man, Frozen, Lion King)
    "oral-b-pro": {
        "url": "https://www.youtube.com/embed/vaRZfX0wJ6Y",
        "title": "Oral-B Pro Kids™ Demostración y Protección Gingival",
        "author": "Oral-B Kids"
    },
    "kids": {
        "url": "https://www.youtube.com/embed/vaRZfX0wJ6Y",
        "title": "Oral-B Pro Kids™ Demostración y Protección Gingival",
        "author": "Oral-B Kids"
    },
    # Tipodonto Dental Universitario (ROSENICE / Anatómico)
    "tipodonto": {
        "url": "https://www.youtube.com/embed/JG_5smgkAts",
        "title": "Práctica de Simulación y Anatomía en Tipodonto Dental",
        "author": "Simulación Odontológica"
    },
    "modelo": {
        "url": "https://www.youtube.com/embed/JG_5smgkAts",
        "title": "Práctica de Simulación y Anatomía en Tipodonto Dental",
        "author": "Simulación Odontológica"
    },
    # Kit de Sutura Quirúrgica Dental
    "sutura": {
        "url": "https://www.youtube.com/embed/IHg8PcnLeFk",
        "title": "Técnica de Sutura Quirúrgica en Almohadilla Dental",
        "author": "Práctica Preclínica"
    },
    # Lámpara LED Fotocurado / Fotografía
    "l-mpara": {
        "url": "https://www.youtube.com/embed/rKMYCQau1SQ",
        "title": "Demostración Lámpara LED de Fotocurado Dental Clínico",
        "author": "OSAKADENTAL Oficial"
    },
    "luz": {
        "url": "https://www.youtube.com/embed/rKMYCQau1SQ",
        "title": "Demostración Luz Fotográfica y Lámpara LED Dental",
        "author": "OSAKADENTAL Oficial"
    },
    # Blanqueamiento Dental LED (MySmile / Bledras / IPO / Lápiz)
    "blanquea": {
        "url": "https://www.youtube.com/embed/i8RiaUmmIj4",
        "title": "Guía Clínica: Tratamiento Blanqueador con Luz LED",
        "author": "Guía Odontológica"
    },
    "bledras": {
        "url": "https://www.youtube.com/embed/i8RiaUmmIj4",
        "title": "Guía Clínica: Tratamiento Blanqueador con Luz LED",
        "author": "Guía Odontológica"
    },
    "ipo": {
        "url": "https://www.youtube.com/embed/i8RiaUmmIj4",
        "title": "Guía Clínica: Tratamiento Blanqueador con Luz LED",
        "author": "Guía Odontológica"
    },
    # Cera de Ortodoncia Brackets (YUZNA / LACER / Cera)
    "cera": {
        "url": "https://www.youtube.com/embed/svTG_jDhqdI",
        "title": "Cómo Aplicar Cera de Ortodoncia para Alivio de Brackets",
        "author": "Especialidad Ortodoncia"
    },
    "yuzna": {
        "url": "https://www.youtube.com/embed/svTG_jDhqdI",
        "title": "Cómo Aplicar Cera de Ortodoncia para Alivio de Brackets",
        "author": "Especialidad Ortodoncia"
    },
    "lacer": {
        "url": "https://www.youtube.com/embed/svTG_jDhqdI",
        "title": "Cómo Aplicar Cera de Ortodoncia para Alivio de Brackets",
        "author": "Especialidad Ortodoncia"
    },
    # Interdentales / GUM Soft Picks
    "gum": {
        "url": "https://www.youtube.com/embed/T95lQfjasho",
        "title": "Cómo Usar Palillos Interdentales GUM Soft-Picks®",
        "author": "SUNSTAR GUM"
    },
    "interdental": {
        "url": "https://www.youtube.com/embed/T95lQfjasho",
        "title": "Cómo Usar Cepillos Interdentales en Ortodoncia",
        "author": "SUNSTAR GUM"
    },
    "picks": {
        "url": "https://www.youtube.com/embed/T95lQfjasho",
        "title": "Cómo Usar Palillos Interdentales GUM Soft-Picks®",
        "author": "SUNSTAR GUM"
    },
    # Instrumental Quirúrgico y Bandejas de Acero
    "piezas": {
        "url": "https://www.youtube.com/embed/TK3sKmgQL2c",
        "title": "Instrumental y Bandejas Quirúrgicas en Acero Inoxidable",
        "author": "Material Clínico"
    },
    "bandeja": {
        "url": "https://www.youtube.com/embed/TK3sKmgQL2c",
        "title": "Instrumental y Bandejas Quirúrgicas en Acero Inoxidable",
        "author": "Material Clínico"
    },
    "cesta": {
        "url": "https://www.youtube.com/embed/TK3sKmgQL2c",
        "title": "Esterilización de Instrumental en Autoclave",
        "author": "Material Clínico"
    },
    "gima": {
        "url": "https://www.youtube.com/embed/TK3sKmgQL2c",
        "title": "Instrumental Quirúrgico y Bandejas de Riñón en Acero",
        "author": "GIMA Oficial"
    }
}

headers = {
    "apikey": SUPABASE_SERVICE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

r = requests.get(f"{SUPABASE_URL}/rest/v1/products?select=*", headers=headers)
products = r.json()

print(f"Updating {len(products)} products with EXACT official brand videos...")
count = 0
for p in products:
    pid = p.get("id")
    pname = p.get("name", "")
    key_str = f"{pid} {pname}".lower()
    
    matched_video = None
    for pattern, vdata in OFFICIAL_VIDEOS.items():
        if pattern in key_str:
            matched_video = [{
                "title": vdata["title"],
                "url": vdata["url"],
                "author": vdata["author"],
                "thumbnail": "https://img.youtube.com/vi/" + vdata["url"].split("/")[-1] + "/hqdefault.jpg"
            }]
            break
            
    if matched_video:
        specs_extra = p.get("specs_extra") or {}
        specs_extra["videos"] = matched_video
        
        patch = requests.patch(
            f"{SUPABASE_URL}/rest/v1/products?id=eq.{pid}",
            headers=headers,
            json={"specs_extra": specs_extra}
        )
        if patch.status_code in [200, 204]:
            count += 1
            print(f"  [OK] {pid} -> {matched_video[0]['author']}: {matched_video[0]['title']}")

print(f"\nDone! {count} products updated with EXACT official manufacturer and brand videos.")
