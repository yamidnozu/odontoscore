# Pages & Features — DentaRank Global (Odontología)

Every page is a **view over `window.__DB__`**. No dental product is hand-written.
This file specifies each page, design system, and the signature dental features (intra-category comparator, 7-axis clinical radar, dental spec table, AI answer blocks) built from normalized data.

Rendering pattern: HTML ships the page shell + SEO/GEO/legal text (works with JS off); `main.js` (IIFE) reads `window.__DB__` and mounts the data-driven components (`04-critical-gotchas.md` D.3 — idempotent mounts, `safe()` wrappers).

---

## Visual Design & Aesthetics (Clinical Authority E-E-A-T)

Dental and healthcare purchasing demands immediate clinical trust, hygiene, precision, and modern aesthetics:

- **Color Palette:**
  - Background: Clean White (`#FFFFFF`) & Medical Soft Surface (`#F8FAFC`)
  - Primary / Trust Blue: `#0E76BC` (Professional Dental Blue)
  - Dark Slate / Medical Navy: `#0F172A` (High contrast typography)
  - Accent / Mint Clean: `#0EA5E9` / `#10B981` (Badges & positive indicators)
  - Border & Dividers: `#E2E8F0` (Crisp, subtle clinical structure)
- **Typography:**
  - Primary / UI: **Inter** (400, 500, 600, 700) for scannable data and technical specs.
  - Headings / Editorial: **Sora** (600, 700) for authority, clinical headlines, and hero presence.
- **Card & Component Styles:**
  - Modern subtle shadows, crisp 1px borders, refined micro-interactions, radar overlays, and high-visibility CTAs.

---

## 1. The Ficha (Dental Product Page)

Top to bottom structure for each generated product page:

1. **Gallery** — Local WebP images (`assets/img/<id>-N.webp`), main view with zoom/lightbox + thumbnail selector.
2. **Header & Buy Box** — Marca, product name, star rating with review count, price with discount tag and «precio orientativo · fecha de captura» notice (invariant 6). Prominent **«Ver precio en Amazon»** button using the sacred `affiliate_url` (invariant 1).
3. **Clinical Radar Chart (7 axes)** — 0-10 polygon (Eficacia, Comodidad de Encías, Durabilidad, Facilidad de Uso, Silencio, Tecnología, Calidad/Precio) labelled "Evaluación Editorial DentaRank".
4. **Dental Spec Table** — Group C specs formatted with units (tecnología, modos de limpieza, presión PSI, capacidad depósito, pulsaciones/min, autonomía, nivel de ruido dB, resistencia IPX, app/sensores, esterilización, material, etc.) with `null` shown as "—". Includes `specs_extra` in an expandable "Especificaciones adicionales" block.
5. **Editorial Analysis (~300 words)** — `cuerpo_editorial`: rigorous clinical editorial explaining mechanism of action, clinical indications, and user experience.
6. **Pros / Contras & Ideal Para** — Two-column clinical pros/cons followed by a highlighted `ideal_para` badge (e.g. "Recomendado para pacientes con brackets o encías propensas a gingivitis").
7. **Resumen de Reseñas de Pacientes** — `resenas_resumen` + real verified Amazon user opinions categorized by sentiment.
8. **Bloque GEO "Preguntas para IA y Pacientes"** — Direct Q&A format optimized for generative AI citation and search engines.
9. **Comparar & Alternativas** — Intra-category recommendation strip and «Añadir al comparador» button.
10. **Repetición de CTA «Ver en Amazon»** + **Aviso de Afiliados y Descargo Médico** (invariant 5).

Structured data: JSON-LD `Product` (real scraped ratings and offers) + `FAQPage` (clinical Q&As).

---

## 2. The Comparator (Intra-Category Dental Engine)

Users comparing a water flosser should not compare it against a whitening kit. The comparator strictly enforces **intra-category comparison**:

- **Selection:** Compare 2 to 4 products of the same `categoria_odontologica` (e.g. 3 Irrigadores Dentales or 3 Cepillos Sónicos).
- **Side-by-Side Dental Specs:**
  - Direct comparison of PSI, pulsation frequency, water tank ml, cleaning modes, decibels, battery life, and included tips.
  - Automatic best-in-row highlighting (e.g., lower noise in dB = green; higher water pressure or pulsation = green).
- **Multi-Product Radar Overlay:** Overlaid polygons in distinctive clinical colors (Trust Blue, Emerald Green, Indigo, Amber) for an instant visual comparison of the 7 axes.
- **Dedicated Affiliate CTAs:** Each column features its direct «Ver en Amazon» button with its respective tracking tag.
- **Shareable Deep-Links:** State reflected in URL hash (e.g., `/comparador.html#cat=irrigadores&ids=dent-002,dent-003`).

---

## 3. Home (Authority & E-E-A-T Portal)

- **Hero:** Authority headline (e.g. "DentaRank — Comparativas y Análisis Técnico de Higiene Bucodental"), value proposition, search bar, and direct category shortcuts.
- **Top Picks by Category:** Quick access cards for "Mejor Cepillo Eléctrico", "Mejor Irrigador Calidad-Precio", "Mejor para Brackets / Ortodoncia".
- **"Cómo Evaluamos" Trust Section:** Clear explanation of evaluation criteria (clinical efficacy, gum protection, noise tests, build quality, independent data).
- **Latest Editorial Guides & Deals Strip:** Featured buying guides and active discounts.

---

## 4. Category Pages (Silo Hubs)

Dedicated category pages:
1. `/categoria/cepillos-electricos.html`
2. `/categoria/irrigadores-dentales.html`
3. `/categoria/blanqueamiento-dental.html`
4. `/categoria/ortodoncia-brackets.html`
5. `/categoria/higiene-infantil.html`
6. `/categoria/instrumental-basico.html`

Each category page includes an introductory guide, category-specific filters (e.g. Filter by Sónico vs Rotatorio, Filter by PSI, Filter by Indicado Para: Brackets/Implantes), and a sortable product grid.

---

## 5. Buying Guides & Editorial Rankings (SEO + GEO Engine)

- Guides: "Mejor irrigador dental para brackets 2026", "Guía definitiva: Cepillos sónicos vs rotatorios", "Kits de blanqueamiento seguros para el esmalte".
- Content: Comprehensive clinical context + structured comparison tables + direct links to product fichas and buy buttons.
- Semantic Schema: `FAQPage` and `ItemList` JSON-LD on all guide pages.

---

## 6. Generator: Static Site Generation (`tools/build_site.py`)

No runtime server dependencies or heavy framework required. A lightweight Python script builds the full static site:

1. Reads `datos/productos.json`.
2. Generates **one static HTML file per record** (e.g., `/producto/dent-oral-b-io-9.html`) with all facts baked into the HTML for instant load, zero-JS accessibility, and optimal SEO.
3. Generates all category pages, intra-category comparator shell, buying guides, ofertas, and legal disclosures.
4. Generates `lib/db.js` (`window.__DB__ = { productos: [...], meta: {...} }`).
5. Injects `?v=YYYYMMDD` cache-buster across all stylesheet and script references.

---

## Definition of Done (Pages)

- [ ] All pages generated strictly from normalized dental data (`productos.json`).
- [ ] Intra-category comparator compares dental specs side by side with multi-radar overlay.
- [ ] Ficha contains complete dental spec table, 7-axis radar, ~300 words clinical editorial, pros/contras, and GEO Q&A block.
- [ ] Palette adheres to Medical White (`#FFFFFF`) + Trust Blue (`#0E76BC`) + Dark Slate (`#0F172A`) with Inter & Sora typography.
- [ ] Affiliate links are sacred and preserved across all buttons.
- [ ] Amazon affiliate disclosure and medical advisory present on every footer and legal page.
- [ ] Valid JSON-LD `Product`, `FAQPage`, and `ItemList` schemas.
