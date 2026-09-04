import React, { useCallback, useEffect, useRef, useState } from 'react';

const Kx = 6, Ky = 7, W0 = 400, H0 = 400;
const ENCODED_PNG = '__ENCODED_PNG_DATA_URI__';
const clamp = (value: number, min: number, max: number) => Math.max(min, Math.min(max, value));

/** True four-neighbor bilinear interpolation. No allocations in the pixel loop. */
export function bilinearSample(image: ImageData, u: number, v: number, out: Uint8ClampedArray, destination: number): void {
  const x0 = Math.floor(u), y0 = Math.floor(v);
  const x1 = Math.min(x0 + 1, image.width - 1), y1 = Math.min(y0 + 1, image.height - 1);
  const fx = u - x0, fy = v - y0;
  const w00 = (1 - fx) * (1 - fy), w10 = fx * (1 - fy);
  const w01 = (1 - fx) * fy, w11 = fx * fy;
  const p00 = (y0 * image.width + x0) * 4, p10 = (y0 * image.width + x1) * 4;
  const p01 = (y1 * image.width + x0) * 4, p11 = (y1 * image.width + x1) * 4;
  const data = image.data;
  out[destination] = Math.round(data[p00] * w00 + data[p10] * w10 + data[p01] * w01 + data[p11] * w11);
  out[destination + 1] = Math.round(data[p00 + 1] * w00 + data[p10 + 1] * w10 + data[p01 + 1] * w01 + data[p11 + 1] * w11);
  out[destination + 2] = Math.round(data[p00 + 2] * w00 + data[p10 + 2] * w10 + data[p01 + 2] * w01 + data[p11 + 2] * w11);
  out[destination + 3] = 255;
}

/** E(s*Kx+a,t*Ky+b)=I[a,b](s,t), including fractional angular coordinates. */
export function decodePixels(encodedImageData: ImageData, thetaX: number, thetaY: number, output: ImageData): ImageData {
  thetaX = clamp(thetaX, 0, Kx - 1);
  thetaY = clamp(thetaY, 0, Ky - 1);
  const out = output.data;
  for (let t = 0; t < H0; t++) {
    const v = t * Ky + thetaY;
    for (let s = 0; s < W0; s++) {
      const u = s * Kx + thetaX;
      bilinearSample(encodedImageData, u, v, out, (t * W0 + s) * 4);
    }
  }
  return output;
}

type Props = {
  /** Optional atlas already in RAM: never fetched, never used by the shipped demo. */
  fallbackAtlas?: ImageData;
};

export default function App({ fallbackAtlas }: Props = {}) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const macroRef = useRef<HTMLCanvasElement>(null);
  const macroViewport = useRef<HTMLDivElement>(null);
  const encodedRef = useRef<ImageData | null>(null);
  const outputRef = useRef<ImageData | null>(null);
  const decodedCanvasRef = useRef<HTMLCanvasElement | null>(null);
  const positionRef = useRef({ x: 2, y: 2 });
  const pointerRef = useRef<{id: number; x: number; y: number} | null>(null);
  const frameRef = useRef<number | null>(null);
  const lastMetricRef = useRef(0);
  const [position, setPosition] = useState(positionRef.current);
  const [ready, setReady] = useState(false);
  const [error, setError] = useState('');
  const [showMacro, setShowMacro] = useState(false);
  const [duration, setDuration] = useState<number | null>(null);
  const [reload, setReload] = useState(0);

  function decode(thetaX: number, thetaY: number): ImageData {
    const output = outputRef.current ?? (outputRef.current = new ImageData(W0, H0));
    if (encodedRef.current) return decodePixels(encodedRef.current, thetaX, thetaY, output);
    if (fallbackAtlas) {
      const tileIndex = Math.round(clamp(thetaY, 0, Ky - 1)) * Kx + Math.round(clamp(thetaX, 0, Kx - 1));
      const tileWidth = fallbackAtlas.width / Kx, tileHeight = fallbackAtlas.height / Ky;
      const a = tileIndex % Kx, b = Math.floor(tileIndex / Kx);
      for (let t = 0; t < H0; t++) for (let s = 0; s < W0; s++) {
        const x = Math.floor(a * tileWidth + s * tileWidth / W0);
        const y = Math.floor(b * tileHeight + t * tileHeight / H0);
        const from = (y * fallbackAtlas.width + x) * 4, to = (t * W0 + s) * 4;
        output.data[to] = fallbackAtlas.data[from]; output.data[to + 1] = fallbackAtlas.data[from + 1];
        output.data[to + 2] = fallbackAtlas.data[from + 2]; output.data[to + 3] = 255;
      }
      return output;
    }
    throw new Error('La PNG codificada todavía no está disponible.');
  }

  const drawRef = useRef<() => void>(() => {});
  drawRef.current = () => {
    if ((!encodedRef.current && !fallbackAtlas) || !canvasRef.current) return;
    const start = performance.now();
    const data = decode(positionRef.current.x, positionRef.current.y);
    const buffer = decodedCanvasRef.current ?? document.createElement('canvas');
    if (!decodedCanvasRef.current) {buffer.width = W0; buffer.height = H0; decodedCanvasRef.current = buffer;}
    buffer.getContext('2d')!.putImageData(data, 0, 0);
    const context = canvasRef.current.getContext('2d')!;
    context.imageSmoothingEnabled = true;
    context.imageSmoothingQuality = 'high';
    context.drawImage(buffer, 0, 0, 480, 480);
    const end = performance.now();
    if (end - lastMetricRef.current > 250 || lastMetricRef.current === 0) {
      lastMetricRef.current = end; setDuration(end - start);
    }
  };

  const schedule = useCallback(() => {
    if (frameRef.current !== null) return;
    frameRef.current = requestAnimationFrame(() => {frameRef.current = null; drawRef.current();});
  }, []);

  useEffect(() => {
    let cancelled = false;
    setReady(false); setError('');
    const image = new Image();
    image.onload = () => {
      if (cancelled) return;
      try {
        if (image.naturalWidth !== W0 * Kx || image.naturalHeight !== H0 * Ky) throw new Error('La imagen debe medir exactamente 2400 × 2800 píxeles.');
        // One image load, one getImageData call. The atlas is never fetched.
        const offscreen = document.createElement('canvas');
        offscreen.width = image.naturalWidth; offscreen.height = image.naturalHeight;
        const context = offscreen.getContext('2d', { willReadFrequently: true });
        if (!context) throw new Error('Canvas 2D no está disponible.');
        context.drawImage(image, 0, 0);
        encodedRef.current = context.getImageData(0, 0, offscreen.width, offscreen.height);
        outputRef.current = new ImageData(W0, H0);
        setReady(true); schedule();
      } catch (reason) {setError(reason instanceof Error ? reason.message : 'No se pudo leer la PNG.');}
    };
    image.onerror = () => {
      if (cancelled) return;
      if (fallbackAtlas) {setReady(true); schedule();}
      else setError('No se pudo cargar la imagen codificada.');
    };
    image.src = ENCODED_PNG;
    return () => {cancelled = true; image.onload = null; image.onerror = null; if (frameRef.current !== null) cancelAnimationFrame(frameRef.current); frameRef.current = null;};
  }, [reload, schedule, fallbackAtlas]);

  useEffect(() => {
    if (!showMacro || !macroRef.current || !encodedRef.current) return;
    const data = encodedRef.current, canvas = macroRef.current;
    canvas.width = data.width; canvas.height = data.height;
    canvas.getContext('2d')!.putImageData(data, 0, 0);
    if (macroViewport.current) {
      macroViewport.current.scrollLeft = data.width * 2 - macroViewport.current.clientWidth / 2;
      macroViewport.current.scrollTop = data.height * 2 - 140;
    }
  }, [showMacro, ready]);

  function move(x: number, y: number) {
    positionRef.current = { x: clamp(x, 0, 5.9), y: clamp(y, 0, 6.9) };
    setPosition(positionRef.current); schedule();
  }
  function pointerMove(event: React.PointerEvent<HTMLCanvasElement>) {
    const previous = pointerRef.current;
    if (!previous || previous.id !== event.pointerId) return;
    move(positionRef.current.x + (event.clientX - previous.x) * 0.02, positionRef.current.y + (event.clientY - previous.y) * 0.02);
    pointerRef.current = { id: event.pointerId, x: event.clientX, y: event.clientY };
  }
  const actualX = Math.min(position.x, 5), actualY = Math.min(position.y, 6);

  return <div className="lf-app">
    <style>{CSS}</style>
    <main className="shell">
      <div className="masthead"><span className="brand">PNG<span className="brand-dot">/</span>LAB</span><span className="smallcaps">EXPERIMENTO INTERACTIVO</span></div>
      <header><div className="eyebrow">42 VISTAS · UN SOLO ARCHIVO</div><h1>Una sola imagen = 3D</h1><p className="subtitle">No es modelo 3D, es una PNG con 42 ángulos dentro de cada píxel</p></header>
      <div className="stage">
        <canvas ref={canvasRef} width={480} height={480} tabIndex={0} aria-label="Visor del diente. Arrastra para cambiar de vista. Usa las flechas del teclado para ajustes finos."
          onPointerDown={event => {if (!ready) return;event.currentTarget.focus({preventScroll:true});event.currentTarget.setPointerCapture(event.pointerId);pointerRef.current={id:event.pointerId,x:event.clientX,y:event.clientY};}}
          onPointerMove={pointerMove} onPointerUp={()=>pointerRef.current=null} onPointerCancel={()=>pointerRef.current=null} onLostPointerCapture={()=>pointerRef.current=null}
          onKeyDown={event=>{const steps:Record<string,[number,number]>={ArrowLeft:[-.05,0],ArrowRight:[.05,0],ArrowUp:[0,-.05],ArrowDown:[0,.05]};if(steps[event.key]){event.preventDefault();const [dx,dy]=steps[event.key];move(position.x+dx,position.y+dy);}}}/>
        {!ready && !error && <div className="status" role="status">Decodificando la PNG…</div>}
        {error && <div className="status error" role="alert">{error}<button onClick={()=>setReload(n=>n+1)}>Reintentar</button></div>}
      </div>
      <div className="gesture">↔ Arrastra para explorar los ángulos ↕</div>
      <section className="controls" aria-label="Controles del visor">
        <div className="view-row"><span>Vista: <strong>{actualX.toFixed(2)} / {actualY.toFixed(2)}</strong></span><button className="text-button" onClick={()=>move(2,2)}>Restablecer</button></div>
        <div className="slider-row"><label htmlFor="angle-x">Horizontal <span>X</span></label><input id="angle-x" type="range" min={0} max={5.9} step={0.01} value={position.x} onChange={e=>move(Number(e.target.value),position.y)} disabled={!ready}/><output htmlFor="angle-x">{position.x.toFixed(2)}</output></div>
        <div className="slider-row"><label htmlFor="angle-y">Vertical <span>Y</span></label><input id="angle-y" type="range" min={0} max={6.9} step={0.01} value={position.y} onChange={e=>move(position.x,Number(e.target.value))} disabled={!ready}/><output htmlFor="angle-y">{position.y.toFixed(2)}</output></div>
        <p className="range-note">La lectura se satura en X=5 e Y=6 para respetar el bloque de 6 × 7 muestras.</p>
      </section>
      <div className="actions"><button className="primary" onClick={()=>setShowMacro(v=>!v)} disabled={!ready}>{showMacro?'Ocultar macro-píxeles':'Ver macro-píxeles'} <span>400 %</span></button><a href={ENCODED_PNG} download="lightfield_encoded.png" className="secondary">Descargar PNG</a></div>
      {showMacro && <section className="macro-section"><div className="view-row"><strong>La PNG entrelazada</strong><span>Zoom 400 % · desplázate para explorar</span></div><div className="macro-viewport" ref={macroViewport} tabIndex={0} aria-label="PNG codificada al 400 por ciento, desplazable"><canvas ref={macroRef} style={{width:9600,height:11200,imageRendering:'pixelated'}}/></div><p>Cada bloque de 6 × 7 píxeles contiene las 42 muestras de una misma posición del diente. Este panel utiliza los mismos datos en memoria.</p></section>}
      <section className="explanation"><div className="formula">u = s × 6 + a <span>·</span> v = t × 7 + b</div><p><strong>(s, t)</strong> es una posición en la imagen de 400 × 400. <strong>(a, b)</strong> elige una de las 42 vistas. Los índices fraccionarios mezclan cuatro vecinos mediante interpolación bilineal.</p><p className="honest">La codificación conserva vistas; no reconstruye geometría. La continuidad depende del atlas generado y la mezcla puede producir imágenes dobles entre ángulos.</p></section>
      <footer><span>PNG sin pérdida · 2400 × 2800 · Canvas 2D</span><span>{duration===null?'Midiendo…':`${duration.toFixed(1)} ms · decodificación y dibujo`}</span></footer>
    </main>
  </div>;
}

const CSS = `
*{box-sizing:border-box}body{margin:0;background:#fff;color:#152233;font-family:Inter,ui-sans-serif,system-ui,-apple-system,sans-serif}.lf-app{background:#fff;min-height:100vh}.shell{max-width:896px;margin:0 auto;padding:25px 28px 30px}.masthead{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #e8edf2;padding-bottom:20px}.brand{font-size:17px;font-weight:800;letter-spacing:1px}.brand-dot{color:#2563eb;margin:0 6px}.smallcaps,.eyebrow{font-size:11px;letter-spacing:1.5px;font-weight:600;color:#657587}.eyebrow{color:#426da6}header{text-align:center;padding:34px 0 24px}h1{font-size:40px;letter-spacing:-1.5px;line-height:1.15;margin:12px 0}.subtitle{font-size:16px;line-height:1.6;color:#687687;max-width:540px;margin:0 auto}.stage{position:relative;display:flex;justify-content:center}.stage>canvas{width:min(480px,100%);height:auto;aspect-ratio:1;background:#fff;border:24px solid white;border-radius:24px;box-shadow:0 14px 55px #1834510e,0 0 0 1px #edf0f3;touch-action:none;cursor:grab}.stage>canvas:active{cursor:grabbing}.status{position:absolute;top:45%;background:#fff;padding:18px;border:1px solid #e1e8f0;border-radius:12px;max-width:90%;text-align:center}.status button{display:block;margin:10px auto}.error{color:#9b3030}.gesture{text-align:center;font-size:13px;color:#8491a1;margin:20px 0}.controls{max-width:540px;margin:0 auto}.view-row{display:flex;align-items:center;justify-content:space-between;gap:14px;font-size:14px;margin-bottom:20px}.view-row strong{font-variant-numeric:tabular-nums}.text-button{padding:0;border:0;color:#64758a;background:transparent;font:13px inherit;cursor:pointer}.slider-row{display:grid;grid-template-columns:115px 1fr 40px;align-items:center;gap:15px;margin:20px 0}.slider-row label{font-size:14px;color:#3e4f62}.slider-row label span{font-size:12px;color:#8f9bac;margin-left:7px}input[type=range]{width:100%;accent-color:#2563eb;cursor:pointer}.slider-row output{text-align:right;font:13px ui-monospace,monospace;color:#4d647e}.range-note{font-size:12px;color:#8491a1;line-height:1.5}.actions{display:flex;justify-content:center;gap:12px;margin:26px 0 34px;flex-wrap:wrap}button,a{outline-offset:4px}button:focus-visible,a:focus-visible,input:focus-visible,canvas:focus-visible{outline:2px solid #2563eb}.primary,.secondary{font:14px system-ui;padding:12px 17px;border-radius:9px;cursor:pointer;text-decoration:none}.primary{background:#1b3555;border:1px solid #1b3555;color:white}.primary:hover{background:#24476e}.primary span{font-size:11px;color:#b4c5da;margin-left:10px}.secondary{background:white;border:1px solid #dce3eb;color:#415671}.secondary:hover{background:#f4f7fa}button:disabled{opacity:.5;cursor:wait}.macro-section{border:1px solid #e1e7ef;padding:18px;border-radius:14px;margin-bottom:26px}.macro-section .view-row>span{font-size:12px;color:#6e7b8d}.macro-viewport{height:300px;overflow:auto;background:#f6f7f9;border-radius:8px;border:1px solid #e5e9ef}.macro-viewport canvas{display:block;max-width:none}.macro-section p{font-size:13px;color:#6d7e90;line-height:1.6}.explanation{border-top:1px solid #e9eef3;padding-top:24px}.formula{text-align:center;font:15px ui-monospace,monospace;letter-spacing:-.2px;color:#355679}.formula span{margin:0 16px;color:#b2becc}.explanation p{font-size:14px;line-height:1.65;color:#63758a;max-width:680px;margin:18px auto}.explanation p.honest{font-size:12px;color:#8b96a4}footer{border-top:1px solid #edf0f4;display:flex;justify-content:space-between;gap:15px;color:#8a97a7;font-size:11px;padding-top:20px;margin-top:26px}@media(max-width:600px){.shell{padding:18px 18px 24px}.smallcaps{font-size:9px;letter-spacing:1px}header{padding:28px 0 20px}h1{font-size:31px;letter-spacing:-1px}.subtitle{font-size:14px}.stage>canvas{border-width:24px}.slider-row{grid-template-columns:92px 1fr 35px;gap:10px}.slider-row label{font-size:13px}.formula{font-size:12px}.formula span{margin:0 6px}.view-row{gap:8px}.macro-section .view-row{align-items:flex-start;flex-direction:column}footer{flex-direction:column;gap:5px}.gesture{font-size:12px}}`;
