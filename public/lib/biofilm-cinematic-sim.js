/**
 * OdontoScore - Simulador Cinematográfico de Biofilm Dental y Patología Endodóntica v2.5
 * Integración con Contexto Anatómico del Diente + Zoom de Inspección Ultraestructural
 * Sin emojis, diseño médico de precisión.
 */
(function (global) {
  'use strict';

  const SCENARIOS = {
    fase1: {
      id: 'fase1',
      title: 'Fase 1: Película Salival Adquirida',
      subtitle: '0 a 2 horas tras profilaxis | Adsorción macromolecular acelular sobre esmalte oclusal',
      image: '../assets/img/biofilm/fase1_pelicula.jpg',
      timeLabel: '0 - 2 Horas',
      anatomicalZone: 'Superficie Oclusal del Esmalte',
      description: 'Corte anatómico sagital de un molar mostrando la corona intacta. El círculo diana señala la fisura oclusal, ampliando hacia los prismas cristalinos de hidroxiapatita donde se adsorben las glicoproteínas salivales.',
      hotspots: [
        {
          id: 'p1_macro',
          name: 'Zona Diana: Fisura Oclusal del Molar',
          x: 29.0,
          y: 20.5,
          category: 'Contexto Anatómico',
          badge: 'Esmalte Coronal',
          detail: 'Superficie del esmalte dental expuesta al flujo salival continuo. En este punto de contacto masticatorio comienza la adsorción electrostática inmediata tras el pulido dental.'
        },
        {
          id: 'p1_pelicula',
          name: 'Película Salival Adquirida (0.1 - 1 µm)',
          x: 73.0,
          y: 36.0,
          category: 'Biopolímero Acelular',
          badge: 'Protección y Anclaje',
          detail: 'Película acelular translúcida formada en segundos por mucinas (MUC5B/MUC7), estaterinas y amilasa. Protege de la atrición ácida, pero expone sitios receptores criptados para bacterias.'
        },
        {
          id: 'p1_prismas',
          name: 'Prismas Hexagonales de Hidroxiapatita',
          x: 68.0,
          y: 65.0,
          category: 'Ultraestructura',
          badge: 'Fosfato de Calcio',
          detail: 'Columnas cristalinas densamente empaquetadas de hidroxiapatita con orientación prismática. Su carga electronegativa neta atrae selectivamente a las proteínas catiónicas de la saliva.'
        }
      ]
    },
    fase2: {
      id: 'fase2',
      title: 'Fase 2: Colonización Primaria y Adhesión',
      subtitle: '2 a 6 horas | Llegada de colonizadores pioneros aerobios y facultativos al esmalte',
      image: '../assets/img/biofilm/fase2_adhesion.jpg',
      timeLabel: '2 - 6 Horas',
      anatomicalZone: 'Esmalte Oclusal Superficial',
      description: 'El molar muestra el inicio de la adherencia en el esmalte superior. El zoom revela cadenas de estreptococos pioneros y bacilos de Actinomyces anclándose a la película mediante fimbrias moleculares.',
      hotspots: [
        {
          id: 'p2_macro',
          name: 'Zona Diana: Esmalte Oclusal Superficial',
          x: 34.0,
          y: 20.0,
          category: 'Contexto Anatómico',
          badge: 'Superficie Dental',
          detail: 'Zona de adherencia inicial donde las fuerzas de corte de la masticación y la saliva interactúan con los primeros colonizadores bacterianos.'
        },
        {
          id: 'p2_strep',
          name: 'Streptococcus sanguinis en Cadenas',
          x: 72.5,
          y: 54.0,
          category: 'Colonizador Pionero',
          badge: 'Grampositivo (+)',
          detail: 'Cocos esféricos en cadenas que reconocen las proteínas ricas en prolina de la película salival. Producen H2O2 como mecanismo de defensa contra bacterias competidoras.'
        },
        {
          id: 'p2_actino',
          name: 'Actinomyces naeslundii Ramificado',
          x: 82.0,
          y: 37.0,
          category: 'Bacilo Filamentoso',
          badge: 'Grampositivo (+)',
          detail: 'Bacilos ramificados con fimbrias tipo 1 (unión al esmalte) y tipo 2 (unión a galactosa). Su consumo constante de oxígeno prepara el nicho para futuros anaerobios.'
        }
      ]
    },
    fase3: {
      id: 'fase3',
      title: 'Fase 3: Co-agregación y Proliferación',
      subtitle: '6 a 24 horas | El puente biológico de Fusobacterium nucleatum en el margen cervical',
      image: '../assets/img/biofilm/fase3_coagregacion.jpg',
      timeLabel: '6 - 24 Horas',
      anatomicalZone: 'Margen Cervical y Zona Interproximal',
      description: 'El corte anatómico señala la acumulación de placa en el cuello del diente. El zoom descubre el puente físico de Fusobacterium nucleatum agrupando cocos en formaciones en mazorca de maíz.',
      hotspots: [
        {
          id: 'p3_macro',
          name: 'Zona Diana: Margen Cervical y Tercio Gingival',
          x: 35.5,
          y: 42.5,
          category: 'Contexto Anatómico',
          badge: 'Cuello Anatómico',
          detail: 'El surco gingival y el espacio interproximal ofrecen protección contra el cepillado, permitiendo la proliferación bacteriana y la formación de microcolonias densas.'
        },
        {
          id: 'p3_fuso',
          name: 'Fusobacterium nucleatum (Puente Biológico)',
          x: 74.5,
          y: 52.0,
          category: 'Complejo Naranja',
          badge: 'Gramnegativo (-)',
          detail: 'Bacilo fusiforme largo que expresa las adhesinas RadD y Fap2. Es el puente físico que conecta a los colonizadores tempranos con los patógenos anaerobios tardíos.'
        },
        {
          id: 'p3_corn',
          name: 'Formación en Mazorca de Maíz (Corn-Cob)',
          x: 79.0,
          y: 34.0,
          category: 'Asociación Tisular',
          badge: 'Simbiosis Estructural',
          detail: 'Rosetas interbacterianas donde un eje central filamentoso queda rodeado por cientos de cocos de Veillonella y Streptococcus, optimizando el traspaso de nutrientes y metabolitos.'
        }
      ]
    },
    fase4: {
      id: 'fase4',
      title: 'Fase 4: Biofilm Maduro y Matriz de EPS',
      subtitle: '24 a 72+ horas | Síntesis de glucanos, canales acuosos y Complejo Rojo en fosas profundas',
      image: '../assets/img/biofilm/fase4_maduracion.jpg',
      timeLabel: '24 - 72+ Horas',
      anatomicalZone: 'Fosa Oclusal con Desmineralización',
      description: 'El molar exhibe placa madura acumulada en el fondo de la fosa oclusal. El zoom muestra la matriz gelatinosa de glucanos con canales acuosos y patógenos anaerobios del Complejo Rojo.',
      hotspots: [
        {
          id: 'p4_macro',
          name: 'Zona Diana: Fosa Oclusal Profunda',
          x: 25.5,
          y: 29.0,
          category: 'Contexto Anatómico',
          badge: 'Inicio de Caries',
          detail: 'Zona de estancamiento retentivo donde el biofilm alcanza su máximo espesor y madurez tridimensional, provocando una caída prolongada del pH por debajo de 5.5.'
        },
        {
          id: 'p4_eps',
          name: 'Matriz Extracelular de EPS (Glucanos)',
          x: 73.0,
          y: 31.0,
          category: 'Glucocáliz Protector',
          badge: 'Barrera x1000',
          detail: 'Matriz mucosa de exopolisacáridos insolubles sintetizada por glucosiltransferasas. Actúa como barrera física contra enjuagues y defensas del huésped.'
        },
        {
          id: 'p4_canales',
          name: 'Canales Acuosos de Flujo Convectivo',
          x: 71.0,
          y: 57.0,
          category: 'Sistema Circulatorio',
          badge: 'Transporte de Fluidos',
          detail: 'Red de hendiduras abiertas entre las microcolonias por donde circula líquido gingival y saliva, garantizando el aporte de nutrientes y la salida de toxinas.'
        },
        {
          id: 'p4_spiro',
          name: 'Treponema denticola y P. gingivalis',
          x: 82.0,
          y: 42.0,
          category: 'Complejo Rojo',
          badge: 'Espiroquetas Móviles',
          detail: 'Anaerobios estrictos de máxima virulencia. Las espiroquetas móviles reptan por la matriz de EPS e inician la penetración destructiva hacia el tejido dental.'
        }
      ]
    },
    fase5: {
      id: 'fase5',
      title: 'Fase 5: Desprendimiento e Invasión de Túbulos Dentinarios',
      subtitle: '> 3 días a semanas | Desmineralización de dentina y migración hacia la pulpa',
      image: '../assets/img/biofilm/fase5_invasion.jpg',
      timeLabel: '> 3 Días',
      anatomicalZone: 'Dentina Peripulpar y Túbulos',
      description: 'El molar muestra una cavidad cariosa profunda que destruyó el esmalte y perforó la dentina. El zoom revela los túbulos dentinarios cilíndricos por donde migran las bacterias hacia la pulpa.',
      hotspots: [
        {
          id: 'p5_macro',
          name: 'Zona Diana: Frente de Invasión Cariosa en Dentina',
          x: 34.0,
          y: 40.5,
          category: 'Contexto Anatómico',
          badge: 'Invasión Pulpar',
          detail: 'Pérdida de la unión amelodentinaria con reblandecimiento de la dentina. Las bacterias desprendidas de la biopelícula superficial se introducen en los canalículos abiertos.'
        },
        {
          id: 'p5_tubulos',
          name: 'Túbulos Dentinarios Cilíndricos (1 - 3 µm)',
          x: 76.5,
          y: 34.0,
          category: 'Anatomía Dental',
          badge: 'Vía de Penetración',
          detail: 'Canalículos microscópicos que atraviesan la dentina en dirección centrípeta hacia la cámara pulpar, conteniendo prolongaciones odontoblásticas y fluido dentinario.'
        },
        {
          id: 'p5_faecalis',
          name: 'Enterococcus faecalis e Invasión Intratubular',
          x: 65.0,
          y: 63.5,
          category: 'Patógeno Endodóntico',
          badge: 'Grampositivo (+)',
          detail: 'Bacterias migrando activamente en el interior de los túbulos dentinarios, alcanzando profundidades de 800 a 1000 µm y originando pulpitis irreversible.'
        },
        {
          id: 'p5_pulpa',
          name: 'Plexo Vascular y Tejido Pulpar',
          x: 85.5,
          y: 24.5,
          category: 'Tejido Pulpar',
          badge: 'Inflamación Aguda',
          detail: 'Tejido conectivo laxo inervado y vascularizado. La invasión bacteriana desata una respuesta inflamatoria pulpar aguda con edema, dolor intenso y necrosis progresiva.'
        }
      ]
    },
    endodoncia_conducto: {
      id: 'endodoncia_conducto',
      title: 'Patología Endodóntica: Necrosis Pulpar y Periodontitis Apical',
      subtitle: 'Corte anatómico sagital de molar con conductos infectados y lesión ósea periapical',
      image: '../assets/img/biofilm/endodoncia_conducto.jpg',
      timeLabel: 'Necrosis y Periápice',
      anatomicalZone: 'Ápice Radicular y Foramen Apical',
      description: 'El molar presenta necrosis total de la cámara pulpar y colonización de los conductos radiculares. El zoom enfoca el foramen apical y el delta radicular donde el biofilm genera una lesión osteolítica periapical.',
      hotspots: [
        {
          id: 'pec_camara',
          name: 'Cámara Pulpar Necrótica y Destrucción Coronal',
          x: 27.0,
          y: 25.0,
          category: 'Infección Primaria',
          badge: 'Necrosis Total',
          detail: 'Colapso vascular pulpar total con degradación del tejido y presencia de gas de putrefacción. El conducto radicular actúa como un reservorio anaeróbico no irrigado.'
        },
        {
          id: 'pec_macro',
          name: 'Zona Diana: Periápice y Foramen Apical',
          x: 35.5,
          y: 80.5,
          category: 'Contexto Anatómico',
          badge: 'Delta Apical',
          detail: 'Área periapical donde los conductos radiculares se abren hacia el ligamento periodontal y el hueso alveolar mandibular, desencadenando la respuesta inmunitaria.'
        },
        {
          id: 'pec_delta',
          name: 'Constricción Apical y Delta Radicular',
          x: 73.5,
          y: 45.0,
          category: 'Límite Anatómico',
          badge: 'Foramen Menor',
          detail: 'El diámetro apical estrecho (0.2 - 0.4 mm) concentra ramificaciones deltas tapizadas de biofilm sésil difícilmente accesibles por instrumentación manual.'
        },
        {
          id: 'pec_biofilm',
          name: 'Biofilm Periapical y Reabsorción Ósea',
          x: 79.0,
          y: 71.0,
          category: 'Periodontitis Apical',
          badge: 'Osteólisis Periapical',
          detail: 'Consorcio anaerobio estricto que desborda el ápice radicular. Los lipopolisacáridos bacterianos estimulan a los osteoclastos para disolver el hueso alveolar circundante.'
        }
      ]
    },
    endodoncia_irrigacion: {
      id: 'endodoncia_irrigacion',
      title: 'Terapéutica Endodóntica: Irrigación Química con NaOCl al 5.25%',
      subtitle: 'Acción química de disolución orgánica, micro-cavitación y lisis bacteriana',
      image: '../assets/img/biofilm/endodoncia_irrigacion.jpg',
      timeLabel: 'Desinfección Química',
      anatomicalZone: 'Tercio Medio y Apical del Conducto',
      description: 'Vista microscópica del tratamiento de conductos: una cánula apical de salida lateral introduce hipoclorito de sodio al 5.25% generando ondas acústicas y efervescencia que desprenden el biofilm de la pared.',
      hotspots: [
        {
          id: 'pei_canula',
          name: 'Cánula de Salida Lateral (Side-Vented 30G)',
          x: 55.5,
          y: 35.0,
          category: 'Dispositivo Clínico',
          badge: 'Seguridad Apical',
          detail: 'Aguja flexible con punta ciega que descarga el irrigante lateralmente contra las paredes dentinarias sin generar presión apical positiva riesgosa.'
        },
        {
          id: 'pei_naocl',
          name: 'Solvente Orgánico NaOCl (5.25%)',
          x: 42.0,
          y: 43.0,
          category: 'Acción Química',
          badge: 'Lisis de Biofilm',
          detail: 'El hipoclorito de sodio ejerce saponificación de lípidos de membrana y degradación de proteínas, desintegrando la matriz de exopolisacáridos del biofilm.'
        },
        {
          id: 'pei_pui',
          name: 'Ondas de Cavitación Ultrasónica (PUI a 30 kHz)',
          x: 64.0,
          y: 22.0,
          category: 'Activación Acústica',
          badge: 'Microflujo Acústico',
          detail: 'La oscilación acústica pasiva crea corrientes en vórtice que empujan el irrigante fresco hacia conductos laterales, itsmos y túbulos dentinarios profundos.'
        },
        {
          id: 'pei_dentina',
          name: 'Dentina Pericanalar Limpia y Permeable',
          x: 42.0,
          y: 72.0,
          category: 'Resultado Terapéutico',
          badge: 'Superficie Estéril',
          detail: 'Pared dentinaria libre de barrillo y biofilm bacteriano, lista para recibir el sellador biocerámico y la gutapercha en la obturación tridimensional definitiva.'
        }
      ]
    }
  };

  const SEQUENCE = ['fase1', 'fase2', 'fase3', 'fase4', 'fase5', 'endodoncia_conducto', 'endodoncia_irrigacion'];

  function BiofilmCinematicSim(container, options) {
    this.container = typeof container === 'string' ? document.querySelector(container) : container;
    if (!this.container) throw new Error('BiofilmCinematicSim: Contenedor no encontrado.');

    this.options = Object.assign({
      onScenarioChange: null,
      onHotspotSelect: null,
      onTimeUpdate: null
    }, options);

    this.currentScenarioIndex = 0;
    this.isPlaying = false;
    this.playbackRate = 1.0;
    this.showHotspots = true;
    this.activeHotspot = null;
    this.playTimer = null;
    this.animFrameId = null;

    this.canvas = null;
    this.ctx = null;
    this.imgElement = null;
    this.hotspotsOverlay = null;
    this.loadedImages = {};

    this.initDOM();
    this.preloadAssets();
    this.loadScenario(0);
    this.initCanvasEffects();
  }

  BiofilmCinematicSim.prototype.initDOM = function () {
    this.container.innerHTML = '';
    this.container.style.position = 'relative';
    this.container.style.overflow = 'hidden';
    this.container.style.borderRadius = '14px';
    this.container.style.aspectRatio = '16 / 9';
    this.container.style.background = '#060B14';
    this.container.style.userSelect = 'none';

    // 1. Imagen fotorealista de fondo con transición
    this.imgElement = document.createElement('img');
    this.imgElement.style.position = 'absolute';
    this.imgElement.style.inset = '0';
    this.imgElement.style.width = '100%';
    this.imgElement.style.height = '100%';
    this.imgElement.style.objectFit = 'cover';
    this.imgElement.style.transition = 'opacity 0.35s ease-in-out, transform 1.2s ease-out';
    this.imgElement.alt = 'Simulación médica de biofilm dental y endodoncia';
    this.container.appendChild(this.imgElement);

    // 2. Lienzo dinámico de partículas biológicas microscópicas
    this.canvas = document.createElement('canvas');
    this.canvas.style.position = 'absolute';
    this.canvas.style.inset = '0';
    this.canvas.style.width = '100%';
    this.canvas.style.height = '100%';
    this.canvas.style.pointerEvents = 'none';
    this.container.appendChild(this.canvas);
    this.ctx = this.canvas.getContext('2d');

    // 3. Capa de hitos anatómicos interactivos (Hotspots)
    this.hotspotsOverlay = document.createElement('div');
    this.hotspotsOverlay.className = 'biofilm-hotspots-overlay';
    this.hotspotsOverlay.style.position = 'absolute';
    this.hotspotsOverlay.style.inset = '0';
    this.hotspotsOverlay.style.pointerEvents = 'none';
    this.container.appendChild(this.hotspotsOverlay);

    // 4. Marca de agua médica estética superior
    const watermark = document.createElement('div');
    watermark.className = 'biofilm-watermark';
    watermark.innerHTML = '<span class="wm-dot"></span> <span id="biofilmTimeBadge">0 - 2 Horas</span>';
    this.container.appendChild(watermark);

    const self = this;
    window.addEventListener('resize', function () {
      self.resizeCanvas();
    });
  };

  BiofilmCinematicSim.prototype.resizeCanvas = function () {
    if (!this.canvas) return;
    const rect = this.container.getBoundingClientRect();
    this.canvas.width = rect.width * (window.devicePixelRatio || 1);
    this.canvas.height = rect.height * (window.devicePixelRatio || 1);
    if (this.ctx) {
      this.ctx.scale(window.devicePixelRatio || 1, window.devicePixelRatio || 1);
    }
  };

  BiofilmCinematicSim.prototype.preloadAssets = function () {
    const self = this;
    SEQUENCE.forEach(function (key) {
      const src = SCENARIOS[key].image;
      const img = new Image();
      img.src = src;
      img.onload = function () {
        self.loadedImages[key] = img;
      };
    });
  };

  BiofilmCinematicSim.prototype.loadScenario = function (index, animated) {
    index = Math.max(0, Math.min(SEQUENCE.length - 1, index));
    this.currentScenarioIndex = index;
    const key = SEQUENCE[index];
    const data = SCENARIOS[key];

    const self = this;
    this.imgElement.style.opacity = '0.35';
    this.imgElement.style.transform = 'scale(1.02)';

    setTimeout(function () {
      self.imgElement.src = data.image;
      self.imgElement.style.opacity = '1';
      self.imgElement.style.transform = 'scale(1)';
    }, 120);

    const badge = this.container.querySelector('#biofilmTimeBadge');
    if (badge) badge.textContent = data.timeLabel + ' | ' + data.anatomicalZone;

    this.renderHotspots(data.hotspots);

    if (this.options.onScenarioChange) {
      this.options.onScenarioChange(data, index, SEQUENCE.length);
    }
  };

  BiofilmCinematicSim.prototype.renderHotspots = function (hotspots) {
    this.hotspotsOverlay.innerHTML = '';
    if (!this.showHotspots) return;

    const self = this;
    hotspots.forEach(function (hp, idx) {
      const pin = document.createElement('button');
      pin.className = 'biofilm-pin-node';
      pin.setAttribute('type', 'button');
      pin.style.left = hp.x + '%';
      pin.style.top = hp.y + '%';
      pin.style.pointerEvents = 'auto';

      pin.innerHTML = `
        <span class="pin-ring"></span>
        <span class="pin-center">${idx + 1}</span>
        <div class="pin-hover-tooltip">
          <span class="tooltip-badge">${hp.badge}</span>
          <div class="tooltip-title">${hp.name}</div>
        </div>
      `;

      pin.addEventListener('click', function (e) {
        e.stopPropagation();
        self.selectHotspot(hp, pin);
      });

      self.hotspotsOverlay.appendChild(pin);
    });

    if (hotspots.length > 0) {
      const firstPin = this.hotspotsOverlay.querySelector('.biofilm-pin-node');
      this.selectHotspot(hotspots[0], firstPin);
    }
  };

  BiofilmCinematicSim.prototype.selectHotspot = function (hp, pinEl) {
    this.activeHotspot = hp;
    const allPins = this.hotspotsOverlay.querySelectorAll('.biofilm-pin-node');
    allPins.forEach(p => p.classList.remove('active'));
    if (pinEl) pinEl.classList.add('active');

    if (this.options.onHotspotSelect) {
      this.options.onHotspotSelect(hp);
    }
  };

  BiofilmCinematicSim.prototype.toggleHotspots = function () {
    this.showHotspots = !this.showHotspots;
    const currentData = SCENARIOS[SEQUENCE[this.currentScenarioIndex]];
    this.renderHotspots(currentData.hotspots);
    return this.showHotspots;
  };

  BiofilmCinematicSim.prototype.play = function () {
    if (this.isPlaying) return;
    this.isPlaying = true;
    const self = this;

    const stepInterval = Math.round(4200 / this.playbackRate);

    this.playTimer = setInterval(function () {
      let nextIndex = self.currentScenarioIndex + 1;
      if (nextIndex >= SEQUENCE.length) {
        nextIndex = 0;
      }
      self.loadScenario(nextIndex, true);
    }, stepInterval);
  };

  BiofilmCinematicSim.prototype.pause = function () {
    this.isPlaying = false;
    if (this.playTimer) {
      clearInterval(this.playTimer);
      this.playTimer = null;
    }
  };

  BiofilmCinematicSim.prototype.togglePlay = function () {
    if (this.isPlaying) this.pause();
    else this.play();
    return this.isPlaying;
  };

  BiofilmCinematicSim.prototype.setPlaybackRate = function (rate) {
    this.playbackRate = rate;
    if (this.isPlaying) {
      this.pause();
      this.play();
    }
  };

  BiofilmCinematicSim.prototype.next = function () {
    this.loadScenario((this.currentScenarioIndex + 1) % SEQUENCE.length, true);
  };

  BiofilmCinematicSim.prototype.prev = function () {
    let prev = this.currentScenarioIndex - 1;
    if (prev < 0) prev = SEQUENCE.length - 1;
    this.loadScenario(prev, true);
  };

  BiofilmCinematicSim.prototype.initCanvasEffects = function () {
    this.resizeCanvas();
    const self = this;

    const particles = [];
    const count = 35;
    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * 800,
        y: Math.random() * 450,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4,
        r: 1.2 + Math.random() * 2.0,
        alpha: 0.15 + Math.random() * 0.4,
        pulse: Math.random() * Math.PI * 2
      });
    }

    function renderLoop(time) {
      self.animFrameId = requestAnimationFrame(renderLoop);
      if (!self.ctx || !self.canvas) return;

      const w = self.container.clientWidth;
      const h = self.container.clientHeight;
      self.ctx.clearRect(0, 0, w, h);

      const currentKey = SEQUENCE[self.currentScenarioIndex];

      if (currentKey === 'endodoncia_irrigacion') {
        self.ctx.fillStyle = 'rgba(103, 232, 249, 0.65)';
        for (let i = 0; i < 24; i++) {
          const bx = w * 0.45 + Math.sin(time * 0.006 + i) * 65;
          const by = h * 0.48 + Math.cos(time * 0.005 + i * 2) * 55;
          const br = 1.5 + (i % 4);
          self.ctx.beginPath();
          self.ctx.arc(bx, by, br, 0, Math.PI * 2);
          self.ctx.fill();
        }
      } else {
        particles.forEach(function (p) {
          p.x += p.vx;
          p.y += p.vy;
          p.pulse += 0.02;

          if (p.x < 0) p.x = w;
          if (p.x > w) p.x = 0;
          if (p.y < 0) p.y = h;
          if (p.y > h) p.y = 0;

          const dynamicAlpha = p.alpha + Math.sin(p.pulse) * 0.12;
          self.ctx.fillStyle = `rgba(56, 189, 248, ${Math.max(0.04, dynamicAlpha)})`;
          self.ctx.beginPath();
          self.ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
          self.ctx.fill();
        });
      }
    }
    this.animFrameId = requestAnimationFrame(renderLoop);
  };

  BiofilmCinematicSim.prototype.destroy = function () {
    this.pause();
    if (this.animFrameId) cancelAnimationFrame(this.animFrameId);
  };

  global.BiofilmCinematicSim = BiofilmCinematicSim;
  global.BIOFILM_SCENARIOS = SCENARIOS;
  global.BIOFILM_SEQUENCE = SEQUENCE;

})(typeof window !== 'undefined' ? window : this);
