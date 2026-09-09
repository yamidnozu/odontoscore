import fs from 'node:fs';

const src = 'dist/calculadora-dosis-pediatrica.html';
const destDir = 'dist/calculadora-dosis-pediatrica';
const destFile = 'dist/calculadora-dosis-pediatrica/index.html';

if (fs.existsSync(src)) {
  fs.mkdirSync(destDir, { recursive: true });
  fs.copyFileSync(src, destFile);
  console.log('✓ Mirrored calculadora-dosis-pediatrica.html -> dist/calculadora-dosis-pediatrica/index.html');
}

// ── Endo3D Trainer (modelox) → dist/simuladores/endodoncia/ ──
// La página src/pages/guias/simulador-endodoncia-3d.astro integra el
// simulador en nativo (sin iframe) y carga desde aquí:
//   /simuladores/endodoncia/data/models.js  (mallas BodyParts3D)
//   /simuladores/endodoncia/engine.js        (motor extraído de modelox)
// modelox/endodoncia.html sigue siendo la única fuente del motor.
const endoEngineSrc = 'modelox/endodoncia.html';
const endoModelsSrc = 'modelox/data/models.js';
const endoDestDir = 'dist/simuladores/endodoncia';

if (fs.existsSync(endoEngineSrc) && fs.existsSync(endoModelsSrc)) {
  const raw = fs.readFileSync(endoEngineSrc, 'utf8');
  const start = raw.lastIndexOf('<script>');
  const end = raw.lastIndexOf('</script>');
  const engine = (start >= 0 && end > start) ? raw.slice(start + '<script>'.length, end) : '';
  if (!engine.trimStart().startsWith('"use strict"') || engine.length < 50000) {
    console.warn('! No se pudo extraer el motor del simulador: revisa modelox/endodoncia.html.');
  } else {
    fs.mkdirSync(endoDestDir + '/data', { recursive: true });
    fs.writeFileSync(endoDestDir + '/engine.js', engine);
    fs.copyFileSync(endoModelsSrc, endoDestDir + '/data/models.js');
    console.log('✓ Simulador endodoncia -> dist/simuladores/endodoncia/ (engine.js + data/models.js)');
  }
} else {
  console.warn('! Falta modelox/endodoncia.html o modelox/data/models.js: simulador no publicado.');
}
