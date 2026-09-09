import os

astro_code = '''---
import BaseLayout from '../../layouts/BaseLayout.astro';

const pageTitle = "Longitud de Trabajo en Endodoncia: Constricción Apical, Localizador y Protocolo Clínico";
const pageDesc = "Guía clínica interactiva y simulador gestual de conductometría: determinación precisa de la longitud de trabajo (LT = APEX −0.5mm), constricción CDC y protocolo paso a paso.";
const canonicalUrl = "https://odontoscore.com/guias/longitud-trabajo-endodoncia.html";

const jsonLd = [
  {
    "@context": "https://schema.org",
    "@type": "MedicalWebPage",
    "name": "Longitud de Trabajo en Endodoncia: Protocolo Clínico y Simulador Apical",
    "url": canonicalUrl,
    "description": "Determinación estricta de la longitud de trabajo endodóntica desde la referencia coronaria hasta la constricción apical. Simulador táctil de conductometría.",
    "author": {
      "@type": "Organization",
      "name": "Comité Clínico OdontoScore"
    },
    "publisher": {
      "@type": "Organization",
      "name": "OdontoScore",
      "logo": {
        "@type": "ImageObject",
        "url": "https://odontoscore.com/assets/img/logo-odontoscore.svg"
      }
    }
  },
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "¿Por qué la longitud de trabajo no es hasta el vértice radiográfico?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "El vértice radiográfico es el extremo anatómico observable en la radiografía, pero el foramen mayor emerge habitualmente entre 0.2 y 0.5 mm en sentido lateral. La constricción apical (unión cemento-dentinaria CDC) se ubica entre 0.5 y 1 mm por detrás del ápice radiográfico. Si se instrumenta hasta el vértice Rx, se sobreinstrumenta el ligamento periodontal, provocando dolor postoperatorio y retraso de la cicatrización."
        }
      },
      {
        "@type": "Question",
        "name": "¿Cuál es la fórmula para la longitud de trabajo definitiva con localizador apical?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "La regla de oro clínica es LT = APEX − 0.5 mm. Se avanza con la lima hasta registrar el nivel 0.0 APEX en el localizador y se retrocede suavemente hasta la marca verde de 0.5 mm, ajustando el tope de silicona a la referencia incisal."
        }
      }
    ]
  }
];
---

<BaseLayout
  title={pageTitle}
  description={pageDesc}
  canonicalUrl={canonicalUrl}
  jsonLd={jsonLd}
>
  <!-- Link to the exact precompiled Tailwind CSS stylesheet -->
  <link rel="stylesheet" href="/styles/longitud-trabajo.css" />

  <style is:inline>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700&display=swap');

    .endo-root {
      font-family: 'Inter', ui-sans-serif, system-ui, -apple-system, sans-serif !important;
      background-color: #FCFCFC;
    }

    .fade-up {
      animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) both;
    }

    @keyframes fadeUp {
      from {
        transform: translateY(24px);
        opacity: 0;
      }
      to {
        transform: translateY(0);
        opacity: 1;
      }
    }
  </style>

  <div class="endo-root min-h-screen bg-[#FCFCFC] text-[#0A0A0A] antialiased selection:bg-[#0066FF]/10 overflow-x-hidden">
    
    <!-- Subheader Glassmorphism Sticky -->
    <div class="sticky top-0 z-40 backdrop-blur-[20px] bg-[#FCFCFC]/80 border-b border-black/[0.06] px-6 md:px-10 h-[44px] flex items-center justify-between">
      <div class="text-[10px] uppercase tracking-[0.2em] text-black/40 font-medium flex items-center gap-2">
        <a href="/#academia" class="hover:text-[#0066FF] transition-colors">← Academia</a>
        <span class="opacity-30">/</span>
        <span>LT — ENDO / V3 clínica real</span>
      </div>
      <div class="text-[10px] tracking-wide text-black/30 hidden md:flex gap-3 items-center">
        <span>mano + boca + diente</span>
        <span class="opacity-30">·</span>
        <span>protocolo real</span>
        <span class="opacity-30">·</span>
        <span style="color:#0066FF" class="font-medium">constricción no ápice</span>
      </div>
    </div>

    <div class="max-w-[1240px] mx-auto">
      
      <!-- ==================== PARTE 1: HERO CONCEPTUAL ==================== -->
      <section class="relative px-6 md:px-10 pt-14 md:pt-20 pb-16 md:pb-24 grid md:grid-cols-[1.05fr_0.95fr] gap-10 md:gap-12 items-center border-b border-black/[0.06]">
        <div class="fade-up">
          <h1 class="text-[12vw] md:text-[7.2vw] font-[200] leading-[0.86] tracking-[-0.05em]">
            Longitud<br />de trabajo
          </h1>
          <div class="mt-6 flex items-start gap-4">
            <div class="mt-2 h-[1px] w-12 bg-black/10 shrink-0"></div>
            <p class="text-[13px] leading-[1.5] tracking-[-0.01em] text-black/60 max-w-[44ch]">
              De la referencia coronaria a la <span class="text-[#0A0A0A] font-medium">constricción apical</span>. 0.5-1mm del ápice radiográfico. 0.5mm definen el éxito endodóntico.
            </p>
          </div>
          <div class="mt-10 flex gap-6 text-[11px] leading-[1.6] max-w-[48ch]">
            <div class="text-black/40">
              LT = distancia<br />
              <span class="text-black font-medium">borde incisal → constricción</span>
            </div>
            <div class="h-8 w-[1px] bg-black/10"></div>
            <div class="text-black/40">
              No es vértice Rx.<br />
              <span class="text-[#0066FF] font-medium">LT = APEX −0.5mm</span>
            </div>
          </div>
        </div>

        <div class="relative fade-up" style="animation-delay:0.15s">
          <div id="heroParallax" class="relative rounded-[32px] overflow-hidden border border-black/[0.06] bg-white aspect-[4/3] md:aspect-[1.15/1]">
            <img 
              src="/images/guias/longitud-trabajo/acceso-boca-referencia-incisal.webp" 
              alt="Mano con guante insertando lima en tipodonto - boca y diente" 
              class="w-full h-full object-cover" 
              loading="eager"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-black/10 to-transparent pointer-events-none"></div>
            <div class="absolute top-4 left-4 md:top-6 md:left-6 rounded-full px-3 py-1.5 bg-white/70 backdrop-blur-[18px] border border-black/[0.06] text-[10px] uppercase tracking-[0.14em] text-black/70 font-semibold">
              Endodoncia • Protocolo real
            </div>
            <div class="absolute bottom-4 left-4 right-4 md:bottom-6 md:left-6 md:right-6 flex justify-between items-end">
              <div class="rounded-[16px] px-3 py-2 bg-[#0A0A0A]/85 backdrop-blur text-white text-[10px] leading-[1.4] max-w-[22ch]">
                Manos con guante azul, abrebocas, tipodonto 21. Referencia: borde incisal.
              </div>
              <div class="rounded-full w-9 h-9 bg-white/80 backdrop-blur grid place-items-center border border-black/10 text-[11px] font-bold">
                21
              </div>
            </div>
          </div>
          <div class="mt-3 text-[10px] text-black/30 tracking-wide">
            Figura A — mano, diente y boca real. Parallax suave al scroll.
          </div>
        </div>
      </section>

      <!-- ==================== PARTE 2: ANATOMÍA & POR QUÉ FALLA ==================== -->
      <section class="px-6 md:px-10 py-16 md:py-24 grid md:grid-cols-[0.9fr_1.1fr] gap-12 md:gap-20 border-b border-black/[0.06]">
        <div>
          <div class="text-[11px] uppercase tracking-[0.2em] text-black/30 font-medium">Qué es y por qué falla</div>
          <h2 class="mt-6 text-[28px] md:text-[36px] font-[200] tracking-[-0.03em] leading-[1.05]">
            No es hasta donde se ve en la Rx. Es hasta donde termina el conducto.
          </h2>
          <div class="mt-6 space-y-4 text-[13px] leading-[1.7] text-black/60 max-w-[46ch]">
            <p>
              <span class="text-black font-semibold">Longitud de trabajo</span> es la distancia entre un punto coronario estable (borde incisal, cúspide) y la constricción apical (unión CDC), donde el conducto es más estrecho. Está 0.5-1mm corta del vértice radiográfico.
            </p>
            <p>
              El ápice radiográfico es vértice anatómico de la raíz en la imagen. El foramen mayor suele estar 0.2-0.5mm lateral. Si instrumentas hasta Rx, sobreinstrumentas, extruyes, lesionas periodonto.
            </p>
            <div class="pt-2 flex gap-3 text-[11px]">
              <div class="px-2.5 py-1 rounded-full bg-black/[0.04] border border-black/[0.06] text-black/70 font-medium">Constricción 0.5mm</div>
              <div class="px-2.5 py-1 rounded-full bg-[#0066FF]/10 border border-[#0066FF]/20 text-[#0066FF] font-semibold">LT = APEX −0.5</div>
            </div>
          </div>
        </div>

        <div class="rounded-[28px] border border-black/[0.06] bg-white p-6 md:p-10 flex flex-col md:flex-row gap-8 items-center">
          <div class="shrink-0">
            <svg viewBox="0 0 180 320" class="w-[140px] md:w-[180px] h-auto">
              <path d="M55 10 C30 40 28 105 62 130 C50 175 68 245 82 285 C88 295 92 295 98 285 C112 245 130 175 118 130 C152 105 150 40 125 10 C110 -2 70 -2 55 10Z" fill="none" stroke="rgba(0,0,0,0.12)" stroke-width="1.5"></path>
              <path d="M90 20 C88 80 86 160 90 265" stroke="#FF4D5A" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="6 4" opacity="0.35" fill="none"></path>
              <line x1="28" y1="18" x2="152" y2="18" stroke="rgba(0,0,0,0.2)" stroke-width="0.8" stroke-dasharray="3 3"></line>
              <text x="10" y="16" font-size="8" fill="rgba(0,0,0,0.4)" font-weight="300">ref. coronaria</text>
              <g>
                <ellipse cx="90" cy="248" rx="16" ry="4" fill="none" stroke="#0066FF" stroke-width="1.2" opacity="0.8"></ellipse>
                <circle cx="90" cy="248" r="2.2" fill="#0066FF"></circle>
                <text x="112" y="251" font-size="8" fill="#0066FF" font-weight="500">constricción</text>
              </g>
              <g>
                <circle cx="90" cy="285" r="2.8" fill="none" stroke="rgba(0,0,0,0.25)" stroke-width="1"></circle>
                <text x="112" y="288" font-size="8" fill="rgba(0,0,0,0.35)">vértice Rx</text>
              </g>
              <line x1="72" y1="250" x2="72" y2="283" stroke="#0066FF" stroke-width="0.7" stroke-dasharray="2 2"></line>
              <text x="40" y="270" font-size="7" fill="#0066FF" font-weight="500">0.5-1mm</text>
              <text x="90" y="312" text-anchor="middle" font-size="9" fill="rgba(0,0,0,0.5)" font-weight="500">LT = APEX −0.5mm</text>
            </svg>
          </div>
          <div class="text-[12px] leading-[1.6] text-black/50 max-w-[32ch]">
            <div class="text-[11px] uppercase tracking-[0.18em] text-black/30 font-medium">Por qué fallas comunes</div>
            <ul class="mt-3 space-y-2 list-disc pl-4 text-black/70">
              <li>Confundes ápice Rx con constricción → sobreobturas.</li>
              <li>Cambias referencia → LT varía 0.5-2mm.</li>
              <li>Stop angulado → lees mal en regla.</li>
              <li>Localizador con conducto inundado → marca errática.</li>
            </ul>
            <div class="mt-4 text-[11px] text-black/40">Esquema suizo minimal, no anatómico pesado.</div>
          </div>
        </div>
      </section>

      <!-- ==================== PARTE 3: ¡EMULADOR APICAL PRIORIZADO! ==================== -->
      <section id="emulador" class="px-6 md:px-10 py-16 md:py-24 border-b border-black/[0.06] grid md:grid-cols-[1.1fr_0.9fr] gap-10 md:gap-16 items-start">
        <!-- Canal interactivo de la Lima -->
        <div 
          id="canalContainer" 
          class="relative h-[64vh] md:h-[86vh] rounded-[32px] border border-black/[0.06] bg-white overflow-hidden select-none touch-none cursor-ns-resize"
        >
          <img 
            src="/images/guias/longitud-trabajo/lima-k10-sondeo.webp" 
            alt="" 
            class="absolute inset-0 w-full h-full object-cover opacity-[0.12] pointer-events-none" 
          />
          <div class="absolute inset-0 grid place-items-center pointer-events-none">
            <svg viewBox="0 0 200 420" class="w-[44%] md:w-[36%] h-auto drop-shadow-[0_20px_30px_rgba(0,0,0,0.08)]">
              <defs>
                <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stop-color="white" stop-opacity="0.9"></stop>
                  <stop offset="100%" stop-color="#E8EFFF" stop-opacity="0.5"></stop>
                </linearGradient>
              </defs>
              <path d="M60 12 C24 52 22 132 66 162 C52 212 72 312 84 362 C92 376 108 376 116 362 C128 312 148 212 134 162 C178 132 176 52 140 12 C122 -6 78 -6 60 12Z" fill="url(#g)" stroke="rgba(0,0,0,0.08)" stroke-width="1.4"></path>
              <path d="M100 20 C98 120 92 220 98 350" stroke="#FF2A3A" stroke-opacity="0.28" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="8 6" fill="none"></path>
              <ellipse cx="99" cy="328" rx="14" ry="4.2" fill="none" stroke="#0066FF" stroke-width="1" opacity="0.7"></ellipse>
            </svg>
          </div>

          <!-- Línea y Handle del Stop de la Lima -->
          <div class="absolute left-1/2 top-0 bottom-0 w-[1px] bg-black/10">
            <div id="fileLine" class="absolute w-[2px] -left-[0.5px] bg-[#0A0A0A]" style="top:6%; height:35.5%"></div>
            <div id="fileHandle" class="absolute left-1/2 -translate-x-1/2 -translate-y-1/2 w-7 h-7 rounded-full bg-[#0A0A0A] border-2 border-white shadow-[0_8px_20px_rgba(0,0,0,0.2)] grid place-items-center cursor-grab active:cursor-grabbing" style="top:41.5%">
              <div class="w-1.5 h-1.5 rounded-full bg-white"></div>
            </div>
            <div id="fileStopBadge" class="absolute left-6 -translate-y-1/2 px-2 py-1 rounded-full bg-white border border-black/10 text-[10px] shadow pointer-events-none" style="top:41.5%">
              stop
            </div>
          </div>

          <!-- Escala Milimétrica (18 a 23 mm) -->
          <div class="absolute right-4 md:right-8 top-[6%] bottom-[6%] w-[1px] bg-black/10">
            <div class="absolute -left-8 flex items-center gap-2" style="top:0%">
              <span class="text-[9px] tracking-widest text-black/25">18</span>
              <div class="w-2 h-[1px] bg-black/15"></div>
            </div>
            <div class="absolute -left-8 flex items-center gap-2" style="top:19.23%">
              <span class="text-[9px] tracking-widest text-black/25">19</span>
              <div class="w-2 h-[1px] bg-black/15"></div>
            </div>
            <div class="absolute -left-8 flex items-center gap-2" style="top:38.46%">
              <span class="text-[9px] tracking-widest text-black/25">20</span>
              <div class="w-2 h-[1px] bg-black/15"></div>
            </div>
            <div class="absolute -left-8 flex items-center gap-2" style="top:57.69%">
              <span class="text-[9px] tracking-widest text-black/25">21</span>
              <div class="w-2 h-[1px] bg-black/15"></div>
            </div>
            <div class="absolute -left-8 flex items-center gap-2" style="top:76.92%">
              <span class="text-[9px] tracking-widest text-black/25">22</span>
              <div class="w-2 h-[1px] bg-black/15"></div>
            </div>
            <div class="absolute -left-8 flex items-center gap-2" style="top:100%">
              <span class="text-[9px] tracking-widest text-black/25">23</span>
              <div class="w-2 h-[1px] bg-black/15"></div>
            </div>
            <div id="scaleTickActive" class="absolute -left-[5px] w-[11px] h-[1px] bg-[#0066FF]" style="top:42.3%"></div>
          </div>

          <div class="absolute bottom-5 left-6 md:left-8 text-[11px] text-black/30">
            ↕ arrastra · snap en constricción azul
          </div>
        </div>

        <!-- Columna Derecha de Lectura y Estado -->
        <div class="md:sticky md:top-[88px]">
          <div class="text-[11px] uppercase tracking-[0.2em] text-black/30 font-medium">Simulador gestual minimal</div>
          <h3 class="mt-4 text-[30px] md:text-[36px] font-[200] tracking-[-0.03em] leading-[0.95]">
            Arrastra.<br />Siente la constricción.
          </h3>
          <div class="mt-8 space-y-6">
            <div class="flex items-center gap-4">
              <div id="statusIconRing" class="w-14 h-14 rounded-full border grid place-items-center transition-all duration-300" style="border-color:#EAB308; box-shadow:none">
                <div id="statusIconDot" class="w-3 h-3 rounded-full transition-transform duration-300" style="background:#EAB308; transform:scale(1)"></div>
              </div>
              <div>
                <div id="statusLabel" class="text-[20px] font-[200] capitalize leading-none">cerca</div>
                <div id="statusDesc" class="mt-1 text-[11px] text-black/40">~1.0 mm · amarillo</div>
              </div>
              <div id="depthBadge" class="ml-auto px-3 py-1 rounded-full text-[11px] border bg-white border-black/10 text-black/30 font-semibold">
                20.2 mm
              </div>
            </div>

            <div class="h-[1px] bg-black/[0.06]"></div>

            <div>
              <div class="text-[11px] uppercase tracking-[0.2em] text-black/30 font-medium">Longitud de trabajo</div>
              <div class="mt-3 flex items-baseline gap-2">
                <span id="workLengthVal" class="text-[52px] font-[200] tracking-[-0.04em] leading-none">19.7</span>
                <span class="text-[13px] text-black/40">mm</span>
                <span class="text-[10px] text-black/30">= APEX −0.5mm</span>
              </div>
              <p class="mt-3 text-[12px] leading-[1.6] text-black/50 max-w-[36ch]">
                Fondo real <span class="text-black/70 font-medium">mano con lima #10 + stop amarillo</span> a 15% opacidad. No es ilustración: es foto clínica de referencia. El diente es translúcido para ver canal.
              </p>
            </div>

            <!-- Validación Táctil (Visible en constricción) -->
            <div id="tactileCard" class="rounded-[18px] bg-[#0A0A0A] text-white p-5 fade-up" style="display:none">
              <div class="text-[10px] uppercase tracking-[0.2em] text-white/40">Validación táctil</div>
              <div id="tactileTitle" class="mt-1 text-[22px] font-[200]">LT: 20.5mm ✓ en zona azul</div>
              <div class="mt-1 text-[11px] text-white/50">Stop perpendicular, sin comprimir. Confirma con Rx a 0.5-1mm del vértice.</div>
            </div>

            <!-- Tarjeta de Localizador Integrado -->
            <div class="rounded-[16px] bg-white border border-black/[0.06] p-4 flex gap-3">
              <img 
                src="/images/guias/longitud-trabajo/localizador-apical-pantalla.webp" 
                alt="localizador" 
                class="w-16 h-16 object-cover rounded-[10px] border border-black/10" 
              />
              <div class="text-[11px] leading-[1.5] text-black/50">
                Localizador integrado: cuando veas 0.5 verde, estás en constricción. La lima deja de avanzar por resistencia.
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ==================== PARTE 4: INSTRUMENTAL EN MANO ==================== -->
      <section class="px-6 md:px-10 py-16 md:py-24 border-b border-black/[0.06]">
        <div class="flex justify-between items-baseline">
          <h2 class="text-[11px] uppercase tracking-[0.2em] text-black/30 font-medium">Instrumental en mano · fotos reales</h2>
          <span class="text-[11px] text-black/30 hidden md:block">4:3 object-cover · sin filtros</span>
        </div>

        <div class="mt-10 grid grid-cols-1 md:grid-cols-3 gap-5 md:gap-6">
          <!-- Instrumento 01 -->
          <div class="group rounded-[22px] border border-black/[0.06] bg-white overflow-hidden hover:border-black/10 transition-colors fade-up">
            <div class="aspect-[4/3] overflow-hidden bg-[#F8F8F8]">
              <img 
                src="/images/guias/longitud-trabajo/lima-k10-sondeo.webp" 
                alt="Lima K #10" 
                class="w-full h-full object-cover group-hover:scale-[1.02] transition-transform duration-700" 
              />
            </div>
            <div class="p-5">
              <div class="flex justify-between items-start">
                <span class="text-[11px] tracking-[0.2em] text-black/25 font-medium">01</span>
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-black/[0.04] border border-black/[0.06] text-black/40 font-medium">Sondeo inicial</span>
              </div>
              <div class="mt-3 text-[18px] font-[300] tracking-[-0.02em] leading-[0.95] text-[#0A0A0A]">Lima K #10</div>
              <div class="mt-2 text-[12px] leading-[1.5] text-black/60">Sondeo inicial, sensación táctil</div>
              <div class="mt-3 text-[11px] leading-[1.4] text-black/35 border-l border-black/10 pl-3">Precurva 15° si hay curva. No fuerces.</div>
            </div>
          </div>

          <!-- Instrumento 02 -->
          <div class="group rounded-[22px] border border-black/[0.06] bg-white overflow-hidden hover:border-black/10 transition-colors fade-up" style="animation-delay:0.06s">
            <div class="aspect-[4/3] overflow-hidden bg-[#F8F8F8]">
              <img 
                src="/images/guias/longitud-trabajo/regla-milimetrada-endodoncia.webp" 
                alt="Regla milimetrada" 
                class="w-full h-full object-cover group-hover:scale-[1.02] transition-transform duration-700" 
              />
            </div>
            <div class="p-5">
              <div class="flex justify-between items-start">
                <span class="text-[11px] tracking-[0.2em] text-black/25 font-medium">02</span>
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-black/[0.04] border border-black/[0.06] text-black/40 font-medium">Medir con tope</span>
              </div>
              <div class="mt-3 text-[18px] font-[300] tracking-[-0.02em] leading-[0.95] text-[#0A0A0A]">Regla milimetrada</div>
              <div class="mt-2 text-[12px] leading-[1.5] text-black/60">Medir con tope a 90°</div>
              <div class="mt-3 text-[11px] leading-[1.4] text-black/35 border-l border-black/10 pl-3">Sin comprimir stop. Lee D0 real.</div>
            </div>
          </div>

          <!-- Instrumento 03 -->
          <div class="group rounded-[22px] border border-black/[0.06] bg-white overflow-hidden hover:border-black/10 transition-colors fade-up" style="animation-delay:0.12s">
            <div class="aspect-[4/3] overflow-hidden bg-[#F8F8F8]">
              <img 
                src="/images/guias/longitud-trabajo/acceso-boca-referencia-incisal.webp" 
                alt="Acceso en boca" 
                class="w-full h-full object-cover group-hover:scale-[1.02] transition-transform duration-700" 
              />
            </div>
            <div class="p-5">
              <div class="flex justify-between items-start">
                <span class="text-[11px] tracking-[0.2em] text-black/25 font-medium">03</span>
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-black/[0.04] border border-black/[0.06] text-black/40 font-medium">Referencia</span>
              </div>
              <div class="mt-3 text-[18px] font-[300] tracking-[-0.02em] leading-[0.95] text-[#0A0A0A]">Acceso en boca</div>
              <div class="mt-2 text-[12px] leading-[1.5] text-black/60">Referencia estable: borde incisal</div>
              <div class="mt-3 text-[11px] leading-[1.4] text-black/35 border-l border-black/10 pl-3">Misma referencia siempre. Marca.</div>
            </div>
          </div>

          <!-- Instrumento 04 -->
          <div class="group rounded-[22px] border border-black/[0.06] bg-white overflow-hidden hover:border-black/10 transition-colors fade-up" style="animation-delay:0.18s">
            <div class="aspect-[4/3] overflow-hidden bg-[#F8F8F8]">
              <img 
                src="/images/guias/longitud-trabajo/localizador-apical-pantalla.webp" 
                alt="Localizador" 
                class="w-full h-full object-cover group-hover:scale-[1.02] transition-transform duration-700" 
              />
            </div>
            <div class="p-5">
              <div class="flex justify-between items-start">
                <span class="text-[11px] tracking-[0.2em] text-black/25 font-medium">04</span>
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-[#0066FF]/10 border border-[#0066FF]/20 text-[#0066FF] font-medium">Gold standard</span>
              </div>
              <div class="mt-3 text-[18px] font-[300] tracking-[-0.02em] leading-[0.95] text-[#0A0A0A]">Localizador</div>
              <div class="mt-2 text-[12px] leading-[1.5] text-black/60">Gold standard electrónico</div>
              <div class="mt-3 text-[11px] leading-[1.4] text-black/35 border-l border-black/10 pl-3">Conducto húmedo, no inundado.</div>
            </div>
          </div>

          <!-- Instrumento 05 -->
          <div class="group rounded-[22px] border border-black/[0.06] bg-white overflow-hidden hover:border-black/10 transition-colors fade-up" style="animation-delay:0.24s">
            <div class="aspect-[4/3] overflow-hidden bg-[#F8F8F8]">
              <img 
                src="/images/guias/longitud-trabajo/radiografia-conductometria-vertice.webp" 
                alt="Rx conductometría" 
                class="w-full h-full object-cover group-hover:scale-[1.02] transition-transform duration-700" 
              />
            </div>
            <div class="p-5">
              <div class="flex justify-between items-start">
                <span class="text-[11px] tracking-[0.2em] text-black/25 font-medium">05</span>
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-black/[0.04] border border-black/[0.06] text-black/40 font-medium">Confirmación</span>
              </div>
              <div class="mt-3 text-[18px] font-[300] tracking-[-0.02em] leading-[0.95] text-[#0A0A0A]">Rx conductometría</div>
              <div class="mt-2 text-[12px] leading-[1.5] text-black/60">Confirmación radiográfica</div>
              <div class="mt-3 text-[11px] leading-[1.4] text-black/35 border-l border-black/10 pl-3">Paralelismo, sostenedor.</div>
            </div>
          </div>
        </div>
      </section>

      <!-- ==================== PARTE 5: PROTOCOLO PASO A PASO ==================== -->
      <section class="border-b border-black/[0.06]">
        <div class="px-6 md:px-10 py-12 flex justify-between items-baseline">
          <h2 class="text-[11px] uppercase tracking-[0.2em] text-black/30 font-medium">Protocolo paso a paso · 6 pasos clínicos reales</h2>
          <span class="text-[11px] text-black/30 hidden md:block">scroll para avanzar · click en número</span>
        </div>

        <!-- Barra Sticky de Navegación por Pasos -->
        <div class="hidden md:flex sticky top-[44px] z-20 px-10 py-3 bg-[#FCFCFC]/90 backdrop-blur border-y border-black/[0.06] gap-2">
          <button class="step-btn h-[28px] px-3 rounded-full text-[11px] tracking-wide border transition-all bg-[#0A0A0A] text-white border-black" data-step="0">01 · Rx</button>
          <button class="step-btn h-[28px] px-3 rounded-full text-[11px] tracking-wide border transition-all bg-white border-black/10 text-black/40 hover:text-black/70" data-step="1">02 · Referencia</button>
          <button class="step-btn h-[28px] px-3 rounded-full text-[11px] tracking-wide border transition-all bg-white border-black/10 text-black/40 hover:text-black/70" data-step="2">03 · Lima</button>
          <button class="step-btn h-[28px] px-3 rounded-full text-[11px] tracking-wide border transition-all bg-white border-black/10 text-black/40 hover:text-black/70" data-step="3">04 · Medición</button>
          <button class="step-btn h-[28px] px-3 rounded-full text-[11px] tracking-wide border transition-all bg-white border-black/10 text-black/40 hover:text-black/70" data-step="4">05 · Localizador</button>
          <button class="step-btn h-[28px] px-3 rounded-full text-[11px] tracking-wide border transition-all bg-white border-black/10 text-black/40 hover:text-black/70" data-step="5">06 · Rx</button>
        </div>

        <!-- Bloques de los 6 Pasos -->
        <div class="divide-y divide-black/[0.06]">
          
          <!-- Paso 01 -->
          <div id="step-0" class="step-block grid md:grid-cols-2 gap-0 min-h-[72vh] md:min-h-[80vh] items-stretch" data-index="0">
            <div class="order-1 px-6 md:px-10 py-10 md:py-16 flex flex-col justify-center border-r border-black/[0.04] bg-white">
              <div class="flex items-baseline gap-4">
                <span class="step-num text-[48px] font-[100] tracking-[-0.05em] leading-none text-[#0066FF]">01</span>
                <span class="text-[11px] uppercase tracking-[0.18em] text-black/30">20.5 mm estimados</span>
              </div>
              <h3 class="mt-6 text-[24px] md:text-[28px] font-[200] tracking-[-0.02em] leading-[1.05] max-w-[18ch]">Rx diagnóstica + longitud estimada</h3>
              <div class="mt-6 space-y-4 max-w-[44ch]">
                <div>
                  <div class="text-[11px] uppercase tracking-[0.18em] text-black/30">Qué haces</div>
                  <p class="mt-2 text-[14px] leading-[1.6] text-black/70">Mides en Rx desde borde incisal intacto hasta vértice radiográfico y restas 3mm para tu lima inicial. No uses ápice anatómico.</p>
                </div>
                <div class="rounded-[12px] bg-[#FF4D5A]/[0.06] border border-[#FF4D5A]/[0.14] px-3 py-2">
                  <div class="text-[11px] leading-[1.5] text-[#B91C1C]">Error: Medir hasta la punta del foramen en Rx. Te pasarás 0.5-1mm.</div>
                </div>
              </div>
            </div>
            <div class="order-2 relative bg-[#F7F7F7] overflow-hidden">
              <div class="absolute inset-0 p-4 md:p-6">
                <div class="w-full h-full rounded-[28px] overflow-hidden border border-black/[0.06] bg-white relative transition-transform duration-700">
                  <img src="/images/guias/longitud-trabajo/radiografia-conductometria-vertice.webp" alt="Rx diagnóstica" class="w-full h-full object-cover" />
                  <div class="absolute bottom-0 left-0 right-0 h-[40%] bg-gradient-to-t from-black/25 to-transparent pointer-events-none"></div>
                  <div class="absolute bottom-4 left-4 rounded-full px-3 py-1 bg-white/75 backdrop-blur border border-black/10 text-[10px]">Rx diagnóstica + longitud estimada</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Paso 02 -->
          <div id="step-1" class="step-block grid md:grid-cols-2 gap-0 min-h-[72vh] md:min-h-[80vh] items-stretch opacity-[0.92]" data-index="1">
            <div class="order-1 md:order-2 px-6 md:px-10 py-10 md:py-16 flex flex-col justify-center border-r border-black/[0.04] bg-[#FCFCFC]">
              <div class="flex items-baseline gap-4">
                <span class="step-num text-[48px] font-[100] tracking-[-0.05em] leading-none text-black/15">02</span>
                <span class="text-[11px] uppercase tracking-[0.18em] text-black/30">Borde incisal 21</span>
              </div>
              <h3 class="mt-6 text-[24px] md:text-[28px] font-[200] tracking-[-0.02em] leading-[1.05] max-w-[18ch]">Referencia coronaria estable</h3>
              <div class="mt-6 space-y-4 max-w-[44ch]">
                <div>
                  <div class="text-[11px] uppercase tracking-[0.18em] text-black/30">Qué haces</div>
                  <p class="mt-2 text-[14px] leading-[1.6] text-black/70">Eliges borde incisal o cúspide intacta, sin desgaste. Lo marcas en ficha y no lo cambias en todo el tratamiento.</p>
                </div>
                <div class="rounded-[12px] bg-[#FF4D5A]/[0.06] border border-[#FF4D5A]/[0.14] px-3 py-2">
                  <div class="text-[11px] leading-[1.5] text-[#B91C1C]">Error: Cambiar referencia entre citas. Pierdes 0.5mm y fracasa sellado.</div>
                </div>
              </div>
            </div>
            <div class="order-2 md:order-1 relative bg-[#F7F7F7] overflow-hidden">
              <div class="absolute inset-0 p-4 md:p-6">
                <div class="w-full h-full rounded-[28px] overflow-hidden border border-black/[0.06] bg-white relative transition-transform duration-700">
                  <img src="/images/guias/longitud-trabajo/acceso-boca-referencia-incisal.webp" alt="Referencia coronaria" class="w-full h-full object-cover" />
                  <div class="absolute bottom-0 left-0 right-0 h-[40%] bg-gradient-to-t from-black/25 to-transparent pointer-events-none"></div>
                  <div class="absolute bottom-4 left-4 rounded-full px-3 py-1 bg-white/75 backdrop-blur border border-black/10 text-[10px]">Referencia coronaria estable</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Paso 03 -->
          <div id="step-2" class="step-block grid md:grid-cols-2 gap-0 min-h-[72vh] md:min-h-[80vh] items-stretch opacity-[0.92]" data-index="2">
            <div class="order-1 px-6 md:px-10 py-10 md:py-16 flex flex-col justify-center border-r border-black/[0.04] bg-[#FCFCFC]">
              <div class="flex items-baseline gap-4">
                <span class="step-num text-[48px] font-[100] tracking-[-0.05em] leading-none text-black/15">03</span>
                <span class="text-[11px] uppercase tracking-[0.18em] text-black/30">K #10 - stop 90°</span>
              </div>
              <h3 class="mt-6 text-[24px] md:text-[28px] font-[200] tracking-[-0.02em] leading-[1.05] max-w-[18ch]">Lima K #10 + stop</h3>
              <div class="mt-6 space-y-4 max-w-[44ch]">
                <div>
                  <div class="text-[11px] uppercase tracking-[0.18em] text-black/30">Qué haces</div>
                  <p class="mt-2 text-[14px] leading-[1.6] text-black/70">Colocas stop de silicona ajustado, perpendicular al eje de la lima, sin deformarlo. Lima precurvada levemente si hay curva.</p>
                </div>
                <div class="rounded-[12px] bg-[#FF4D5A]/[0.06] border border-[#FF4D5A]/[0.14] px-3 py-2">
                  <div class="text-[11px] leading-[1.5] text-[#B91C1C]">Error: Stop angulado o comprimido. Lectura falsa +1mm.</div>
                </div>
              </div>
            </div>
            <div class="order-2 relative bg-[#F7F7F7] overflow-hidden">
              <div class="absolute inset-0 p-4 md:p-6">
                <div class="w-full h-full rounded-[28px] overflow-hidden border border-black/[0.06] bg-white relative transition-transform duration-700">
                  <img src="/images/guias/longitud-trabajo/lima-k10-sondeo.webp" alt="Lima K #10 + stop" class="w-full h-full object-cover" />
                  <div class="absolute bottom-0 left-0 right-0 h-[40%] bg-gradient-to-t from-black/25 to-transparent pointer-events-none"></div>
                  <div class="absolute bottom-4 left-4 rounded-full px-3 py-1 bg-white/75 backdrop-blur border border-black/10 text-[10px]">Lima K #10 + stop</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Paso 04 -->
          <div id="step-3" class="step-block grid md:grid-cols-2 gap-0 min-h-[72vh] md:min-h-[80vh] items-stretch opacity-[0.92]" data-index="3">
            <div class="order-1 md:order-2 px-6 md:px-10 py-10 md:py-16 flex flex-col justify-center border-r border-black/[0.04] bg-[#FCFCFC]">
              <div class="flex items-baseline gap-4">
                <span class="step-num text-[48px] font-[100] tracking-[-0.05em] leading-none text-black/15">04</span>
                <span class="text-[11px] uppercase tracking-[0.18em] text-black/30">21.0 mm reales</span>
              </div>
              <h3 class="mt-6 text-[24px] md:text-[28px] font-[200] tracking-[-0.02em] leading-[1.05] max-w-[18ch]">Medición con regla</h3>
              <div class="mt-6 space-y-4 max-w-[44ch]">
                <div>
                  <div class="text-[11px] uppercase tracking-[0.18em] text-black/30">Qué haces</div>
                  <p class="mt-2 text-[14px] leading-[1.6] text-black/70">Llevas lima a regla endodóntica. Lees desde punta D0 hasta base del stop, sin estirar. Calibras cada vez.</p>
                </div>
                <div class="rounded-[12px] bg-[#FF4D5A]/[0.06] border border-[#FF4D5A]/[0.14] px-3 py-2">
                  <div class="text-[11px] leading-[1.5] text-[#B91C1C]">Error: Medir por encima del stop. Subestimas longitud.</p>
                </div>
              </div>
            </div>
            <div class="order-2 md:order-1 relative bg-[#F7F7F7] overflow-hidden">
              <div class="absolute inset-0 p-4 md:p-6">
                <div class="w-full h-full rounded-[28px] overflow-hidden border border-black/[0.06] bg-white relative transition-transform duration-700">
                  <img src="/images/guias/longitud-trabajo/regla-milimetrada-endodoncia.webp" alt="Medición con regla" class="w-full h-full object-cover" />
                  <div class="absolute bottom-0 left-0 right-0 h-[40%] bg-gradient-to-t from-black/25 to-transparent pointer-events-none"></div>
                  <div class="absolute bottom-4 left-4 rounded-full px-3 py-1 bg-white/75 backdrop-blur border border-black/10 text-[10px]">Medición con regla</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Paso 05 -->
          <div id="step-4" class="step-block grid md:grid-cols-2 gap-0 min-h-[72vh] md:min-h-[80vh] items-stretch opacity-[0.92]" data-index="4">
            <div class="order-1 px-6 md:px-10 py-10 md:py-16 flex flex-col justify-center border-r border-black/[0.04] bg-[#FCFCFC]">
              <div class="flex items-baseline gap-4">
                <span class="step-num text-[48px] font-[100] tracking-[-0.05em] leading-none text-black/15">05</span>
                <span class="text-[11px] uppercase tracking-[0.18em] text-black/30">0.5 mm constricción</span>
              </div>
              <h3 class="mt-6 text-[24px] md:text-[28px] font-[200] tracking-[-0.02em] leading-[1.05] max-w-[18ch]">Localizador apical</h3>
              <div class="mt-6 space-y-4 max-w-[44ch]">
                <div>
                  <div class="text-[11px] uppercase tracking-[0.18em] text-black/30">Qué haces</div>
                  <p class="mt-2 text-[14px] leading-[1.6] text-black/70">Conectas clip labial, lima al gancho. Avanzas lento hasta 00 APEX (pitido largo), retrocedes hasta marca 0.5 verde.</p>
                </div>
                <div class="rounded-[12px] bg-[#FF4D5A]/[0.06] border border-[#FF4D5A]/[0.14] px-3 py-2">
                  <div class="text-[11px] leading-[1.5] text-[#B91C1C]">Error: Conducto seco o inundado con hipoclorito puro. Marca errática.</div>
                </div>
              </div>
            </div>
            <div class="order-2 relative bg-[#F7F7F7] overflow-hidden">
              <div class="absolute inset-0 p-4 md:p-6">
                <div class="w-full h-full rounded-[28px] overflow-hidden border border-black/[0.06] bg-white relative transition-transform duration-700">
                  <img src="/images/guias/longitud-trabajo/localizador-apical-pantalla.webp" alt="Localizador apical" class="w-full h-full object-cover" />
                  <div class="absolute bottom-0 left-0 right-0 h-[40%] bg-gradient-to-t from-black/25 to-transparent pointer-events-none"></div>
                  <div class="absolute bottom-4 left-4 rounded-full px-3 py-1 bg-white/75 backdrop-blur border border-black/10 text-[10px]">Localizador apical</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Paso 06 (Double image: boca + rx) -->
          <div id="step-5" class="step-block grid md:grid-cols-2 gap-0 min-h-[72vh] md:min-h-[80vh] items-stretch opacity-[0.92]" data-index="5">
            <div class="order-1 md:order-2 px-6 md:px-10 py-10 md:py-16 flex flex-col justify-center border-r border-black/[0.04] bg-[#FCFCFC]">
              <div class="flex items-baseline gap-4">
                <span class="step-num text-[48px] font-[100] tracking-[-0.05em] leading-none text-black/15">06</span>
                <span class="text-[11px] uppercase tracking-[0.18em] text-black/30">LT definitiva 20.5 mm</span>
              </div>
              <h3 class="mt-6 text-[24px] md:text-[28px] font-[200] tracking-[-0.02em] leading-[1.05] max-w-[18ch]">Rx conductometría y LT definitiva</h3>
              <div class="mt-6 space-y-4 max-w-[44ch]">
                <div>
                  <div class="text-[11px] uppercase tracking-[0.18em] text-black/30">Qué haces</div>
                  <p class="mt-2 text-[14px] leading-[1.6] text-black/70">LT = longitud marcada por localizador. Confirmas en Rx que la lima queda 0.5-1mm corta del vértice Rx. Documentas.</p>
                </div>
                <div class="rounded-[12px] bg-[#FF4D5A]/[0.06] border border-[#FF4D5A]/[0.14] px-3 py-2">
                  <div class="text-[11px] leading-[1.5] text-[#B91C1C]">Error: Dejar lima en ápice Rx pensando que es constricción.</div>
                </div>
              </div>
            </div>
            <div class="order-2 md:order-1 relative bg-[#F7F7F7] overflow-hidden">
              <div class="absolute inset-0 p-4 md:p-6">
                <div class="w-full h-full rounded-[28px] overflow-hidden border border-black/[0.06] bg-white relative transition-transform duration-700">
                  <div class="grid grid-cols-2 h-full">
                    <img src="/images/guias/longitud-trabajo/acceso-boca-referencia-incisal.webp" class="w-full h-full object-cover" alt="boca mano" />
                    <img src="/images/guias/longitud-trabajo/radiografia-conductometria-vertice.webp" class="w-full h-full object-cover border-l border-black/10" alt="rx" />
                  </div>
                  <div class="absolute top-4 left-4 rounded-full px-2.5 py-1 bg-white/80 backdrop-blur border border-black/10 text-[10px]">LT definitiva</div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </section>

      <!-- ==================== FOOTER: CHECKLIST CLÍNICO CORRIDO ==================== -->
      <footer class="px-6 md:px-10 py-10 bg-white border-t border-black/[0.06]">
        <div class="flex flex-col md:flex-row gap-8 justify-between">
          <div class="max-w-[58ch]">
            <div class="text-[10px] uppercase tracking-[0.2em] text-black/25">Checklist clínico corrido · sin botones gordos</div>
            <p class="mt-3 text-[12px] leading-[1.8] tracking-[-0.01em] text-black/60">
              <span class="text-black font-semibold">Rx diagnóstica</span> mide borde incisal→vértice Rx −3mm → elige <span class="text-black font-semibold">referencia estable</span> (borde incisal 21) → <span class="text-black font-semibold">lima K #10</span> pasiva + stop a 90° sin deformar → <span class="text-black font-semibold">regla</span> lectura D0→base stop → <span class="text-black font-semibold">localizador</span> conducto húmedo, avanza a 00 APEX y retrocede a 0.5mm → <span class="text-[#0066FF] font-semibold">LT = APEX −0.5mm</span> → <span class="text-black font-semibold">Rx conductometría</span> 0.5-1mm corta de ápice Rx → documenta referencia + LT definitiva → obtura a LT. Falla si confundes ápice Rx con constricción.
            </p>
          </div>
          <div class="text-[10px] leading-[1.7] text-black/30 max-w-[34ch]">
            <div class="font-medium text-black/50">LT — ENDO / V3 · fotos reales clínicas</div>
            <div class="mt-1">Imágenes: lima-k10 · regla-milimetrada · boca-tipodonto · localizador · radiografia</div>
            <div class="mt-2">Diseño: #FCFCFC · Inter 100/200/300 · acento #0066FF · glass 18px · border 1px rgba(0,0,0,0.06) · drag + scroll storytelling</div>
            <div class="mt-2 text-black/40">© 2026 · clínica real, no placeholder</div>
          </div>
        </div>
      </footer>

    </div>
  </div>
</BaseLayout>

<script is:inline>
(function() {
  // 1. Parallax suave en Hero
  const heroParallax = document.getElementById('heroParallax');
  if (heroParallax) {
    window.addEventListener('scroll', () => {
      const scrollY = window.scrollY;
      if (scrollY < 800) {
        heroParallax.style.transform = `translateY(${scrollY * -0.04}px)`;
      }
    }, { passive: true });
  }

  // 2. Simulador gestual minimal del conducto apical
  const container = document.getElementById('canalContainer');
  const fileLine = document.getElementById('fileLine');
  const fileHandle = document.getElementById('fileHandle');
  const fileStopBadge = document.getElementById('fileStopBadge');
  const scaleTickActive = document.getElementById('scaleTickActive');

  const statusIconRing = document.getElementById('statusIconRing');
  const statusIconDot = document.getElementById('statusIconDot');
  const statusLabel = document.getElementById('statusLabel');
  const statusDesc = document.getElementById('statusDesc');
  const depthBadge = document.getElementById('depthBadge');
  const workLengthVal = document.getElementById('workLengthVal');
  const tactileCard = document.getElementById('tactileCard');
  const tactileTitle = document.getElementById('tactileTitle');

  if (container && fileLine && fileHandle) {
    let depth = 20.2;
    let isDragging = false;

    function getStatus(l) {
      if (l < 19.5) return { label: 'lejos', color: '#A1A1AA', desc: '2.0+ mm · busca conducto', inZone: false };
      if (l < 20.6) return { label: 'cerca', color: '#EAB308', desc: '~1.0 mm · amarillo', inZone: false };
      if (l < 21.5) return { label: 'constricción', color: '#0066FF', desc: '0.5 mm · zona ideal', inZone: true };
      if (l < 22.2) return { label: 'apex', color: '#EF4444', desc: '0.0 APEX · foramen', inZone: false };
      return { label: 'sobre', color: '#991B1B', desc: 'sobrepasado · retrocede', inZone: false };
    }

    function updateVisuals(l) {
      const status = getStatus(l);
      const needleHeightPercent = ((l - 18) / 5.2) * 84;
      const topOffsetPercent = 6 + needleHeightPercent;
      const rulerTickPercent = ((l - 18) / 5.2) * 100;
      const workLength = (l - 0.5).toFixed(1);

      fileLine.style.height = `${needleHeightPercent}%`;
      fileHandle.style.top = `${topOffsetPercent}%`;
      fileStopBadge.style.top = `${topOffsetPercent}%`;
      scaleTickActive.style.top = `${rulerTickPercent}%`;

      statusIconRing.style.borderColor = status.color;
      statusIconRing.style.boxShadow = status.label === 'constricción' ? `0 0 24px ${status.color}55` : 'none';
      statusIconDot.style.background = status.color;
      statusIconDot.style.transform = status.inZone ? 'scale(1.25)' : 'scale(1)';

      statusLabel.textContent = status.label;
      statusDesc.textContent = status.desc;
      depthBadge.textContent = `${l.toFixed(1)} mm`;

      if (status.inZone) {
        depthBadge.className = 'ml-auto px-3 py-1 rounded-full text-[11px] border bg-[#0066FF] text-white border-[#0066FF] font-semibold';
      } else {
        depthBadge.className = 'ml-auto px-3 py-1 rounded-full text-[11px] border bg-white border-black/10 text-black/30';
      }

      workLengthVal.textContent = workLength;

      if (tactileCard && tactileTitle) {
        if (status.inZone) {
          tactileCard.style.display = 'block';
          tactileTitle.textContent = `LT: ${workLength}mm ✓ en zona azul`;
        } else {
          tactileCard.style.display = 'none';
        }
      }
    }

    function handlePointer(e) {
      if (!isDragging || !container) return;
      const rect = container.getBoundingClientRect();
      const offsetY = e.clientY - rect.top;
      let newDepth = 18 + Math.max(0, Math.min(1, offsetY / rect.height)) * 5.2;

      // Resistencia táctil / Snap en constricción (20.6 a 21.6 mm)
      if (newDepth > 20.6 && newDepth < 21.6) {
        newDepth = newDepth * 0.55 + 9.495;
      }

      updateVisuals(newDepth);
    }

    container.addEventListener('pointerdown', (e) => {
      isDragging = true;
      handlePointer(e);
    });

    window.addEventListener('pointermove', (e) => {
      if (isDragging) handlePointer(e);
    });

    window.addEventListener('pointerup', () => {
      isDragging = false;
    });

    // Iniciar con 20.2mm
    updateVisuals(depth);
  }

  // 3. ScrollSpy e interactividad de los 6 Pasos
  const stepBtns = document.querySelectorAll('.step-btn');
  const stepBlocks = document.querySelectorAll('.step-block');

  stepBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      const idx = btn.getAttribute('data-step');
      const targetBlock = document.getElementById(`step-${idx}`);
      if (targetBlock) {
        targetBlock.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  });

  if ('IntersectionObserver' in window && stepBlocks.length > 0) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const idx = entry.target.getAttribute('data-index');
          
          stepBtns.forEach((b) => {
            if (b.getAttribute('data-step') === idx) {
              b.className = 'step-btn h-[28px] px-3 rounded-full text-[11px] tracking-wide border transition-all bg-[#0A0A0A] text-white border-black';
            } else {
              b.className = 'step-btn h-[28px] px-3 rounded-full text-[11px] tracking-wide border transition-all bg-white border-black/10 text-black/40 hover:text-black/70';
            }
          });

          stepBlocks.forEach((sb) => {
            const blockNum = sb.querySelector('.step-num');
            const cardInner = sb.querySelector('.order-1');
            if (sb.getAttribute('data-index') === idx) {
              sb.classList.remove('opacity-[0.92]');
              if (blockNum) {
                blockNum.style.color = '#0066FF';
              }
              if (cardInner) {
                cardInner.style.backgroundColor = '#FFFFFF';
              }
            } else {
              sb.classList.add('opacity-[0.92]');
              if (blockNum) {
                blockNum.style.color = 'rgba(0,0,0,0.15)';
              }
              if (cardInner) {
                cardInner.style.backgroundColor = '#FCFCFC';
              }
            }
          });
        }
      });
    }, { rootMargin: '-40% 0px -40% 0px', threshold: 0 });

    stepBlocks.forEach((sb) => observer.observe(sb));
  }
})();
</script>
'''

with open('src/pages/guias/longitud-trabajo-endodoncia.astro', 'w', encoding='utf-8') as f:
    f.write(astro_code)

print('Updated src/pages/guias/longitud-trabajo-endodoncia.astro successfully!')
