# The Dental Product Schema — normalize everything

Every dental product is a **typed, normalized record**.
Messy Amazon text in, comparable oral health specs out. Pages, intra-category comparators, radar charts, and AI search engines read these fields. If a value isn't normalized here, it cannot be compared or evaluated.

---

## The five field groups (Dental Schema)

| Group | Purpose | Per-niche? |
|---|---|---|
| **A. Identity & affiliate** | what it is + multi-marketplace earning | same structure, dental fields |
| **B. Commercial** | price snapshot, offers, stars, reviews | same for all niches |
| **C. Technical specs** | dental clinical & mechanical specs | **dental-specific (8-15 specs)** |
| **D. Comparison scores** | 0-10 radar chart axes | **dental-specific (7 axes)** |
| **E. Editorial & Clinical** | expert analysis, pros/cons, indications | dental-specific clinical content |

---

## Group A — Identity & Affiliate (Load-bearing, never fake)

```json
"id":            "dent-001",
"asin":          "B089W4XKQY",
"name":          "Oral-B iO Series 9 Cepillo Eléctrico Recargable",
"marca":         "Oral-B",
"categoria_odontologica": "cepillos_electricos", // enum
"affiliate_url": "https://amzn.to/4gDental1",    // User's link VERBATIM (sacred)
"affiliate_tag": "dentarank-es-21",              // User's tag preserved
"canonical_url": "https://www.amazon.es/dp/B089W4XKQY",
"images":        ["assets/img/dent-001-1.webp", "assets/img/dent-001-2.webp"],
"category":      "Cepillos Eléctricos",
"isFeatured":    true,
"showInTopMenu": true
```

*Invariants:* `affiliate_url` and `affiliate_tag` are sacred. Buy buttons directly bind to `affiliate_url`.

---

## Group B — Commercial (Snapshot with date)

```json
"retailPrice":      279.99,
"discountedPrice":  199.95,
"rango_precio":     "premium",      // economico | medio | alto | premium
"valoracion_media": 4.6,            // Amazon stars
"resenas_cantidad": 4520,
"precio_fecha":     "2026-08-22"    // capture date (prices go stale)
```

---

## Group C — Technical Dental Specs (The Clinical Engine)

Every spec is typed with its canonical unit. Unmapped attributes go to `specs_extra`.

```json
"categoria_odontologica":   "cepillos_electricos", // cepillos_electricos | irrigadores_dentales | blanqueamiento_dental | ortodoncia_brackets | higiene_infantil | instrumental_basico
"tipo_producto":            "cepillo_electrico_magnetico",
"tecnologia":               "rotatorio",          // sonico | rotatorio | irrigador | led
"modos_limpieza":           7,                    // número de modos (Limpieza Diaria, Sensible, Blanqueamiento, etc.)
"presion_agua_psi":         null,                 // psi (para irrigadores, ej. 10-100)
"capacidad_deposito_ml":    null,                 // ml (para irrigadores, ej. 600)
"pulsaciones_min":          17400,                // oscilaciones / pulsaciones por minuto
"autonomia_dias":           14,                   // días de autonomía con 2 usos/día
"tiempo_carga_h":           3.0,                  // horas para carga completa (magnética rápida)
"cabezales_incluidos":      1,                    // número de cabezales/boquillas en caja
"nivel_ruido_db":           58,                   // decibelios (nivel sonoro en operación)
"resistencia_ipx":          "IPX7",               // resistencia al agua
"app_conectada":            true,                 // Bluetooth + IA de seguimiento de cepillado
"material":                 "Polímero médico libre de BPA",
"esterilizable_autoclave":  false,                // true para instrumental profesional
"indicado_para":            ["encias_sensibles", "implantes", "blanqueamiento"], // [brackets, implantes, encias_sensibles, ninios, ortodoncia]
"specs_extra": {
  "Sensor de presión": "Inteligente 360° (rojo/blanco/verde)",
  "Pantalla": "Interactiva a color OLED",
  "Frecuencia vibración": "Microvibraciones magnéticas iO"
}
```

### Spec Normalization Rules:
- **`categoria_odontologica`**: Enum obligatorio que controla la compatibilidad del comparador.
- **`presion_agua_psi`**: En irrigadores, rango máximo en PSI (ej. 100 PSI en sobremesa, 75 PSI en portátiles).
- **`pulsaciones_min`**: En cepillos sónicos (31.000 - 62.000 mov/min) o irrigadores (1.200 - 1.700 pulso/min).
- **`indicado_para`**: Array de etiquetas estandarizadas que alimentan los filtros clínicos y guías temáticas.
- **`null`**: Si el dato no está disponible ni en Amazon ni en la web oficial del fabricante, se guarda `null` (la UI muestra "—"). Jamás inventar.

---

## Group D — Comparison Radar Scores (0 to 10)

Calculated during the enrichment step, providing the 7 visual axes for the radar chart and side-by-side comparison.

```json
"score_eficacia":          9.5,
"score_comodidad_encias":  9.0,
"score_durabilidad":       8.5,
"score_facilidad_uso":     8.8,
"score_silencio":          8.0,
"score_tecnologia":        9.8,
"score_calidad_precio":    7.5
```

### How each score is calculated:

1. **`score_eficacia` (Eficacia en Remoción de Placa / Limpieza):**
   - *De:* `pulsaciones_min` + `presion_agua_psi` + `tecnologia` + `modos_limpieza`.
   - Cepillos sónicos de >31.000 mov/min o magnéticos iO y pulsaciones de irrigador >1.400 pulso/min obtienen base 8.5-10.
2. **`score_comodidad_encias` (Protección Gingival y Confort):**
   - *De:* Sensor de presión + modos específicos para encías/sensible + boquillas periodontales + material ultrasuave.
   - Puntuación máxima si incluye sensor luminoso de sobrepresión y modo ultrasensible.
3. **`score_durabilidad` (Calidad de Construcción y Resistencia):**
   - *De:* `resistencia_ipx` (IPX7 = +2), batería de Litio vs NiMH, `material` médico, garantía oficial de marca reputada.
4. **`score_facilidad_uso` (Ergonomía, Recarga y Mantenimiento):**
   - *De:* `autonomia_dias` (>14 días = +3), `tiempo_carga_h` (<4h = +2), peso equilibrado, facilidad de llenado de depósito o cambio de cabezales.
5. **`score_silencio` (Nivel Acústico en Decibelios):**
   - *De:* `nivel_ruido_db`.
   - <55 dB = 9.5-10 | 55-65 dB = 8-9 | 66-75 dB = 6-7 | >75 dB (compresores antiguos) = <5.
6. **`score_tecnologia` (Innovación, Sensores y Conectividad):**
   - *De:* `app_conectada` (Bluetooth/IA) + pantalla interactiva + microvibraciones + temporizador por cuadrantes.
7. **`score_calidad_precio` (Valor por Euro invertido):**
   - *De:* Relación entre specs clínicas (`eficacia` + `durabilidad` + `cabezales_incluidos`) frente al `discountedPrice`.

*Nota:* Los scores son relativos a la categoría del producto (un irrigador portátil se evalúa contra irrigadores, no contra lámparas de polimerizar).

---

## Group E — Editorial & Clinical Copy

```json
"description":         "El Oral-B iO Series 9 combina tecnología magnética de microvibraciones con un cabezal redondo de inspiración profesional y seguimiento 3D por IA.",
"cuerpo_editorial":    "<p>El Oral-B iO Series 9 representa la cúspide de la tecnología de higiene bucodental doméstica...</p>",
"pros": [
  "Tecnología magnética iO con limpieza suave y profunda",
  "Sensor de presión inteligente que alerta si cepillas muy fuerte o suave",
  "Seguimiento 3D de 16 zonas con inteligencia artificial",
  "Cargador magnético rápido (3 horas)"
],
"contras": [
  "Precio elevado en comparación con gamas tradicionales",
  "Los recambios de cabezales iO tienen un coste superior"
],
"ideal_para":          "Pacientes exigentes que buscan máxima salud gingival, personas con implantes o manchas dentales que desean guía precisa por IA.",
"destacado_editorial": "La mejor tecnología de cepillado eléctrico del mercado según valoraciones clínicas.",
"resenas_resumen":     "Los usuarios destacan la sensación de limpieza profesional similar a una profilaxis en clínica y la suavidad en encías sensibles."
```

---

## Designing for a New Sub-Category or Multi-Marketplace

1. Scrape 2-3 sample products (Oral-B iO, Waterpik WP-660EU, Philips Sonicare 9900 Prestige).
2. Extract clinical and technical specs to Group C.
3. Compute Group D radar scores across the category min/max.
4. Keep A, B, E in standard format.
