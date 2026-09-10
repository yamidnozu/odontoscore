import fs from 'node:fs';
import path from 'node:path';

const src = 'dist/calculadora-dosis-pediatrica.html';
const destDir = 'dist/calculadora-dosis-pediatrica';
const destFile = 'dist/calculadora-dosis-pediatrica/index.html';

if (fs.existsSync(src)) {
  fs.mkdirSync(destDir, { recursive: true });
  fs.copyFileSync(src, destFile);
  console.log('✓ Mirrored calculadora-dosis-pediatrica.html -> dist/calculadora-dosis-pediatrica/index.html');
}

function copyDir(from, to) {
  fs.mkdirSync(to, { recursive: true });
  for (const entry of fs.readdirSync(from, { withFileTypes: true })) {
    const s = path.join(from, entry.name);
    const d = path.join(to, entry.name);
    if (entry.isDirectory()) copyDir(s, d);
    else fs.copyFileSync(s, d);
  }
}

function extractScripts(html) {
  const out = [];
  const re = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
  let m;
  while ((m = re.exec(html))) {
    out.push({ attrs: m[1] || '', body: m[2] || '' });
  }
  return out;
}

// ── Endo3D Trainer (modelox) → dist/simuladores/endodoncia/ ──
const endoEngineSrc = 'modelox/endodoncia.html';
const endoModelsSrc = 'modelox/data/models.js';
const endoDestDir = 'dist/simuladores/endodoncia';
const mpSrcDir = 'modelox/vendor/mediapipe';

if (fs.existsSync(endoEngineSrc) && fs.existsSync(endoModelsSrc)) {
  const raw = fs.readFileSync(endoEngineSrc, 'utf8');
  const scripts = extractScripts(raw);
  const inline = scripts.filter((s) => !/\bsrc\s*=/.test(s.attrs));
  const vision = inline.find((s) => s.body.includes('self.MPVision') && s.body.includes('HandLandmarker'));
  const engine = [...inline].reverse().find((s) => s.body.trimStart().startsWith('"use strict"'));

  fs.mkdirSync(endoDestDir + '/data', { recursive: true });

  if (engine && engine.body.length >= 50000) {
    fs.writeFileSync(endoDestDir + '/engine.js', engine.body);
    fs.copyFileSync(endoModelsSrc, endoDestDir + '/data/models.js');
    console.log('✓ Simulador endodoncia -> dist/simuladores/endodoncia/engine.js');
  } else {
    console.warn('! No se pudo extraer el motor del simulador: revisa modelox/endodoncia.html.');
  }

  if (vision && vision.body.length > 100000) {
    fs.writeFileSync(endoDestDir + '/vision-engine.js', vision.body);
    console.log('✓ MediaPipe vision-engine.js');
  } else {
    console.warn('! No se pudo extraer el motor de visión MediaPipe.');
  }

  if (fs.existsSync(mpSrcDir)) {
    const mpDest = path.join(endoDestDir, 'vendor', 'mediapipe');
    const wasmSrc = path.join(mpSrcDir, 'wasm');
    if (fs.existsSync(wasmSrc)) copyDir(wasmSrc, path.join(mpDest, 'wasm'));
    fs.mkdirSync(mpDest, { recursive: true });
    const task = path.join(mpSrcDir, 'hand_landmarker.task');
    if (fs.existsSync(task)) {
      fs.copyFileSync(task, path.join(mpDest, 'hand_landmarker.task'));
    }
    const bundle = path.join(mpSrcDir, 'vision_bundle.js');
    if (fs.existsSync(bundle)) {
      fs.copyFileSync(bundle, path.join(mpDest, 'vision_bundle.js'));
    }
    console.log('✓ MediaPipe wasm + hand_landmarker.task + vision_bundle.js');
  }
} else {
  console.warn('! Falta modelox/endodoncia.html o modelox/data/models.js: simulador no publicado.');
}
