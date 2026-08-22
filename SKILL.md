---
name: crear-web-afiliados-amazon
description: Build a data-driven Amazon affiliate website for Dental & Oral Health Products on Hostinger, guided end to end. (a) CONNECT the Hostinger account to Claude Code. (b) BUILD a premium clinical comparison/blog affiliate site for Dental Products (DentaRank Global): normalized oral health database and auto-generated pages with spec tables, 7-axis radar score panels, clinical editorial text, pros/cons, reviews, intra-category comparator, category hubs and buying guides. (c) POPULATE it - the user pastes their Amazon affiliate links, the bundled scraper extracts each product, and you normalize and enrich it into the database with manufacturer verification (Oral-B, Philips, Waterpik, Colgate). (d) PUBLISH it to Hostinger and add features on request. Use whenever the user wants an affiliate site, an Amazon comparison or blog site for dental products, or to add products from their affiliate links. Triggers include crea una web de afiliados, web de comparativas de odontologia, blog de salud dental, anade estos productos con mis enlaces, and their English equivalents.
---

# Affiliate Studio · Dental Edition | Proyecto: DentaRank Global (dentarank.global) — multi-marketplace y multi-idioma SEO+GEO

Four **independent capabilities** for building a **data-driven Amazon affiliate site for Dental & Oral Care Products**: not a flat list of product cards, but a clinical comparison engine where every product is a normalized record, and pages (fichas, intra-category comparators, category guides, radar charts) are **generated from that data**.

- 🔌 **Connect** the Hostinger account to Claude.
- 🏗️ **Build** the affiliate site: database schema + generated pages for dental categories (Cepillos Eléctricos, Irrigadores, Blanqueamiento, Ortodoncia/Brackets, Higiene Infantil, Instrumental Profesional).
- 📥 **Populate** it: affiliate links → scraped, normalized, enriched records with verified dental specs.
- 🚀 **Publish** it live to Hostinger (and add features on request).

**v2 — dental architecture & production rules:**
- The scraper sets **`google_search=True`** by default — beating Amazon's anti-bot. Retry blocked links 1–2×.
- **Prices/stock are per the shopper's country, requiring NO proxy:** run locally in the target country (`amazon.es`, `amazon.com.mx`, `amazon.com`). Details in `06-populate-pipeline.md`.
- **Multi-marketplace & i18n structure:** routing for `/es/`, `/es-mx/`, `/en/`, `/pt/` with `hreflang` and localized affiliate tag mapping.
- **GEO & AI Search blocks:** structured "Preguntas para IA y Pacientes" optimized for ChatGPT Search, Perplexity, and Gemini AI Overviews.
- **Build pages with a generator script** (`tools/build_site.py`) — one static HTML per record, core clinical facts baked in, JS enriches radar and comparator.
- **Bump the `?v=` cache-buster on every build**.

---

## THE GOLDEN RULE: do only what was asked, then stop

- *"conéctame Hostinger"* → only connect and verify.
- *"hazme una web de afiliados de productos de odontología"* → only build the site + empty database. Don't scrape, don't publish.
- *"añade estos productos: <links>"* → only populate (scrape → normalize → enrich → save). Don't redesign.
- *"publícala"* → only publish.

At the end offer **one** sentence naming the next step («¿la lleno con tus enlaces de afiliado de productos dentales?»). Never start it unprompted.

---

## Route the request → capability

| What they say / the situation | Capability | Primary ref |
|---|---|---|
| "conéctame Hostinger", "vincula mi hosting" | 🔌 **Connect** | `12-hostinger-connect.md` |
| "hazme una web de afiliados de odontología", no project yet | 🏗️ **Build** | `02` → `03` → `05` |
| "añade estos productos", pastes dental affiliate links | 📥 **Populate** | `06-populate-pipeline.md` |
| Project exists: "cambia…", "añade una feature", "otra sección" | ✏️ **Edit** | existing files + invariants |
| "publícala", "súbela" | 🚀 **Publish** | `13-hostinger-deploy.md` |
| "¿qué categoría dental me recomiendas?", "dame ideas" | 🎯 **Recommend** | `02-niche-and-architecture.md` |
| "no funciona", "se ve vieja", "el comparador falla" | ✅ **Verify** | `08`, `10`, `04` |

---

## The build → populate flow (the heart of this skill)

The data model comes first, pages are generated from it, and real data arrives from the user's affiliate links.

### 🏗️ Build (structure first, with 2-3 dental samples)
1. **Dental Schema (`04-product-schema.md`):** Commercial fields + Group C (8-15 dental specs: PSI, pulsations, cleaning modes, battery days, dB, IPX, sterilization, indications) + Group D (7-axis radar scores) + Group E (clinical editorial & GEO Q&A).
2. **Data Store (`03-data-store.md`):** Static `datos/productos.json` + `lib/db.js` (`window.__DB__`).
3. **Generate Pages (`05-pages-and-features.md`):** Home with clinical authority (White `#FFFFFF` + Trust Blue `#0E76BC` + Inter/Sora), category hubs, generated product fichas, intra-category comparator, buying guides ("Mejor irrigador para brackets 2026"), deals, and legal/medical disclosures.
4. **Initialize with 2-3 sample products:** Oral-B iO Series 9, Waterpik WP-660EU, Philips Sonicare 9900 Prestige, clearly marked as samples.

### 📥 Populate (data arrives from affiliate links)
`06-populate-pipeline.md` full recipe:
1. User pastes their Amazon affiliate links (short `amzn.to` or full tagged URLs).
2. `scripts/amazon_extractor.py` scrapes title, brand, price, rating, reviews, hi-res images, specs, bullets, and reviews.
3. **Normalize + Enrich:** Map specs into typed dental fields, verify missing specs against manufacturer portals (Oral-B, Philips, Waterpik, Colgate), compute 7-axis radar scores, write clinical editorial and GEO AI blocks.
4. Save to `datos/productos.json` and regenerate pages.

### 🚀 Publish & extend
Deploy per `13-hostinger-deploy.md`.

---

## Always-on invariants

**Communication:** The user is non-technical. Speak clearly: "extraigo los datos de tus enlaces", "la ficha técnica dental de cada producto", "la base de datos de tu tienda".

**Affiliate & Clinical invariants:**
1. **The affiliate link is sacred.** Preserve the user's exact affiliate URL and tag on every product; every «Ver en Amazon» button uses it. Never strip or rewrite tags.
2. **Data first, pages second.** Every product page, comparator row, and chart reads from the normalized database.
3. **Normalize everything.** Raw text ("10-100 psi", "31.000 oscilaciones") maps to typed numbers and canonical units.
4. **Never invent specs or reviews.** If a spec is unverified, store `null` ("—"). Never synthesize clinical or pressure numbers.
5. **Affiliate disclosure & medical disclaimer are legally required.** Visible on every page (Amazon Associates disclosure + notice that content is informational and does not replace dental professional diagnosis).
6. **Prices are snapshots.** Label as "precio orientativo, consúltalo en Amazon" with the capture date.

**Web quality invariants:**
Classic `<script defer>` + IIFE + `window.__DB__`; `.htaccess` + `?v=YYYYMMDD`; native smooth scroll; clinical design token system; content hardcoded in HTML for zero-JS SEO and fast paint; console clean; preview over HTTP.

---

## Files index

```
SKILL.md                              ← this file — router + dental build/populate flow
intake-template.md                    ← the few questions for fresh dental builds
recommended-settings.json             ← optional zero-prompt pre-authorization
evals/evals.json                      ← capability-routing evals for dental niche
reference/
  01-stack-and-conventions.md         ← file structure, IIFE, ESM bridge (shared)
  02-niche-and-architecture.md        ← dental niche, categories, i18n, SEO + GEO
  03-data-store.md                    ← JSON vs PHP+SQLite; window.__DB__
  04-product-schema.md                ← normalized dental schema (8-15 specs, 7 radar axes)
  04-critical-gotchas.md              ← web invariants & production gotchas
  05-pages-and-features.md            ← home E-E-A-T, dental fichas, intra-category comparator, guides
  06-populate-pipeline.md             ← links → scrape → normalize → enrich (Oral-B, Waterpik, Philips)
  14-mapa-autonomia.md                ← optional visual features
  03-effects-catalog.md               ← copy-paste UI effects
  07..10, 12, 13                      ← troubleshooting, checklist, deploy, connect
templates/
  htaccess.template                   ← copy as .htaccess to project root
  producto.schema.json                ← dental schema contract
  ficha.example.html                  ← reference dental product ficha structure
scripts/
  amazon_extractor.py                 ← scraper (Scrapling + stealth browser)
  descargar-librerias.py              ← vendor libraries
  diagnostico.ps1 / .sh               ← environment diagnostics
  verify_project.py                   ← post-generation verification
```
