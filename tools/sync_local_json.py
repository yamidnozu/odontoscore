import json
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

env_path = Path("c:/Proyectos/bussiness/store-odontologia/.env")
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://lgaolwxeizxynkpcjsse.supabase.co")
ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

r = requests.get(f"{SUPABASE_URL}/rest/v1/products?select=*", headers={"apikey": ANON_KEY, "Authorization": f"Bearer {ANON_KEY}"})
products = r.json()

ROOT = Path("c:/Proyectos/bussiness/store-odontologia")
with open(ROOT / "asins.json", "w", encoding="utf-8") as f:
    json.dump(products, f, indent=2, ensure_ascii=False)

with open(ROOT / "datos" / "productos.json", "w", encoding="utf-8") as f:
    json.dump(products, f, indent=2, ensure_ascii=False)

print(f"Synced {len(products)} products with exact official videos to local JSON files.")
