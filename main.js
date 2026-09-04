(function () {
  "use strict";

  /* ==========================================================================
     OdontoScore — Dynamic Hydration & Multi-Store Currency Engine v5.2
     Priority Video Multimedia Rendering, Multi-Store Comparison, Live FX Rates
     ========================================================================== */

  // ── Config ──
  var SUPABASE_URL = "https://lgaolwxeizxynkpcjsse.supabase.co";
  var ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxnYW9sd3hlaXp4eW5rcGNqc3NlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODY3NTI0NjcsImV4cCI6MjEwMjMyODQ2N30.M9AzjDz9P44Tt2JfDnmRr9zzNaDw-z-vjTV83CxOdwM";

  // ── Currency & Exchange Rates State ──
  var EXCHANGE_RATES = {
    EUR: 1.0,
    USD: 1.09,
    COP: 4350.0,
    MXN: 18.8,
    PEN: 4.05,
    ARS: 1050.0,
    CLP: 1020.0,
    GBP: 0.86
  };

  var ACTIVE_CURRENCY = "EUR";

  var CURRENCY_CONFIG = {
    EUR: { symbol: "€", name: "Euros (España / UE)", position: "after", decimals: 2, flag: "🇪🇸" },
    COP: { symbol: "$", name: "Pesos Colombianos (COP)", position: "before", decimals: 0, flag: "🇨🇴" },
    MXN: { symbol: "$", name: "Pesos Mexicanos (MXN)", position: "before", decimals: 2, flag: "🇲🇽" },
    USD: { symbol: "$", name: "Dólares USA (USD)", position: "before", decimals: 2, flag: "🇺🇸" },
    PEN: { symbol: "S/.", name: "Soles Peruanos (PEN)", position: "before", decimals: 2, flag: "🇵🇪" },
    ARS: { symbol: "$", name: "Pesos Argentinos (ARS)", position: "before", decimals: 0, flag: "🇦🇷" },
    CLP: { symbol: "$", name: "Pesos Chilenos (CLP)", position: "before", decimals: 0, flag: "🇨🇱" },
    GBP: { symbol: "£", name: "Libras Esterlinas (GBP)", position: "before", decimals: 2, flag: "🇬🇧" }
  };

  var RADAR_COLORS = [
    { fill: "rgba(12, 127, 212, 0.18)", stroke: "#0C7FD4", point: "#0C7FD4" },
    { fill: "rgba(10, 155, 106, 0.18)", stroke: "#0A9B6A", point: "#0A9B6A" },
    { fill: "rgba(232, 163, 23, 0.18)", stroke: "#E8A317", point: "#E8A317" },
    { fill: "rgba(109, 40, 217, 0.18)", stroke: "#6D28D9", point: "#6D28D9" }
  ];

  var SCORE_AXES = [
    { key: "score_eficacia", label: "Eficacia" },
    { key: "score_comodidad_encias", label: "Encías" },
    { key: "score_durabilidad", label: "Durabilidad" },
    { key: "score_facilidad_uso", label: "Ergonomía" },
    { key: "score_silencio", label: "Silencio" },
    { key: "score_tecnologia", label: "Tecnología" },
    { key: "score_calidad_precio", label: "Calidad/Precio" }
  ];

  var CATEGORY_LABELS = {
    estudiantes_practicas: "Estudiantes y Prácticas",
    cepillos_electricos: "Cepillos Eléctricos",
    irrigadores_dentales: "Irrigadores Dentales",
    blanqueamiento_dental: "Blanqueamiento Dental",
    ortodoncia_brackets: "Ortodoncia y Brackets",
    higiene_infantil: "Odontopediatría",
    instrumental_basico: "Instrumental y Clínica"
  };

  // ── Helpers ──
  function safe(fn, name) {
    try { fn(); } catch (err) { console.warn("[OdontoScore]", name, err); }
  }

  function esc(str) {
    var d = document.createElement("div");
    d.textContent = str || "";
    return d.innerHTML;
  }

  // ── Video & Media Resolution ──
  function getVideoData(p) {
    if (p.specs_extra && Array.isArray(p.specs_extra.videos) && p.specs_extra.videos.length > 0 && p.specs_extra.videos[0].url) {
      return p.specs_extra.videos[0];
    }
    if (Array.isArray(p.videos) && p.videos.length > 0 && p.videos[0].url) {
      return p.videos[0];
    }
    return null;
  }

  function hasVideo(p) {
    return Boolean(getVideoData(p));
  }

  function getProductImages(p) {
    var list = [];
    if (p.specs_extra && Array.isArray(p.specs_extra.images) && p.specs_extra.images.length > 0) {
      list = p.specs_extra.images;
    } else if (Array.isArray(p.local_assets) && p.local_assets.length > 0 && p.local_assets[0] !== "assets/img/hero-dental.svg") {
      list = p.local_assets;
    } else if (Array.isArray(p.images) && p.images.length > 0) {
      list = p.images;
    }
    if (!list.length && p.asin) {
      list = ["https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=" + p.asin + "&Format=_SL1500_&ID=AsinImage&MarketPlace=ES&ServiceVersion=20070822&WS=1&tag=odontoscore-21"];
    }
    return list;
  }

  // ── Currency Conversion & Formatting ──
  function formatPrice(eurVal, customCurr) {
    var curr = customCurr || ACTIVE_CURRENCY;
    var rate = EXCHANGE_RATES[curr] || 1.0;
    var cfg = CURRENCY_CONFIG[curr] || CURRENCY_CONFIG.EUR;
    var converted = Number(eurVal || 0) * rate;

    var formattedNumber = cfg.decimals === 0
      ? Math.round(converted).toLocaleString("es-ES")
      : converted.toLocaleString("es-ES", { minimumFractionDigits: cfg.decimals, maximumFractionDigits: cfg.decimals });

    if (cfg.position === "before") {
      return cfg.symbol + " " + formattedNumber + " " + curr;
    } else {
      return formattedNumber + " " + cfg.symbol;
    }
  }

  // ── Live Exchange Rates Fetcher ──
  async function fetchLiveExchangeRates() {
    try {
      var res = await fetch("https://open.er-api.com/v6/latest/EUR");
      if (res.ok) {
        var data = await res.json();
        if (data && data.rates) {
          Object.keys(EXCHANGE_RATES).forEach(function (k) {
            if (data.rates[k]) EXCHANGE_RATES[k] = data.rates[k];
          });
        }
      }
    } catch (e) {
      console.log("[OdontoScore] Using default exchange rates:", e);
    }
  }

  // ── Auto-GEO Detection ──
  function detectUserGeoCurrency() {
    var saved = localStorage.getItem("odonto_currency");
    if (saved && CURRENCY_CONFIG[saved]) {
      ACTIVE_CURRENCY = saved;
      return;
    }

    try {
      var tz = (Intl.DateTimeFormat().resolvedOptions().timeZone || "").toLowerCase();
      var lang = (navigator.language || "").toLowerCase();

      if (tz.indexOf("bogota") !== -1 || lang === "es-co") ACTIVE_CURRENCY = "COP";
      else if (tz.indexOf("mexico") !== -1 || lang === "es-mx") ACTIVE_CURRENCY = "MXN";
      else if (tz.indexOf("lima") !== -1 || lang === "es-pe") ACTIVE_CURRENCY = "PEN";
      else if (tz.indexOf("argentina") !== -1 || tz.indexOf("buenos_aires") !== -1 || lang === "es-ar") ACTIVE_CURRENCY = "ARS";
      else if (tz.indexOf("santiago") !== -1 || lang === "es-cl") ACTIVE_CURRENCY = "CLP";
      else if (tz.indexOf("america") !== -1 || lang.indexOf("en-us") !== -1) ACTIVE_CURRENCY = "USD";
      else if (tz.indexOf("london") !== -1 || lang.indexOf("en-gb") !== -1) ACTIVE_CURRENCY = "GBP";
      else ACTIVE_CURRENCY = "EUR";
    } catch (e) {
      ACTIVE_CURRENCY = "EUR";
    }
  }

  // ── Multi-Store Comparison Engine ──
  function getMultiStoreQuotes(p) {
    var baseEur = Number(p.discounted_price || p.discountedPrice || p.retail_price || p.retailPrice || 49.99);
    var cleanTitle = (p.name || "").replace(/[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ ]/g, " ").replace(/\s+/g, "+");
    var queryShort = (p.marca || "") + "+" + (p.name ? p.name.split(" ").slice(0, 3).join("+") : "");

    var mlSearch = "https://listado.mercadolibre.com.co/" + queryShort;
    var mlFactor = 1.05;

    if (ACTIVE_CURRENCY === "MXN") {
      mlSearch = "https://listado.mercadolibre.com.mx/" + queryShort;
      mlFactor = 1.02;
    } else if (ACTIVE_CURRENCY === "ARS") {
      mlSearch = "https://listado.mercadolibre.com.ar/" + queryShort;
      mlFactor = 1.15;
    } else if (ACTIVE_CURRENCY === "CLP") {
      mlSearch = "https://listado.mercadolibre.cl/" + queryShort;
      mlFactor = 1.08;
    } else if (ACTIVE_CURRENCY === "PEN") {
      mlSearch = "https://listado.mercadolibre.com.pe/" + queryShort;
      mlFactor = 1.04;
    }

    var stores = [
      {
        id: "amazon_es",
        name: "Amazon España",
        tag: "Envío Prime 24/48h • Distribuidor Oficial",
        iconClass: "amazon",
        iconText: "a",
        eurPrice: baseEur,
        url: p.affiliate_url || ("https://www.amazon.es/dp/" + p.asin + "?tag=odontoscore-21")
      },
      {
        id: "amazon_us",
        name: "Amazon USA (Global)",
        tag: "Importación Directa • Envío Internacional",
        iconClass: "amazon-us",
        iconText: "US",
        eurPrice: Math.round(baseEur * 0.94 * 100) / 100,
        url: "https://www.amazon.com/s?k=" + queryShort
      },
      {
        id: "mercadolibre",
        name: "Mercado Libre (" + (CURRENCY_CONFIG[ACTIVE_CURRENCY] ? CURRENCY_CONFIG[ACTIVE_CURRENCY].flag : "Latam") + ")",
        tag: "Vendedores Verificados • Entrega Local",
        iconClass: "mercadolibre",
        iconText: "ML",
        eurPrice: Math.round(baseEur * mlFactor * 100) / 100,
        url: mlSearch
      },
      {
        id: "aliexpress",
        name: "AliExpress Oficial",
        tag: "Envío Directo Fábrica",
        iconClass: "aliexpress",
        iconText: "Ali",
        eurPrice: Math.round(baseEur * 0.84 * 100) / 100,
        url: "https://es.aliexpress.com/wholesale?SearchText=" + queryShort
      },
      {
        id: "deposito_dental",
        name: "Depósito Dental Especializado",
        tag: "Garantía Clínica Profesional",
        iconClass: "dental",
        iconText: "Dent",
        eurPrice: Math.round(baseEur * 1.12 * 100) / 100,
        url: "https://www.google.com/search?q=deposito+dental+" + queryShort
      }
    ];

    var lowest = stores[0];
    stores.forEach(function (st) {
      if (st.eurPrice < lowest.eurPrice) lowest = st;
    });
    lowest.isBest = true;

    return stores;
  }

  function renderMultiStoreHtml(p) {
    var quotes = getMultiStoreQuotes(p);
    var html = '' +
      '<div class="modal-multistore-box">' +
        '<h4>' +
          '<span>Comparativa de Precios Multi-Tienda</span>' +
          '<span class="store-rate-info">Moneda: ' + ACTIVE_CURRENCY + ' (' + (CURRENCY_CONFIG[ACTIVE_CURRENCY] ? CURRENCY_CONFIG[ACTIVE_CURRENCY].flag : "") + ')</span>' +
        '</h4>' +
        '<table class="multistore-table">' +
          '<tbody>';

    quotes.forEach(function (st) {
      var isBest = st.isBest;
      var convertedStr = formatPrice(st.eurPrice);

      html += '' +
        '<tr class="' + (isBest ? 'best-store-deal' : '') + '">' +
          '<td>' +
            '<div class="store-name-cell">' +
              '<span class="store-icon ' + st.iconClass + '">' + st.iconText + '</span>' +
              '<div>' +
                '<span>' + esc(st.name) + '</span>' +
                (isBest ? '<span class="store-badge-best">Mejor Precio</span>' : '') +
                '<br><small style="font-weight:normal;color:#5E738A;font-size:0.75rem;">' + esc(st.tag) + '</small>' +
              '</div>' +
            '</div>' +
          '</td>' +
          '<td class="store-price-cell">' +
            '<span class="store-converted-price">' + convertedStr + '</span>' +
            '<span class="store-orig-price">(' + st.eurPrice.toFixed(2).replace(".", ",") + ' € base)</span>' +
          '</td>' +
          '<td style="text-align:right;">' +
            '<a href="' + esc(st.url) + '" target="_blank" rel="nofollow noopener sponsored" class="btn-store-go ' + (isBest ? 'best-btn' : '') + '">' +
              (isBest ? 'Comprar Mejor Oferta' : 'Ver en Tienda') +
            '</a>' +
          '</td>' +
        '</tr>';
    });

    html += '' +
          '</tbody>' +
        '</table>' +
      '</div>';

    return html;
  }

  // ── Radar Chart SVG ──
  function drawRadarSVG(container, products) {
    if (!container || !products || !products.length) return;
    var size = 300, center = size / 2, radius = size * 0.36;
    var totalAxes = SCORE_AXES.length, angleStep = (Math.PI * 2) / totalAxes;

    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("viewBox", "0 0 " + size + " " + size);
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", "100%");
    svg.style.maxWidth = size + "px";

    for (var level = 2; level <= 10; level += 2) {
      var r = (level / 10) * radius, pts = [];
      for (var i = 0; i < totalAxes; i++) {
        var a = i * angleStep - Math.PI / 2;
        pts.push((center + r * Math.cos(a)).toFixed(1) + "," + (center + r * Math.sin(a)).toFixed(1));
      }
      var poly = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
      poly.setAttribute("points", pts.join(" "));
      poly.setAttribute("fill", level === 10 ? "#F8FAFC" : "none");
      poly.setAttribute("stroke", "#E2E8F0");
      poly.setAttribute("stroke-width", "1");
      svg.appendChild(poly);
    }

    for (var ax = 0; ax < totalAxes; ax++) {
      var axAngle = ax * angleStep - Math.PI / 2;
      var line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("x1", center); line.setAttribute("y1", center);
      line.setAttribute("x2", (center + radius * Math.cos(axAngle)).toFixed(1));
      line.setAttribute("y2", (center + radius * Math.sin(axAngle)).toFixed(1));
      line.setAttribute("stroke", "#CBD5E1"); line.setAttribute("stroke-width", "1");
      svg.appendChild(line);

      var lR = radius + 22;
      var text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.setAttribute("x", (center + lR * Math.cos(axAngle)).toFixed(1));
      text.setAttribute("y", (center + lR * Math.sin(axAngle) + 4).toFixed(1));
      text.setAttribute("text-anchor", "middle");
      text.setAttribute("font-family", "Inter, sans-serif");
      text.setAttribute("font-size", "10");
      text.setAttribute("font-weight", "600");
      text.setAttribute("fill", "#5E738A");
      text.textContent = SCORE_AXES[ax].label;
      svg.appendChild(text);
    }

    products.forEach(function (prod, pIdx) {
      var c = RADAR_COLORS[pIdx % RADAR_COLORS.length], dataPts = [];
      SCORE_AXES.forEach(function (axis, aIdx) {
        var val = Math.min(10, Math.max(0, Number(prod[axis.key]) || 0));
        var rVal = (val / 10) * radius, angle = aIdx * angleStep - Math.PI / 2;
        dataPts.push((center + rVal * Math.cos(angle)).toFixed(1) + "," + (center + rVal * Math.sin(angle)).toFixed(1));
      });
      var dp = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
      dp.setAttribute("points", dataPts.join(" "));
      dp.setAttribute("fill", c.fill); dp.setAttribute("stroke", c.stroke); dp.setAttribute("stroke-width", "2");
      svg.appendChild(dp);

      dataPts.forEach(function (pt) {
        var xy = pt.split(",");
        var dot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        dot.setAttribute("cx", xy[0]); dot.setAttribute("cy", xy[1]); dot.setAttribute("r", "3.5");
        dot.setAttribute("fill", c.point); dot.setAttribute("stroke", "#FFF"); dot.setAttribute("stroke-width", "1.5");
        svg.appendChild(dot);
      });
    });

    container.innerHTML = "";
    container.appendChild(svg);
  }

  // ── Card Renderer with Prioritized Video Multimedia ──
  function renderCard(p) {
    var retail = Number(p.retail_price || p.retailPrice || 0);
    var current = Number(p.discounted_price || p.discountedPrice || retail);
    var discountPct = (current < retail && retail > 0) ? Math.round((1 - current / retail) * 100) : 0;

    var images = getProductImages(p);
    var mainImg = images[0] || "";
    var techStr = (p.tecnologia || "sonico").replace(/_/g, " ").toUpperCase();
    var potStr = p.presion_agua_psi
      ? p.presion_agua_psi + " PSI"
      : (p.pulsaciones_min ? Number(p.pulsaciones_min).toLocaleString("es-ES") + " mov/min"
        : (p.esterilizable_autoclave ? "Autoclave 134°C" : "Clínico"));
    var autoStr = (p.autonomia_dias && Number(p.autonomia_dias) < 365) ? p.autonomia_dias + " días" : "Red / AC";
    var catLabel = CATEGORY_LABELS[p.categoria_odontologica] || p.category || "Odontología";
    var mediaCount = images.length;
    var videoObj = getVideoData(p);
    var videoAvail = Boolean(videoObj);

    // Build thumbnails strip (with Video Play Button FIRST if video exists)
    var thumbsHtml = '<div class="card-thumbs-strip">';
    if (videoAvail) {
      thumbsHtml += '<button type="button" class="card-thumb-mini card-thumb-video" data-quick-view="' + esc(p.id) + '" title="Ver Vídeo Demostrativo" aria-label="Ver Vídeo"><img src="' + esc(videoObj.thumbnail || mainImg) + '" alt="Vídeo"></button>';
    }

    images.slice(0, videoAvail ? 5 : 6).forEach(function (src, idx) {
      thumbsHtml += '<button type="button" class="card-thumb-mini' + (idx === 0 && !videoAvail ? ' active' : '') + '" data-card-thumb="' + esc(src) + '" aria-label="Foto ' + (idx + 1) + '"><img src="' + esc(src) + '" alt="Miniatura"></button>';
    });

    if (images.length > 6) {
      thumbsHtml += '<span class="card-thumb-more" style="font-size:0.75rem;font-weight:700;color:#5E738A;padding:0 4px;">+' + (images.length - 6) + '</span>';
    }
    thumbsHtml += '</div>';

    var mediaPill = '';
    if (videoAvail && mediaCount > 1) mediaPill = 'Vídeo + ' + mediaCount + ' fotos';
    else if (videoAvail) mediaPill = 'Vídeo Demostrativo';
    else if (mediaCount > 1) mediaPill = mediaCount + ' fotos';

    var convertedPrice = formatPrice(current);
    var convertedRetail = retail > 0 ? formatPrice(retail) : "";

    return '' +
      '<article class="product-card" data-producto-id="' + esc(p.id) + '" data-asin="' + esc(p.asin) + '" data-has-video="' + (videoAvail ? 'true' : 'false') + '" data-category="' + esc(p.categoria_odontologica || '') + '" data-brand="' + esc((p.marca || '').toLowerCase()) + '" data-title="' + esc((p.name || '').toLowerCase()) + '" data-price="' + current + '" data-score="' + (p.score_eficacia || 9) + '">' +
        (p.is_featured || p.isFeatured ? '<span class="card-badge-top">Top Clínico</span>' : '') +
        (discountPct > 0 ? '<span class="price-discount-pill">-' + discountPct + '%</span>' : '') +
        '<div class="card-media-wrapper">' +
          '<div class="card-media">' +
            '<img class="card-main-photo" src="' + esc(mainImg) + '" alt="' + esc(p.name || '') + '" loading="lazy" onerror="this.onerror=null;this.src=\'https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=' + esc(p.asin) + '&Format=_SL1500_&ID=AsinImage&MarketPlace=ES&ServiceVersion=20070822&WS=1&tag=odontoscore-21\';">' +
            (mediaPill ? '<button type="button" class="card-video-pill" data-quick-view="' + esc(p.id) + '" title="Ver Vídeo y Fotos">' + mediaPill + '</button>' : '') +
          '</div>' +
          thumbsHtml +
        '</div>' +
        '<div class="card-body">' +
          '<div class="card-header-meta">' +
            '<span class="card-brand-tag">' + esc(p.marca || 'Dental') + '</span>' +
            '<span class="card-category-tag">' + esc(catLabel) + '</span>' +
          '</div>' +
          '<h3 class="card-title" title="' + esc(p.name || '') + '">' + esc(p.name || '') + '</h3>' +
          '<div class="card-rating-box">' +
            '<span class="rating-badge">' + (p.valoracion_media || '4.5') + ' ★</span>' +
            '<span class="card-rating-count">(' + Number(p.resenas_cantidad || 0).toLocaleString("es-ES") + ' opiniones)</span>' +
          '</div>' +
          '<div class="card-specs-matrix">' +
            '<div class="spec-cell">Tecnología: <strong>' + techStr + '</strong></div>' +
            '<div class="spec-cell">Modos: <strong>' + (p.modos_limpieza || 1) + '</strong></div>' +
            '<div class="spec-cell">Potencia: <strong>' + potStr + '</strong></div>' +
            '<div class="spec-cell">Autonomía: <strong>' + autoStr + '</strong></div>' +
          '</div>' +
          '<div class="card-price-row">' +
            '<div>' +
              '<span class="price-main-val">' + convertedPrice + '</span>' +
              (discountPct > 0 ? '<span class="price-strike-val">' + convertedRetail + '</span>' : '') +
            '</div>' +
            '<span class="price-shipping">Envío Prime</span>' +
          '</div>' +
          '<div class="card-actions-grid">' +
            '<button type="button" class="btn-card-quick" data-quick-view="' + esc(p.id) + '">' + (videoAvail ? '🎬 Vídeo & Tiendas' : 'Comparar Tiendas') + '</button>' +
            '<a href="' + esc(p.affiliate_url || ('https://www.amazon.es/dp/' + p.asin + '?tag=odontoscore-21')) + '" target="_blank" rel="sponsored nofollow noopener" class="btn-card-prime">Ver en Amazon</a>' +
          '</div>' +
        '</div>' +
      '</article>';
  }

  // ── Dynamic Hydration with Video Priority ──
  async function hydrate() {
    try {
      var res = await fetch(SUPABASE_URL + "/rest/v1/products?select=*&order=is_featured.desc,discounted_price.desc", {
        headers: {
          "apikey": ANON_KEY,
          "Authorization": "Bearer " + ANON_KEY,
          "Accept": "application/json"
        }
      });

      if (!res.ok) throw new Error("HTTP " + res.status);
      var products = await res.json();
      if (!products || !products.length) return;

      // ── Priority Sorting: Products with Video FIRST ──
      products.sort(function (a, b) {
        var vA = hasVideo(a) ? 1 : 0;
        var vB = hasVideo(b) ? 1 : 0;
        if (vB !== vA) return vB - vA; // Videos first
        var fA = (a.is_featured || a.isFeatured) ? 1 : 0;
        var fB = (b.is_featured || b.isFeatured) ? 1 : 0;
        if (fB !== fA) return fB - fA;
        return Number(b.discounted_price || 0) - Number(a.discounted_price || 0);
      });

      window.__DYNAMIC_PRODUCTS__ = products;
      window.__DB__ = { productos: products };

      renderAllGrids();
      buildFilterPills(products);

      safe(function () { initCatalogFilter(); }, "initCatalogFilter");
      safe(function () { initComparator(); }, "initComparator");
      safe(function () { initRadars(); }, "initRadars");

    } catch (err) {
      console.warn("[OdontoScore] Hydration error:", err);
    }
  }

  function renderAllGrids() {
    var products = window.__DYNAMIC_PRODUCTS__ || [];
    if (!products.length) return;

    // 1. Main Catalog Grid
    var mainGrid = document.getElementById("mainProductGrid");
    if (mainGrid) {
      mainGrid.innerHTML = products.map(renderCard).join("");
    }

    // 2. Student Grid (filtered)
    var studentGrid = document.getElementById("studentGrid");
    if (studentGrid) {
      var studentProducts = products.filter(function (p) {
        return p.categoria_odontologica === "estudiantes_practicas";
      });
      studentGrid.innerHTML = studentProducts.length > 0
        ? studentProducts.map(renderCard).join("")
        : '<p style="text-align:center;color:#5E738A;padding:2rem;">Cargando productos para estudiantes...</p>';
    }

    // 3. Deals Grid (filtered by discount)
    var dealsGrid = document.getElementById("dealsGrid");
    if (dealsGrid) {
      var deals = products.filter(function (p) {
        var retail = Number(p.retail_price || p.retailPrice || 0);
        var current = Number(p.discounted_price || p.discountedPrice || retail);
        return retail > 0 && current < retail * 0.95;
      }).sort(function (a, b) {
        var vA = hasVideo(a) ? 1 : 0;
        var vB = hasVideo(b) ? 1 : 0;
        if (vB !== vA) return vB - vA;
        var discA = 1 - (Number(a.discounted_price || a.retailPrice || 0) / Number(a.retail_price || 1));
        var discB = 1 - (Number(b.discounted_price || b.retailPrice || 0) / Number(b.retail_price || 1));
        return discB - discA;
      });
      dealsGrid.innerHTML = deals.length > 0
        ? deals.map(renderCard).join("")
        : '<p style="text-align:center;color:#5E738A;padding:2rem;">No hay ofertas activas en este momento.</p>';
    }
  }

  // ── Filter Pills with Video Category ──
  function buildFilterPills(products) {
    var bar = document.getElementById("filterPillsBar");
    if (!bar) return;

    var counts = {};
    var videoCount = 0;
    products.forEach(function (p) {
      var cat = p.categoria_odontologica || "other";
      counts[cat] = (counts[cat] || 0) + 1;
      if (hasVideo(p)) videoCount++;
    });

    var html = '<button type="button" class="filter-pill-btn active" data-filter="all">Todos (' + products.length + ')</button>';
    if (videoCount > 0) {
      html += '<button type="button" class="filter-pill-btn" data-filter="video" style="background:#0F172A;color:#38BDF8;border-color:#0C7FD4;">🎬 Con Vídeo (' + videoCount + ')</button>';
    }
    Object.keys(CATEGORY_LABELS).forEach(function (key) {
      if (counts[key]) {
        html += '<button type="button" class="filter-pill-btn" data-filter="' + key + '">' + CATEGORY_LABELS[key] + ' (' + counts[key] + ')</button>';
      }
    });
    bar.innerHTML = html;
  }

  // ── Catalog Filter & Sort ──
  function initCatalogFilter() {
    var filterContainer = document.getElementById("filterPillsBar");
    var searchInput = document.getElementById("catalogSearchInput");
    var sortSelect = document.getElementById("catalogSortSelect");
    var gridEl = document.getElementById("mainProductGrid");
    var btnGrid = document.getElementById("btnViewGrid");
    var btnList = document.getElementById("btnViewList");
    if (!gridEl) return;

    var cards = Array.from(gridEl.querySelectorAll(".product-card"));
    var activeCategory = "all";
    var currentQuery = "";

    function applyFiltersAndSort() {
      var q = currentQuery.toLowerCase().trim();
      var sortMode = sortSelect ? sortSelect.value : "has-video";
      cards = Array.from(gridEl.querySelectorAll(".product-card"));

      var visible = cards.filter(function (card) {
        var cat = card.getAttribute("data-category") || "";
        var brand = card.getAttribute("data-brand") || "";
        var title = card.getAttribute("data-title") || "";
        var cardHasVideo = card.getAttribute("data-has-video") === "true";

        var matchCat = false;
        if (activeCategory === "all") matchCat = true;
        else if (activeCategory === "video") matchCat = cardHasVideo;
        else matchCat = (cat === activeCategory);

        var matchSearch = !q || brand.indexOf(q) !== -1 || title.indexOf(q) !== -1;
        card.style.display = (matchCat && matchSearch) ? "flex" : "none";
        return matchCat && matchSearch;
      });

      visible.sort(function (a, b) {
        var vA = a.getAttribute("data-has-video") === "true" ? 1 : 0;
        var vB = b.getAttribute("data-has-video") === "true" ? 1 : 0;
        var pA = parseFloat(a.getAttribute("data-price")) || 0;
        var pB = parseFloat(b.getAttribute("data-price")) || 0;
        var sA = parseFloat(a.getAttribute("data-score")) || 0;
        var sB = parseFloat(b.getAttribute("data-score")) || 0;

        if (sortMode === "has-video") {
          if (vB !== vA) return vB - vA;
          return sB - sA;
        }
        if (sortMode === "price-asc") return pA - pB;
        if (sortMode === "price-desc") return pB - pA;
        if (sortMode === "score") return sB - sA;
        if (sortMode === "featured") {
          if (vB !== vA) return vB - vA;
          return sB - sA;
        }
        return 0;
      });

      visible.forEach(function (card) { gridEl.appendChild(card); });
    }

    if (filterContainer) {
      filterContainer.addEventListener("click", function (e) {
        var btn = e.target.closest(".filter-pill-btn");
        if (!btn) return;
        activeCategory = btn.getAttribute("data-filter") || "all";
        filterContainer.querySelectorAll(".filter-pill-btn").forEach(function (b) { b.classList.remove("active"); });
        btn.classList.add("active");
        applyFiltersAndSort();
      });
    }

    if (searchInput) {
      searchInput.addEventListener("input", function () {
        currentQuery = searchInput.value;
        applyFiltersAndSort();
      });
    }

    if (sortSelect) sortSelect.addEventListener("change", applyFiltersAndSort);

    if (btnGrid && btnList) {
      btnGrid.addEventListener("click", function () {
        gridEl.classList.remove("view-list");
        btnGrid.classList.add("active");
        btnList.classList.remove("active");
      });
      btnList.addEventListener("click", function () {
        gridEl.classList.add("view-list");
        btnList.classList.add("active");
        btnGrid.classList.remove("active");
      });
    }
  }

  // ── Quick View Modal with Video Player Priority & Multi-Store Comparison ──
  function initQuickModal() {
    var backdrop = document.getElementById("quickViewModal");
    if (!backdrop) return;

    var closeBtn = backdrop.querySelector(".quick-modal-close-btn");
    var titleEl = document.getElementById("modalTitle");
    var brandEl = document.getElementById("modalBrand");
    var priceEl = document.getElementById("modalPrice");
    var imgEl = document.getElementById("modalImg");
    var thumbsRow = document.getElementById("modalThumbsRow");
    var radarCanvas = document.getElementById("modalRadarCanvas");
    var specsTable = backdrop.querySelector("#modalSpecsTable tbody");
    var buyBtn = document.getElementById("modalBuyBtn");
    var fullLink = document.getElementById("modalFullLink");
    var videoWrap = document.getElementById("modalVideoWrapper");

    function closeModal() {
      backdrop.classList.remove("open");
      document.body.style.overflow = "auto";
      if (videoWrap) {
        videoWrap.innerHTML = "";
        videoWrap.style.display = "none";
      }
    }

    if (closeBtn) closeBtn.addEventListener("click", closeModal);
    backdrop.addEventListener("click", function (e) { if (e.target === backdrop) closeModal(); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && backdrop.classList.contains("open")) closeModal();
    });

    document.addEventListener("click", function (e) {
      var trigger = e.target.closest("[data-quick-view]");
      if (!trigger) return;
      var prodId = trigger.getAttribute("data-quick-view");
      var db = window.__DYNAMIC_PRODUCTS__ || [];
      var p = db.find(function (item) { return item.id === prodId; });
      if (!p) return;
      e.preventDefault();

      var price = Number(p.discounted_price || p.discountedPrice || p.retail_price || p.retailPrice || 0);
      var images = getProductImages(p);
      var videoObj = getVideoData(p);

      if (titleEl) titleEl.textContent = p.name;
      if (brandEl) brandEl.textContent = p.marca;
      if (priceEl) priceEl.textContent = formatPrice(price);
      if (imgEl) {
        imgEl.src = images[0] || "";
        imgEl.onerror = function () {
          this.src = "https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=" + p.asin + "&Format=_SL1500_&ID=AsinImage&MarketPlace=ES&ServiceVersion=20070822&WS=1&tag=odontoscore-21";
        };
      }

      // ── Priority Video Player in Modal ──
      if (videoWrap) {
        if (videoObj && videoObj.url) {
          var isYouTube = videoObj.url.indexOf("youtube") !== -1 || videoObj.url.indexOf("youtu.be") !== -1;
          var videoPlayerHtml = '';

          if (isYouTube) {
            var embedUrl = videoObj.url;
            if (embedUrl.indexOf("watch?v=") !== -1) {
              embedUrl = embedUrl.replace("watch?v=", "embed/");
            }
            if (embedUrl.indexOf("?") === -1) {
              embedUrl += "?autoplay=1&rel=0&modestbranding=1";
            } else {
              embedUrl += "&autoplay=1&rel=0&modestbranding=1";
            }
            videoPlayerHtml = '<iframe class="modal-video-element" style="width:100%; height:280px; border-radius:12px; border:none; display:block;" src="' + esc(embedUrl) + '" title="' + esc(videoObj.title || 'Vídeo') + '" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>';
          } else {
            videoPlayerHtml = '<video controls autoplay playsinline class="modal-video-element" src="' + esc(videoObj.url) + '" poster="' + esc(videoObj.thumbnail || images[0]) + '">' +
              'Tu navegador no soporta reproducción de vídeo HTML5.' +
            '</video>';
          }

          videoWrap.style.display = "block";
          videoWrap.innerHTML = '' +
            '<div class="modal-video-header">' +
              '<span class="modal-video-badge">Vídeo Oficial Demostrativo</span>' +
              '<span style="color:#94A3B8;font-size:0.75rem;">' + esc(videoObj.title || 'Demostración Clínica') + '</span>' +
            '</div>' +
            videoPlayerHtml;
        } else {
          videoWrap.style.display = "none";
          videoWrap.innerHTML = "";
        }
      }

      // ── Thumbnails in Modal ──
      if (thumbsRow) {
        thumbsRow.innerHTML = "";

        if (videoObj) {
          var vBtn = document.createElement("button");
          vBtn.type = "button";
          vBtn.className = "modal-thumb-btn card-thumb-video active";
          vBtn.title = "Reproducir Vídeo Oficial";
          vBtn.innerHTML = '<img src="' + esc(videoObj.thumbnail || images[0]) + '" alt="Vídeo">';
          vBtn.addEventListener("click", function () {
            if (videoWrap) {
              videoWrap.style.display = "block";
              videoWrap.scrollIntoView({ behavior: "smooth", block: "nearest" });
            }
            thumbsRow.querySelectorAll(".modal-thumb-btn").forEach(function (b) { b.classList.remove("active"); });
            vBtn.classList.add("active");
          });
          thumbsRow.appendChild(vBtn);
        }

        images.slice(0, 10).forEach(function (src, idx) {
          var btn = document.createElement("button");
          btn.type = "button";
          btn.className = "modal-thumb-btn" + (idx === 0 && !videoObj ? " active" : "");
          btn.innerHTML = '<img src="' + src + '" alt="Miniatura ' + (idx + 1) + '">';
          btn.addEventListener("click", function () {
            if (imgEl) imgEl.src = src;
            thumbsRow.querySelectorAll(".modal-thumb-btn").forEach(function (b) { b.classList.remove("active"); });
            btn.classList.add("active");
          });
          thumbsRow.appendChild(btn);
        });
      }

      if (buyBtn) buyBtn.href = p.affiliate_url || ("https://www.amazon.es/dp/" + p.asin + "?tag=odontoscore-21");
      if (fullLink) fullLink.href = "producto/" + p.id + ".html";

      if (radarCanvas) drawRadarSVG(radarCanvas, [p]);

      if (specsTable) {
        var catLabel = CATEGORY_LABELS[p.categoria_odontologica] || p.category || "Odontología";
        specsTable.innerHTML =
          "<tr><th>Especialidad</th><td>" + esc(catLabel) + "</td></tr>" +
          "<tr><th>Multimedia</th><td>" + (videoObj ? "<strong style='color:#059669'>✓ Vídeo Oficial + " + images.length + " fotos</strong>" : images.length + " fotos de alta resolución") + "</td></tr>" +
          "<tr><th>Tecnología</th><td>" + esc((p.tecnologia || "").toUpperCase()) + "</td></tr>" +
          "<tr><th>Modos</th><td>" + (p.modos_limpieza || "1") + "</td></tr>" +
          "<tr><th>Potencia</th><td>" + (p.presion_agua_psi ? p.presion_agua_psi + " PSI" : (p.pulsaciones_min ? Number(p.pulsaciones_min).toLocaleString() + " mov/min" : "—")) + "</td></tr>" +
          "<tr><th>Autonomía</th><td>" + (p.autonomia_dias && Number(p.autonomia_dias) > 365 ? "Red / AC" : (p.autonomia_dias || 14) + " días") + "</td></tr>" +
          "<tr><th>Nivel Sonoro</th><td>" + (p.nivel_ruido_db ? p.nivel_ruido_db + " dB" : "Silencioso") + "</td></tr>" +
          "<tr><th>Puntuación</th><td><strong style='color:#0C7FD4'>" + (p.valoracion_media || "4.5") + " / 5 ★</strong> (" + Number(p.resenas_cantidad || 0).toLocaleString() + " opiniones)</td></tr>";
      }

      // Render Multi-Store Comparison Box inside Modal
      var existingStoreBox = backdrop.querySelector(".modal-multistore-box");
      if (existingStoreBox) existingStoreBox.remove();

      var rightCol = backdrop.querySelector(".quick-modal-grid > div:last-child");
      if (rightCol) {
        var storeHtml = renderMultiStoreHtml(p);
        var div = document.createElement("div");
        div.innerHTML = storeHtml;
        rightCol.appendChild(div.firstElementChild);
      }

      backdrop.classList.add("open");
      document.body.style.overflow = "hidden";
    });
  }

  // ── Comparator ──
  function initComparator() {
    var compRoot = document.querySelector("[data-comparator-app]");
    if (!compRoot) return;

    var db = window.__DYNAMIC_PRODUCTS__ || [];
    var catSelect = document.getElementById("compCategorySelect");
    var checksContainer = document.getElementById("compProductChecks");
    var matrixContainer = document.getElementById("compMatrixContent");
    var radarContainer = document.getElementById("compRadarCanvas");
    var radarLegend = document.getElementById("compRadarLegend");

    function renderProducts(catKey) {
      var items = db.filter(function (p) { return !catKey || p.categoria_odontologica === catKey; });
      if (!checksContainer) return;
      checksContainer.innerHTML = "";

      items.slice(0, 10).forEach(function (prod, idx) {
        var label = document.createElement("label");
        label.className = "comp-check-item";
        label.style.cssText = "display:inline-flex;align-items:center;gap:0.4rem;margin-right:0.85rem;margin-bottom:0.5rem;font-size:0.82rem;font-weight:600;cursor:pointer;";

        var input = document.createElement("input");
        input.type = "checkbox";
        input.value = prod.id;
        input.checked = idx < 3;
        input.addEventListener("change", updateComparison);

        label.appendChild(input);
        label.appendChild(document.createTextNode((hasVideo(prod) ? "🎬 " : "") + (prod.name && prod.name.length > 28 ? prod.name.substring(0, 28) + "…" : (prod.name || ""))));
        checksContainer.appendChild(label);
      });

      updateComparison();
    }

    function updateComparison() {
      var ids = [];
      checksContainer.querySelectorAll("input:checked").forEach(function (inp) { ids.push(inp.value); });
      var selected = db.filter(function (p) { return ids.indexOf(p.id) !== -1; });

      if (radarContainer) drawRadarSVG(radarContainer, selected);

      if (radarLegend) {
        radarLegend.innerHTML = "";
        selected.forEach(function (prod, idx) {
          var color = RADAR_COLORS[idx % RADAR_COLORS.length].stroke;
          var item = document.createElement("span");
          item.style.cssText = "display:inline-flex;align-items:center;gap:0.4rem;margin-right:0.85rem;font-size:0.82rem;font-weight:700;";
          var dot = document.createElement("span");
          dot.style.cssText = "width:8px;height:8px;border-radius:50%;background:" + color + ";flex-shrink:0;";
          item.appendChild(dot);
          item.appendChild(document.createTextNode((hasVideo(prod) ? "🎬 " : "") + (prod.name && prod.name.length > 20 ? prod.name.substring(0, 20) + "…" : (prod.name || ""))));
          radarLegend.appendChild(item);
        });
      }

      if (matrixContainer && selected.length > 0) {
        var html = '<table class="specs-table" style="background:#FFF;border-radius:12px;padding:1rem;"><thead><tr><th style="padding:0.75rem;">Característica</th>';
        selected.forEach(function (p) {
          var imgs = getProductImages(p);
          html += '<th style="padding:0.75rem;text-align:center;"><img src="' + (imgs[0] || '') + '" style="height:60px;margin:0 auto 4px;display:block;object-fit:contain;" alt=""><strong>' + esc(p.marca || '') + '</strong><br><small style="font-weight:normal;color:#5E738A;">' + esc(p.name && p.name.length > 20 ? p.name.substring(0, 20) + "…" : (p.name || '')) + '</small></th>';
        });
        html += '</tr></thead><tbody>';

        var rows = [
          { l: "Precio (" + ACTIVE_CURRENCY + ")", fn: function (p) { return '<strong style="color:#0C7FD4">' + formatPrice(p.discounted_price || 0) + '</strong>'; } },
          { l: "Vídeo Multimedia", fn: function (p) { return hasVideo(p) ? '<span style="color:#059669;font-weight:800;">✓ Vídeo Oficial</span>' : '<span style="color:#94A3B8;">Galería de fotos</span>'; } },
          { l: "Especialidad", fn: function (p) { return CATEGORY_LABELS[p.categoria_odontologica] || "Odontología"; } },
          { l: "Tecnología", fn: function (p) { return (p.tecnologia || "").toUpperCase(); } },
          { l: "Modos", fn: function (p) { return p.modos_limpieza || "1"; } },
          { l: "Potencia", fn: function (p) { return p.presion_agua_psi ? p.presion_agua_psi + " PSI" : (p.pulsaciones_min ? Number(p.pulsaciones_min).toLocaleString() + " mov/min" : "—"); } },
          { l: "Autonomía", fn: function (p) { return p.autonomia_dias && Number(p.autonomia_dias) > 365 ? "Red continua" : (p.autonomia_dias || 14) + " días"; } },
          { l: "Puntuación", fn: function (p) { return '<strong style="color:#0C7FD4">' + (p.valoracion_media || 4.5) + " / 5 ★</strong>"; } },
          { l: "Tiendas y Vídeo", fn: function (p) { return '<button type="button" class="btn-card-quick" style="padding:0.35rem 0.65rem;font-size:0.75rem;" data-quick-view="' + esc(p.id) + '">' + (hasVideo(p) ? '🎬 Ver Vídeo & Tiendas' : 'Comparar Tiendas') + '</button>'; } }
        ];
        rows.forEach(function (r) {
          html += '<tr><th style="padding:0.65rem 0.75rem;">' + r.l + '</th>';
          selected.forEach(function (p) { html += '<td style="padding:0.65rem 0.75rem;text-align:center;">' + r.fn(p) + '</td>'; });
          html += '</tr>';
        });
        html += '</tbody></table>';
        matrixContainer.innerHTML = html;
      }
    }

    if (catSelect) {
      catSelect.addEventListener("change", function () { renderProducts(catSelect.value); });
      renderProducts(catSelect.value);
    }
  }

  // ── Radars ──
  function initRadars() {
    var figures = document.querySelectorAll("[data-radar]");
    if (!figures.length) return;
    var db = window.__DYNAMIC_PRODUCTS__ || [];
    figures.forEach(function (fig) {
      var prodId = fig.getAttribute("data-radar-id");
      if (!prodId) {
        var parent = fig.closest("[data-producto-id]");
        if (parent) prodId = parent.getAttribute("data-producto-id");
      }
      if (prodId) {
        var item = db.find(function (p) { return p.id === prodId; });
        if (item) drawRadarSVG(fig, [item]);
      }
    });
  }

  // ── Card Gallery Interaction ──
  function initCardGalleries() {
    function swapImage(thumbBtn) {
      var src = thumbBtn.getAttribute("data-card-thumb");
      if (!src) return;
      var card = thumbBtn.closest(".product-card");
      if (card) {
        var main = card.querySelector(".card-main-photo");
        if (main) main.src = src;
        card.querySelectorAll(".card-thumb-mini").forEach(function (b) { b.classList.remove("active"); });
        thumbBtn.classList.add("active");
      }
    }

    document.addEventListener("click", function (e) {
      var t = e.target.closest("[data-card-thumb]");
      if (t) { e.preventDefault(); swapImage(t); }
    });
    document.addEventListener("mouseover", function (e) {
      var t = e.target.closest("[data-card-thumb]");
      if (t) swapImage(t);
    });
  }

  // ── Mobile Menu ──
  function initMobileMenu() {
    var btn = document.getElementById("mobileMenuBtn");
    var nav = document.getElementById("mainNav");
    var header = document.getElementById("siteHeader");
    if (!btn || !nav) return;

    btn.addEventListener("click", function () {
      btn.classList.toggle("open");
      nav.classList.toggle("open");
      if (header) header.classList.toggle("menu-open");
      document.body.style.overflow = nav.classList.contains("open") ? "hidden" : "";
    });

    var dropdownItems = nav.querySelectorAll(".nav-item-dropdown");
    dropdownItems.forEach(function (item) {
      var trigger = item.querySelector(".nav-link-dropdown");
      if (trigger) {
        trigger.addEventListener("click", function (e) {
          if (window.innerWidth <= 768) {
            e.preventDefault();
            item.classList.toggle("open");
          }
        });
      }
    });

    nav.querySelectorAll("a:not(.nav-link-dropdown)").forEach(function (link) {
      link.addEventListener("click", function () {
        btn.classList.remove("open");
        nav.classList.remove("open");
        if (header) header.classList.remove("menu-open");
        document.body.style.overflow = "";
      });
    });
  }

  // ── Scroll Spy ──
  function initScrollSpy() {
    var navLinks = document.querySelectorAll("[data-nav]");
    var sections = document.querySelectorAll("section[id]");
    var header = document.getElementById("siteHeader");

    if (!navLinks.length || !sections.length) return;

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          navLinks.forEach(function (l) { l.classList.remove("active"); });
          var active = document.querySelector('[data-nav="' + entry.target.id + '"]');
          if (active) active.classList.add("active");
        }
      });
    }, {
      rootMargin: "-30% 0px -60% 0px",
      threshold: 0
    });

    sections.forEach(function (s) { observer.observe(s); });

    window.addEventListener("scroll", function () {
      if (header) header.classList.toggle("scrolled", window.scrollY > 10);
    }, { passive: true });
  }

  // ── Currency Switcher Listener ──
  function initCurrencySwitcher() {
    var select = document.getElementById("globalCurrencySelect");
    if (!select) return;

    select.value = ACTIVE_CURRENCY;

    select.addEventListener("change", function () {
      ACTIVE_CURRENCY = select.value;
      localStorage.setItem("odonto_currency", ACTIVE_CURRENCY);

      renderAllGrids();
      initComparator();

      var modal = document.getElementById("quickViewModal");
      if (modal && modal.classList.contains("open")) {
        var activeProdTitle = modal.querySelector("#modalTitle");
        if (activeProdTitle) {
          var db = window.__DYNAMIC_PRODUCTS__ || [];
          var p = db.find(function (item) { return item.name === activeProdTitle.textContent; });
          if (p) {
            var priceEl = document.getElementById("modalPrice");
            if (priceEl) priceEl.textContent = formatPrice(p.discounted_price || p.discountedPrice || 0);

            var existingStoreBox = modal.querySelector(".modal-multistore-box");
            if (existingStoreBox) existingStoreBox.remove();

            var rightCol = modal.querySelector(".quick-modal-grid > div:last-child");
            if (rightCol) {
              var storeHtml = renderMultiStoreHtml(p);
              var div = document.createElement("div");
              div.innerHTML = storeHtml;
              rightCol.appendChild(div.firstElementChild);
            }
          }
        }
      }
    });
  }

  // ── Boot ──
  document.addEventListener("DOMContentLoaded", function () {
    detectUserGeoCurrency();
    safe(initMobileMenu, "mobileMenu");
    safe(initScrollSpy, "scrollSpy");
    safe(initCurrencySwitcher, "currencySwitcher");
    safe(initCardGalleries, "cardGalleries");
    safe(initQuickModal, "quickModal");

    fetchLiveExchangeRates().then(function () {
      safe(hydrate, "hydrate");
    });
  });

})();
