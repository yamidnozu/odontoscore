---
name: crear-web-afiliados-amazon
description: Build and maintain a data-driven Amazon affiliate website for Dental & Oral Health Products on Hostinger, connected to Supabase and Amazon PA-API 5.0. (a) SYNC with Amazon PA-API 5.0 / Rainforest fallback into Supabase. (b) BUILD static pages with 7-axis clinical radar charts, intra-category comparators, spec tables, and SEO/GEO blocks. (c) POPULATE new ASINs legally without scraping. (d) PUBLISH / Deploy live to Hostinger.
---

# Affiliate Studio · Dental Edition | Proyecto: DentaRank Global (dentarank.global / odontoscore.com)

Four **independent capabilities** for maintaining a high-performance **Amazon Affiliate Dental Comparison & Authority Platform**:

- 🔄 **Sync** (`tools/sync_supabase.py`): Amazon PA-API 5.0 (with Rainforest API fallback) → Supabase (Source of Truth) → Local Cache (`datos/productos.json`, `lib/db.js`).
- 🏗️ **Build** (`tools/build_site.py`): Supabase / JSON Cache → Baked HTML pages (Home, Fichas, Intra-Category Comparator, Category Hubs, Buying Guides, Deals, Legal/Medical Disclaimers, Sitemaps).
- 📥 **Populate** (`asins.json` & Supabase): Add new dental ASINs to the database and enrich clinical specs (Groups C, D, E).
- 🚀 **Publish** (`hosting_deployStaticWebsite` / GitHub Actions): Deploy static bundle to Hostinger via API or automated FTP every 6h.

---

## Data Pipeline: Supabase + PA-API 5.0 + Hybrid Live Refresh

```
                                  ┌────────────────────────┐
                                  │   Amazon PA-API 5.0    │
                                  │  (Rainforest Fallback) │
                                  └───────────┬────────────┘
                                              │ (every 6h or manual)
                                              ▼
┌──────────────────────┐          ┌────────────────────────┐
│     asins.json       ├─────────►│  tools/sync_supabase.py│
└──────────────────────┘          └───────────┬────────────┘
                                              │ (UPSERT Group B + Price History)
                                              ▼
                                  ┌────────────────────────┐
                                  │   Supabase Database    │◄───────┐ (Client live refresh)
                                  │   (Source of Truth)    │        │
                                  └───────────┬────────────┘        │
                                              │                     │
                                              ▼                     │
                                  ┌────────────────────────┐        │
                                  │  datos/productos.json  │        │
                                  │      lib/db.js         │        │
                                  └───────────┬────────────┘        │
                                              │                     │
                                              ▼                     │
                                  ┌────────────────────────┐        │
                                  │  tools/build_site.py   │        │
                                  └───────────┬────────────┘        │
                                              │ (SSG Build)         │
                                              ▼                     │
                                  ┌────────────────────────┐        │
                                  │ Static HTML / Hostinger│────────┘
                                  │  (main.js with fade)   │
                                  └────────────────────────┘
```

---

## 🚫 Critical Policy: No Direct Scraping

- **Prohibición de Scrapers:** Prohibido el uso de scraping directo o navegadores automatizados contra Amazon (`scripts/amazon_extractor.py` eliminado).
- **Cumplimiento Legal:** Todas las consultas de precio, stock y metadatos se realizan a través de la **Amazon Product Advertising API (PA-API 5.0)** oficial o de **Rainforest API** como fallback de transición.

---

## Always-On Invariants

1. **The Affiliate Tag is Sacred:** El tag oficial es `odontoscore-21`. Todos los enlaces `affiliate_url` y botones de compra redirigen con este tag.
2. **Data First, Pages Second:** Ninguna ficha ni producto se escribe a mano en HTML. Se gestiona en Supabase / `asins.json` y se compila con `tools/build_site.py`.
3. **No Invented Specs:** Todo dato no confirmado permanece como `null` ("—").
4. **Clinical Disclaimer & Disclosure:** Aviso de Afiliados de Amazon y Descargo Médico presentes en todos los pies de página y fichas.
5. **Zero-JS Fallback & High Performance:** El contenido base y los precios se hornean en el HTML estático para máxima velocidad y SEO, mientras que `main.js` actualiza en vivo con Supabase REST sin romper la navegación.

---

## Comandos Principales

```bash
# 1. Sincronizar precios desde PA-API hacia Supabase y regenerar caché local
python tools/sync_supabase.py

# 2. Modo prueba sin escribir en Supabase
python tools/sync_supabase.py --dry-run

# 3. Compilar el sitio estático completo
python tools/build_site.py

# 4. Probar en servidor local
python -m http.server 8000
```
