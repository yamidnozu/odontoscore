/**
 * OdontoScore - Simulador 3D de Biofilm Oral y Patología Endodóntica v1.0
 * Desarrollado con Three.js para renderizado de microbiota, matriz EPS y conducto radicular.
 * Sin dependencias externas adicionales ni emojis.
 */
(function (global) {
  'use strict';

  // Taxonomía y datos clínicos de microorganismos modelados
  const MICROBE_DATA = {
    s_sanguinis: {
      name: 'Streptococcus sanguinis',
      gram: 'Grampositivo (+)',
      morphology: 'Cocos en cadenas cortas (0.8 - 1.0 µm)',
      phase: 2,
      role: 'Colonizador primario pionero. Adhesinas fimbriales FimA que reconocen amilasa y proteínas ricas en prolina (PRPs) de la película adquirida.',
      clinical: 'Produce peróxido de hidrógeno antagonista contra patógenos periodontales tempranos, pero facilita la sucesión ecológica posterior.'
    },
    s_mitis: {
      name: 'Streptococcus mitis',
      gram: 'Grampositivo (+)',
      morphology: 'Cocos ovoides en pares o cadenas (0.6 - 0.8 µm)',
      phase: 2,
      role: 'Colonizador pionero esencial. Secreta proteasas IgA1 que neutralizan las defensas humorales de la saliva.',
      clinical: 'Componente del 60-80% de la microbiota en las primeras 4 horas tras la profilaxis dental.'
    },
    a_naeslundii: {
      name: 'Actinomyces naeslundii',
      gram: 'Grampositivo (+)',
      morphology: 'Bacilos ramificados pleomórficos (1.5 - 3.0 µm)',
      phase: 2,
      role: 'Colonizador primario con fimbrias tipo 1 (unión al esmalte) y tipo 2 (unión a galactosa en estreptococos).',
      clinical: 'Facilita la transición de una placa estrictamente aeróbica a microaerofílica en el tercio cervical y radicular.'
    },
    f_nucleatum: {
      name: 'Fusobacterium nucleatum',
      gram: 'Gramnegativo (-)',
      morphology: 'Bacilos fusiformes alargados con extremos afilados (5 - 10 µm)',
      phase: 3,
      role: 'El "puente biológico" central de la coagregación (Complejo Naranja). Posee la adhesina RadD y Fap2.',
      clinical: 'Permite el anclaje físico de patógenos anaerobios estrictos que no pueden unirse directamente al esmalte.'
    },
    v_parvula: {
      name: 'Veillonella parvula',
      gram: 'Gramnegativo (-)',
      morphology: 'Diplococos muy pequeños (0.3 - 0.5 µm)',
      phase: 3,
      role: 'Consumidor obligado de ácido láctico producido por estreptococos, convirtiéndolo en ácidos más débiles (propionato/acetato).',
      clinical: 'Simbiosis metabólica estrecha que amortigua el descenso del pH crítico.'
    },
    p_gingivalis: {
      name: 'Porphyromonas gingivalis',
      gram: 'Gramnegativo (-)',
      morphology: 'Cocobacilos anaerobios estrictos con fimbrias mayores y menores',
      phase: 4,
      role: 'Miembro culminante del Complejo Rojo de Socransky. Secreta gingipaínas (RgpA, RgpB, Kgp) altamente proteolíticas.',
      clinical: 'Inductor clave de disbiosis, degradación de colágeno gingival y reabsorción ósea periodontal.'
    },
    t_denticola: {
      name: 'Treponema denticola',
      gram: 'Gramnegativo (-)',
      morphology: 'Espiroqueta helicoidal flexible y móvil (6 - 15 µm)',
      phase: 4,
      role: 'Motilidad mediante filamentos periplásmicos a través de la matriz de EPS espesa. Miembro del Complejo Rojo.',
      clinical: 'Penetra tejidos blandos e invaden conductos laterales y itsmos endodónticos.'
    },
    e_faecalis: {
      name: 'Enterococcus faecalis',
      gram: 'Grampositivo (+)',
      morphology: 'Cocos ovoides en parejas o cadenas cortas (0.6 - 2.0 µm)',
      phase: 5,
      role: 'Patógeno endodóntico primordial en infecciones persistentes/secundarias. Bomba de protones que tolera pH > 11.5.',
      clinical: 'Invade los túbulos dentinarios hasta profundidades de 800-1000 µm y resiste la medicación intraconducto tradicional con hidróxido de calcio.'
    }
  };

  function BiofilmSimulator(container, options) {
    this.container = typeof container === 'string' ? document.querySelector(container) : container;
    if (!this.container) throw new Error('BiofilmSimulator: Contenedor no encontrado.');

    this.options = Object.assign({
      onPhaseChange: null,
      onMicrobeSelected: null,
      onProgress: null
    }, options);

    this.currentPhase = 1; // 1 a 5
    this.progress = 0;     // 0.0 a 1.0 continuo
    this.isPlaying = false;
    this.playbackRate = 1.0;
    this.isIrrigating = false;
    this.irrigationProgress = 0;
    this.currentCameraView = 'surface'; // 'surface' | 'tubules' | 'canal'

    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.controls = null;
    this.animId = null;
    this.clock = new THREE.Clock();

    this.meshGroups = {
      enamelSurface: null,
      pellicle: null,
      tubulesCrossSection: null,
      rootCanalSagittal: null,
      microbes: null,
      epsMatrix: null,
      irrigationFluid: null,
      nutrientChannels: null
    };

    this.microbeMeshes = [];
    this.raycaster = new THREE.Raycaster();
    this.mouse = new THREE.Vector2(-999, -999);
    this.hoveredMicrobe = null;

    this.init();
  }

  BiofilmSimulator.prototype.init = function () {
    const width = this.container.clientWidth || 800;
    const height = this.container.clientHeight || 550;

    // Escena
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x060b14); // Azul marino quirúrgico muy profundo
    this.scene.fog = new THREE.FogExp2(0x060b14, 0.012);

    // Cámara
    this.camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    this.camera.position.set(0, 18, 38);

    // Renderizador WebGL
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
    this.renderer.setSize(width, height);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.15;
    this.container.appendChild(this.renderer.domElement);

    // Controles de órbita
    if (typeof THREE.OrbitControls !== 'undefined') {
      this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
      this.controls.enableDamping = true;
      this.controls.dampingFactor = 0.05;
      this.controls.maxDistance = 85;
      this.controls.minDistance = 6;
      this.controls.maxPolarAngle = Math.PI / 2 + 0.1;
      this.controls.target.set(0, 2, 0);
    }

    // Iluminación médica de alta precisión
    this.setupLighting();

    // Construcción de la geometría anatómica y microbiológica
    this.buildAnatomy();
    this.buildMicrobes();
    this.buildEPSMatrix();
    this.buildIrrigationEffect();

    // Eventos interactivos
    this.bindEvents();

    // Actualizar estado inicial (Fase 1)
    this.updatePhase(1, false);

    // Loop de animación
    this.animate = this.animate.bind(this);
    this.animate();
  };

  BiofilmSimulator.prototype.setupLighting = function () {
    const ambient = new THREE.AmbientLight(0x283b54, 1.2);
    this.scene.add(ambient);

    // Luz principal tipo lámpara cialítica dental
    const mainLight = new THREE.DirectionalLight(0xe0f2fe, 2.2);
    mainLight.position.set(15, 30, 25);
    this.scene.add(mainLight);

    // Luz de relleno cian para resaltar la biopelícula
    const fillLight = new THREE.DirectionalLight(0x0284c7, 1.4);
    fillLight.position.set(-20, 15, -10);
    this.scene.add(fillLight);

    // Luz cálida para la pulpa dental profunda
    const pulpLight = new THREE.PointLight(0xf43f5e, 1.8, 40);
    pulpLight.position.set(0, -6, 0);
    this.scene.add(pulpLight);
  };

  BiofilmSimulator.prototype.buildAnatomy = function () {
    // 1. Superficie de esmalte de hidroxiapatita (prisma de esmalte ondulado y estriado)
    const enamelGeo = new THREE.CylinderGeometry(18, 17, 3.5, 64, 8);
    const enamelMat = new THREE.MeshStandardMaterial({
      color: 0xf1f5f9,
      roughness: 0.25,
      metalness: 0.1,
      bumpScale: 0.08
    });
    const enamel = new THREE.Mesh(enamelGeo, enamelMat);
    enamel.position.set(0, -1.8, 0);
    this.meshGroups.enamelSurface = enamel;
    this.scene.add(enamel);

    // Prisma cristalino de hidroxiapatita en el borde
    const rimGeo = new THREE.TorusGeometry(18, 0.4, 16, 64);
    const rimMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.4 });
    const rim = new THREE.Mesh(rimGeo, rimMat);
    rim.rotation.x = Math.PI / 2;
    rim.position.y = -0.1;
    this.scene.add(rim);

    // 2. Capa de Película Salival Adquirida (translúcida, rica en glicoproteínas)
    const pellicleGeo = new THREE.CylinderGeometry(18.05, 17.95, 0.15, 64);
    const pellicleMat = new THREE.MeshPhysicalMaterial({
      color: 0x38bdf8,
      transparent: true,
      opacity: 0.45,
      roughness: 0.15,
      transmission: 0.6,
      thickness: 0.8
    });
    const pellicle = new THREE.Mesh(pellicleGeo, pellicleMat);
    pellicle.position.set(0, 0.05, 0);
    this.meshGroups.pellicle = pellicle;
    this.scene.add(pellicle);

    // 3. Corte transversal de Túbulos Dentinarios (Modo 'tubules')
    const tubulesGroup = new THREE.Group();
    tubulesGroup.visible = false;

    // Matriz de dentina mineralizada
    const dentinBlockGeo = new THREE.BoxGeometry(26, 12, 16);
    const dentinBlockMat = new THREE.MeshStandardMaterial({
      color: 0xfef08a,
      roughness: 0.6,
      metalness: 0.05
    });
    const dentinBlock = new THREE.Mesh(dentinBlockGeo, dentinBlockMat);
    tubulesGroup.add(dentinBlock);

    // Túbulos dentinarios cilíndricos microscópicos con fluido peritubular
    const tubuleGeo = new THREE.CylinderGeometry(0.55, 0.55, 12.2, 16);
    const tubuleMat = new THREE.MeshStandardMaterial({
      color: 0x0284c7,
      roughness: 0.2,
      transparent: true,
      opacity: 0.5
    });

    for (let x = -10; x <= 10; x += 2.8) {
      for (let z = -6; z <= 6; z += 2.8) {
        const t = new THREE.Mesh(tubuleGeo, tubuleMat);
        t.position.set(x + (Math.random() - 0.5) * 0.4, 0, z + (Math.random() - 0.5) * 0.4);
        tubulesGroup.add(t);
      }
    }
    tubulesGroup.position.set(0, 0, -2);
    this.meshGroups.tubulesCrossSection = tubulesGroup;
    this.scene.add(tubulesGroup);

    // 4. Sistema Sagital Endodóntico (Cámara pulpar, conducto radicular principal, itsmo, foramen apical)
    const canalGroup = new THREE.Group();
    canalGroup.visible = false;

    // Contorno de raíz y corona dental en corte
    const rootShape = new THREE.Shape();
    rootShape.moveTo(-7, 10);
    rootShape.lineTo(7, 10);
    rootShape.quadraticCurveTo(6, 0, 3.5, -12);
    rootShape.quadraticCurveTo(2, -18, 0, -22); // Ápice
    rootShape.quadraticCurveTo(-2, -18, -3.5, -12);
    rootShape.quadraticCurveTo(-6, 0, -7, 10);

    const extrudeSettings = { depth: 3.5, bevelEnabled: true, bevelSegments: 3, steps: 1, bevelSize: 0.3, bevelThickness: 0.3 };
    const rootGeo = new THREE.ExtrudeGeometry(rootShape, extrudeSettings);
    const rootMat = new THREE.MeshStandardMaterial({
      color: 0xf8fafc,
      roughness: 0.35,
      transparent: true,
      opacity: 0.85
    });
    const rootMesh = new THREE.Mesh(rootGeo, rootMat);
    rootMesh.position.set(0, 0, -1.75);
    canalGroup.add(rootMesh);

    // Conducto radicular interno necrótico (luz del conducto con biofilm periapical)
    const canalShape = new THREE.Shape();
    canalShape.moveTo(-2.2, 8.5);
    canalShape.lineTo(2.2, 8.5);
    canalShape.quadraticCurveTo(1.5, 0, 1.0, -10);
    canalShape.quadraticCurveTo(0.6, -17, 0.3, -21.8); // Foramen apical estrecho
    canalShape.lineTo(-0.3, -21.8);
    canalShape.quadraticCurveTo(-0.6, -17, -1.0, -10);
    canalShape.quadraticCurveTo(-1.5, 0, -2.2, 8.5);

    const canalGeo = new THREE.ExtrudeGeometry(canalShape, { depth: 2.0, bevelEnabled: false });
    const canalMat = new THREE.MeshStandardMaterial({
      color: 0x991b1b, // Necrosis pulpar
      roughness: 0.4,
      emissive: 0x450a0a,
      emissiveIntensity: 0.4
    });
    const canalMesh = new THREE.Mesh(canalGeo, canalMat);
    canalMesh.position.set(0, 0, -1.0);
    canalGroup.add(canalMesh);

    // Lesión periapical granulomatosa/quística en el periápice
    const lesionGeo = new THREE.SphereGeometry(3.5, 24, 24);
    const lesionMat = new THREE.MeshStandardMaterial({
      color: 0xdc2626,
      roughness: 0.7,
      transparent: true,
      opacity: 0.75,
      emissive: 0x7f1d1d,
      emissiveIntensity: 0.6
    });
    const lesion = new THREE.Mesh(lesionGeo, lesionMat);
    lesion.position.set(0, -23.5, 0);
    canalGroup.add(lesion);

    canalGroup.position.set(0, 5, 0);
    this.meshGroups.rootCanalSagittal = canalGroup;
    this.scene.add(canalGroup);
  };

  BiofilmSimulator.prototype.buildMicrobes = function () {
    const microbesGroup = new THREE.Group();
    this.microbeMeshes = [];

    // Geometrías base
    const sphereGeo = new THREE.SphereGeometry(0.42, 16, 16);
    const ovalGeo = new THREE.SphereGeometry(0.48, 16, 16);
    ovalGeo.scale(1, 1.35, 1);
    const rodGeo = new THREE.CylinderGeometry(0.32, 0.32, 1.6, 12);
    const fusiformGeo = new THREE.CylinderGeometry(0.12, 0.38, 2.8, 12);
    const spirocheteGeo = new THREE.TorusGeometry(1.0, 0.12, 8, 24, Math.PI * 2.5);

    // Materiales con códigos de color de contraste médico
    const mats = {
      strep: new THREE.MeshStandardMaterial({ color: 0x38bdf8, roughness: 0.3, emissive: 0x0369a1, emissiveIntensity: 0.2 }),
      actinomyces: new THREE.MeshStandardMaterial({ color: 0x818cf8, roughness: 0.4, emissive: 0x4338ca, emissiveIntensity: 0.2 }),
      fusobacterium: new THREE.MeshStandardMaterial({ color: 0xfb923c, roughness: 0.35, emissive: 0xc2410c, emissiveIntensity: 0.25 }),
      veillonella: new THREE.MeshStandardMaterial({ color: 0xfacc15, roughness: 0.3 }),
      porphyromonas: new THREE.MeshStandardMaterial({ color: 0xf43f5e, roughness: 0.2, emissive: 0x9f1239, emissiveIntensity: 0.3 }),
      treponema: new THREE.MeshStandardMaterial({ color: 0xa855f7, roughness: 0.3, emissive: 0x6b21a8, emissiveIntensity: 0.3 }),
      enterococcus: new THREE.MeshStandardMaterial({ color: 0x10b981, roughness: 0.25, emissive: 0x047857, emissiveIntensity: 0.35 })
    };

    const addMicrobe = (key, geo, mat, count, radiusSpread, minPhase, yBase, ySpread) => {
      for (let i = 0; i < count; i++) {
        const mesh = new THREE.Mesh(geo, mat);
        const angle = Math.random() * Math.PI * 2;
        const rad = Math.sqrt(Math.random()) * radiusSpread;
        const x = Math.cos(angle) * rad;
        const z = Math.sin(angle) * rad;
        const y = yBase + Math.random() * ySpread;

        mesh.position.set(x, y, z);
        mesh.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, Math.random() * Math.PI);

        mesh.userData = {
          key: key,
          info: MICROBE_DATA[key],
          minPhase: minPhase,
          originalY: y,
          originalScale: 1.0,
          driftSpeed: 0.2 + Math.random() * 0.4,
          driftOffset: Math.random() * Math.PI * 2
        };

        microbesGroup.add(mesh);
        this.microbeMeshes.push(mesh);
      }
    };

    // Distribución escalonada por fases
    // Fase 2 (Colonizadores primarios)
    addMicrobe('s_sanguinis', sphereGeo, mats.strep, 36, 15, 2, 0.4, 0.4);
    addMicrobe('s_mitis', sphereGeo, mats.strep, 28, 14, 2, 0.4, 0.4);
    addMicrobe('a_naeslundii', rodGeo, mats.actinomyces, 22, 13, 2, 0.5, 0.6);

    // Fase 3 (Co-agregación y puente de Fusobacterium)
    addMicrobe('f_nucleatum', fusiformGeo, mats.fusobacterium, 32, 14, 3, 0.8, 1.8);
    addMicrobe('v_parvula', sphereGeo, mats.veillonella, 26, 12, 3, 0.7, 1.2);

    // Fase 4 (Maduración y Complejo Rojo)
    addMicrobe('p_gingivalis', ovalGeo, mats.porphyromonas, 35, 13, 4, 1.2, 2.5);
    addMicrobe('t_denticola', spirocheteGeo, mats.treponema, 18, 11, 4, 1.5, 3.2);

    // Fase 5 (Invasión y Endodoncia - Enterococcus faecalis)
    addMicrobe('e_faecalis', ovalGeo, mats.enterococcus, 42, 12, 5, 0.4, 4.0);

    this.meshGroups.microbes = microbesGroup;
    this.scene.add(microbesGroup);
  };

  BiofilmSimulator.prototype.buildEPSMatrix = function () {
    const epsGroup = new THREE.Group();

    // Nube translúcida de EPS (glucanos y fructanos)
    const epsGeo = new THREE.CylinderGeometry(15.5, 16.5, 3.8, 48, 4);
    const epsMat = new THREE.MeshPhysicalMaterial({
      color: 0x0284c7,
      transparent: true,
      opacity: 0.0, // Inicia invisible en fase 1
      roughness: 0.1,
      transmission: 0.85,
      thickness: 1.2,
      depthWrite: false
    });
    const epsMesh = new THREE.Mesh(epsGeo, epsMat);
    epsMesh.position.set(0, 1.9, 0);
    epsGroup.add(epsMesh);

    // Canales de fluidos y transporte convectivo de nutrientes
    const channelMat = new THREE.MeshBasicMaterial({
      color: 0x38bdf8,
      transparent: true,
      opacity: 0.0,
      wireframe: true
    });
    for (let i = 0; i < 6; i++) {
      const angle = (i / 6) * Math.PI * 2;
      const cGeo = new THREE.CylinderGeometry(0.6, 0.8, 3.8, 8);
      const cMesh = new THREE.Mesh(cGeo, channelMat);
      cMesh.position.set(Math.cos(angle) * 7.5, 1.9, Math.sin(angle) * 7.5);
      epsGroup.add(cMesh);
    }

    this.meshGroups.epsMatrix = epsMesh;
    this.meshGroups.nutrientChannels = epsGroup;
    this.scene.add(epsGroup);
  };

  BiofilmSimulator.prototype.buildIrrigationEffect = function () {
    // Simulación de flujo de irrigante (NaOCl 5.25% + EDTA 17%) con cánula apical
    const irrGroup = new THREE.Group();
    irrGroup.visible = false;

    // Cánula de irrigación metálica fina con salida lateral (Side-vented 30G)
    const cannulaGeo = new THREE.CylinderGeometry(0.35, 0.35, 14, 16);
    const cannulaMat = new THREE.MeshStandardMaterial({
      color: 0xe2e8f0,
      metalness: 0.85,
      roughness: 0.2
    });
    const cannula = new THREE.Mesh(cannulaGeo, cannulaMat);
    cannula.position.set(0, 4, 0);
    irrGroup.add(cannula);

    // Nube de efervescencia y burbujas de oxígeno liberadas por el hipoclorito de sodio
    const bubbleCount = 75;
    const bubbleGeo = new THREE.BufferGeometry();
    const positions = new Float32Array(bubbleCount * 3);
    for (let i = 0; i < bubbleCount; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 4;
      positions[i * 3 + 1] = -2 - Math.random() * 15;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 4;
    }
    bubbleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const bubbleMat = new THREE.PointsMaterial({
      color: 0x67e8f9,
      size: 0.6,
      transparent: true,
      opacity: 0.8
    });
    const bubbles = new THREE.Points(bubbleGeo, bubbleMat);
    irrGroup.add(bubbles);

    this.meshGroups.irrigationFluid = irrGroup;
    this.scene.add(irrGroup);
  };

  BiofilmSimulator.prototype.bindEvents = function () {
    const self = this;
    const dom = this.renderer.domElement;

    // Redimensionamiento responsive
    window.addEventListener('resize', function () {
      if (!self.container) return;
      const w = self.container.clientWidth;
      const h = self.container.clientHeight || 550;
      self.camera.aspect = w / h;
      self.camera.updateProjectionMatrix();
      self.renderer.setSize(w, h);
    });

    // Raycaster para selección e inspección táctil/cursor
    const onPointerMove = function (e) {
      const rect = dom.getBoundingClientRect();
      self.mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      self.mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      self.raycaster.setFromCamera(self.mouse, self.camera);
      const visibleMicrobes = self.microbeMeshes.filter(m => m.visible);
      const intersects = self.raycaster.intersectObjects(visibleMicrobes);

      if (intersects.length > 0) {
        const hit = intersects[0].object;
        dom.style.cursor = 'pointer';
        if (self.hoveredMicrobe !== hit) {
          if (self.hoveredMicrobe) self.hoveredMicrobe.scale.set(1, 1, 1);
          self.hoveredMicrobe = hit;
          self.hoveredMicrobe.scale.set(1.5, 1.5, 1.5);
          if (self.options.onMicrobeSelected) {
            self.options.onMicrobeSelected(hit.userData.info);
          }
        }
      } else {
        dom.style.cursor = 'grab';
        if (self.hoveredMicrobe) {
          self.hoveredMicrobe.scale.set(1, 1, 1);
          self.hoveredMicrobe = null;
        }
      }
    };

    dom.addEventListener('pointermove', onPointerMove);
    dom.addEventListener('pointerdown', function (e) {
      dom.style.cursor = 'grabbing';
      onPointerMove(e);
    });
    dom.addEventListener('pointerup', function () {
      dom.style.cursor = 'grab';
    });
  };

  BiofilmSimulator.prototype.setCameraView = function (viewName) {
    this.currentCameraView = viewName;

    if (viewName === 'surface') {
      // Vista oclusal de la superficie del esmalte con biopelícula
      this.meshGroups.enamelSurface.visible = true;
      this.meshGroups.pellicle.visible = true;
      this.meshGroups.tubulesCrossSection.visible = false;
      this.meshGroups.rootCanalSagittal.visible = false;
      this.meshGroups.microbes.position.set(0, 0, 0);

      this.animateCamera(0, 16, 32, 0, 2, 0);
    } else if (viewName === 'tubules') {
      // Corte histológico de túbulos dentinarios
      this.meshGroups.enamelSurface.visible = false;
      this.meshGroups.pellicle.visible = false;
      this.meshGroups.tubulesCrossSection.visible = true;
      this.meshGroups.rootCanalSagittal.visible = false;
      this.meshGroups.microbes.position.set(0, 2.5, 0);

      this.animateCamera(0, 10, 24, 0, 0, 0);
    } else if (viewName === 'canal') {
      // Corte sagital de endodoncia (conducto radicular y periápice)
      this.meshGroups.enamelSurface.visible = false;
      this.meshGroups.pellicle.visible = false;
      this.meshGroups.tubulesCrossSection.visible = false;
      this.meshGroups.rootCanalSagittal.visible = true;
      this.meshGroups.microbes.position.set(0, -6, 0);

      this.animateCamera(0, -5, 42, 0, -8, 0);
    }
  };

  BiofilmSimulator.prototype.animateCamera = function (px, py, pz, tx, ty, tz) {
    if (!this.controls) return;
    const startPos = this.camera.position.clone();
    const targetPos = new THREE.Vector3(px, py, pz);
    const startTarget = this.controls.target.clone();
    const endTarget = new THREE.Vector3(tx, ty, tz);
    const startTime = performance.now();
    const duration = 600;
    const self = this;

    function step(now) {
      const p = Math.min(1, (now - startTime) / duration);
      const ease = 1 - Math.pow(1 - p, 3);

      self.camera.position.lerpVectors(startPos, targetPos, ease);
      self.controls.target.lerpVectors(startTarget, endTarget, ease);
      self.controls.update();

      if (p < 1) {
        requestAnimationFrame(step);
      }
    }
    requestAnimationFrame(step);
  };

  BiofilmSimulator.prototype.updatePhase = function (phaseNumber, notify) {
    this.currentPhase = Math.max(1, Math.min(5, phaseNumber));
    this.progress = (this.currentPhase - 1) / 4.0;

    // Actualizar visibilidad de bacterias según la fase
    this.microbeMeshes.forEach(mesh => {
      const req = mesh.userData.minPhase;
      mesh.visible = (req <= this.currentPhase);
      // Animación de escala de aparición
      if (mesh.visible) {
        const phaseRatio = (this.currentPhase - req + 1) / 2.0;
        const s = Math.min(1.0, 0.4 + phaseRatio * 0.6);
        mesh.scale.set(s, s, s);
      }
    });

    // Actualizar espesor y opacidad de la matriz EPS
    if (this.meshGroups.epsMatrix) {
      if (this.currentPhase < 4) {
        this.meshGroups.epsMatrix.material.opacity = (this.currentPhase === 3) ? 0.18 : 0.0;
      } else if (this.currentPhase === 4) {
        this.meshGroups.epsMatrix.material.opacity = 0.55;
      } else if (this.currentPhase === 5) {
        this.meshGroups.epsMatrix.material.opacity = 0.72;
      }
    }

    // Canales de nutrientes
    if (this.meshGroups.nutrientChannels) {
      this.meshGroups.nutrientChannels.children.forEach(child => {
        if (child !== this.meshGroups.epsMatrix) {
          child.material.opacity = (this.currentPhase >= 4) ? 0.45 : 0.0;
        }
      });
    }

    // Película salival adquirida
    if (this.meshGroups.pellicle) {
      this.meshGroups.pellicle.material.opacity = (this.currentPhase >= 1) ? 0.5 : 0.0;
    }

    if (notify !== false && this.options.onPhaseChange) {
      this.options.onPhaseChange(this.currentPhase, this.progress);
    }
  };

  BiofilmSimulator.prototype.setProgress = function (progressRatio) {
    this.progress = Math.max(0, Math.min(1, progressRatio));
    // Mapear 0..1 a fases 1..5
    const computedPhase = Math.min(5, Math.floor(this.progress * 4) + 1);
    if (computedPhase !== this.currentPhase) {
      this.updatePhase(computedPhase, true);
    }
    if (this.options.onProgress) {
      this.options.onProgress(this.progress, computedPhase);
    }
  };

  BiofilmSimulator.prototype.play = function () {
    this.isPlaying = true;
  };

  BiofilmSimulator.prototype.pause = function () {
    this.isPlaying = false;
  };

  BiofilmSimulator.prototype.togglePlay = function () {
    if (this.isPlaying) this.pause();
    else this.play();
    return this.isPlaying;
  };

  BiofilmSimulator.prototype.setPlaybackRate = function (rate) {
    this.playbackRate = rate;
  };

  BiofilmSimulator.prototype.triggerEndodonticIrrigation = function (callback) {
    this.isIrrigating = true;
    this.irrigationProgress = 0;
    this.setCameraView('canal');
    this.meshGroups.irrigationFluid.visible = true;

    const self = this;
    const startTime = performance.now();
    const duration = 3800; // 3.8 segundos de animación de desinfección

    function step(now) {
      const elapsed = now - startTime;
      self.irrigationProgress = Math.min(1, elapsed / duration);

      // Efecto 1: Descenso de la cánula
      const cannula = self.meshGroups.irrigationFluid.children[0];
      if (cannula) {
        cannula.position.y = 8 - self.irrigationProgress * 18;
      }

      // Efecto 2: Reducción drástica del biofilm y matriz bacteriana por NaOCl
      const lisisFactor = 1 - self.irrigationProgress * 0.92;
      self.microbeMeshes.forEach(mesh => {
        if (mesh.userData.minPhase === 5) {
          mesh.scale.set(lisisFactor, lisisFactor, lisisFactor);
        }
      });

      if (self.meshGroups.epsMatrix) {
        self.meshGroups.epsMatrix.material.opacity = Math.max(0.05, 0.72 * lisisFactor);
      }

      if (self.irrigationProgress < 1) {
        requestAnimationFrame(step);
      } else {
        self.isIrrigating = false;
        setTimeout(() => {
          self.meshGroups.irrigationFluid.visible = false;
          if (callback) callback();
        }, 1200);
      }
    }
    requestAnimationFrame(step);
  };

  BiofilmSimulator.prototype.animate = function () {
    this.animId = requestAnimationFrame(this.animate);

    const delta = this.clock.getDelta();
    const time = this.clock.getElapsedTime();

    // Avance de video si está en reproducción
    if (this.isPlaying && !this.isIrrigating) {
      this.progress += (delta * 0.08 * this.playbackRate);
      if (this.progress >= 1.0) {
        this.progress = 1.0;
        this.isPlaying = false;
      }
      this.setProgress(this.progress);
    }

    // Micro-movimiento fisiológico browniano de bacterias vivas
    this.microbeMeshes.forEach(mesh => {
      if (mesh.visible) {
        const u = mesh.userData;
        mesh.position.y = u.originalY + Math.sin(time * u.driftSpeed + u.driftOffset) * 0.08;
        if (u.key === 't_denticola') {
          // Espiroqueta móvil rotando en espiral
          mesh.rotation.z += delta * 1.8;
        }
      }
    });

    // Animación de burbujas de irrigación
    if (this.isIrrigating && this.meshGroups.irrigationFluid.visible) {
      const pts = this.meshGroups.irrigationFluid.children[1];
      if (pts) {
        pts.rotation.y += delta * 3;
      }
    }

    if (this.controls) {
      this.controls.update();
    }

    this.renderer.render(this.scene, this.camera);
  };

  BiofilmSimulator.prototype.destroy = function () {
    if (this.animId) cancelAnimationFrame(this.animId);
    if (this.renderer && this.renderer.domElement && this.renderer.domElement.parentNode) {
      this.renderer.domElement.parentNode.removeChild(this.renderer.domElement);
    }
  };

  // Exponer en espacio global
  global.BiofilmSimulator = BiofilmSimulator;
  global.MICROBE_DATA = MICROBE_DATA;

})(typeof window !== 'undefined' ? window : this);
