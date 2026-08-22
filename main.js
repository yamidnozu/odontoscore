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

  function initRadars() {
    var radarFigures = document.querySelectorAll("[data-radar]");
    if (!radarFigures.length) return;

    var db = window.__DB__ || { productos: [] };

    radarFigures.forEach(function (fig) {
      var prodId = fig.getAttribute("data-radar-id");
      if (!prodId) {
        var ficha = fig.closest("[data-producto-id]");
        if (ficha) prodId = ficha.getAttribute("data-producto-id");
      }

      if (prodId) {
        var item = db.productos.find(function (p) { return p.id === prodId; });
        if (item) {
          drawRadarSVG(fig, [item]);
        }
      }
    });
  }

  /**
   * Combined Live Search + Category Filter Bar
   */
  function initCatalogFilter() {
    var filterContainer = document.querySelector("[data-catalog-filters]");
    var searchInput = document.querySelector("#catalogSearchInput");
    var cards = document.querySelectorAll("#mainProductGrid .product-card");

    var activeCategory = "all";
    var currentQuery = "";

    function applyFilters() {
      var q = currentQuery.toLowerCase().trim();
      var visibleCount = 0;

      cards.forEach(function (card) {
        var cardCat = card.getAttribute("data-category") || "";
        var cardBrand = card.getAttribute("data-brand") || "";
        var cardTitle = card.getAttribute("data-title") || "";

        var matchesCat = (activeCategory === "all" || cardCat === activeCategory);
        var matchesSearch = !q || cardBrand.indexOf(q) !== -1 || cardTitle.indexOf(q) !== -1;

        if (matchesCat && matchesSearch) {
          card.style.display = "flex";
          visibleCount++;
        } else {
          card.style.display = "none";
        }
      });
    }

    if (filterContainer) {
      var buttons = filterContainer.querySelectorAll(".filter-pill-btn");
      buttons.forEach(function (btn) {
        btn.addEventListener("click", function () {
          activeCategory = btn.getAttribute("data-filter") || "all";
          buttons.forEach(function (b) { b.classList.remove("active"); });
          btn.classList.add("active");
          applyFilters();
        });
      });
    }

    if (searchInput) {
      searchInput.addEventListener("input", function () {
        currentQuery = searchInput.value;
        applyFilters();
      });
    }
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
      var db = window.__DB__ || { productos: [] };
      var p = db.productos.find(function (item) { return item.id === prodId; });
      if (!p) return;

      e.preventDefault();

      if (titleEl) titleEl.textContent = p.name;
      if (brandEl) brandEl.textContent = p.marca;
      if (priceEl) priceEl.textContent = p.discountedPrice + " €";
      if (imgEl) {
        imgEl.src = p.images && p.images[0] ? p.images[0] : "assets/img/hero-dental.svg";
        imgEl.onerror = function() { this.src = "assets/img/hero-dental.svg"; };
      }
      if (buyBtn) buyBtn.href = p.affiliate_url;
      if (fullLink) fullLink.href = "producto/" + p.id + ".html";

      if (radarCanvas) {
        drawRadarSVG(radarCanvas, [p]);
      }

      if (specsTable) {
        specsTable.innerHTML = "" +
          "<tr><th>Especialidad</th><td>" + p.category + "</td></tr>" +
          "<tr><th>Tecnología</th><td>" + (p.tecnologia || "").toUpperCase() + "</td></tr>" +
          "<tr><th>Modos / Ajustes</th><td>" + (p.modos_limpieza || "1") + "</td></tr>" +
          "<tr><th>Presión / Potencia</th><td>" + (p.presion_agua_psi ? p.presion_agua_psi + " PSI" : (p.pulsaciones_min ? p.pulsaciones_min.toLocaleString() + " puls/min" : "—")) + "</td></tr>" +
          "<tr><th>Autonomía</th><td>" + (p.autonomia_dias > 365 ? "Red / No aplica" : p.autonomia_dias + " días") + "</td></tr>" +
          "<tr><th>Nivel Ruido</th><td>" + (p.nivel_ruido_db ? p.nivel_ruido_db + " dB" : "0 dB (Silencioso)") + "</td></tr>" +
          "<tr><th>Puntuación</th><td><strong style='color:#0E76BC'>" + p.valoracion_media + " / 5 ★</strong> (" + (p.resenas_cantidad || 0) + " reseñas)</td></tr>";
      }

      modalBackdrop.classList.add("open");
      document.body.style.overflow = "hidden";
    });
  }

  function initComparator() {
    var compRoot = document.querySelector("[data-comparator-app]");
    if (!compRoot) return;

    var db = window.__DB__ || { productos: [] };
    var categorySelect = compRoot.querySelector("#compCategorySelect");
    var productChecksContainer = compRoot.querySelector("#compProductChecks");
    var matrixContainer = compRoot.querySelector("#compMatrixContent");
    var radarContainer = compRoot.querySelector("#compRadarCanvas");
    var radarLegend = compRoot.querySelector("#compRadarLegend");

    function renderCategoryProducts(catKey) {
      var items = db.productos.filter(function (p) {
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
        label.appendChild(document.createTextNode(prod.name.length > 32 ? prod.name.substring(0, 32) + "..." : prod.name));
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

      var selectedProducts = db.productos.filter(function (p) {
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
          item.appendChild(document.createTextNode(prod.name.substring(0, 22) + "..."));
          radarLegend.appendChild(item);
        });
      }

      if (matrixContainer && selectedProducts.length > 0) {
        var tableHtml = '<table class="compare-matrix-table"><thead><tr><th class="row-label">Característica</th>';
        selectedProducts.forEach(function (p) {
          tableHtml += '<th><img src="' + (p.images && p.images[0] ? p.images[0] : 'assets/img/hero-dental.svg') + '" style="height:60px;margin:0 auto 6px;display:block;object-fit:contain;" alt="' + p.name + '"><strong>' + p.marca + '</strong><br><small>' + p.name.substring(0, 25) + '...</small></th>';
        });
        tableHtml += '</tr></thead><tbody>';

        var rows = [
          { label: "Precio Orientativo", fn: function(p) { return p.discountedPrice + ' €' + (p.discountedPrice < p.retailPrice ? ' <small style="color:#DC2626">(-' + Math.round((1 - p.discountedPrice/p.retailPrice)*100) + '%)</small>' : ''); } },
          { label: "Especialidad", fn: function(p) { return p.category; } },
          { label: "Tecnología", fn: function(p) { return (p.tecnologia || '').toUpperCase(); } },
          { label: "Modos / Ajustes", fn: function(p) { return p.modos_limpieza || "1"; } },
          { label: "Presión / Potencia", fn: function(p) { return p.presion_agua_psi ? p.presion_agua_psi + ' PSI' : (p.pulsaciones_min ? p.pulsaciones_min.toLocaleString() + ' puls/min' : '—'); } },
          { label: "Autonomía", fn: function(p) { return p.autonomia_dias > 365 ? 'Red / No aplica' : p.autonomia_dias + ' días'; } },
          { label: "Nivel Ruido (dB)", fn: function(p) { return p.nivel_ruido_db ? p.nivel_ruido_db + ' dB' : '0 dB (Silencioso)'; } },
          { label: "Puntuación", fn: function(p) { return '<strong style="color:#0E76BC">' + p.valoracion_media + ' / 5 ★</strong>'; } },
          { label: "Comprar en Amazon", fn: function(p) { return '<a class="btn-card-amazon" href="' + p.affiliate_url + '" target="_blank" rel="sponsored nofollow noopener">Ver en Amazon</a>'; } }
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
    safe(initQuickModal, "initQuickModal");
    safe(initComparator, "initComparator");
  });

})();
