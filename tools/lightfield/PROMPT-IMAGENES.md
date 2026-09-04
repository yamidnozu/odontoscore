# Prompts reutilizables: cualquier objeto aislado

Sustituye `[OBJETO]`, `[RASGOS FIJOS]` y `[ESTILO]`. Ejemplos: una zapatilla, un fósil, una figura, un automóvil, un órgano ilustrado o una pieza mecánica. Usa un único ejemplar estático, no un tema abstracto, una escena cambiante ni varios objetos independientes.

Estos prompts buscan coherencia visual, no garantizan geometría exacta. Los ángulos son objetivos de generación. Hay que revisar las imágenes antes de codificarlas.

## 1. Crear la referencia maestra

Si tienes fotografías del mismo objeto desde distintos lados, adjúntalas en vez de inventar una identidad nueva. Una sola referencia no describe sus caras ocultas.

```text
Create a master visual reference of ONE specific [OBJETO].
Style: [ESTILO]. Fixed identity features: [RASGOS FIJOS].
Show the whole object upright in a neutral, almost orthographic front three-quarter view, large but fully inside the frame. Pure white opaque background #FFFFFF. Soft diffuse studio lighting, enough surface shading to reveal form, no cast shadow, no floor, no environment, no text, no labels, no grid, no border, no extra objects. PNG.
Choose a coherent, physically plausible construction. Keep visible distinguishing features easy to recognize so the same specimen can be followed through subsequent views. Do not add a decorative marker or watermark.
This image will serve as the identity reference for a multi-view sheet. Do not generate the multi-view sheet yet.
```

Guarda la referencia. Adjunta esta misma imagen a las siguientes generaciones. No te limites a decir «el mismo de antes» si el generador no conserva la referencia.

## 2. Generar primero las seis vistas neutras

Usa el siguiente prompt con `[ELEVACION]=0`. Adjunta la referencia maestra. Esta primera lámina sirve también como referencia para las seis siguientes.

## 3. Prompt de cada lámina de seis vistas

Repite este prompt una vez por elevación de la tabla. Adjunta siempre la referencia maestra y, una vez disponible, la lámina neutra aprobada. No uses únicamente la última imagen generada como referencia: acumularía cambios de identidad.

```text
Generate ONE clean multi-view PNG sheet of the EXACT SAME [OBJETO] shown in the attached reference images.
Style: [ESTILO]. Mandatory fixed identity: [RASGOS FIJOS].
The first reference defines appearance. The approved neutral six-view sheet, when attached, defines the same specimen's front, sides and back. Preserve its proportions, construction, colors, topology, asymmetries and recognizable surface details. Do not redesign it between cells.

LAYOUT
Exactly 3 columns × 2 rows = SIX views, row-major order. Target canvas 1536×1024 pixels, six equal 512×512 square cells; if that size is unavailable, keep the exact 3:2 canvas ratio and equal square cells. No gutters, visible grid, labels, borders, captions or external margin around the sheet.
Each cell contains exactly one complete object, centered on the same stable pivot, with a pure white background #FFFFFF. Keep at least 12% clear white margin inside every cell. Nothing may touch or cross a cell boundary. Same orthographic camera scale throughout: no automatic enlargement of narrower views. No cropping.

CAMERA AND ORDER
The object's front is azimuth 0°. Its top remains upright in world coordinates. Positive azimuth orbits the camera from the front toward the object's own right side, then behind, then toward its left side. Do not mirror images to fake reverse views.
All six views use the SAME camera elevation: [ELEVACION] degrees above the horizontal plane. Positive means looking downward from above; negative means looking upward from below. Camera always looks at the same object center, with zero roll; no floor may hide the underside.
Top row, left to right: azimuth 0°, 60°, 120°.
Bottom row, left to right: azimuth 180°, 240°, 300°.
Only camera position changes. Keep the object rigid and identical. Use near-orthographic projection and consistent soft diffuse illumination. Retain natural surface shading; omit cast shadows and environment.

CONSISTENCY CHECK
Verify six complete separate silhouettes; correct viewpoint order; coherent front/back and left/right relationships; unchanged part count and connections; believable visibility and occlusion; identical materials; no pose changes, added parts or missing parts. A feature must disappear when the object's body occludes it, not remain pasted onto every face. Do not render six copies of the same view.
Check the approved references before final output. If a specified angle or hidden structure cannot be maintained reliably, state that limitation instead of claiming verified exact consistency.
Return only this six-view PNG sheet, not a viewer, contact-sheet mockup or software screenshot.
```

## 4. Archivos y orden del atlas

Genera primero la elevación 0 y después las restantes. Guarda cada resultado con el nombre correspondiente:

| Elevación solicitada | Nombre en source/views/ | Fila final del atlas |
| --- | --- | --- |
| +60° | elevation_p60.png | 1 |
| +40° | elevation_p40.png | 2 |
| +20° | elevation_p20.png | 3 |
| 0° | elevation_p0.png | 4 |
| −20° | elevation_m20.png | 5 |
| −40° | elevation_m40.png | 6 |
| −60° | elevation_m60.png | 7 |

Cada fila final conserva las seis columnas 0°, 60°, 120°, 180°, 240°, 300°. No coloques una vista cenital aislada entre filas laterales: la mezcla del visor produciría superposiciones bruscas.

## 5. Revisión antes de usar

- Revisa detalles asimétricos: ¿pertenecen al mismo objeto y aparecen en el lado correcto?
- Compara filas consecutivas en la misma columna: la elevación debe cambiar gradualmente, sin saltos de escala, forma o centro.
- Revisa que las vistas traseras sean realmente traseras y no frontales repetidas.
- Rechaza láminas con piezas cortadas, otras piezas entrando desde los bordes o cambios estructurales. Regenera la lámina defectuosa adjuntando otra vez las referencias aprobadas.
- Tras ensamblar, inspecciona `source/atlas.png`. El recorte automático puede equivocarse con materiales transparentes o componentes desconectados.
- No le pidas al generador que cree directamente `lightfield_encoded.png`: la distribución exacta de sus píxeles la calcula `source/encode.py`.

## 6. Convertir y abrir

Con las dependencias del README instaladas, ejecuta desde la raíz del proyecto:

```sh
python source/assemble_rows.py source/views.json
python source/encode.py
npm run build
```

Abre `dist/index.html`. Cambiar las imágenes fuente sin ejecutar estos pasos no cambia la PNG incrustada en el visor.
