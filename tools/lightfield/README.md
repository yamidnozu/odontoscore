# Visor de un objeto desde una sola PNG

Copia del código de la aplicación del diente, con su imagen actual, lista para abrir y modificar. No requiere la cuenta ni el alojamiento originales. No se incluyen credenciales ni configuración de publicación.

## Abrir sin instalar nada

Descomprime todo el ZIP y abre `dist/index.html` en tu navegador. Contiene React y la PNG incrustados; no necesita Internet para mostrar el diente. No abras el HTML dentro del ZIP sin extraerlo.

## Archivos importantes

- `source/App.tsx`: componente React + TypeScript completo, con la PNG incrustada.
- `source/App.template.tsx`: plantilla editable. Edita esta, porque el build sobrescribe App.tsx.
- `source/views/`: siete láminas originales, seis vistas por lámina.
- `source/views.json`: nombres de esas siete láminas, relativos a esta carpeta.
- `source/assemble_rows.py`: aísla los seis objetos de cada lámina, los ordena y arma el atlas.
- `source/atlas.png`: atlas legible de 6 columnas × 7 filas.
- `source/atlas-calibration.json`: registro de recortes y posiciones; los ángulos son objetivos solicitados, no mediciones de cámara.
- `source/encode.py`: transforma el atlas en la PNG intercalada y comprueba las 42 vistas sin pérdida.
- `source/build.mjs`: incrusta esa PNG y compila la aplicación autónoma.
- `dist/lightfield_encoded.png`: única imagen que utiliza el visor; también está incrustada en el HTML y App.tsx.
- `PROMPT-IMAGENES.md`: prompts y orden exacto para cambiar de objeto.

## Usar otro objeto

Necesitas Python 3 y Node.js con npm. Desde la carpeta que contiene package.json:

```sh
python -m pip install Pillow numpy scipy
npm ci
```

1. Genera las siete láminas siguiendo `PROMPT-IMAGENES.md`.
2. Reemplaza los siete PNG de `source/views/`, conservando sus nombres. NO basta con cambiar el archivo PNG de dist: el HTML tiene la imagen anterior incrustada hasta recompilar.
3. Ejecuta, en este orden:

```sh
python source/assemble_rows.py source/views.json
python source/encode.py
npm run build
```

4. Abre el nuevo `dist/index.html`. Recarga la pestaña si estaba abierta.

Para cambiar textos o controles, edita `source/App.template.tsx` y ejecuta `npm run build`.

### Si ya tienes un atlas bien recortado

Debe tener 6 columnas × 7 filas, sin separadores ni márgenes externos que desplacen la cuadrícula. Cada celda contiene un solo objeto completo. Ideal: 2400 × 2800 px, celdas de 400 × 400. Usa el orden de ángulos indicado en el prompt.

```sh
python source/encode.py "ruta/a/mi-atlas.png"
npm run build
```

### Si el ensamblador no encuentra seis objetos

Está diseñado para siluetas separadas sobre blanco. Puede fallar con objetos transparentes, muy blancos, peludos o compuestos por piezas desconectadas. No asumas que seis componentes detectados equivalen a seis vistas correctas: revisa `source/atlas.png`. Si falla, prepara manualmente las 42 celdas sobre blanco en un editor y usa la opción de atlas directo. No añadas bordes ni números dentro de las imágenes.

## Qué hace realmente

Para cada píxel espacial `(s,t)` de una vista, su color se guarda en `(u,v)` de la PNG mediante:

`u = s*6+a`, `v = t*7+b`.

`a` es la columna angular (0–5) y `b` la fila angular (0–6). Cada bloque de 6×7 píxeles contiene 42 muestras angulares del mismo píxel espacial: NO hay 42 imágenes dentro de un único píxel.

El visor usa Canvas 2D e interpolación bilineal. No usa Three.js, WebGL ni modelos 3D. No reconstruye superficies ocultas ni crea vistas físicamente correctas: mezcla vistas ya almacenadas.

## Límites importantes de esta versión

- Seis orientaciones horizontales solicitadas: 0°, 60°, 120°, 180°, 240°, 300°. La interfaz actual está limitada en los extremos; no hace una vuelta continua de 300° a 360°/0°.
- Los controles muestran X hasta 5,9 e Y hasta 6,9 por la especificación original, pero la decodificación limita los valores efectivos a 5 y 6. El tramo final de cada control no añade vistas.
- La interpolación puede producir doble contorno. Más calidad de imagen no elimina por sí sola ese límite, y un prompt no garantiza consistencia geométrica exacta.
- Cambiar el número de vistas requiere modificar codificador, decodificador y controles. Este paquete espera exactamente 42.
- La PNG codificada no debe redimensionarse, comprimirse como JPEG ni pasar por optimizadores que alteren píxeles. El aspecto entrelazado de esa PNG es intencional.
- `source/verify.mjs` se conserva como prueba de desarrollo original; requiere un volcado RGBA temporal preparado aparte. Para el flujo de uso normal, `encode.py` ya comprueba la inversión exacta de las 42 vistas.

La aplicación publicada no fue modificada al preparar esta descarga.
