import os

astro_content = """---
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
  <div class="endo-page min-h-screen bg-[#FCFCFC] text-[#0A0A0A] antialiased selection:bg-[#0066FF]/10 overflow-x-hidden">
    
    <!-- Subheader Glassmorphism Sticky -->
    <div class="sticky top-0 z-40 backdrop-blur-[20px] bg-[#FCFCFC]/80 border-b border-black/[0.06] px-6 md:px-10 h-[46px] flex items-center justify-between">
      <div class="flex items-center gap-3">
        <a href="/#academia" class="text-[11px] text-black/40 hover:text-[#0066FF] transition-colors">← Academia</a>
        <span class="text-black/20">/</span>
        <div class="text-[10px] uppercase tracking-[0.2em] text-black/50 font-medium">LT · ENDO / V3 clínica real</div>
      </div>
      <div class="hidden sm:flex items-center gap-4 text-[11px] text-black/40">
        <span>mano + boca + diente</span>
        <span class="w-1 h-1 rounded-full bg-black/20"></span>
        <span>protocolo real</span>
        <span class="w-1 h-1 rounded-full bg-[#0066FF]"></span>
        <span class="text-[#0066FF] font-medium">constricción no ápice</span>
      </div>
    </div>

    <div class="max-w-[1240px] mx-auto">
      
      <!-- ==================== PARTE 1: HERO CONCEPTUAL ==================== -->
      <section class="relative px-6 md:px-10 pt-12 md:pt-16 pb-14 md:pb-20 grid md:grid-cols-[1.05fr_0.95fr] gap-10 md:gap-12 items-center border-b border-black/[0.06]">
        <div class="fade-up">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#0066FF]/10 border border-[#0066FF]/20 text-[#0066FF] text-[11px] font-medium tracking-wide mb-6">
            <span>●</span> Endodoncia Clínica & Conductometría
          </div>
          <h1 class="text-[11vw] md:text-[6.5vw] font-[200] leading-[0.88] tracking-[-0.05em]">
            Longitud<br />de trabajo
          </h1>
          <div class="mt-6 flex items-start gap-4">
            <div class="mt-2 h-[1px] w-12 bg-black/10 shrink-0"></div>
            <p class="text-[14px] leading-[1.6] tracking-[-0.01em] text-black/60 max-w-[44ch]">
              De la referencia coronaria a la <span class="text-[#0A0A0A] font-medium">constricción apical</span>. 0.5-1mm del ápice radiográfico. 0.5mm definen el éxito endodóntico.
            </p>
          </div>
          <div class="mt-8 flex flex-wrap gap-6 text-[12px] leading-[1.6] max-w-[48ch]">
            <div class="text-black/40">
              LT = distancia <br />
              <span class="text-black font-medium">borde incisal → constricción</span>
            </div>
            <div class="h-8 w-[1px] bg-black/10"></div>
            <div class="text-black/40">
              No es vértice Rx. <br />
              <span class="text-[#0066FF] font-semibold">LT = APEX −0.5mm</span>
            </div>
          </div>
        </div>

        <div class="relative fade-up" style="animation-delay:0.15s">
          <div class="relative rounded-[32px] overflow-hidden border border-black/[0.06] bg-white aspect-[4/3] md:aspect-[1.15/1]">
            <img 
              src="/images/guias/longitud-trabajo/acceso-boca-referencia-incisal.webp" 
              alt="Mano con guante insertando lima en tipodonto - boca y diente" 
              class="w-full h-full object-cover"
              loading="eager"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent pointer-events-none"></div>
            <div class="absolute top-4 left-4 md:top-6 md:left-6 rounded-full px-3 py-1.5 bg-white/80 backdrop-blur-[18px] border border-black/[0.06] text-[10px] uppercase tracking-[0.14em] text-black/70 font-semibold">
              Endodoncia • Protocolo real
            </div>
            <div class="absolute bottom-4 left-4 right-4 md:bottom-6 md:left-6 md:right-6 flex justify-between items-end">
              <div class="rounded-[16px] px-3.5 py-2.5 bg-[#0A0A0A]/85 backdrop-blur text-white text-[11px] leading-[1.4] max-w-[26ch]">
                Manos con guante azul, abrebocas, tipodonto 21. Referencia: borde incisal.
              </div>
              <div class="rounded-full w-9 h-9 bg-white/90 backdrop-blur grid place-items-center border border-black/10 text-[11px] font-bold">
                21
              </div>
            </div>
          </div>
          <div class="mt-3 text-[10px] text-black/30 tracking-wide">
            Figura A — mano, diente y boca real. Registro clínico estandarizado.
          </div>
        </div>
      </section>

      <!-- ==================== PARTE 1B: ANATOMÍA & POR QUÉ FALLA ==================== -->
      <section class="px-6 md:px-10 py-14 md:py-20 grid md:grid-cols-[0.9fr_1.1fr] gap-12 md:gap-16 border-b border-black/[0.06]">
        <div>
          <div class="text-[11px] uppercase tracking-[0.2em] text-black/30 font-medium">Qué es y por qué falla</div>
          <h2 class="mt-4 text-[28px] md:text-[36px] font-[200] tracking-[-0.03em] leading-[1.05]">
            No es hasta donde se ve en la Rx. Es hasta donde termina el conducto.
          </h2>
          <div class="mt-6 space-y-4 text-[13px] leading-[1.7] text-black/60 max-w-[46ch]">
            <p>
              <strong class="text-black font-semibold">Longitud de trabajo</strong> es la distancia entre un punto coronario estable (borde incisal, cúspide) y la constricción apical (unión CDC), donde el conducto es más estrecho. Está 0.5-1mm corta del vértice radiográfico.
            </p>
            <p>
              El ápice radiográfico es vértice anatómico de la raíz en la imagen. El foramen mayor suele estar 0.2-0.5mm lateral. Si instrumentas hasta Rx, sobreinstrumentas, extruyes, lesionas periodonto.
            </p>
            <div class="pt-2 flex flex-wrap gap-3 text-[11px]">
              <div class="px-3 py-1 rounded-full bg-black/[0.04] border border-black/[0.06] text-black/70 font-medium">Constricción 0.5mm</div>
              <div class="px-3 py-1 rounded-full bg-[#0066FF]/10 border border-[#0066FF]/20 text-[#0066FF] font-semibold">LT = APEX −0.5</div>
            </div>
          </div>
        </div>

        <div class="rounded-[28px] border border-black/[0.06] bg-white p-6 md:p-10 flex flex-col md:flex-row gap-8 items-center">
          <div class="shrink-0">
            <svg viewBox="0 0 180 320" class="w-[140px] md:w-[170px] h-auto" aria-label="Diagrama esquemático de constricción apical">
              <path d="M55 10 C30 40 28 105 62 130 C50 175 68 245 82 285 C88 295 92 295 98 285 C112 245 130 175 118 130 C152 105 150 40 125 10 C110 -2 70 -2 55 10Z" fill="none" stroke="rgba(0,0,0,0.12)" stroke-width="1.5"></path>
              <path d="M90 20 C88 80 86 160 90 265" stroke="#FF4D5A" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="6 4" opacity="0.35" fill="none"></path>
              <line x1="28" y1="18" x2="152" y2="18" stroke="rgba(0,0,0,0.2)" stroke-width="0.8" stroke-dasharray="3 3"></line>
              <text x="10" y="16" font-size="8" fill="rgba(0,0,0,0.4)" font-weight="400">ref. coronaria</text>
              <g>
                <ellipse cx="90" cy="248" rx="16" ry="4" fill="none" stroke="#0066FF" stroke-width="1.2" opacity="0.8"></ellipse>
                <circle cx="90" cy="248" r="2.2" fill="#0066FF"></circle>
                <text x="112" y="251" font-size="8" fill="#0066FF" font-weight="600">constricción</text>
              </g>
              <g>
                <circle cx="90" cy="285" r="2.8" fill="none" stroke="rgba(0,0,0,0.25)" stroke-width="1"></circle>
                <text x="112" y="288" font-size="8" fill="rgba(0,0,0,0.45)">vértice Rx</text>
              </g>
              <line x1="72" y1="250" x2="72" y2="283" stroke="#0066FF" stroke-width="0.7" stroke-dasharray="2 2"></line>
              <text x="36" y="270" font-size="7.5" fill="#0066FF" font-weight="600">0.5-1mm</text>
              <text x="90" y="312" text-anchor="middle" font-size="9" fill="rgba(0,0,0,0.6)" font-weight="600">LT = APEX −0.5mm</text>
            </svg>
          </div>
          <div class="text-[12px] leading-[1.6] text-black/60 max-w-[32ch]">
            <div class="text-[11px] uppercase tracking-[0.18em] text-black/40 font-semibold">Por qué fallas comunes</div>
            <ul class="mt-3 space-y-2 list-disc pl-4 text-black/70">
              <li>Confundes ápice Rx con constricción → sobreobturas.</li>
              <li>Cambias referencia → LT varía 0.5-2mm.</li>
              <li>Stop angulado → lees mal en regla.</li>
              <li>Localizador con conducto inundado → marca errática.</li>
            </ul>
            <div class="mt-4 text-[11px] text-black/40 font-medium">Esquema suizo minimal, no anatómico pesado.</div>
          </div>
        </div>
      </section>

      <!-- ==================== PARTE 2: ¡EMULADOR APICAL PRIORIZADO! ==================== -->
      <section id="emulador" class="px-6 md:px-10 py-14 md:py-20 border-b border-black/[0.06] grid md:grid-cols-[1.1fr_0.9fr] gap-10 md:gap-16 items-start bg-[#FAFBFD]/50">
        <!-- Columna Interactiva del Conducto -->
        <div 
          id="canalContainer" 
          class="relative h-[64vh] md:h-[82vh] rounded-[32px] border border-black/[0.06] bg-white overflow-hidden select-none touch-none cursor-ns-resize shadow-sm"
        >
          <img 
            src="/images/guias/longitud-trabajo/lima-k10-sondeo.webp" 
            alt="" 
            class="absolute inset-0 w-full h-full object-cover opacity-[0.09] pointer-events-none" 
          />
          <div class="absolute inset-0 grid place-items-center pointer-events-none">
            <svg viewBox="0 0 200 420" class="w-[46%] md:w-[38%] h-auto drop-shadow-[0_20px_30px_rgba(0,0,0,0.06)]">
              <defs>
                <linearGradient id="toothGradient" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stop-color="white" stop-opacity="0.95"></stop>
                  <stop offset="100%" stop-color="#E8EFFF" stop-opacity="0.55"></stop>
                </linearGradient>
              </defs>
              <path d="M60 12 C24 52 22 132 66 162 C52 212 72 312 84 362 C92 376 108 376 116 362 C128 312 148 212 134 162 C178 132 176 52 140 12 C122 -6 78 -6 60 12Z" fill="url(#toothGradient)" stroke="rgba(0,0,0,0.1)" stroke-width="1.4"></path>
              <path d="M100 20 C98 120 92 220 98 350" stroke="#FF2A3A" stroke-opacity="0.3" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="8 6" fill="none"></path>
              <ellipse cx="99" cy="328" rx="14" ry="4.2" fill="none" stroke="#0066FF" stroke-width="1.2" opacity="0.8"></ellipse>
            </svg>
          </div>

          <!-- Línea y Handle del Stop de la Lima -->
          <div class="absolute left-1/2 top-0 bottom-0 w-[1px] bg-black/10">
            <div id="fileLine" class="absolute w-[2.5px] -left-[0.75px] bg-[#0A0A0A]"></div>
            <div id="fileHandle" class="absolute left-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-[#0A0A0A] border-2 border-white shadow-[0_8px_20px_rgba(0,0,0,0.25)] grid place-items-center cursor-grab active:cursor-grabbing">
              <div class="w-2 h-2 rounded-full bg-white"></div>
            </div>
            <div id="fileStopBadge" class="absolute left-7 -translate-y-1/2 px-2.5 py-1 rounded-full bg-white border border-black/10 text-[10px] font-bold shadow-sm pointer-events-none">
              stop
            </div>
          </div>

          <!-- Escala Milimétrica a la Derecha -->
          <div class="absolute right-4 md:right-8 top-[6%] bottom-[6%] w-[1px] bg-black/10">
            <div class="absolute -left-8 flex items-center gap-2" style="top:0%">
              <span class="text-[9px] tracking-widest text-black/30 font-medium">18</span>
              <div class="w-2 h-[1px] bg-black/20"></div>
            </div>
            <div class="absolute -left-8 flex items-center gap-2" style="top:19.23%">
              <span class="text-[9px] tracking-widest text-black/30 font-medium">19</span>
              <div class="w-2 h-[1px] bg-black/20"></div>
            </div>
            <div class="absolute -left-8 flex items-center gap-2" style="top:38.46%">
              <span class="text-[9px] tracking-widest text-black/30 font-medium">20</span>
              <div class="w-2 h-[1px] bg-black/20"></div>
            </div>
            <div class="absolute -left-8 flex items-center gap-2" style="top:57.69%">
              <span class="text-[9px] tracking-widest text-black/30 font-medium">21</span>
              <div class="w-2 h-[1px] bg-black/20"></div>
            </div>
            <div class="absolute -left-8 flex items-center gap-2" style="top:76.92%">
              <span class="text-[9px] tracking-widest text-black/30 font-medium">22</span>
              <div class="w-2 h-[1px] bg-black/20"></div>
            </div>
            <div class="absolute -left-8 flex items-center gap-2" style="top:100%">
              <span class="text-[9px] tracking-widest text-black/30 font-medium">23</span>
              <div class="w-2 h-[1px] bg-black/20"></div>
            </div>
            <!-- Indicador actual de la escala -->
            <div id="scalePointer" class="absolute -left-[6px] w-[13px] h-[2px] bg-[#0066FF] transition-all duration-75"></div>
          </div>

          <div class="absolute bottom-5 left-6 md:left-8 text-[11px] text-black/40 font-medium flex items-center gap-2">
            <span>↕</span> arrastra la lima · siente el snap en la constricción azul
          </div>
        </div>

        <!-- Columna de Feedback y Lectura en Tiempo Real -->
        <div class="md:sticky md:top-[74px]">
          <div class="inline-flex items-center gap-2 text-[11px] uppercase tracking-[0.2em] text-[#0066FF] font-semibold">
            <span class="w-2 h-2 rounded-full bg-[#0066FF] animate-pulse"></span>
            Simulador Gestual Apical & Localizador Digital
          </div>
          <h3 class="mt-3 text-[30px] md:text-[38px] font-[200] tracking-[-0.03em] leading-[0.98]">
            Arrastra.<br />Siente la constricción.
          </h3>

          <div class="mt-8 space-y-6">
            <!-- Indicador de Zona y Status -->
            <div class="flex items-center gap-4">
              <div id="statusIconRing" class="w-14 h-14 rounded-full border grid place-items-center transition-all duration-300">
                <div id="statusIconDot" class="w-3.5 h-3.5 rounded-full transition-all duration-300"></div>
              </div>
              <div>
                <div id="statusLabel" class="text-[22px] font-[300] capitalize leading-none text-[#0A0A0A]"></div>
                <div id="statusDesc" class="mt-1 text-[11px] text-black/50 font-medium"></div>
              </div>
              <div id="depthBadge" class="ml-auto px-3.5 py-1.5 rounded-full text-[12px] font-bold border transition-colors">
                -- mm
              </div>
            </div>

            <div class="h-[1px] bg-black/[0.06]"></div>

            <!-- Lectura de Longitud de Trabajo -->
            <div>
              <div class="text-[11px] uppercase tracking-[0.2em] text-black/35 font-medium">Longitud de trabajo recomendada</div>
              <div class="mt-3 flex items-baseline gap-2">
                <span id="workLengthVal" class="text-[54px] font-[200] tracking-[-0.04em] leading-none text-[#0A0A0A]">--</span>
                <span class="text-[14px] text-black/40 font-medium">mm</span>
                <span class="text-[11px] text-black/30 font-semibold">= APEX −0.5mm</span>
              </div>
              <p class="mt-3 text-[12px] leading-[1.65] text-black/55 max-w-[36ch]">
                Respaldo clínico real: la referencia coronaria fija es el borde incisal. El localizador electrónico calibra la impedancia tisular hasta la constricción CDC.
              </p>
            </div>

            <!-- Alerta táctil en zona óptima -->
            <div id="tactileCard" class="rounded-[20px] bg-[#0A0A0A] text-white p-5 fade-up transition-all duration-300">
              <div class="text-[10px] uppercase tracking-[0.2em] text-white/40 font-semibold">Validación táctil y electrónica</div>
              <div id="tactileTitle" class="mt-1 text-[20px] font-[200]">LT: -- mm ✓ en zona azul</div>
              <div class="mt-1 text-[11px] text-white/60 leading-relaxed">
                Stop perpendicular, sin comprimir. Confirma con radiografía periapical a 0.5-1mm del vértice anatómico.
              </div>
            </div>

            <!-- Badge de Localizador Integrado -->
            <div class="rounded-[18px] bg-white border border-black/[0.06] p-4 flex gap-4 items-center shadow-xs">
              <img 
                src="/images/guias/longitud-trabajo/localizador-apical-pantalla.webp" 
                alt="Localizador apical" 
                class="w-16 h-16 object-cover rounded-[12px] border border-black/10 shrink-0" 
              />
              <div class="text-[11px] leading-[1.5] text-black/60">
                <strong class="text-black font-semibold">Localizador integrado:</strong> cuando veas 0.5 verde en la pantalla, has alcanzado la constricción fisiológica. La lima percibe resistencia apical pasiva.
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ==================== PARTE 3: INSTRUMENTAL EN MANO ==================== -->
      <section class="px-6 md:px-10 py-14 md:py-20 border-b border-black/[0.06]">
        <div class="flex justify-between items-baseline mb-8">
          <div>
            <div class="text-[11px] uppercase tracking-[0.2em] text-black/30 font-medium">Instrumental en mano</div>
            <h2 class="mt-2 text-[26px] md:text-[32px] font-[200] tracking-[-0.03em] text-[#0A0A0A]">
              El equipo esencial en bandeja clínica
            </h2>
          </div>
          <span class="text-[11px] text-black/30 hidden md:block">Registro fotográfico real · sin filtros</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 md:gap-6">
          <!-- Item 01 -->
          <div class="group rounded-[22px] border border-black/[0.06] bg-white overflow-hidden hover:border-black/15 transition-all">
            <div class="aspect-[4/3] overflow-hidden bg-[#F8F8F8]">
              <img 
                src="/images/guias/longitud-trabajo/lima-k10-sondeo.webp" 
                alt="Lima K #10" 
                class="w-full h-full object-cover group-hover:scale-[1.02] transition-transform duration-500" 
              />
            </div>
            <div class="p-5">
              <div class="flex justify-between items-start">
                <span class="text-[11px] tracking-[0.2em] text-black/30 font-semibold">01</span>
                <span class="text-[10px] px-2.5 py-0.5 rounded-full bg-black/[0.04] border border-black/[0.06] text-black/50 font-medium">Sondeo inicial</span>
              </div>
              <div class="mt-3 text-[18px] font-[300] tracking-[-0.02em] leading-tight text-[#0A0A0A]">Lima K #10</div>
              <div class="mt-2 text-[12px] leading-[1.5] text-black/60">Sondeo inicial y sensación táctil del conducto.</div>
              <div class="mt-3 text-[11px] leading-[1.4] text-black/40 border-l border-black/10 pl-3">Precurva 15° si hay curvatura. No fuerces apicalmente.</div>
            </div>
          </div>

          <!-- Item 02 -->
          <div class="group rounded-[22px] border border-black/[0.06] bg-white overflow-hidden hover:border-black/15 transition-all">
            <div class="aspect-[4/3] overflow-hidden bg-[#F8F8F8]">
              <img 
                src="/images/guias/longitud-trabajo/regla-milimetrada-endodoncia.webp" 
                alt="Regla milimetrada" 
                class="w-full h-full object-cover group-hover:scale-[1.02] transition-transform duration-500" 
              />
            </div>
            <div class="p-5">
              <div class="flex justify-between items-start">
                <span class="text-[11px] tracking-[0.2em] text-black/30 font-semibold">02</span>
                <span class="text-[10px] px-2.5 py-0.5 rounded-full bg-black/[0.04] border border-black/[0.06] text-black/50 font-medium">Medición 90°</span>
              </div>
              <div class="mt-3 text-[18px] font-[300] tracking-[-0.02em] leading-tight text-[#0A0A0A]">Regla milimetrada</div>
              <div class="mt-2 text-[12px] leading-[1.5] text-black/60">Medir con tope de silicona perpendicular a 90°.</div>
              <div class="mt-3 text-[11px] leading-[1.4] text-black/40 border-l border-black/10 pl-3">Sin comprimir el stop. Lee desde la punta D0 real.</div>
            </div>
          </div>

          <!-- Item 03 -->
          <div class="group rounded-[22px] border border-black/[0.06] bg-white overflow-hidden hover:border-black/15 transition-all">
            <div class="aspect-[4/3] overflow-hidden bg-[#F8F8F8]">
              <img 
                src="/images/guias/longitud-trabajo/localizador-apical-pantalla.webp" 
                alt="Localizador apical" 
                class="w-full h-full object-cover group-hover:scale-[1.02] transition-transform duration-500" 
              />
            </div>
            <div class="p-5">
              <div class="flex justify-between items-start">
                <span class="text-[11px] tracking-[0.2em] text-black/30 font-semibold">03</span>
                <span class="text-[10px] px-2.5 py-0.5 rounded-full bg-[#0066FF]/10 border border-[#0066FF]/20 text-[#0066FF] font-semibold">Gold Standard</span>
              </div>
              <div class="mt-3 text-[18px] font-[300] tracking-[-0.02em] leading-tight text-[#0A0A0A]">Localizador electrónico</div>
              <div class="mt-2 text-[12px] leading-[1.5] text-black/60">Detección de impedancia multifrecuencia en tiempo real.</div>
              <div class="mt-3 text-[11px] leading-[1.4] text-black/40 border-l border-black/10 pl-3">Conducto húmedo, no inundado en hipoclorito libre.</div>
            </div>
          </div>
        </div>
      </section>

      <!-- ==================== PARTE 4: PROTOCOLO PASO A PASO ==================== -->
      <section class="border-b border-black/[0.06]">
        <div class="px-6 md:px-10 py-12 flex justify-between items-baseline">
          <div>
            <div class="text-[11px] uppercase tracking-[0.2em] text-black/30 font-medium">Protocolo clínico paso a paso</div>
            <h2 class="mt-2 text-[26px] md:text-[34px] font-[200] tracking-[-0.03em] text-[#0A0A0A]">
              Los 6 pasos clínicos reales para conductometría
            </h2>
          </div>
          <span class="text-[11px] text-black/30 hidden md:block">Haz clic en cada paso para revisar</span>
        </div>

        <!-- Barra de Pasos -->
        <div class="flex overflow-x-auto px-6 md:px-10 py-3 bg-[#FCFCFC] border-y border-black/[0.06] gap-2">
          <button class="step-nav-btn active h-[30px] px-3.5 rounded-full text-[11px] font-semibold border transition-all whitespace-nowrap" data-step="0">01 · Rx diagnóstica</button>
          <button class="step-nav-btn h-[30px] px-3.5 rounded-full text-[11px] font-semibold border transition-all whitespace-nowrap" data-step="1">02 · Referencia</button>
          <button class="step-nav-btn h-[30px] px-3.5 rounded-full text-[11px] font-semibold border transition-all whitespace-nowrap" data-step="2">03 · Lima #10</button>
          <button class="step-nav-btn h-[30px] px-3.5 rounded-full text-[11px] font-semibold border transition-all whitespace-nowrap" data-step="3">04 · Regla</button>
          <button class="step-nav-btn h-[30px] px-3.5 rounded-full text-[11px] font-semibold border transition-all whitespace-nowrap" data-step="4">05 · Localizador</button>
          <button class="step-nav-btn h-[30px] px-3.5 rounded-full text-[11px] font-semibold border transition-all whitespace-nowrap" data-step="5">06 · Rx Conductometría</button>
        </div>

        <!-- Tarjetas Detalladas de Pasos -->
        <div id="stepsDeck" class="divide-y divide-black/[0.06]">
          
          <!-- Paso 01 -->
          <div class="step-card grid md:grid-cols-2 gap-0 min-h-[55vh] items-stretch" data-step-index="0">
            <div class="px-6 md:px-10 py-10 md:py-14 flex flex-col justify-center border-r border-black/[0.04] bg-white">
              <div class="flex items-baseline gap-4">
                <span class="text-[44px] font-[100] text-[#0066FF] tracking-[-0.05em] leading-none">01</span>
                <span class="text-[11px] uppercase tracking-[0.18em] text-black/35 font-semibold">20.5 mm estimados</span>
              </div>
              <h3 class="mt-4 text-[24px] md:text-[28px] font-[200] tracking-[-0.02em] leading-tight text-[#0A0A0A]">
                Rx diagnóstica + longitud estimada
              </h3>
              <div class="mt-6 space-y-4 max-w-[44ch]">
                <div>
                  <div class="text-[11px] uppercase tracking-[0.18em] text-black/35 font-medium">Qué haces</div>
                  <p class="mt-2 text-[14px] leading-[1.65] text-black/70">
                    Mides en la radiografía inicial desde el borde incisal intacto hasta el vértice radiográfico y restas 3 mm de margen de seguridad para tu lima inicial de sondeo. No uses el ápice anatómico.
                  </p>
                </div>
                <div class="rounded-[12px] bg-[#FF4D5A]/[0.06] border border-[#FF4D5A]/[0.14] px-3.5 py-2.5">
                  <div class="text-[11px] leading-[1.5] text-[#B91C1C] font-medium">
                    <strong>Error común:</strong> Medir hasta la punta del foramen en Rx sin descontar el margen. Te pasarás 0.5 a 1.0 mm en la instrumentación.
                  </div>
                </div>
              </div>
            </div>
            <div class="relative bg-[#F7F7F7] p-6 flex items-center justify-center">
              <div class="w-full h-full rounded-[24px] overflow-hidden border border-black/[0.06] bg-white relative max-h-[420px]">
                <img src="/images/guias/longitud-trabajo/radiografia-conductometria-vertice.webp" alt="Radiografía diagnóstica" class="w-full h-full object-cover" />
                <div class="absolute bottom-4 left-4 rounded-full px-3 py-1 bg-white/80 backdrop-blur border border-black/10 text-[10px] font-semibold text-black/80">
                  Rx diagnóstica de referencia
                </div>
              </div>
            </div>
          </div>

          <!-- Paso 02 -->
          <div class="step-card grid md:grid-cols-2 gap-0 min-h-[55vh] items-stretch hidden" data-step-index="1">
            <div class="px-6 md:px-10 py-10 md:py-14 flex flex-col justify-center border-r border-black/[0.04] bg-white">
              <div class="flex items-baseline gap-4">
                <span class="text-[44px] font-[100] text-[#0066FF] tracking-[-0.05em] leading-none">02</span>
                <span class="text-[11px] uppercase tracking-[0.18em] text-black/35 font-semibold">Borde incisal 21</span>
              </div>
              <h3 class="mt-4 text-[24px] md:text-[28px] font-[200] tracking-[-0.02em] leading-tight text-[#0A0A0A]">
                Referencia coronaria estable
              </h3>
              <div class="mt-6 space-y-4 max-w-[44ch]">
                <div>
                  <div class="text-[11px] uppercase tracking-[0.18em] text-black/35 font-medium">Qué haces</div>
                  <p class="mt-2 text-[14px] leading-[1.65] text-black/70">
                    Eliges un borde incisal o cúspide intacta sin desgaste ni restauraciones desadaptadas. Lo anotas en la ficha clínica y no lo cambias en ninguna cita del tratamiento.
                  </p>
                </div>
                <div class="rounded-[12px] bg-[#FF4D5A]/[0.06] border border-[#FF4D5A]/[0.14] px-3.5 py-2.5">
                  <div class="text-[11px] leading-[1.5] text-[#B91C1C] font-medium">
                    <strong>Error común:</strong> Cambiar de referencia (ej. de cúspide mesiovestibular a distovestibular). Pierdes 0.5 a 2 mm y fracasa el sellado apical.
                  </div>
                </div>
              </div>
            </div>
            <div class="relative bg-[#F7F7F7] p-6 flex items-center justify-center">
              <div class="w-full h-full rounded-[24px] overflow-hidden border border-black/[0.06] bg-white relative max-h-[420px]">
                <img src="/images/guias/longitud-trabajo/acceso-boca-referencia-incisal.webp" alt="Referencia coronaria estable" class="w-full h-full object-cover" />
                <div class="absolute bottom-4 left-4 rounded-full px-3 py-1 bg-white/80 backdrop-blur border border-black/10 text-[10px] font-semibold text-black/80">
                  Borde incisal intacto seleccionado
                </div>
              </div>
            </div>
          </div>

          <!-- Paso 03 -->
          <div class="step-card grid md:grid-cols-2 gap-0 min-h-[55vh] items-stretch hidden" data-step-index="2">
            <div class="px-6 md:px-10 py-10 md:py-14 flex flex-col justify-center border-r border-black/[0.04] bg-white">
              <div class="flex items-baseline gap-4">
                <span class="text-[44px] font-[100] text-[#0066FF] tracking-[-0.05em] leading-none">03</span>
                <span class="text-[11px] uppercase tracking-[0.18em] text-black/35 font-semibold">K #10 - stop 90°</span>
              </div>
              <h3 class="mt-4 text-[24px] md:text-[28px] font-[200] tracking-[-0.02em] leading-tight text-[#0A0A0A]">
                Lima K #10 + tope de silicona
              </h3>
              <div class="mt-6 space-y-4 max-w-[44ch]">
                <div>
                  <div class="text-[11px] uppercase tracking-[0.18em] text-black/35 font-medium">Qué haces</div>
                  <p class="mt-2 text-[14px] leading-[1.65] text-black/70">
                    Colocas el tope de silicona ajustado, estrictamente perpendicular al eje de la lima sin comprimirlo. Si el conducto presenta curvatura, precurvas levemente la punta en 15°.
                  </p>
                </div>
                <div class="rounded-[12px] bg-[#FF4D5A]/[0.06] border border-[#FF4D5A]/[0.14] px-3.5 py-2.5">
                  <div class="text-[11px] leading-[1.5] text-[#B91C1C] font-medium">
                    <strong>Error común:</strong> Tope angulado o comprimido contra el vástago. Provoca lectura falsa de +1 mm.
                  </div>
                </div>
              </div>
            </div>
            <div class="relative bg-[#F7F7F7] p-6 flex items-center justify-center">
              <div class="w-full h-full rounded-[24px] overflow-hidden border border-black/[0.06] bg-white relative max-h-[420px]">
                <img src="/images/guias/longitud-trabajo/lima-k10-sondeo.webp" alt="Lima K10 con tope" class="w-full h-full object-cover" />
                <div class="absolute bottom-4 left-4 rounded-full px-3 py-1 bg-white/80 backdrop-blur border border-black/10 text-[10px] font-semibold text-black/80">
                  Tope perpendicular a 90°
                </div>
              </div>
            </div>
          </div>

          <!-- Paso 04 -->
          <div class="step-card grid md:grid-cols-2 gap-0 min-h-[55vh] items-stretch hidden" data-step-index="3">
            <div class="px-6 md:px-10 py-10 md:py-14 flex flex-col justify-center border-r border-black/[0.04] bg-white">
              <div class="flex items-baseline gap-4">
                <span class="text-[44px] font-[100] text-[#0066FF] tracking-[-0.05em] leading-none">04</span>
                <span class="text-[11px] uppercase tracking-[0.18em] text-black/35 font-semibold">21.0 mm reales</span>
              </div>
              <h3 class="mt-4 text-[24px] md:text-[28px] font-[200] tracking-[-0.02em] leading-tight text-[#0A0A0A]">
                Medición con regla endodóntica
              </h3>
              <div class="mt-6 space-y-4 max-w-[44ch]">
                <div>
                  <div class="text-[11px] uppercase tracking-[0.18em] text-black/35 font-medium">Qué haces</div>
                  <p class="mt-2 text-[14px] leading-[1.65] text-black/70">
                    Llevas la lima a la regla milimetrada. Lees con precisión desde la punta activa D0 hasta la base del tope de silicona, sin doblar la lima. Calibras cada medición.
                  </p>
                </div>
                <div class="rounded-[12px] bg-[#FF4D5A]/[0.06] border border-[#FF4D5A]/[0.14] px-3.5 py-2.5">
                  <div class="text-[11px] leading-[1.5] text-[#B91C1C] font-medium">
                    <strong>Error común:</strong> Medir por encima del tope de silicona o estirar la lima. Provoca subestimación de la longitud de trabajo real.
                  </div>
                </div>
              </div>
            </div>
            <div class="relative bg-[#F7F7F7] p-6 flex items-center justify-center">
              <div class="w-full h-full rounded-[24px] overflow-hidden border border-black/[0.06] bg-white relative max-h-[420px]">
                <img src="/images/guias/longitud-trabajo/regla-milimetrada-endodoncia.webp" alt="Regla milimetrada" class="w-full h-full object-cover" />
                <div class="absolute bottom-4 left-4 rounded-full px-3 py-1 bg-white/80 backdrop-blur border border-black/10 text-[10px] font-semibold text-black/80">
                  Lectura milimétrica calibrada
                </div>
              </div>
            </div>
          </div>

          <!-- Paso 05 -->
          <div class="step-card grid md:grid-cols-2 gap-0 min-h-[55vh] items-stretch hidden" data-step-index="4">
            <div class="px-6 md:px-10 py-10 md:py-14 flex flex-col justify-center border-r border-black/[0.04] bg-white">
              <div class="flex items-baseline gap-4">
                <span class="text-[44px] font-[100] text-[#0066FF] tracking-[-0.05em] leading-none">05</span>
                <span class="text-[11px] uppercase tracking-[0.18em] text-[#0066FF] font-semibold">0.5 mm constricción</span>
              </div>
              <h3 class="mt-4 text-[24px] md:text-[28px] font-[200] tracking-[-0.02em] leading-tight text-[#0A0A0A]">
                Determinación electrónica con Localizador
              </h3>
              <div class="mt-6 space-y-4 max-w-[44ch]">
                <div>
                  <div class="text-[11px] uppercase tracking-[0.18em] text-black/35 font-medium">Qué haces</div>
                  <p class="mt-2 text-[14px] leading-[1.65] text-black/70">
                    Conectas el clip labial al paciente y el gancho a la lima. Avanzas lentamente hasta que el localizador marque 0.0 APEX con pitido continuo, y luego retrocedes hasta la marca verde de 0.5 mm.
                  </p>
                </div>
                <div class="rounded-[12px] bg-[#FF4D5A]/[0.06] border border-[#FF4D5A]/[0.14] px-3.5 py-2.5">
                  <div class="text-[11px] leading-[1.5] text-[#B91C1C] font-medium">
                    <strong>Error común:</strong> Usar localizador con la cámara pulpar inundada de hipoclorito de sodio o el conducto completamente seco. Genera lecturas erráticas.
                  </div>
                </div>
              </div>
            </div>
            <div class="relative bg-[#F7F7F7] p-6 flex items-center justify-center">
              <div class="w-full h-full rounded-[24px] overflow-hidden border border-black/[0.06] bg-white relative max-h-[420px]">
                <img src="/images/guias/longitud-trabajo/localizador-apical-pantalla.webp" alt="Localizador apical electrónico" class="w-full h-full object-cover" />
                <div class="absolute bottom-4 left-4 rounded-full px-3 py-1 bg-white/80 backdrop-blur border border-black/10 text-[10px] font-semibold text-black/80">
                  Marca 0.5 mm en verde alcanzada
                </div>
              </div>
            </div>
          </div>

          <!-- Paso 06 -->
          <div class="step-card grid md:grid-cols-2 gap-0 min-h-[55vh] items-stretch hidden" data-step-index="5">
            <div class="px-6 md:px-10 py-10 md:py-14 flex flex-col justify-center border-r border-black/[0.04] bg-white">
              <div class="flex items-baseline gap-4">
                <span class="text-[44px] font-[100] text-[#0066FF] tracking-[-0.05em] leading-none">06</span>
                <span class="text-[11px] uppercase tracking-[0.18em] text-[#0066FF] font-semibold">LT definitiva 20.5 mm</span>
              </div>
              <h3 class="mt-4 text-[24px] md:text-[28px] font-[200] tracking-[-0.02em] leading-tight text-[#0A0A0A]">
                Rx conductometría y LT definitiva
              </h3>
              <div class="mt-6 space-y-4 max-w-[44ch]">
                <div>
                  <div class="text-[11px] uppercase tracking-[0.18em] text-black/35 font-medium">Qué haces</div>
                  <p class="mt-2 text-[14px] leading-[1.65] text-black/70">
                    LT = longitud exacta marcada por el localizador. Tomas radiografía de conductometría confirmando que la punta de la lima queda a 0.5-1 mm del vértice radiográfico. Documentas la medida en la historia clínica.
                  </p>
                </div>
                <div class="rounded-[12px] bg-[#FF4D5A]/[0.06] border border-[#FF4D5A]/[0.14] px-3.5 py-2.5">
                  <div class="text-[11px] leading-[1.5] text-[#B91C1C] font-medium">
                    <strong>Error común:</strong> Dejar la lima en el mismo vértice radiográfico pensando que allí está la constricción. Provoca sobreinstrumentación y lesión periapical.
                  </div>
                </div>
              </div>
            </div>
            <div class="relative bg-[#F7F7F7] p-6 flex items-center justify-center">
              <div class="w-full h-full rounded-[24px] overflow-hidden border border-black/[0.06] bg-white relative grid grid-cols-2 max-h-[420px]">
                <img src="/images/guias/longitud-trabajo/acceso-boca-referencia-incisal.webp" class="w-full h-full object-cover" alt="boca mano" />
                <img src="/images/guias/longitud-trabajo/radiografia-conductometria-vertice.webp" class="w-full h-full object-cover border-l border-black/10" alt="rx conductometria" />
                <div class="absolute top-4 left-4 rounded-full px-3 py-1 bg-white/80 backdrop-blur border border-black/10 text-[10px] font-semibold text-black/80">
                  LT definitiva confirmada
                </div>
              </div>
            </div>
          </div>

        </div>
      </section>

      <!-- ==================== PARTE 5: CHECKLIST CLÍNICO CORRIDO ==================== -->
      <footer class="px-6 md:px-10 py-12 bg-white">
        <div class="flex flex-col md:flex-row gap-8 justify-between">
          <div class="max-w-[62ch]">
            <div class="text-[10px] uppercase tracking-[0.2em] text-black/35 font-bold">Checklist clínico corrido · sin botones gordos</div>
            <p class="mt-3 text-[13px] leading-[1.8] tracking-[-0.01em] text-black/60">
              <strong class="text-black">Rx diagnóstica</strong> mide borde incisal→vértice Rx −3mm → elige <strong class="text-black">referencia estable</strong> (borde incisal 21) → <strong class="text-black">lima K #10</strong> pasiva + stop a 90° sin deformar → <strong class="text-black">regla</strong> lectura D0→base stop → <strong class="text-black">localizador</strong> conducto húmedo, avanza a 00 APEX y retrocede a 0.5mm → <span class="text-[#0066FF] font-semibold">LT = APEX −0.5mm</span> → <strong class="text-black">Rx conductometría</strong> 0.5-1mm corta de ápice Rx → documenta referencia + LT definitiva → obtura a LT. Falla si confundes ápice Rx con constricción.
            </p>
          </div>
          <div class="text-[11px] leading-[1.7] text-black/35 max-w-[34ch]">
            <div class="font-medium text-black/50">LT — ENDO / V3 · Protocolo Oficial OdontoScore</div>
            <div class="mt-1">Imágenes clínicas reales: lima K #10, regla milimetrada, acceso coronal, localizador apical y radiografía de conductometría.</div>
            <div class="mt-2 text-black/30">© 2026 OdontoScore · Academia Clínica de Endodoncia</div>
          </div>
        </div>
      </footer>

    </div>
  </div>
</BaseLayout>

<script is:inline>
(() => {
  // Lógica de interacción del Emulador Apical
  const container = document.getElementById('canalContainer');
  const fileLine = document.getElementById('fileLine');
  const fileHandle = document.getElementById('fileHandle');
  const fileStopBadge = document.getElementById('fileStopBadge');
  const scalePointer = document.getElementById('scalePointer');
  const statusIconRing = document.getElementById('statusIconRing');
  const statusIconDot = document.getElementById('statusIconDot');
  const statusLabel = document.getElementById('statusLabel');
  const statusDesc = document.getElementById('statusDesc');
  const depthBadge = document.getElementById('depthBadge');
  const workLengthVal = document.getElementById('workLengthVal');
  const tactileCard = document.getElementById('tactileCard');
  const tactileTitle = document.getElementById('tactileTitle');

  if (!container || !fileLine) return;

  let depth = 20.2; // mm inicial
  let isDragging = false;

  function getStatus(l) {
    if (l < 19.5) return { label: "lejos", color: "#A1A1AA", desc: "2.0+ mm → busca conducto", inZone: false };
    if (l < 20.6) return { label: "cerca", color: "#EAB308", desc: "~1.0 mm → aproximación", inZone: false };
    if (l < 21.5) return { label: "constricción", color: "#0066FF", desc: "0.5 mm → zona ideal (unión CDC)", inZone: true };
    if (l < 22.2) return { label: "apex", color: "#EF4444", desc: "0.0 APEX → foramen mayor", inZone: false };
    return { label: "sobre", color: "#991B1B", desc: "sobrepasado → retrocede de inmediato", inZone: false };
  }

  function updateVisuals(l) {
    depth = l;
    const progress = Math.max(0, Math.min(1, (l - 18) / 5.2));
    const topPct = 6 + progress * 84;

    // Actualizar posición de la lima y el stop
    fileLine.style.top = "6%";
    fileLine.style.height = `${progress * 84}%`;
    fileHandle.style.top = `${topPct}%`;
    fileStopBadge.style.top = `${topPct}%`;
    scalePointer.style.top = `${progress * 100}%`;

    // Estado clínico
    const status = getStatus(l);
    const workLength = (l - 0.5).toFixed(1);

    statusIconRing.style.borderColor = status.color;
    statusIconRing.style.boxShadow = status.inZone ? `0 0 24px ${status.color}55` : "none";
    statusIconDot.style.background = status.color;
    statusIconDot.style.transform = status.inZone ? "scale(1.25)" : "scale(1)";

    statusLabel.textContent = status.label;
    statusDesc.textContent = status.desc;
    depthBadge.textContent = `${l.toFixed(1)} mm`;

    if (status.inZone) {
      depthBadge.className = "ml-auto px-3.5 py-1.5 rounded-full text-[12px] font-bold border bg-[#0066FF] text-white border-[#0066FF]";
    } else {
      depthBadge.className = "ml-auto px-3.5 py-1.5 rounded-full text-[12px] font-bold border bg-white border-black/10 text-black/40";
    }

    workLengthVal.textContent = workLength;

    if (tactileCard && tactileTitle) {
      if (status.inZone) {
        tactileCard.style.display = "block";
        tactileCard.style.opacity = "1";
        tactileTitle.textContent = `LT: ${workLength}mm ✓ en zona azul`;
      } else {
        tactileCard.style.display = "none";
        tactileCard.style.opacity = "0";
      }
    }
  }

  function handlePointer(e) {
    if (!isDragging || !container) return;
    const rect = container.getBoundingClientRect();
    const offsetY = e.clientY - rect.top;
    let newDepth = 18 + Math.max(0, Math.min(1, offsetY / rect.height)) * 5.2;

    // Resistencia táctil sutil / Snap en constricción (20.7 a 21.5 mm)
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

  // Inicializar emulador
  updateVisuals(depth);

  // Navegación interactiva de los 6 Pasos
  const stepBtns = document.querySelectorAll('.step-nav-btn');
  const stepCards = document.querySelectorAll('.step-card');

  stepBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      const stepIndex = btn.getAttribute('data-step');

      stepBtns.forEach((b) => {
        b.classList.remove('active', 'bg-[#0A0A0A]', 'text-white', 'border-black');
        b.classList.add('bg-white', 'border-black/10', 'text-black/40');
      });
      btn.classList.add('active', 'bg-[#0A0A0A]', 'text-white', 'border-black');
      btn.classList.remove('bg-white', 'border-black/10', 'text-black/40');

      stepCards.forEach((card) => {
        if (card.getAttribute('data-step-index') === stepIndex) {
          card.classList.remove('hidden');
        } else {
          card.classList.add('hidden');
        }
      });
    });
  });
})();
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700&display=swap');

  .endo-page {
    font-family: 'Inter', ui-sans-serif, system-ui, -apple-system, sans-serif;
  }

  .fade-up {
    animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) both;
  }

  @keyframes fadeUp {
    from {
      transform: translateY(20px);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }

  .step-nav-btn.active {
    background-color: #0a0a0a !important;
    color: #ffffff !important;
    border-color: #0a0a0a !important;
  }
</style>
"""

with open('src/pages/guias/longitud-trabajo-endodoncia.astro', 'w', encoding='utf-8') as f:
    f.write(astro_content)

print("Created src/pages/guias/longitud-trabajo-endodoncia.astro!")
