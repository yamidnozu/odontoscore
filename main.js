(function () {
  "use strict";

  function safe(fn, name) {
    try {
      fn();
    } catch (err) {
      console.warn("[OdontoScore safe-init] Failed:", name, err);
    }
  }

  var RADAR_COLORS = [
    { fill: "rgba(14, 118, 188, 0.25)", stroke: "#0E76BC", point: "#0E76BC" },
    { fill: "rgba(16, 185, 129, 0.25)", stroke: "#10B981", point: "#10B981" },
    { fill: "rgba(245, 158, 11, 0.25)", stroke: "#F59E0B", point: "#F59E0B" },
    { fill: "rgba(139, 92, 246, 0.25)", stroke: "#8B5CF6", point: "#8B5CF6" }
  ];

  var SCORE_AXES = [
    { key: "score_eficacia", label: "Eficacia" },
    { key: "score_comodidad_encias", label: "Encías/Tejidos" },
    { key: "score_durabilidad", label: "Durabilidad" },
    { key: "score_facilidad_uso", label: "Ergonomía" },
    { key: "score_silencio", label: "Silencio" },
    { key: "score_tecnologia", label: "Tecnología" },
    { key: "score_calidad_precio", label: "Calidad/Precio" }
  ];

  function drawRadarSVG(container, products) {
    if (!container || !products || products.length === 0) return;

    var size = 320;
    var center = size / 2;
    var radius = size * 0.38;
    var totalAxes = SCORE_AXES.length;
    var angleStep = (Math.PI * 2) / totalAxes;

    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("viewBox", "0 0 " + size + " " + size);
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", "100%");
    svg.style.maxWidth = size + "px";

    for (var level = 2; level <= 10; level += 2) {
      var r = (level / 10) * radius;
      var webPoints = [];
      for (var i = 0; i < totalAxes; i++) {
        var angle = i * angleStep - Math.PI / 2;
        var x = center + r * Math.cos(angle);
        var y = center + r * Math.sin(angle);
        webPoints.push(x.toFixed(1) + "," + y.toFixed(1));
      }
      var polygon = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
      polygon.setAttribute("points", webPoints.join(" "));
      polygon.setAttribute("fill", level === 10 ? "#F8FAFC" : "none");
      polygon.setAttribute("stroke", "#E2E8F0");
      polygon.setAttribute("stroke-width", "1");
      svg.appendChild(polygon);
    }

    for (var a = 0; a < totalAxes; a++) {
      var axisAngle = a * angleStep - Math.PI / 2;
      var axX = center + radius * Math.cos(axisAngle);
      var axY = center + radius * Math.sin(axisAngle);

      var line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("x1", center);
      line.setAttribute("y1", center);
      line.setAttribute("x2", axX.toFixed(1));
      line.setAttribute("y2", axY.toFixed(1));
      line.setAttribute("stroke", "#CBD5E1");
      line.setAttribute("stroke-width", "1");
      svg.appendChild(line);

      var labelR = radius + 22;
      var lx = center + labelR * Math.cos(axisAngle);
      var ly = center + labelR * Math.sin(axisAngle);

      var text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.setAttribute("x", lx.toFixed(1));
      text.setAttribute("y", (ly + 4).toFixed(1));
      text.setAttribute("text-anchor", "middle");
      text.setAttribute("font-family", "Inter, sans-serif");
      text.setAttribute("font-size", "10");
      text.setAttribute("font-weight", "600");
      text.setAttribute("fill", "#475569");
      text.textContent = SCORE_AXES[a].label;
      svg.appendChild(text);
    }

    products.forEach(function (prod, pIdx) {
      var colorScheme = RADAR_COLORS[pIdx % RADAR_COLORS.length];
      var polyPoints = [];

      SCORE_AXES.forEach(function (axis, aIdx) {
        var val = Number(prod[axis.key]) || 0;
        var rVal = (Math.min(10, Math.max(0, val)) / 10) * radius;
        var angle = aIdx * angleStep - Math.PI / 2;
        var px = center + rVal * Math.cos(angle);
        var py = center + rVal * Math.sin(angle);
        polyPoints.push(px.toFixed(1) + "," + py.toFixed(1));
      });

      var dataPoly = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
      dataPoly.setAttribute("points", polyPoints.join(" "));
      dataPoly.setAttribute("fill", colorScheme.fill);
      dataPoly.setAttribute("stroke", colorScheme.stroke);
      dataPoly.setAttribute("stroke-width", "2.5");
      svg.appendChild(dataPoly);

      polyPoints.forEach(function (pt) {
        var coords = pt.split(",");
        var dot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        dot.setAttribute("cx", coords[0]);
        dot.setAttribute("cy", coords[1]);
        dot.setAttribute("r", "4");
        dot.setAttribute("fill", colorScheme.point);
        dot.setAttribute("stroke", "#FFFFFF");
        dot.setAttribute("stroke-width", "1.5");
        svg.appendChild(dot);
      });
    });

    container.innerHTML = "";
    container.appendChild(svg);
  }

  function getProductImage(p) {
    if (p.specs_extra && p.specs_extra.image_url) return p.specs_extra.image_url;
    if (p.local_assets && p.local_assets[0] && p.local_assets[0] !== "assets/img/hero-dental.svg") return p.local_assets[0];
    if (p.images && p.images[0] && p.images[0] !== "assets/img/hero-dental.svg") return p.images[0];
    return "https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&ASIN=" + (p.asin || "") + "&Format=_SL800_&ID=AsinImage&MarketPlace=ES&ServiceVersion=20070822&WS=1&tag=odontoscore-21";
  }

  function renderDynamicCard(p) {
    var discountPct = 0;
    var retail = Number(p.retail_price || p.retailPrice || 49.99);
    var current = Number(p.discounted_price || p.discountedPrice || retail);
    if (current < retail) {
      discountPct = Math.round((1 - current / retail) * 100);
    }

    var imgUrl = getProductImage(p);
    var techStr = (p.tecnologia || "sonico").replace(/_/g, " ").toUpperCase();
    var potenciaStr = p.presion_agua_psi ? p.presion_agua_psi + " PSI" : (p.pulsaciones_min ? Number(p.pulsaciones_min).toLocaleString() + " puls/min" : (p.esterilizable_autoclave ? "Autoclave 134°C" : "Clínico"));
    var autonomiaStr = (p.autonomia_dias && Number(p.autonomia_dias) < 365) ? p.autonomia_dias + " días" : "Red Eléctrica / AC";

    return "" +
      "<article class='product-card' data-producto-id='" + p.id + "' data-asin='" + p.asin + "' data-category='" + (p.categoria_odontologica || "") + "' data-brand='" + (p.marca || "").toLowerCase() + "' data-title='" + (p.name || "").toLowerCase() + "' data-price='" + current + "' data-score='" + (p.score_eficacia || 9) + "'>" +
        (p.is_featured || p.isFeatured ? "<span class='card-badge-top' style='position:absolute;top:1rem;left:1rem;z-index:10;background:#0F172A;color:#FFF;font-size:0.75rem;font-weight:700;padding:3px 10px;border-radius:999px;'>★ Top Recomendado</span>" : "") +
        (discountPct > 0 ? "<span class='price-discount-pill' style='position:absolute;top:1rem;right:1rem;z-index:10;'>-" + discountPct + "%</span>" : "") +
        "<div class='card-media'>" +
          "<img src='" + imgUrl + "' alt='" + (p.name || "") + "' loading='lazy' onerror=\"this.onerror=null;this.src='assets/img/hero-dental.svg';\">" +
        "</div>" +
        "<div class='card-body'>" +
          "<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:0.35rem;'>" +
            "<span style='font-size:0.75rem;font-weight:800;color:#0E76BC;letter-spacing:0.05em;text-transform:uppercase;'>" + (p.marca || "Dental") + "</span>" +
            "<span style='font-size:0.7rem;color:#475569;font-weight:700;background:#F1F5F9;padding:2px 8px;border-radius:999px;'>" + (p.category || "Odontología") + "</span>" +
          "</div>" +
          "<h3 class='card-title' title='" + (p.name || "") + "'>" + (p.name || "") + "</h3>" +
          "<div class='card-rating-box'>" +
            "<span class='rating-badge'>★ " + (p.valoracion_media || "4.5") + "</span>" +
            "<span style='font-size:0.8rem;color:#64748B;'>(" + Number(p.resenas_cantidad || 500).toLocaleString() + " valoraciones)</span>" +
          "</div>" +
          "<div class='card-specs-matrix'>" +
            "<div class='spec-cell'>⚙️ <strong>" + techStr + "</strong></div>" +
            "<div class='spec-cell'>🎛️ <strong>" + (p.modos_limpieza || 1) + " Modos</strong></div>" +
            "<div class='spec-cell'>⚡ <strong>" + potenciaStr + "</strong></div>" +
            "<div class='spec-cell'>🔋 <strong>" + autonomiaStr + "</strong></div>" +
          "</div>" +
          "<div class='card-price-row'>" +
            "<div>" +
              "<span class='price-main-val'>" + current.toFixed(2).replace(".", ",") + " €</span>" +
              (discountPct > 0 ? "<span class='price-strike-val'>" + retail.toFixed(2).replace(".", ",") + " €</span>" : "") +
            "</div>" +
            "<span style='font-size:0.75rem;font-weight:700;color:#16A34A;display:flex;align-items:center;gap:0.25rem;'>✓ Prime 24/48h</span>" +
          "</div>" +
          "<div class='card-actions-grid'>" +
            "<button type='button' class='btn-card-quick' data-quick-view='" + p.id + "'>" +
              "<span>⚡ Ficha &amp; Radar</span>" +
            "</button>" +
            "<a href='" + (p.affiliate_url || ("https://www.amazon.es/dp/" + p.asin + "?tag=odontoscore-21")) + "' target='_blank' rel='sponsored nofollow noopener' class='btn-card-prime'>" +
              "<span>🛒 Ver en Amazon</span>" +
            "</a>" +
          "</div>" +
          "<div style='margin-top:0.75rem;padding-top:0.5rem;border-top:1px dashed #E2E8F0;display:flex;align-items:center;justify-content:center;'>" +
            "<label style='font-size:0.8rem;font-weight:600;color:#64748B;cursor:pointer;display:inline-flex;align-items:center;gap:0.35rem;'>" +
              "<input type='checkbox' class='product-compare-checkbox' value='" + p.id + "' data-name='" + (p.name ? p.name.substring(0, 25) : "") + "...'>" +
              "<span>⚖️ Añadir al Comparador</span>" +
            "</label>" +
          "</div>" +
        "</div>" +
      "</article>";
  }

  /**
   * Dynamic Catalog Hydration directly from Supabase REST API
   */
  async function hydrateDynamicCatalog() {
    var brand = window.__BRAND__ || {};
    var supabaseUrl = brand.supabaseUrl || "https://lgaolwxeizxynkpcjsse.supabase.co";
    var anonKey = brand.supabaseAnonKey || "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxnYW9sd3hlaXp4eW5rcGNqc3NlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODY3NTI0NjcsImV4cCI6MjEwMjMyODQ2N30.M9AzjDz9P44Tt2JfDnmRr9zzNaDw-z-vjTV83CxOdwM";

    var gridEl = document.querySelector("#mainProductGrid");
    if (!gridEl) return;

    try {
      var res = await fetch(supabaseUrl.replace(/\/$/, "") + "/rest/v1/products?select=*&order=is_featured.desc,discounted_price.desc", {
        headers: {
          "apikey": anonKey,
          "Authorization": "Bearer " + anonKey,
          "Accept": "application/json"
        }
      });

      if (res.ok) {
        var products = await res.json();
        if (products && products.length > 0) {
          window.__DYNAMIC_PRODUCTS__ = products;
          window.__DB__ = { productos: products };

          // Re-render grid dynamically
          gridEl.innerHTML = products.map(renderDynamicCard).join("");

          // Re-bind events
          initCatalogFilter();
          initFloatingDock();
          initComparator();
          initRadars();
        }
      }
    } catch (err) {
      console.warn("[OdontoScore] Dynamic fetch fallback to static cache:", err);
    }
  }

  function initCatalogFilter() {
    var filterContainer = document.querySelector("[data-catalog-filters]");
    var searchInput = document.querySelector("#catalogSearchInput");
    var sortSelect = document.querySelector("#catalogSortSelect");
    var gridEl = document.querySelector("#mainProductGrid");
    var btnGrid = document.querySelector("#btnViewGrid");
    var btnList = document.querySelector("#btnViewList");

    if (!gridEl) return;

    var cards = Array.from(gridEl.querySelectorAll(".product-card"));
    var activeCategory = "all";
    var currentQuery = "";

    function applyFiltersAndSort() {
      var q = currentQuery.toLowerCase().trim();
      var sortMode = sortSelect ? sortSelect.value : "featured";

      var visibleCards = cards.filter(function (card) {
        var cardCat = card.getAttribute("data-category") || "";
        var cardBrand = card.getAttribute("data-brand") || "";
        var cardTitle = card.getAttribute("data-title") || "";

        var matchesCat = (activeCategory === "all" || cardCat === activeCategory);
        var matchesSearch = !q || cardBrand.indexOf(q) !== -1 || cardTitle.indexOf(q) !== -1;

        if (matchesCat && matchesSearch) {
          card.style.display = "flex";
          return true;
        } else {
          card.style.display = "none";
          return false;
        }
      });

      visibleCards.sort(function (a, b) {
        var priceA = parseFloat(a.getAttribute("data-price")) || 0;
        var priceB = parseFloat(b.getAttribute("data-price")) || 0;
        var scoreA = parseFloat(a.getAttribute("data-score")) || 0;
        var scoreB = parseFloat(b.getAttribute("data-score")) || 0;

        if (sortMode === "price-asc") return priceA - priceB;
        if (sortMode === "price-desc") return priceB - priceA;
        if (sortMode === "score") return scoreB - scoreA;
        return 0;
      });

      visibleCards.forEach(function (card) {
        gridEl.appendChild(card);
      });
    }

    if (filterContainer) {
      var buttons = filterContainer.querySelectorAll(".filter-pill-btn");
      buttons.forEach(function (btn) {
        btn.addEventListener("click", function () {
          activeCategory = btn.getAttribute("data-filter") || "all";
          buttons.forEach(function (b) { b.classList.remove("active"); });
          btn.classList.add("active");
          applyFiltersAndSort();
        });
      });
    }

    if (searchInput) {
      searchInput.addEventListener("input", function () {
        currentQuery = searchInput.value;
        applyFiltersAndSort();
      });
    }

    if (sortSelect) {
      sortSelect.addEventListener("change", applyFiltersAndSort);
    }

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

  function initFloatingDock() {
    var dock = document.querySelector("#floatingCompareDock");
    var countText = document.querySelector("#floatingCompareCountText");
    var checkboxes = document.querySelectorAll(".product-compare-checkbox");

    function updateDock() {
      var checked = document.querySelectorAll(".product-compare-checkbox:checked");
      var count = checked.length;

      if (count > 0 && dock) {
        dock.classList.add("visible");
        if (countText) {
          countText.textContent = count + (count === 1 ? " producto seleccionado" : " productos seleccionados");
        }
      } else if (dock) {
        dock.classList.remove("visible");
      }
    }

    checkboxes.forEach(function (chk) {
      chk.addEventListener("change", updateDock);
    });
  }

  function initQuickModal() {
    var modalBackdrop = document.querySelector("#quickViewModal");
    if (!modalBackdrop) return;

    var closeBtn = modalBackdrop.querySelector(".quick-modal-close-btn");
    var titleEl = modalBackdrop.querySelector("#modalTitle");
    var brandEl = modalBackdrop.querySelector("#modalBrand");
    var priceEl = modalBackdrop.querySelector("#modalPrice");
    var imgEl = modalBackdrop.querySelector("#modalImg");
    var radarCanvas = modalBackdrop.querySelector("#modalRadarCanvas");
    var specsTable = modalBackdrop.querySelector("#modalSpecsTable tbody");
    var buyBtn = modalBackdrop.querySelector("#modalBuyBtn");
    var fullLink = modalBackdrop.querySelector("#modalFullLink");

    function closeModal() {
      modalBackdrop.classList.remove("open");
      document.body.style.overflow = "auto";
    }

    if (closeBtn) closeBtn.addEventListener("click", closeModal);
    modalBackdrop.addEventListener("click", function (e) {
      if (e.target === modalBackdrop) closeModal();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && modalBackdrop.classList.contains("open")) {
        closeModal();
      }
    });

    document.addEventListener("click", function (e) {
      var trigger = e.target.closest("[data-quick-view]");
      if (!trigger) return;

      var prodId = trigger.getAttribute("data-quick-view");
      var db = window.__DYNAMIC_PRODUCTS__ || (window.__DB__ && window.__DB__.productos) || [];
      var p = db.find(function (item) { return item.id === prodId; });
      if (!p) return;

      e.preventDefault();

      var priceVal = Number(p.discounted_price || p.discountedPrice || p.retail_price || p.retailPrice || 0);
      var imgUrl = getProductImage(p);

      if (titleEl) titleEl.textContent = p.name;
      if (brandEl) brandEl.textContent = p.marca;
      if (priceEl) priceEl.textContent = priceVal.toFixed(2).replace(".", ",") + " €";
      if (imgEl) {
        imgEl.src = imgUrl;
        imgEl.onerror = function() { this.src = "assets/img/hero-dental.svg"; };
      }
      if (buyBtn) buyBtn.href = p.affiliate_url || ("https://www.amazon.es/dp/" + p.asin + "?tag=odontoscore-21");
      if (fullLink) fullLink.href = "producto/" + p.id + ".html";

      if (radarCanvas) {
        drawRadarSVG(radarCanvas, [p]);
      }

      if (specsTable) {
        specsTable.innerHTML = "" +
          "<tr><th>Especialidad</th><td>" + (p.category || "Odontología") + "</td></tr>" +
          "<tr><th>Tecnología</th><td>" + (p.tecnologia || "").toUpperCase() + "</td></tr>" +
          "<tr><th>Modos / Ajustes</th><td>" + (p.modos_limpieza || "1") + "</td></tr>" +
          "<tr><th>Presión / Potencia</th><td>" + (p.presion_agua_psi ? p.presion_agua_psi + " PSI" : (p.pulsaciones_min ? Number(p.pulsaciones_min).toLocaleString() + " puls/min" : "—")) + "</td></tr>" +
          "<tr><th>Autonomía</th><td>" + (p.autonomia_dias && Number(p.autonomia_dias) > 365 ? "Red / AC" : (p.autonomia_dias || 14) + " días") + "</td></tr>" +
          "<tr><th>Nivel Ruido</th><td>" + (p.nivel_ruido_db ? p.nivel_ruido_db + " dB" : "0 dB (Silencioso)") + "</td></tr>" +
          "<tr><th>Puntuación</th><td><strong style='color:#0E76BC'>" + (p.valoracion_media || "4.5") + " / 5 ★</strong> (" + Number(p.resenas_cantidad || 500).toLocaleString() + " reseñas)</td></tr>";
      }

      modalBackdrop.classList.add("open");
      document.body.style.overflow = "hidden";
    });
  }

  function initComparator() {
    var compRoot = document.querySelector("[data-comparator-app]");
    if (!compRoot) return;

    var db = window.__DYNAMIC_PRODUCTS__ || (window.__DB__ && window.__DB__.productos) || [];
    var categorySelect = compRoot.querySelector("#compCategorySelect");
    var productChecksContainer = compRoot.querySelector("#compProductChecks");
    var matrixContainer = compRoot.querySelector("#compMatrixContent");
    var radarContainer = compRoot.querySelector("#compRadarCanvas");
    var radarLegend = compRoot.querySelector("#compRadarLegend");

    function renderCategoryProducts(catKey) {
      var items = db.filter(function (p) {
        return !catKey || p.categoria_odontologica === catKey;
      });

      if (!productChecksContainer) return;
      productChecksContainer.innerHTML = "";

      items.slice(0, 10).forEach(function (prod, idx) {
        var label = document.createElement("label");
        label.className = "comp-check-item";
        label.style.display = "inline-flex";
        label.style.alignItems = "center";
        label.style.gap = "0.4rem";
        label.style.marginRight = "1rem";
        label.style.marginBottom = "0.5rem";
        label.style.fontSize = "0.85rem";
        label.style.fontWeight = "600";
        label.style.cursor = "pointer";

        var input = document.createElement("input");
        input.type = "checkbox";
        input.value = prod.id;
        input.checked = idx < 3;

        input.addEventListener("change", updateComparison);

        label.appendChild(input);
        label.appendChild(document.createTextNode(prod.name && prod.name.length > 32 ? prod.name.substring(0, 32) + "..." : (prod.name || "")));
        productChecksContainer.appendChild(label);
      });

      updateComparison();
    }

    function updateComparison() {
      var selectedIds = [];
      var checkedInputs = productChecksContainer.querySelectorAll("input:checked");
      checkedInputs.forEach(function (inp) {
        selectedIds.push(inp.value);
      });

      var selectedProducts = db.filter(function (p) {
        return selectedIds.indexOf(p.id) !== -1;
      });

      if (radarContainer) {
        drawRadarSVG(radarContainer, selectedProducts);
      }

      if (radarLegend) {
        radarLegend.innerHTML = "";
        selectedProducts.forEach(function (prod, idx) {
          var color = RADAR_COLORS[idx % RADAR_COLORS.length].stroke;
          var item = document.createElement("span");
          item.style.display = "inline-flex";
          item.style.alignItems = "center";
          item.style.gap = "0.4rem";
          item.style.marginRight = "1rem";
          item.style.fontSize = "0.85rem";
          item.style.fontWeight = "700";

          var dot = document.createElement("span");
          dot.style.width = "10px";
          dot.style.height = "10px";
          dot.style.borderRadius = "50%";
          dot.style.backgroundColor = color;

          item.appendChild(dot);
          item.appendChild(document.createTextNode(prod.name && prod.name.length > 22 ? prod.name.substring(0, 22) + "..." : (prod.name || "")));
          radarLegend.appendChild(item);
        });
      }

      if (matrixContainer && selectedProducts.length > 0) {
        var tableHtml = '<table class="compare-matrix-table"><thead><tr><th class="row-label">Característica</th>';
        selectedProducts.forEach(function (p) {
          var imgUrl = getProductImage(p);
          tableHtml += '<th><img src="' + imgUrl + '" style="height:60px;margin:0 auto 6px;display:block;object-fit:contain;" alt="' + (p.name || "") + '"><strong>' + (p.marca || "") + '</strong><br><small>' + (p.name && p.name.length > 25 ? p.name.substring(0, 25) + "..." : (p.name || "")) + '</small></th>';
        });
        tableHtml += '</tr></thead><tbody>';

        var rows = [
          { label: "Precio Orientativo", fn: function(p) { var cur = Number(p.discounted_price || p.discountedPrice || 0); var ret = Number(p.retail_price || p.retailPrice || cur); return cur.toFixed(2).replace(".", ",") + ' €' + (cur < ret ? ' <small style="color:#DC2626">(-' + Math.round((1 - cur/ret)*100) + '%)</small>' : ''); } },
          { label: "Especialidad", fn: function(p) { return p.category || "Odontología"; } },
          { label: "Tecnología", fn: function(p) { return (p.tecnologia || '').toUpperCase(); } },
          { label: "Modos / Ajustes", fn: function(p) { return p.modos_limpieza || "1"; } },
          { label: "Presión / Potencia", fn: function(p) { return p.presion_agua_psi ? p.presion_agua_psi + ' PSI' : (p.pulsaciones_min ? Number(p.pulsaciones_min).toLocaleString() + ' puls/min' : '—'); } },
          { label: "Autonomía", fn: function(p) { return p.autonomia_dias && Number(p.autonomia_dias) > 365 ? 'Red / AC' : (p.autonomia_dias || 14) + ' días'; } },
          { label: "Nivel Ruido (dB)", fn: function(p) { return p.nivel_ruido_db ? p.nivel_ruido_db + ' dB' : '0 dB (Silencioso)'; } },
          { label: "Puntuación", fn: function(p) { return '<strong style="color:#0E76BC">' + (p.valoracion_media || 4.5) + ' / 5 ★</strong>'; } },
          { label: "Comprar en Amazon", fn: function(p) { return '<a class="btn-card-prime" style="padding:0.5rem;" href="' + (p.affiliate_url || ('https://www.amazon.es/dp/' + p.asin + '?tag=odontoscore-21')) + '" target="_blank" rel="sponsored nofollow noopener">🛒 Ver en Amazon</a>'; } }
        ];

        rows.forEach(function (r) {
          tableHtml += '<tr><th class="row-label">' + r.label + '</th>';
          selectedProducts.forEach(function (p) {
            tableHtml += '<td>' + r.fn(p) + '</td>';
          });
          tableHtml += '</tr>';
        });

        tableHtml += '</tbody></table>';
        matrixContainer.innerHTML = tableHtml;
      }
    }

    if (categorySelect) {
      categorySelect.addEventListener("change", function () {
        renderCategoryProducts(categorySelect.value);
      });
      renderCategoryProducts(categorySelect.value);
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    safe(initRadars, "initRadars");
    safe(initCatalogFilter, "initCatalogFilter");
    safe(initFloatingDock, "initFloatingDock");
    safe(initQuickModal, "initQuickModal");
    safe(initComparator, "initComparator");
    safe(hydrateDynamicCatalog, "hydrateDynamicCatalog");
  });

})();
