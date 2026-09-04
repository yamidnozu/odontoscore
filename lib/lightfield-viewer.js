/**
 * OdontoScore Lightfield 3D Interactive Engine v1.1
 * Decodifica en tiempo real 42 vistas desde la PNG entrelazada (2400×2800).
 * Basado en la implementación de referencia sin pérdidas de App.template.tsx.
 */
(function (global) {
  'use strict';

  const Kx = 6;  // 6 columnas de azimut (0°, 60°, 120°, 180°, 240°, 300°)
  const Ky = 7;  // 7 filas de elevación (+60°, +40°, +20°, 0°, -20°, -40°, -60°)
  const W0 = 400;
  const H0 = 400;

  function clamp(val, min, max) {
    return Math.max(min, Math.min(max, val));
  }

  function bilinearSample(image, u, v, out, destination) {
    const x0 = Math.floor(u), y0 = Math.floor(v);
    const x1 = Math.min(x0 + 1, image.width - 1), y1 = Math.min(y0 + 1, image.height - 1);
    const fx = u - x0, fy = v - y0;
    const w00 = (1 - fx) * (1 - fy), w10 = fx * (1 - fy);
    const w01 = (1 - fx) * fy, w11 = fx * fy;
    const p00 = (y0 * image.width + x0) * 4, p10 = (y0 * image.width + x1) * 4;
    const p01 = (y1 * image.width + x0) * 4, p11 = (y1 * image.width + x1) * 4;
    const data = image.data;
    out[destination]     = Math.round(data[p00] * w00 + data[p10] * w10 + data[p01] * w01 + data[p11] * w11);
    out[destination + 1] = Math.round(data[p00 + 1] * w00 + data[p10 + 1] * w10 + data[p01 + 1] * w01 + data[p11 + 1] * w11);
    out[destination + 2] = Math.round(data[p00 + 2] * w00 + data[p10 + 2] * w10 + data[p01 + 2] * w01 + data[p11 + 2] * w11);
    out[destination + 3] = 255;
  }

  function decodePixels(encodedImageData, thetaX, thetaY, output) {
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

  function LightfieldViewer(options) {
    this.canvas = typeof options.canvas === 'string' ? document.querySelector(options.canvas) : options.canvas;
    if (!this.canvas) throw new Error('LightfieldViewer: canvas no encontrado.');

    this.imageSrc = options.imageSrc;
    this.onAngleChange = options.onAngleChange || null;
    this.onReady = options.onReady || null;

    this.thetaX = options.initialX !== undefined ? options.initialX : 0;
    this.thetaY = options.initialY !== undefined ? options.initialY : 3; // 3 = Ecuador (0°)
    this.isReady = false;
    this.isPlaying = false;
    this.orbitDirection = 1;

    this.pointerState = null;
    this.animFrameId = null;

    this.init();
  }

  LightfieldViewer.prototype.init = function () {
    const self = this;
    const canvas = this.canvas;

    canvas.width = 400;
    canvas.height = 400;

    this.bufferCanvas = document.createElement('canvas');
    this.bufferCanvas.width = W0;
    this.bufferCanvas.height = H0;
    this.bufferCtx = this.bufferCanvas.getContext('2d');
    this.outputData = this.bufferCtx.createImageData(W0, H0);

    this.displayCtx = canvas.getContext('2d');
    this.displayCtx.imageSmoothingEnabled = true;
    this.displayCtx.imageSmoothingQuality = 'high';

    const img = new Image();
    img.onload = function () {
      try {
        if (img.naturalWidth !== W0 * Kx || img.naturalHeight !== H0 * Ky) {
          throw new Error('La imagen debe medir exactamente 2400 × 2800 píxeles. Dimensiones actuales: ' + img.naturalWidth + ' × ' + img.naturalHeight);
        }
        const offscreen = document.createElement('canvas');
        offscreen.width = img.naturalWidth;
        offscreen.height = img.naturalHeight;
        const offCtx = offscreen.getContext('2d', { willReadFrequently: true });
        offCtx.drawImage(img, 0, 0);
        self.encodedData = offCtx.getImageData(0, 0, offscreen.width, offscreen.height);
        self.isReady = true;

        if (self.onReady) self.onReady();
        self.render();
      } catch (err) {
        console.error('Error al decodificar Lightfield PNG:', err);
      }
    };
    const dataSrc = (typeof window !== 'undefined' && window.LIGHTFIELD_DATA_URI) ? window.LIGHTFIELD_DATA_URI : self.imageSrc;
    img.src = dataSrc;

    this.bindEvents();
  };

  LightfieldViewer.prototype.bindEvents = function () {
    const self = this;
    const canvas = this.canvas;

    canvas.addEventListener('pointerdown', function (e) {
      if (!self.isReady) return;
      canvas.setPointerCapture(e.pointerId);
      self.pointerState = { id: e.pointerId, x: e.clientX, y: e.clientY };
      if (self.isPlaying) self.stopOrbit();
    });

    canvas.addEventListener('pointermove', function (e) {
      if (!self.pointerState || self.pointerState.id !== e.pointerId) return;
      const dx = e.clientX - self.pointerState.x;
      const dy = e.clientY - self.pointerState.y;
      self.pointerState.x = e.clientX;
      self.pointerState.y = e.clientY;

      // Movimiento horizontal continuo con wrap 0..5.9
      let newX = self.thetaX + dx * 0.018;
      if (newX < 0) newX += (Kx - 0.01);
      if (newX >= Kx) newX %= Kx;
      self.thetaX = newX;

      // Movimiento vertical (clamped entre 0 y 6)
      self.thetaY = clamp(self.thetaY + dy * 0.018, 0, Ky - 1);

      self.render();
    });

    function endPointer(e) {
      if (self.pointerState && self.pointerState.id === e.pointerId) {
        self.pointerState = null;
      }
    }

    canvas.addEventListener('pointerup', endPointer);
    canvas.addEventListener('pointercancel', endPointer);
  };

  LightfieldViewer.prototype.render = function () {
    if (!this.isReady || !this.encodedData) return;

    decodePixels(this.encodedData, this.thetaX, this.thetaY, this.outputData);

    this.bufferCtx.putImageData(this.outputData, 0, 0);
    this.displayCtx.drawImage(this.bufferCanvas, 0, 0, this.canvas.width, this.canvas.height);

    if (this.onAngleChange) {
      const degX = Math.round((this.thetaX / (Kx - 1)) * 300);
      const degY = Math.round(60 - (this.thetaY / (Ky - 1)) * 120);
      this.onAngleChange({
        thetaX: this.thetaX,
        thetaY: this.thetaY,
        degX: degX,
        degY: degY
      });
    }
  };

  LightfieldViewer.prototype.setAngles = function (thetaX, thetaY) {
    if (thetaX !== undefined) this.thetaX = clamp(thetaX, 0, Kx - 1);
    if (thetaY !== undefined) this.thetaY = clamp(thetaY, 0, Ky - 1);
    this.render();
  };

  LightfieldViewer.prototype.startOrbit = function (speed) {
    const step = speed || 0.025;
    this.isPlaying = true;
    const self = this;

    function loop() {
      if (!self.isPlaying) return;
      self.thetaX += step * self.orbitDirection;
      if (self.thetaX >= Kx - 1) {
        self.thetaX = Kx - 1;
        self.orbitDirection = -1;
      } else if (self.thetaX <= 0) {
        self.thetaX = 0;
        self.orbitDirection = 1;
      }
      self.render();
      self.animFrameId = requestAnimationFrame(loop);
    }
    cancelAnimationFrame(this.animFrameId);
    this.animFrameId = requestAnimationFrame(loop);
  };

  LightfieldViewer.prototype.stopOrbit = function () {
    this.isPlaying = false;
    cancelAnimationFrame(this.animFrameId);
  };

  LightfieldViewer.prototype.toggleOrbit = function () {
    if (this.isPlaying) this.stopOrbit();
    else this.startOrbit();
    return this.isPlaying;
  };

  global.LightfieldViewer = LightfieldViewer;
})(window);
