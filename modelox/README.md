# Cráneo y dientes — BodyParts3D

Abre `index.html` directamente en el navegador. La aplicación carga automáticamente las mallas originales incluidas en `data/models.js`; no requiere CDN, servidor ni conexión para visualizar.

La única fuente anatómica es [BodyParts3D LATEST](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/README_e.html): `isa_BP3D_4.0_obj_99.zip`, `isa_parts_list_e.txt` e `isa_element_parts.txt`. Las tablas vinculan los conceptos FMA con los archivos de elementos, cuyos nombres no son los FMA. Los OBJ extraídos se conservan sin modificar en `data/obj/`. El manifiesto `data/provenance.json` contiene las correspondencias, URL de origen y SHA-256 de cada OBJ. La extracción usa rangos HTTP del ZIP oficial; solo se registra un hash del ZIP completo cuando se dispone de él.

No se generan sustitutos anatómicos. Si falta una malla, la preparación falla. El visor únicamente rota y escala las coordenadas originales para mostrarlas; la separación de mandíbula es una vista ilustrativa, no una simulación del movimiento articular.

Para regenerar los datos conservando las dos tablas oficiales en `data/`, ejecuta `node prepare-models.cjs`. Si el ZIP completo está presente, se lee localmente; de lo contrario, se descargan sus elementos mediante rangos HTTP. La selección contiene 20 estructuras óseas y 28 dientes permanentes. El archivo oficial ya tiene reducción de polígonos al 99%; no se añade detalle inventado.

Se conservó el HTML anterior en `index.original.html` como respaldo. `fix-viewer.cjs` documenta la migración inicial; no debe ejecutarse sobre el HTML ya corregido.

**Atribución:** BodyParts3D, © The Database Center for Life Science licensed under CC Attribution 4.0 International. Véase la [licencia oficial](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/lic.html).

## Simulador de endodoncia (`endodoncia.html`)

Ábrelo con doble clic, sin servidor. Usa las mallas reales de `data/models.js` (6 dientes: 11, 13, 14, 16, 36 y 31) para practicar la determinación de la longitud de trabajo: cavidad de acceso real por diente, lima que sigue el conducto, regla milimetrada clicable, Rx de conductometría simulada, localizador apical y modo práctica con ápice oculto.

**Modo gestos (Paso 4, opcional):** con la cámara web, la pinza pulgar-índice mueve la lima; el riel muestra las zonas objetivo por fase (A: lima inicial, B: conductometría/LT) y mantener la pinza cerrada 1 s fija la LT. Todo se procesa en el PC, nada se graba ni se sube. Funciona offline gracias a `vendor/mediapipe/` (MediaPipe Tasks Vision 0.10.14, Apache 2.0; véase `vendor/mediapipe/NOTA.txt`). La mano da control grueso por fases; el 0.1 mm exacto se ajusta con los botones.
