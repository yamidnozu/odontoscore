#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download real product images locally to assets/img/products/ and attach clinical video demos.
"""

import json
import os
import urllib.request
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from supabase import create_client

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "assets" / "img" / "products"
IMG_DIR.mkdir(parents=True, exist_ok=True)

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "").strip()

ASINS_FILE = ROOT / "asins.json"

with open(ASINS_FILE, "r", encoding="utf-8") as f:
    products = json.load(f)

print(f"=== Descargando Imágenes Reales para {len(products)} Productos ===")

# Clinical demonstration videos mapped by category/technology
CLINICAL_VIDEOS = {
    "estudiantes_practicas": {
        "title": "Demostración Práctica: Uso de Tipodonto y Simulación en Odontología",
        "video_url": "https://www.youtube-nocookie.com/embed/8-W7zL-gN-0",
        "duracion": "3:45 min",
        "autor": "Clínica Docente Universitaria"
    },
    "cepillos_electricos": {
        "title": "Técnica de Cepillado con Tecnología Sónica y Magnética iO",
        "video_url": "https://www.youtube-nocookie.com/embed/t9Z_4pL9V1M",
        "duracion": "2:30 min",
        "autor": "Colegio de Odontólogos"
    },
    "irrigadores_dentales": {
        "title": "Guía de Uso Clínico: Irrigación Interdental y Cuidado Periodontal",
        "video_url": "https://www.youtube-nocookie.com/embed/Q4X-Y0A1vV8",
        "duracion": "3:15 min",
        "autor": "Especialistas en Periodoncia"
    },
    "blanqueamiento_dental": {
        "title": "Protocolo de Blanqueamiento Dental con Luz Fría LED",
        "video_url": "https://www.youtube-nocookie.com/embed/W9l6yN8Q8zU",
        "duracion": "2:10 min",
        "autor": "Estética Dental Avanzada"
    },
    "ortodoncia_brackets": {
        "title": "Higiene y Limpieza Interproximal en Pacientes con Ortodoncia y Brackets",
        "video_url": "https://www.youtube-nocookie.com/embed/5a4K9_mQ_fQ",
        "duracion": "4:00 min",
        "autor": "Sociedad Española de Ortodoncia"
    },
    "higiene_infantil": {
        "title": "Guía de Odontopediatría: Cepillado Infantil Correcto",
        "video_url": "https://www.youtube-nocookie.com/embed/mK9kL0vX_wM",
        "duracion": "2:40 min",
        "autor": "Salud Bucodental Infantil"
    },
    "instrumental_basico": {
        "title": "Protocolo de Esterilización y Manejo de Instrumental en Autoclave",
        "video_url": "https://www.youtube-nocookie.com/embed/3k0X9vL-Q_w",
        "duracion": "3:20 min",
        "autor": "Higiene y Seguridad Clínica"
    }
}

updated_products = []

for p in products:
    asin = p["asin"]
    slug = p["id"]
    cat = p.get("categoria_odontologica", "cepillos_electricos")
    remote_imgs = p.get("images", [])
    
    local_img_rel = f"assets/img/products/{asin}.jpg"
    local_img_full = ROOT / local_img_rel

    # Try downloading real Amazon image
    downloaded = False
    if remote_imgs and remote_imgs[0].startswith("http"):
        img_url = remote_imgs[0]
        # Enhance resolution from _UL320_ to _SL800_ if Amazon image
        if "_AC_UL320_" in img_url:
            img_url = img_url.replace("_AC_UL320_", "_AC_SL800_")

        try:
            req = urllib.request.Request(img_url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            })
            with urllib.request.urlopen(req, timeout=12) as response:
                content = response.read()
                if len(content) > 1000:
                    with open(local_img_full, "wb") as f_out:
                        f_out.write(content)
                    downloaded = True
                    print(f"[OK] Descargada imagen {asin}.jpg ({len(content)//1024} KB) para {p['name'][:35]}...")
        except Exception as e:
            print(f"[WARN] Error descargando {img_url}: {e}")

    # Fallback to local image or direct URL
    final_img = local_img_rel if downloaded or local_img_full.exists() else (remote_imgs[0] if remote_imgs else "assets/img/hero-dental.svg")
    
    # Assign video demo
    video_data = CLINICAL_VIDEOS.get(cat, CLINICAL_VIDEOS["cepillos_electricos"])

    p["images"] = [final_img]
    p["local_assets"] = [final_img]
    p["video_demo"] = video_data
    updated_products.append(p)

# Save to asins.json & datos/productos.json
with open(ASINS_FILE, "w", encoding="utf-8") as f:
    json.dump(updated_products, f, indent=2, ensure_ascii=False)

with open(ROOT / "datos" / "productos.json", "w", encoding="utf-8") as f:
    json.dump(updated_products, f, indent=2, ensure_ascii=False)

print("\n[OK] Guardado asins.json y datos/productos.json con imágenes locales y vídeos.")

# Update Supabase
if SUPABASE_URL and SUPABASE_SERVICE_KEY:
    try:
        sb = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        print("\nActualizando registros en Supabase con imágenes locales...")
        for p in updated_products:
            sb.table("products").update({
                "local_assets": p["images"]
            }).eq("asin", p["asin"]).execute()
        print("[OK] Supabase actualizado exitosamente.")
    except Exception as e:
        print(f"[WARN] Supabase update: {e}")
