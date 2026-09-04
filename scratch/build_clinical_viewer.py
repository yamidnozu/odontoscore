import re
from pathlib import Path

path = Path('guias/anatomia-dental-3d-por-capas.html')
content = path.read_text(encoding='utf-8')

# 1. Update Title and Meta
content = re.sub(
    r'<title>.*?</title>',
    '<title>Atlas Anatómico y Clínico del Molar Permanente | OdontoScore Academia</title>',
    content
)
content = re.sub(
    r'<meta name="description" content=".*?">',
    '<meta name="description" content="Atlas interactivo de anatomía dental: exploración de caras vestibulares, proximales, tabla oclusal y raíces con notas clínicas sobre esmalte, dentina, furca y ápices.">',
    content
)

# 2. Update Header / Intro
old_header_pattern = re.compile(
    r'<!-- Encabezado Clínico -->.*?<!-- ====================================================================\s+CONTENEDOR MAESTRO DEL ATLAS INTERACTIVO',
    re.DOTALL
)

new_header = '''<!-- Encabezado Clínico -->
    <header style="max-width: 880px; margin-bottom: 1.5rem;">
      <div style="display:inline-flex; align-items:center; gap:0.5rem; background:rgba(12,127,212,0.1); color:#0C7FD4; padding:0.35rem 0.85rem; border-radius:var(--radius-full); font-size:0.75rem; font-weight:800; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:0.75rem;">
        <span>ANATOMÍA DENTAL CLÍNICA</span> · <span>EXPLORADOR INTERACTIVO 3D</span>
      </div>
      <h1 style="font-size: clamp(2rem, 3.8vw, 2.75rem); color: var(--color-navy); line-height: 1.2; margin-bottom: 0.75rem; letter-spacing: -0.02em;">
        Atlas Anatómico y Clínico del Molar Permanente
      </h1>
      <p style="font-size: 1.05rem; color: var(--color-slate); line-height: 1.6;">
        Examina la morfología coronal, caras axiales, tabla oclusal y ápices radiculares. <strong>Toca los puntos anatómicos señalados sobre el diente</strong> para consultar su función masticatoria y aplicaciones prácticas en operatoria, endodoncia y periodoncia.
      </p>
    </header>

    <!-- ====================================================================
         CONTENEDOR MAESTRO DEL ATLAS INTERACTIVO'''

content = old_header_pattern.sub(new_header, content)

# 3. Update Mode Tabs
old_tabs_pattern = re.compile(
    r'<div class="mode-nav-tabs" role="tablist">.*?</div>\s*<!-- ================================================================',
    re.DOTALL
)

new_tabs = '''<div class="mode-nav-tabs" role="tablist">
        <button type="button" class="mode-tab-btn active" id="tabBtnSequence" role="tab" aria-selected="true">
          <span>1. Morfología Dental y Caras Clínicas (Explorador 3D)</span>
        </button>
        <button type="button" class="mode-tab-btn" id="tabBtnHistology" role="tab" aria-selected="false">
          <span>2. Corte Histológico y Tejidos Internos</span>
        </button>
      </div>

      <!-- ================================================================'''

content = old_tabs_pattern.sub(new_tabs, content)

# 4. Inject Hotspot CSS
hotspot_css = '''
    /* Hotspots y Notas Anatómicas sobre el Visor */
    .hotspots-overlay {
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 25;
    }

    .hotspot-pin {
      position: absolute;
      transform: translate(-50%, -50%);
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: rgba(14, 165, 233, 0.95);
      color: #FFFFFF;
      border: 2px solid #FFFFFF;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.72rem;
      font-weight: 800;
      cursor: pointer;
      pointer-events: auto;
      box-shadow: 0 0 12px rgba(14, 165, 233, 0.8);
      transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
      user-select: none;
    }

    .hotspot-pin:hover, .hotspot-pin.active {
      transform: translate(-50%, -50%) scale(1.35);
      background: #38BDF8;
      box-shadow: 0 0 20px rgba(56, 189, 248, 1);
      z-index: 35;
    }

    .hotspot-tooltip {
      position: absolute;
      bottom: calc(100% + 8px);
      left: 50%;
      transform: translateX(-50%);
      background: rgba(11, 20, 38, 0.96);
      border: 1px solid rgba(56, 189, 248, 0.5);
      color: #FFFFFF;
      padding: 0.35rem 0.65rem;
      border-radius: var(--radius-sm);
      font-size: 0.72rem;
      font-weight: 600;
      white-space: nowrap;
      pointer-events: none;
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.6);
      display: none;
      z-index: 40;
    }

    .hotspot-pin:hover .hotspot-tooltip, .hotspot-pin.active .hotspot-tooltip {
      display: block;
    }

    /* Selector Rápido de Caras Anatómicas */
    .face-selector-bar {
      display: flex;
      gap: 0.4rem;
      overflow-x: auto;
      margin: 0.85rem 0 0.6rem;
      padding-bottom: 0.25rem;
    }

    .btn-face-tab {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.14);
      color: #CBD5E1;
      padding: 0.35rem 0.75rem;
      font-size: 0.75rem;
      font-weight: 600;
      border-radius: var(--radius-full);
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s ease;
    }

    .btn-face-tab:hover {
      background: rgba(255, 255, 255, 0.1);
      color: #FFFFFF;
    }

    .btn-face-tab.active {
      background: #0284C7;
      border-color: #38BDF8;
      color: #FFFFFF;
      font-weight: 700;
      box-shadow: 0 0 10px rgba(2, 132, 199, 0.5);
    }
'''

if '.hotspots-overlay' not in content:
    content = content.replace('  </style>', hotspot_css + '\n  </style>')

# 5. Update Viewport HTML & Controls
old_sequence_view = re.compile(
    r'<div class="atlas-content-grid" id="viewSectionSequence">.*?<!-- ================================================================\s+MODO 2:',
    re.DOTALL
)

new_sequence_view = '''<div class="atlas-content-grid" id="viewSectionSequence">
        
        <!-- Columna Izquierda: Viewport y Selector Anatómico -->
        <div>
          <div class="step-viewport" id="stepViewport" style="position:relative;cursor:grab;touch-action:none;user-select:none;">
            <!-- HUD Superior -->
            <div class="step-hud" style="z-index:20;">
              <span class="hud-chip accent" id="badgeStepName">Cara Vestibular</span>
              <span class="hud-chip" id="badgeStepCount">Puntos de Interés Clínico</span>
            </div>

            <!-- Canvas Lightfield Interactivo en tiempo real -->
            <canvas id="lightfieldCanvas" width="400" height="400" style="position:absolute;inset:0;width:100%;height:100%;object-fit:contain;touch-action:none;display:none;z-index:10;cursor:grab;"></canvas>

            <!-- Imagen Activa del Paso (Fallback y precarga instantánea) -->
            <img id="stepImage" src="../assets/img/secuencia_360/paso_1_0deg_frontal_corte.jpg" alt="Ángulo anatómico del molar" style="position:relative;z-index:2;width:100%;height:100%;object-fit:contain;">

            <!-- Pines / Hotspots Interactivos directamente sobre la pieza -->
            <div class="hotspots-overlay" id="hotspotsContainer"></div>

            <!-- HUD Inferior: Indicador Clínico -->
            <div style="position:absolute;bottom:0.65rem;left:0.75rem;right:0.75rem;display:flex;justify-content:space-between;align-items:center;pointer-events:none;z-index:20;">
              <span style="background:rgba(11,20,38,0.85);color:#94A3B8;font-size:0.68rem;padding:3px 8px;border-radius:999px;font-weight:600;border:1px solid rgba(255,255,255,0.1);">
                Toca los puntos para ver notas clínicas · Arrastra para girar
              </span>
              <span id="activeHotspotCountBadge" style="background:#0284C7;color:#FFFFFF;font-size:0.68rem;padding:3px 8px;border-radius:999px;font-weight:700;">
                Vista Seleccionada
              </span>
            </div>
          </div>

          <!-- Selector Rápido de Caras Anatómicas -->
          <div class="face-selector-bar" id="faceSelectorBar">
            <button type="button" class="btn-face-tab active" data-scenario-idx="0">Cara Vestibular</button>
            <button type="button" class="btn-face-tab" data-scenario-idx="1">Transición Mesial</button>
            <button type="button" class="btn-face-tab" data-scenario-idx="2">Cara Mesial</button>
            <button type="button" class="btn-face-tab" data-scenario-idx="3">Cara Lingual</button>
            <button type="button" class="btn-face-tab" data-scenario-idx="4">Transición Distal</button>
            <button type="button" class="btn-face-tab" data-scenario-idx="5">Cara Distal</button>
            <button type="button" class="btn-face-tab" data-scenario-idx="6">Tabla Oclusal</button>
            <button type="button" class="btn-face-tab" data-scenario-idx="7">Raíz y Ápices</button>
          </div>

          <!-- Barra de Navegación por Caras -->
          <div class="steps-stepper-bar" style="margin-top:0.75rem;">
            <div class="step-indicator-wrapper active" data-step-target="0" title="Cara Vestibular">
              <div class="step-indicator-node">1</div>
              <span class="step-indicator-label">Vestibular</span>
            </div>
            <div class="step-indicator-wrapper" data-step-target="1" title="Transición Mesial">
              <div class="step-indicator-node">2</div>
              <span class="step-indicator-label">Vesto-Mesial</span>
            </div>
            <div class="step-indicator-wrapper" data-step-target="2" title="Cara Mesial">
              <div class="step-indicator-node">3</div>
              <span class="step-indicator-label">Mesial</span>
            </div>
            <div class="step-indicator-wrapper" data-step-target="3" title="Cara Lingual">
              <div class="step-indicator-node">4</div>
              <span class="step-indicator-label">Lingual</span>
            </div>
            <div class="step-indicator-wrapper" data-step-target="4" title="Transición Distal">
              <div class="step-indicator-node">5</div>
              <span class="step-indicator-label">Disto-Lingual</span>
            </div>
            <div class="step-indicator-wrapper" data-step-target="5" title="Cara Distal">
              <div class="step-indicator-node">6</div>
              <span class="step-indicator-label">Distal</span>
            </div>
            <div class="step-indicator-wrapper" data-step-target="6" title="Tabla Oclusal">
              <div class="step-indicator-node">7</div>
              <span class="step-indicator-label">Oclusal</span>
            </div>
            <div class="step-indicator-wrapper" data-step-target="7" title="Raíz y Ápices">
              <div class="step-indicator-node">8</div>
              <span class="step-indicator-label">Ápices</span>
            </div>
          </div>

          <!-- Filmstrip de Vistas -->
          <div class="filmstrip-row" id="filmstripContainer">
            <div class="filmstrip-thumb active" data-thumb-idx="0" title="Cara Vestibular">
              <img src="../assets/img/secuencia_360/paso_1_0deg_frontal_corte.jpg" alt="Vestibular">
              <span class="filmstrip-deg">Vestibular</span>
            </div>
            <div class="filmstrip-thumb" data-thumb-idx="1" title="Vesto-Mesial">
              <img src="../assets/img/secuencia_360/paso_2_45deg_vestibular_mesial.jpg" alt="Vesto-Mesial">
              <span class="filmstrip-deg">V-Mesial</span>
            </div>
            <div class="filmstrip-thumb" data-thumb-idx="2" title="Cara Mesial">
              <img src="../assets/img/secuencia_360/paso_3_90deg_lateral_corte.jpg" alt="Mesial">
              <span class="filmstrip-deg">Mesial</span>
            </div>
            <div class="filmstrip-thumb" data-thumb-idx="3" title="Cara Lingual">
              <img src="../assets/img/secuencia_360/paso_4_135deg_lingual_mesial.jpg" alt="Lingual">
              <span class="filmstrip-deg">Lingual</span>
            </div>
            <div class="filmstrip-thumb" data-thumb-idx="4" title="Disto-Lingual">
              <img src="../assets/img/secuencia_360/paso_5_180deg_posterior_corte.jpg" alt="Disto-Lingual">
              <span class="filmstrip-deg">D-Lingual</span>
            </div>
            <div class="filmstrip-thumb" data-thumb-idx="5" title="Cara Distal">
              <img src="../assets/img/secuencia_360/paso_6_225deg_lingual_distal.jpg" alt="Distal">
              <span class="filmstrip-deg">Distal</span>
            </div>
            <div class="filmstrip-thumb" data-thumb-idx="6" title="Tabla Oclusal">
              <img src="../assets/img/secuencia_360/paso_7_270deg_lateral_externo.jpg" alt="Oclusal">
              <span class="filmstrip-deg">Oclusal</span>
            </div>
            <div class="filmstrip-thumb" data-thumb-idx="7" title="Raíz y Ápices">
              <img src="../assets/img/secuencia_360/paso_8_315deg_hemiseccion_3d.jpg" alt="Ápices">
              <span class="filmstrip-deg">Ápices</span>
            </div>
          </div>

        </div>

        <!-- Columna Derecha: Ficha Clínica y Notas Anatómicas -->
        <div class="sidebar-step-col">
          
          <!-- Botones de Navegación Simple -->
          <div>
            <div style="font-size:0.75rem; font-weight:700; color:#94A3B8; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:0.5rem;">
              Navegación Anatómica
            </div>
            <div class="btn-stepper-actions">
              <button type="button" class="btn-step-act" id="btnPrevStep">
                <span>Cara Anterior</span>
              </button>
              <button type="button" class="btn-step-act primary" id="btnNextStep">
                <span>Cara Siguiente</span>
              </button>
              <button type="button" class="btn-step-act" id="btnPlaySequence">
                <span>Giro Continuo</span>
              </button>
            </div>
          </div>

          <!-- Ficha Clínica de la Cara y del Punto Seleccionado -->
          <div class="step-clinical-card" id="stepCard">
            <span class="step-type-chip type-surface" id="stepTypeChip">Morfología Coronal</span>
            <div class="step-card-title" id="stepTitle">
              <span>Cara Vestibular y Cúspides</span>
            </div>
            <div class="step-card-desc" id="stepDesc">
              Superficie orientada hacia el vestíbulo bucal. Destaca la convexidad de las cúspides vestibulares, el perfil cervical y la bifurcación radicular anatómica.
            </div>
            <div>
              <div style="font-size:0.72rem; font-weight:700; color:#94A3B8; text-transform:uppercase; margin-bottom:0.35rem;">
                Puntos Anatómicos en esta Cara (Toca para seleccionar):
              </div>
              <div class="step-structures-list" id="stepStructures"></div>
            </div>
            <div class="step-card-pearl" id="stepPearl">
              <strong>Relevancia Clínica:</strong> Referencia fundamental en estética dental, contorno de restauraciones Clase V de Black y evaluación de biotipo gingival vestibular.
            </div>
          </div>

        </div>
      </div>

      <!-- ================================================================
           MODO 2:'''

content = old_sequence_view.sub(new_sequence_view, content)

# 6. Update JavaScript Engine
old_script_pattern = re.compile(
    r'// ── 2\. DATOS DE LOS 8 ÁNGULOS DE ROTACIÓN 360°.*?// ── 3\. MOTOR DEL ATLAS HISTOLÓGICO MAESTRO CON PINES ──',
    re.DOTALL
)

new_script = '''// ── 2. ESCENARIOS ANATÓMICOS CON NOTAS Y PINES INTERACTIVOS ──
    var CLINICAL_SCENARIOS = [
      {
        id: "vestibular",
        name: "Cara Vestibular",
        thetaX: 0,
        thetaY: 3,
        type: "Morfología Coronal y Radicular",
        typeClass: "type-surface",
        file: "../assets/img/secuencia_360/paso_1_0deg_frontal_corte.jpg",
        title: "Cara Vestibular: Morfología y Relieve",
        desc: "Superficie orientada hacia el vestíbulo bucal. Presenta la convexidad de las dos cúspides vestibulares, el surco vertical de desarrollo y la bifurcación de las raíces mesial y distal.",
        clinical: "Referencia para restauraciones Clase V de Black, determinación del perfil de emergencia y valoración del biotipo periodontal vestibular.",
        hotspots: [
          { id: "cusp_mv", num: "1", x: 42, y: 34, title: "Cúspide Mesiovestibular", desc: "Cúspide cortante con vertientes lisas bien delimitadas.", pearl: "Su vertiente oclusal contacta con la fosa central superior en oclusión céntrica." },
          { id: "cusp_dv", num: "2", x: 58, y: 35, title: "Cúspide Distovestibular", desc: "Cúspide de menor volumen y más redondeada que la mesiovestibular.", pearl: "Canaliza el bolo alimenticio hacia la tronera distovestibular en la masticación." },
          { id: "groove_v", num: "3", x: 50, y: 40, title: "Surco de Desarrollo Vestibular", desc: "Depresión longitudinal que separa ambas cúspides vestibulares.", pearl: "Zona susceptible a acúmulo de biofilm y caries de fisura; diana de sellado preventivo." },
          { id: "lac", num: "4", x: 50, y: 49, title: "Línea Amelocementaria (LAC)", desc: "Cuello anatómico que delimita el esmalte coronal del cemento radicular.", pearl: "Punto de referencia milimétrico para situar el margen de coronas y carillas." },
          { id: "furca", num: "5", x: 50, y: 64, title: "Bifurcación Radicular (Furca)", desc: "Punto de divergencia anatómica entre la raíz mesial y la raíz distal.", pearl: "Se evalúa con sonda de Nabers para clasificar lesiones de furca (Hamp I a III)." },
          { id: "apex", num: "6", x: 49, y: 83, title: "Ápices Radiculares", desc: "Terminación radicular con curvatura fisiológica distal.", pearl: "Punto crítico de instrumentación endodóntica y obturación hermética tridimensional." }
        ]
      },
      {
        id: "vestomesial",
        name: "Transición Vesto-Mesial",
        thetaX: 1,
        thetaY: 3,
        type: "Ángulo Línea Proximal",
        typeClass: "type-surface",
        file: "../assets/img/secuencia_360/paso_2_45deg_vestibular_mesial.jpg",
        title: "Transición Mesial y Cresta Marginal",
        desc: "Perspectiva oblicua que muestra el ángulo línea mesiovestibular, el área de contacto proximal y la emergencia de la papila interdental.",
        clinical: "El diseño de matrices y cuñas en Clase II debe respetar esta curvatura para devolver el punto de contacto anatómico sin sobrecontornos.",
        hotspots: [
          { id: "cresta_m", num: "1", x: 45, y: 34, title: "Cresta Marginal Mesial", desc: "Borde de esmalte que delimita la vertiente oclusal mesial.", pearl: "Debe reproducir el reborde marginal para evitar empaquetamiento de comida interproximal." },
          { id: "punto_cont", num: "2", x: 40, y: 42, title: "Área de Contacto Proximal", desc: "Punto de apoyo con el diente contiguo.", pearl: "Protege la papila gingival interdentaria de la fuerza directa del impacto masticatorio." },
          { id: "concavidad_cerv", num: "3", x: 45, y: 52, title: "Concavidad Cervical Mesial", desc: "Depresión anatómica en el tercio cervical de la raíz.", pearl: "Zona crítica propensa a márgenes desbordantes de composite o amalgama." },
          { id: "raiz_mesial", num: "4", x: 47, y: 70, title: "Tronco Radicular Mesial", desc: "Superficie externa ancha de la raíz mesial.", pearl: "Alberga dos conductos radiculares (MV y ML) unidos por un istmo anatómico." }
        ]
      },
      {
        id: "mesial",
        name: "Cara Mesial",
        thetaX: 2,
        thetaY: 3,
        type: "Perfil Proximal Puro",
        typeClass: "type-surface",
        file: "../assets/img/secuencia_360/paso_3_90deg_lateral_corte.jpg",
        title: "Cara Mesial: Dimensión Vestíbulo-Lingual",
        desc: "Proyección mesial directa. Muestra la amplia dimensión bucolingual del molar, la inclinación lingual de las cúspides y la depresión longitudinal de la raíz.",
        clinical: "Esencial en endodoncia para comprender la curvatura radicular y el acceso a los dos conductos mesiales sin debilitar la furca.",
        hotspots: [
          { id: "cusp_ml", num: "1", x: 57, y: 34, title: "Cúspide Mesiolingual", desc: "Cúspide principal de soporte y trituración.", pearl: "Recibe el mayor porcentaje de carga axial durante el ciclo masticatorio." },
          { id: "surco_dep", num: "2", x: 50, y: 65, title: "Surco Radicular Longitudinal", desc: "Canaladura longitudinal sobre la raíz mesial.", pearl: "Frecuente depósito de cálculo subgingival de difícil acceso para el raspado." },
          { id: "espacio_inter", num: "3", x: 44, y: 74, title: "Espacio Interradicular", desc: "Espacio entre raíces ocupado por el hueso alveolar septal.", pearl: "La pérdida ósea interradicular conduce a compromiso de furca Grado II o III." }
        ]
      },
      {
        id: "lingual",
        name: "Cara Lingual",
        thetaX: 3,
        thetaY: 3,
        type: "Morfología Lingual",
        typeClass: "type-surface",
        file: "../assets/img/secuencia_360/paso_4_135deg_lingual_mesial.jpg",
        title: "Cara Lingual: Cúspides Funcionales",
        desc: "Superficie orientada hacia la lengua. Exhibe cúspides de contorno redondeado y un perfil axial liso continuo hacia la raíz.",
        clinical: "Zona expuesta al flujo salival de las glándulas submandibulares, con predisposición a cálculo supra y subgingival lingual.",
        hotspots: [
          { id: "cusp_ling", num: "1", x: 47, y: 34, title: "Cúspides Linguales", desc: "Cúspides funcionales que orientan el plano oclusal lingual.", pearl: "Protegen la mucosa lingual de pellizcamientos durante el cierre mandibular." },
          { id: "surco_ling", num: "2", x: 50, y: 41, title: "Surco Lingual de Desarrollo", desc: "Hendidura suave sobre la cara lingual.", pearl: "Puede terminar en una foseta lingual ciega vulnerable a caries no visibles." },
          { id: "raiz_ling", num: "3", x: 50, y: 68, title: "Convexidad Radicular Lingual", desc: "Contorno liso y continuo de las raíces por lingual.", pearl: "Superficie favorable para el acceso con curetas periodontales Gracey 11/12." }
        ]
      },
      {
        id: "distolingual",
        name: "Transición Disto-Lingual",
        thetaX: 4,
        thetaY: 3,
        type: "Ángulo Línea Distal",
        typeClass: "type-surface",
        file: "../assets/img/secuencia_360/paso_5_180deg_posterior_corte.jpg",
        title: "Transición Distal y Reborde Marginal",
        desc: "Perspectiva posterior-oblicua orientada hacia la tronera distal. Revela la menor altura relativa del reborde distal y la morfología del cono radicular posterior.",
        clinical: "En oclusión terapéutica, el reborde marginal distal previene contactos prematuros en movimientos de lateralidad y protrusión.",
        hotspots: [
          { id: "reborde_d", num: "1", x: 52, y: 35, title: "Reborde Marginal Distal", desc: "Cresta de esmalte situada más apicalmente que la mesial.", pearl: "Control oclusal: su falta de armonía genera facetas de desgaste patológico." },
          { id: "cono_distal", num: "2", x: 50, y: 68, title: "Raíz Distal Cónica", desc: "Raíz posterior redondeada y recta.", pearl: "Aloja habitualmente un conducto amplio y recto de fácil instrumentación." }
        ]
      },
      {
        id: "distal",
        name: "Cara Distal",
        thetaX: 5,
        thetaY: 3,
        type: "Perfil Posterior",
        typeClass: "type-surface",
        file: "../assets/img/secuencia_360/paso_6_225deg_lingual_distal.jpg",
        title: "Cara Distal: Relieve y Espacio Retromolar",
        desc: "Proyección distal pura del molar. Permite evaluar la relación con el diente distal adyacente o el reborde desdentado retromolar.",
        clinical: "Superficie distal de difícil higiene; el uso de hilo dental o cepillos interproximales es mandatorio para prevenir caries radiculares.",
        hotspots: [
          { id: "cont_dist", num: "1", x: 45, y: 42, title: "Área de Contacto Distal", desc: "Zona plana de contacto interdentario.", pearl: "En ausencia del segundo molar, actúa como pilar terminal en prótesis fija." },
          { id: "cuello_dist", num: "2", x: 48, y: 52, title: "Línea Cervical Distal", desc: "Línea amelocementaria con menor concavidad que en la cara mesial.", pearl: "Menor ondulación anatómica de la inserción epitelial conectiva." }
        ]
      },
      {
        id: "oclusal",
        name: "Tabla Oclusal",
        thetaX: 0,
        thetaY: 0,
        type: "Superficie Masticatoria",
        typeClass: "type-surface",
        file: "../assets/img/secuencia_360/paso_7_270deg_lateral_externo.jpg",
        title: "Tabla Oclusal: Cúspides, Fosas y Surcos",
        desc: "Visión superior completa de la cara masticatoria. Expone el relieve de fosas principales, surco central mesiodistal y crestas triangulares.",
        clinical: "Referencia para tallado cavitario, encerado oclusal funcional de Gnathología y ajuste de contactos céntricos y excéntricos.",
        hotspots: [
          { id: "fosa_cen", num: "1", x: 50, y: 47, title: "Fosa Central Oclusal", desc: "Punto más profundo donde confluyen los surcos principales.", pearl: "Área con el mayor porcentaje de caries oclusal; zona prioritaria de sellado de fisuras." },
          { id: "surco_md", num: "2", x: 50, y: 39, title: "Surco Principal Mesiodistal", desc: "Hendidura anatómica que separa cúspides vestibulares y linguales.", pearl: "Vía de escape del bolo alimenticio en los ciclos masticatorios." },
          { id: "crestas_triang", num: "3", x: 42, y: 47, title: "Crestas Triangulares", desc: "Planos inclinados cuspídeos que confluyen al centro.", pearl: "Deben esculpirse anatómicamente para evitar interferencias oclusales." },
          { id: "fosa_dist", num: "4", x: 60, y: 48, title: "Foseta Triangular Distal", desc: "Depresión secundaria que limita con la cresta marginal.", pearl: "Punto de apoyo para la cúspide antagonista durante la deglución." }
        ]
      },
      {
        id: "apices",
        name: "Raíz y Ápices",
        thetaX: 0,
        thetaY: 5,
        type: "Zona Apical y Foramen",
        typeClass: "type-surface",
        file: "../assets/img/secuencia_360/paso_8_315deg_hemiseccion_3d.jpg",
        title: "Zona Apical: Forámenes Radiculares",
        desc: "Visión basal inferior dirigida a los ápices de las raíces mesial y distal.",
        clinical: "En endodoncia, la determinación exacta de la constricción apical (límite CDC) evita la sobreinstrumentación hacia los tejidos periapicales.",
        hotspots: [
          { id: "foramen_m", num: "1", x: 43, y: 62, title: "Foramen Apical Mesial", desc: "Apertura apical de la raíz mesial (frecuente doble conducto).", pearl: "La longitud de trabajo se sitúa a 0.5 - 1.0 mm del foramen radiográfico." },
          { id: "foramen_d", num: "2", x: 55, y: 64, title: "Foramen Apical Distal", desc: "Salida apical de la raíz distal.", pearl: "Puede presentar un delta apical con ramificaciones vasculares colaterales." },
          { id: "cemento_ap", num: "3", x: 49, y: 55, title: "Cemento Apical Reparativo", desc: "Capa gruesa de cemento celular en el ápice.", pearl: "Capaz de formar un tapón biológico mineralizado tras la endodoncia." }
        ]
      }
    ];

    // Pre-carga inmediata de todas las imágenes
    var PRELOADED_CACHE = [];
    CLINICAL_SCENARIOS.forEach(function (item) {
      var preloadImg = new Image();
      preloadImg.src = item.file;
      PRELOADED_CACHE.push(preloadImg);
    });

    // ── INTEGRACIÓN DEL EXPLORADOR DENTAL 3D ──
    var lfCanvas = document.getElementById("lightfieldCanvas");
    var lfViewer = null;

    if (typeof LightfieldViewer !== "undefined" && lfCanvas) {
      try {
        lfViewer = new LightfieldViewer({
          canvas: lfCanvas,
          imageSrc: "../assets/img/lightfield_diente_encoded.png",
          initialX: 0,
          initialY: 3,
          onReady: function () {
            lfCanvas.style.display = "block";
            if (stepImage) stepImage.style.display = "none";
          }
        });
      } catch (err) {
        console.warn("Explorador fallback a imágenes estáticas:", err);
      }
    }

    // Elementos del DOM
    var stepImage = document.getElementById("stepImage");
    var badgeStepName = document.getElementById("badgeStepName");
    var badgeStepCount = document.getElementById("badgeStepCount");
    var hotspotsContainer = document.getElementById("hotspotsContainer");
    var stepTypeChip = document.getElementById("stepTypeChip");
    var stepTitle = document.getElementById("stepTitle");
    var stepDesc = document.getElementById("stepDesc");
    var stepStructures = document.getElementById("stepStructures");
    var stepPearl = document.getElementById("stepPearl");
    var faceTabs = document.querySelectorAll(".btn-face-tab");

    var btnPrevStep = document.getElementById("btnPrevStep");
    var btnNextStep = document.getElementById("btnNextStep");
    var btnPlaySequence = document.getElementById("btnPlaySequence");
    var stepWrappers = document.querySelectorAll(".step-indicator-wrapper");
    var filmstripThumbs = document.querySelectorAll(".filmstrip-thumb");

    var currentScenario = 0;
    var totalScenarios = CLINICAL_SCENARIOS.length;
    var playTimer = null;
    var activeHotspotId = null;

    function renderHotspots(scenario) {
      if (!hotspotsContainer) return;
      hotspotsContainer.innerHTML = "";

      scenario.hotspots.forEach(function (spot, idx) {
        var pin = document.createElement("button");
        pin.type = "button";
        pin.className = "hotspot-pin" + (activeHotspotId === spot.id ? " active" : "");
        pin.style.left = spot.x + "%";
        pin.style.top = spot.y + "%";
        pin.setAttribute("data-hotspot-id", spot.id);
        pin.setAttribute("aria-label", spot.title);
        pin.textContent = spot.num;

        // Tooltip flotante sobre el pin
        var tooltip = document.createElement("span");
        tooltip.className = "hotspot-tooltip";
        tooltip.textContent = spot.title;
        pin.appendChild(tooltip);

        pin.addEventListener("click", function (e) {
          e.stopPropagation();
          selectHotspot(spot);
        });

        hotspotsContainer.appendChild(pin);
      });
    }

    function selectHotspot(spot) {
      activeHotspotId = spot.id;

      // Actualizar estado activo en los pines
      if (hotspotsContainer) {
        var pins = hotspotsContainer.querySelectorAll(".hotspot-pin");
        pins.forEach(function (p) {
          if (p.getAttribute("data-hotspot-id") === spot.id) {
            p.classList.add("active");
          } else {
            p.classList.remove("active");
          }
        });
      }

      // Actualizar estado activo en los chips de la lista lateral
      if (stepStructures) {
        var tags = stepStructures.querySelectorAll(".structure-tag");
        tags.forEach(function (t) {
          if (t.getAttribute("data-hotspot-id") === spot.id) {
            t.style.background = "#0284C7";
            t.style.borderColor = "#38BDF8";
            t.style.color = "#FFFFFF";
          } else {
            t.style.background = "rgba(255,255,255,0.08)";
            t.style.borderColor = "rgba(255,255,255,0.1)";
            t.style.color = "#E2E8F0";
          }
        });
      }

      // Actualizar contenido de la tarjeta clínica
      stepTitle.textContent = spot.title;
      stepDesc.textContent = spot.desc;
      stepPearl.innerHTML = "<strong>Relevancia Clínica:</strong> " + spot.pearl;
    }

    function renderScenario(idx) {
      currentScenario = (idx + totalScenarios) % totalScenarios;
      var data = CLINICAL_SCENARIOS[currentScenario];
      activeHotspotId = null;

      // Actualizar imagen con fallback
      stepImage.src = data.file;

      // Actualizar badges
      badgeStepName.textContent = data.name;
      badgeStepCount.textContent = data.hotspots.length + " Puntos Anatómicos Marcados";

      // Orientar el modelo 3D
      if (lfViewer) {
        if (lfViewer.isReady) {
          lfCanvas.style.display = "block";
          if (stepImage) stepImage.style.display = "none";
        }
        lfViewer.setAngles(data.thetaX, data.thetaY);
      }

      // Renderizar los pines interactivos sobre la cara
      renderHotspots(data);

      // Actualizar selector rápido de caras
      faceTabs.forEach(function (tab, i) {
        if (i === currentScenario) {
          tab.classList.add("active");
        } else {
          tab.classList.remove("active");
        }
      });

      // Actualizar chip y textos de la tarjeta lateral
      stepTypeChip.className = "step-type-chip " + data.typeClass;
      stepTypeChip.textContent = data.type;
      stepTitle.textContent = data.title;
      stepDesc.textContent = data.desc;
      stepPearl.innerHTML = "<strong>Relevancia Clínica:</strong> " + data.clinical;

      // Construir lista de puntos anatómicos interactivos
      stepStructures.innerHTML = "";
      data.hotspots.forEach(function (spot) {
        var span = document.createElement("button");
        span.type = "button";
        span.className = "structure-tag";
        span.style.cursor = "pointer";
        span.style.textAlign = "left";
        span.setAttribute("data-hotspot-id", spot.id);
        span.textContent = spot.num + ". " + spot.title;
        span.addEventListener("click", function () {
          selectHotspot(spot);
        });
        stepStructures.appendChild(span);
      });

      // Actualizar stepper
      stepWrappers.forEach(function (wrap, i) {
        if (i === currentScenario) {
          wrap.classList.add("active");
        } else {
          wrap.classList.remove("active");
        }
      });

      // Actualizar filmstrip
      filmstripThumbs.forEach(function (thumb, i) {
        if (i === currentScenario) {
          thumb.classList.add("active");
        } else {
          thumb.classList.remove("active");
        }
      });
    }

    // Clic en el selector de caras
    faceTabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        stopAutoPlay();
        var target = parseInt(this.getAttribute("data-scenario-idx"), 10);
        renderScenario(target);
      });
    });

    // Botones de avance / retroceso
    btnPrevStep.addEventListener("click", function () {
      stopAutoPlay();
      renderScenario(currentScenario - 1);
    });

    btnNextStep.addEventListener("click", function () {
      stopAutoPlay();
      renderScenario(currentScenario + 1);
    });

    // Clic en los nodos del stepper
    stepWrappers.forEach(function (wrap) {
      wrap.addEventListener("click", function () {
        stopAutoPlay();
        var target = parseInt(this.getAttribute("data-step-target"), 10);
        renderScenario(target);
      });
    });

    // Clic en las miniaturas del filmstrip
    filmstripThumbs.forEach(function (thumb) {
      thumb.addEventListener("click", function () {
        stopAutoPlay();
        var target = parseInt(this.getAttribute("data-thumb-idx"), 10);
        renderScenario(target);
      });
    });

    // Rotación automática continua
    function startAutoPlay() {
      playTimer = setInterval(function () {
        renderScenario(currentScenario + 1);
      }, 2500);
      btnPlaySequence.classList.add("primary");
      btnPlaySequence.innerHTML = "<span>Pausar Giro</span>";
    }

    function stopAutoPlay() {
      if (playTimer) {
        clearInterval(playTimer);
        playTimer = null;
      }
      btnPlaySequence.classList.remove("primary");
      btnPlaySequence.innerHTML = "<span>Giro Continuo</span>";
    }

    btnPlaySequence.addEventListener("click", function () {
      if (playTimer) {
        stopAutoPlay();
      } else {
        startAutoPlay();
      }
    });

    // ── 3. MOTOR DEL ATLAS HISTOLÓGICO MAESTRO CON PINES ──'''

content = old_script_pattern.sub(new_script, content)

# 7. Update initial call from renderStep(0) to renderScenario(0)
content = content.replace('renderStep(0);', 'renderScenario(0);')

path.write_text(content, encoding='utf-8')
print("Successfully upgraded guias/anatomia-dental-3d-por-capas.html to clinical dental focus with interactive hotspots!")
