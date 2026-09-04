import re

def update_guide():
    path = 'guias/anatomia-dental-3d-por-capas.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update viewport HTML
    old_viewport_markup = re.search(
        r'<div class="step-viewport" id="stepViewport">.*?</div>\s*<!-- Slider',
        content,
        re.DOTALL
    )
    if old_viewport_markup:
        new_viewport_markup = """<div class="step-viewport" id="stepViewport" style="position:relative;cursor:grab;touch-action:none;user-select:none;">
            <!-- HUD Superior -->
            <div class="step-hud" style="z-index:20;">
              <span class="hud-chip accent" id="badgeStepName">0° · Vista Frontal (Vestibular)</span>
              <span class="hud-chip" id="badgeStepCount">42 Ángulos Continuos (Arrastra para girar)</span>
            </div>

            <!-- Canvas Lightfield Interactivo en tiempo real -->
            <canvas id="lightfieldCanvas" width="400" height="400" style="position:absolute;inset:0;width:100%;height:100%;object-fit:contain;touch-action:none;display:none;z-index:10;cursor:grab;"></canvas>

            <!-- Imagen Activa del Paso (Fallback y precarga instantánea) -->
            <img id="stepImage" src="../assets/img/secuencia_360/paso_1_0deg_frontal_corte.jpg" alt="Ángulo anatómico del molar 360" style="position:relative;z-index:2;width:100%;height:100%;object-fit:contain;">

            <!-- HUD Inferior: Indicador de orientación y ayuda de gestos -->
            <div style="position:absolute;bottom:0.65rem;left:0.75rem;right:0.75rem;display:flex;justify-content:space-between;align-items:center;pointer-events:none;z-index:20;">
              <span style="background:rgba(11,20,38,0.85);color:#94A3B8;font-size:0.68rem;padding:3px 8px;border-radius:999px;font-weight:600;border:1px solid rgba(255,255,255,0.1);">
                Arrastra horizontal 360° · vertical para inclinar
              </span>
              <span id="liveAnglePill" style="background:#0284C7;color:#FFFFFF;font-size:0.68rem;padding:3px 8px;border-radius:999px;font-weight:700;font-family:'JetBrains Mono',monospace;">
                0° azim · 0° elev
              </span>
            </div>
          </div>

          <!-- Selector de Inclinación Vertical (Tilt Presets) -->
          <div style="display:flex;gap:0.4rem;align-items:center;margin:0.75rem 0 0.5rem;flex-wrap:wrap;">
            <span style="font-size:0.72rem;color:#94A3B8;font-weight:700;text-transform:uppercase;letter-spacing:0.04em;">Elevación:</span>
            <button type="button" class="btn-tilt-preset" data-tilt="0" style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.15);color:#E2E8F0;padding:2px 8px;font-size:0.72rem;border-radius:4px;cursor:pointer;">Cénit Oclusal (+60°)</button>
            <button type="button" class="btn-tilt-preset" data-tilt="1" style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.15);color:#E2E8F0;padding:2px 8px;font-size:0.72rem;border-radius:4px;cursor:pointer;">Oclusal Oblicua (+40°)</button>
            <button type="button" class="btn-tilt-preset" data-tilt="2" style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.15);color:#E2E8F0;padding:2px 8px;font-size:0.72rem;border-radius:4px;cursor:pointer;">Cúspides (+20°)</button>
            <button type="button" class="btn-tilt-preset active" data-tilt="3" style="background:#0284C7;border:1px solid #38BDF8;color:#FFFFFF;padding:2px 8px;font-size:0.72rem;border-radius:4px;cursor:pointer;font-weight:700;">Ecuador (0°)</button>
            <button type="button" class="btn-tilt-preset" data-tilt="5" style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.15);color:#E2E8F0;padding:2px 8px;font-size:0.72rem;border-radius:4px;cursor:pointer;">Radicular (-40°)</button>
            <button type="button" class="btn-tilt-preset" data-tilt="6" style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.15);color:#E2E8F0;padding:2px 8px;font-size:0.72rem;border-radius:4px;cursor:pointer;">Ápices (-60°)</button>
          </div>

          <!-- Slider"""
        content = content.replace(old_viewport_markup.group(0), new_viewport_markup)

    # 2. Update slider label to remove any emoji symbol
    content = content.replace("️ Desliza para rotar el diente en 360°:", "Desliza para rotar el diente en 360°:")

    # 3. Add script reference for lib/lightfield-viewer.js before </body>
    if 'lib/lightfield-viewer.js' not in content:
        content = content.replace('</body>', '<script src="../lib/lightfield-viewer.js?v=20260903_v75"></script>\n</body>')

    # 4. Update SEQUENCE_DATA with true clinical angles
    new_sequence_data = """var SEQUENCE_DATA = [
      {
        step: 1,
        angle: 0,
        thetaX: 0,
        thetaY: 3,
        angleLabel: "0° · Cara Vestibular Frontal",
        type: "Vista Frontal Ecuatorial",
        typeClass: "type-surface",
        file: "../assets/img/secuencia_360/paso_1_0deg_frontal_corte.jpg",
        title: "Ángulo 0° · Cara Vestibular y Surco de Desarrollo",
        desc: "Proyección vestibular pura a 0° de elevación. Permite apreciar la convexidad de las cúspides vestibulares (mesiovestibular y distovestibular), el perfil de emergencia radicular y la bifurcación anatómica de las raíces mesial y distal.",
        structures: ["Cúspide mesiovestibular", "Cúspide distovestibular", "Surco de desarrollo vestibular", "Línea amelocementaria (LAC)", "Tronera radicular vestibular"],
        clinical: "Referencia para restauraciones estéticas, diseño de márgenes de coronas y evaluación de biotipo periodontal en zona vestibular."
      },
      {
        step: 2,
        angle: 60,
        thetaX: 1,
        thetaY: 3,
        angleLabel: "60° · Vista Vestibular-Mesial",
        type: "Proyección Oblicua",
        typeClass: "type-surface",
        file: "../assets/img/secuencia_360/paso_2_45deg_vestibular_mesial.jpg",
        title: "Ángulo 60° · Transición Mesial y Cresta Marginal",
        desc: "Rotación oblicua que revela el punto de contacto interproximal mesial, la concavidad subcervical y la transición entre la cara vestibular y el plano mesial.",
        structures: ["Cresta marginal mesial", "Área de contacto interproximal", "Raíz mesial (cara libre)", "Convexidad axial mesiovestibular"],
        clinical: "Esencial para el ajuste de matrices seccionales en cavidades Clase II compuestas y preservación de la papila mesial."
      },
      {
        step: 3,
        angle: 120,
        thetaX: 2,
        thetaY: 3,
        angleLabel: "120° · Vista Mesial-Lingual",
        type: "Proyección Proximal",
        typeClass: "type-surface",
        file: "../assets/img/secuencia_360/paso_3_90deg_lateral_corte.jpg",
        title: "Ángulo 120° · Cara Mesial y Raíz Mesial",
        desc: "Perspectiva proximal que muestra la gran amplitud vestíbulo-lingual de la raíz mesial, su surco longitudinal y la inclinación lingual de las cúspides.",
        structures: ["Surco de depresión radicular mesial", "Cúspide mesiolingual", "Límite cervical proximal", "Espacio interradicular"],
        clinical: "En endodoncia, la raíz mesial alberga frecuentemente dos conductos (mesiovestibular y mesiolingual) conectados por un istmo anatómico."
      },
      {
        step: 4,
        angle: 180,
        thetaX: 3,
        thetaY: 3,
        angleLabel: "180° · Cara Lingual Posterior",
        type: "Vista Lingual Ecuatorial",
        typeClass: "type-surface",
        file: "../assets/img/secuencia_360/paso_4_135deg_lingual_mesial.jpg",
        title: "Ángulo 180° · Cara Lingual y Cúspides Funcionales",
        desc: "Vista lingual completa a 180°. Se identifican las cúspides linguales con mayor altura de vertiente, el perfil lingual continuo y la superficie radicular lingual lisa.",
        structures: ["Cúspide mesiolingual", "Cúspide distolingual", "Surco intercuspídeo lingual", "Superficie cervical lingual"],
        clinical: "Zona de inserción de las fibras supraalveolares y localización crítica de depósitos subgingivales por proximidad salival."
      },
      {
        step: 5,
        angle: 240,
        thetaX: 4,
        thetaY: 3,
        angleLabel: "240° · Cara Distal-Lingual",
        type: "Proyección Oblicua",
        typeClass: "type-surface",
        file: "../assets/img/secuencia_360/paso_5_180deg_posterior_corte.jpg",
        title: "Ángulo 240° · Reborde Marginal Distal",
        desc: "Perspectiva posterior-oblicua hacia la tronera distal. Muestra la menor convexidad relativa de la corona distal y la orientación cónica de la raíz distal.",
        structures: ["Reborde marginal distal", "Vertiente distal de la cresta oblicua", "Raíz distal cónica", "Cuello anatómico distal"],
        clinical: "Control oclusal fundamental: las prematuridades en el reborde marginal distal pueden causar facetas de desgaste y sobrecarga periodontal."
      },
      {
        step: 6,
        angle: 300,
        thetaX: 5,
        thetaY: 3,
        angleLabel: "300° · Vista Distal-Vestibular",
        type: "Proyección Proximal",
        typeClass: "type-surface",
        file: "../assets/img/secuencia_360/paso_6_225deg_lingual_distal.jpg",
        title: "Ángulo 300° · Cara Distovestibular y Furca Distal",
        desc: "Cierre de la órbita 360° en la transición hacia la cara vestibular. Se examina la convexidad cuspídea distal y la entrada distal a la bifurcación radicular.",
        structures: ["Cúspide distovestibular", "Entrada a la furca distal", "Raíz distal (vertiente externa)", "Línea de unión esmalte-cemento"],
        clinical: "Diagnóstico periodontal: las lesiones de furca distales requieren sondaje con sonda Nabers angulada debido a la inclinación anatómica."
      },
      {
        step: 7,
        angle: 90,
        thetaX: 0,
        thetaY: 0,
        angleLabel: "Cénit · Cara Oclusal (+60°)",
        type: "Vista Oclusal Cenital",
        typeClass: "type-surface",
        file: "../assets/img/secuencia_360/paso_7_270deg_lateral_externo.jpg",
        title: "Ángulo Cenital (+60°) · Topografía Oclusal y Fosas",
        desc: "Perspectiva cenital perpendicular a la tabla oclusal. Revela con fidelidad micrométrica el surco principal mesiodistal, la fosa central, las fosetas triangulares y los planos inclinados cuspídeos.",
        structures: ["Fosa central oclusal", "Surco principal mesiodistal", "Foseta triangular mesial", "Crestas triangulares cuspídeas", "Rebordes marginales"],
        clinical: "Patrón anatómico para encerado de diagnóstico, tallado de restauraciones indirectas (inlays/onlays) y sellado de fisuras preventivo."
      },
      {
        step: 8,
        angle: 270,
        thetaX: 0,
        thetaY: 5,
        angleLabel: "Basal · Ápices Radiculares (-40°)",
        type: "Vista Radicular Basal",
        typeClass: "type-surface",
        file: "../assets/img/secuencia_360/paso_8_315deg_hemiseccion_3d.jpg",
        title: "Ángulo Basal (-40°) · Ápices y Forámenes Radiculares",
        desc: "Perspectiva inferior oblicua orientada hacia los ápices radiculares. Expone la curvatura apical mesial y distal y la zona de emergencia de los forámenes nutricios.",
        structures: ["Ápice radicular mesial", "Ápice radicular distal", "Foramen apical principal", "Zona de constricción CDC", "Cemento apical"],
        clinical: "Anatomía apical de alta trascendencia en endodoncia: respeto de la constricción apical para evitar sobreobturación y sellado tridimensional hermético."
      }
    ];"""

    content = re.sub(
        r'var SEQUENCE_DATA = \[.*?\];',
        new_sequence_data,
        content,
        flags=re.DOTALL
    )

    # 5. Connect LightfieldViewer in script
    old_script_init = re.search(
        r'// Elementos del DOM\s*var stepImage = document\.getElementById\("stepImage"\);',
        content
    )
    if old_script_init:
        new_script_init = """// ── INTEGRACIÓN MOTOR LIGHTFIELD 3D INTERACTIVO ──
    var lfCanvas = document.getElementById("lightfieldCanvas");
    var liveAnglePill = document.getElementById("liveAnglePill");
    var tiltButtons = document.querySelectorAll(".btn-tilt-preset");
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
          },
          onAngleChange: function (angles) {
            if (liveAnglePill) {
              liveAnglePill.textContent = angles.degX + "° azim · " + (angles.degY >= 0 ? "+" : "") + angles.degY + "° elev";
            }
          }
        });
      } catch (err) {
        console.warn("Lightfield fallback a fotos estáticas:", err);
      }
    }

    // Botones de presets de inclinación vertical
    tiltButtons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        tiltButtons.forEach(function (b) { b.classList.remove("active"); b.style.background = "rgba(255,255,255,0.06)"; b.style.borderColor = "rgba(255,255,255,0.15)"; b.style.fontWeight = "normal"; });
        btn.classList.add("active");
        btn.style.background = "#0284C7";
        btn.style.borderColor = "#38BDF8";
        btn.style.fontWeight = "700";
        var tiltVal = parseInt(btn.getAttribute("data-tilt"), 10);
        if (lfViewer) lfViewer.setAngles(undefined, tiltVal);
      });
    });

    // Elementos del DOM
    var stepImage = document.getElementById("stepImage");"""
        content = content.replace(old_script_init.group(0), new_script_init)

    # 6. In renderStep(idx), synchronize lfViewer
    content = content.replace(
        'badgeStepName.textContent = data.angleLabel;',
        """badgeStepName.textContent = data.angleLabel;
      if (lfViewer) {
        lfViewer.setAngles(data.thetaX, data.thetaY);
        // Actualizar tilt button activo
        tiltButtons.forEach(function (btn) {
          var tVal = parseInt(btn.getAttribute("data-tilt"), 10);
          if (tVal === data.thetaY) {
            btn.classList.add("active");
            btn.style.background = "#0284C7";
            btn.style.borderColor = "#38BDF8";
            btn.style.fontWeight = "700";
          } else {
            btn.classList.remove("active");
            btn.style.background = "rgba(255,255,255,0.06)";
            btn.style.borderColor = "rgba(255,255,255,0.15)";
            btn.style.fontWeight = "normal";
          }
        });
      }"""
    )

    # 7. Update btnPlaySequence to use lfViewer continuous smooth orbit
    old_play_toggle = re.search(
        r'btnPlaySequence\.addEventListener\("click", function \(\) \{.*?\}\);',
        content,
        re.DOTALL
    )
    if old_play_toggle:
        new_play_toggle = """btnPlaySequence.addEventListener("click", function () {
      if (lfViewer && lfViewer.isReady) {
        var isPlaying = lfViewer.toggleOrbit(0.025);
        if (isPlaying) {
          btnPlaySequence.classList.add("primary");
          btnPlaySequence.innerHTML = "<span>Pausar Rotación</span>";
        } else {
          btnPlaySequence.classList.remove("primary");
          btnPlaySequence.innerHTML = "<span>Rotación Continua 360°</span>";
        }
      } else {
        if (playTimer) {
          stopAutoPlay();
        } else {
          startAutoPlay();
        }
      }
    });"""
        content = content.replace(old_play_toggle.group(0), new_play_toggle)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("anatomia-dental-3d-por-capas.html updated with Lightfield 3D Interactive Engine!")

if __name__ == '__main__':
    update_guide()
