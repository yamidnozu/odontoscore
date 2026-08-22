# Populate — Dental Affiliate Links → Scraped → Normalized → Enriched → Saved

This pipeline takes the user's Amazon dental affiliate links and turns each into a complete, clinically normalized record. The scraper is bundled in `scripts/amazon_extractor.py` (Scrapling + stealth browser).

**Golden rule of populate:** Scrape is FACTS, enrich is JUDGMENT, and the two never blur. A missing spec is `null` (never invented). An editorial score is explicitly labelled editorial.

---

## 1. Environment & Scraper Setup

The scraper utilizes **Scrapling** with stealth browser capabilities (Camoufox):

```bash
python -m pip install "scrapling[fetchers]"
scrapling install          # downloads stealth browser (one time)
```

Explain it in simple, non-technical terms: «voy a preparar la herramienta para extraer los datos de tus enlaces de productos dentales».

---

## 2. Input Contract & Affiliate Links

The user pastes their Amazon dental affiliate links (one per line):
- Short links: `https://amzn.to/3Dental1`
- Full URLs with tag: `https://www.amazon.es/dp/B089W4XKQY?tag=dentarank-es-21`

The pipeline expands short links, extracts the ASIN, and preserves the user's `affiliate_url` and `affiliate_tag` verbatim (invariant 1). If a pasted link lacks an affiliate tag, flag it immediately: «este enlace no tiene tu etiqueta de afiliado, ¿me pasas el enlace monetizado?».

---

## 3. Scrape Execution

```bash
python scripts/amazon_extractor.py "<enlace>" --download --out datos/raw/<asin>
```

The scraper extracts: title, brand, price, currency, rating, reviews count, hi-res image URLs, feature bullets, A+ dental marketing text, full technical spec tables, and verified buyer reviews.

### 3.1 Anti-Bot Protection & Location-Based Prices
1. **`google_search=True` is the default** — Sets Google search referer headers to bypass Amazon anti-bot screening. If an extraction fails, **retry 1–2 times with a short pause**.
2. **Visitor Country IP:** Amazon displays prices and stock availability based on the machine's geo-IP. The user running this locally in their target country gets accurate in-stock prices with zero proxy configuration required.

### 3.2 Dead Links & Delisted Products
If a link returns HTTP 404 / "Producto no disponible", log the dead ASIN and notify the user to provide an updated link. Never synthesize fake products.

---

## 4. Normalization (Raw Amazon Data → Dental Schema)

The raw `details` table from Amazon contains free text ("Presión: 10 a 100 psi", "Pulsaciones: 31.000 por minuto", "Cabezales: 4 boquillas incluidas").

The normalization step converts this into the dental schema (`04-product-schema.md`):
- `categoria_odontologica`: Determine the appropriate category (`cepillos_electricos`, `irrigadores_dentales`, `blanqueamiento_dental`, `ortodoncia_brackets`, `higiene_infantil`, `instrumental_basico`).
- `presion_agua_psi`: Extract numerical value (e.g. 100).
- `pulsaciones_min`: Extract frequency (e.g. 31000 or 1400).
- `modos_limpieza`: Integer count of distinct modes.
- `autonomia_dias` & `tiempo_carga_h`: Parse battery specs.
- `resistencia_ipx`: Map to "IPX7", "IPX8", etc.
- `indicado_para`: Array of clinical tags (e.g. `["brackets", "implantes", "encias_sensibles"]`).

---

## 5. Enrichment & Authoritative Sources

Amazon technical tables can be incomplete or omit key dental specifications (e.g., exact PSI, water pulse rate, noise decibels, or sterilization capabilities).

### Authoritative Verification Sources:
When Amazon data is missing or ambiguous, consult authoritative manufacturer and dental sources:
1. **Manufacturer Portals:**
   - [oral-b.es](https://www.oral-b.es) / [oralb.com](https://www.oralb.com) (iO microvibrations, modes, pressure sensors)
   - [philips.es/c-m-pe/cuidado-bucal](https://www.philips.es) / Sonicare (sonic movements/min, BrushSync)
   - [waterpik.es](https://www.waterpik.es) / [waterpik.com](https://www.waterpik.com) (exact PSI ranges, reservoir capacity ml, clinical trials)
   - [colgate.es](https://www.colgate.es) (whitening formulations, optical LED specs)
2. **Clinical Consensus & Dental Forums:**
   - Sociedad Española de Periodoncia (SEPA), American Dental Association (ADA) Seal of Acceptance databases, and specialized dental review literature.

*Rule:* If a spec is confirmed from the manufacturer's official page, add it to the record. If it cannot be verified anywhere, leave it as `null` ("—"). Never guess numbers.

---

## 6. Score Calculation & Clinical Editorial

1. **Calculate the 7 Radar Scores (0 to 10):**
   - `score_eficacia`
   - `score_comodidad_encias`
   - `score_durabilidad`
   - `score_facilidad_uso`
   - `score_silencio`
   - `score_tecnologia`
   - `score_calidad_precio`
   *Note:* Whenever new products are added to a category, recalculate scores across that category's min/max to maintain consistent comparison standards.
2. **Clinical Editorial & Review Summary:**
   - Generate high-quality ~300 words `cuerpo_editorial` explaining how the product performs, who it benefits, and its real-world handling.
   - Summarize user pros/cons and write the `ideal_para` clinical recommendation.
   - Generate the GEO "Preguntas para IA y Pacientes" block.

---

## 7. Save & Rebuild Site

1. Write the updated record to `datos/productos.json`.
2. Generate static fichas, updated category hubs, comparator tables, and `lib/db.js`.
3. Bump `?v=YYYYMMDD` cache-buster.
4. Report the result clearly to the user: N dental products processed, highlighted specs, any missing fields that returned `null`, and links added.
