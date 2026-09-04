import re
from pathlib import Path

VERSION = "20260903_v72"

# Root header HTML
ROOT_HEADER = '''<header class="site-header" id="siteHeader">
  <div class="container nav-wrapper">
    <a href="index.html" class="brand-logo" title="OdontoScore - Portal Odontológico">
      <img src="assets/img/logo-odontoscore.svg" alt="OdontoScore" height="38">
    </a>
    <button type="button" class="mobile-menu-toggle" id="mobileMenuBtn" aria-label="Menú">
      <span></span><span></span><span></span>
    </button>
    <nav class="main-nav" id="mainNav">
      <ul class="nav-links">
        <li><a href="index.html#catalogo">Catálogo</a></li>
        <li><a href="index.html#estudiantes">Estudiantes</a></li>
        <li class="nav-item-dropdown">
          <a href="index.html#academia" class="nav-link-dropdown" aria-haspopup="true" aria-expanded="false">
            Academia
            <svg class="dropdown-arrow" width="10" height="6" viewBox="0 0 10 6" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M1 1L5 5L9 1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </a>
          <div class="nav-dropdown-menu">
            <a href="guias/anatomia-dental-3d-por-capas.html" class="dropdown-link">Atlas Anatómico Dental 360°</a>
            <a href="guias/semiologia-pares-craneales-odontologia.html" class="dropdown-link">Semiología y Pares Craneales</a>
            <a href="guias/mejor-cepillo-electrico-encias-sensibles-2026.html" class="dropdown-link">Guía: Encías Sensibles</a>
            <a href="guias/mejor-irrigador-dental-brackets-2026.html" class="dropdown-link">Guía: Higiene en Ortodoncia</a>
            <div class="dropdown-divider"></div>
            <a href="index.html#academia" class="dropdown-link-all">Ver toda la Academia →</a>
          </div>
        </li>
        <li><a href="comparador.html">Comparador</a></li>
        <li><a href="ofertas.html">Ofertas</a></li>
        <li><a href="index.html#faq">FAQ</a></li>
      </ul>
      <div class="nav-actions">
        <a href="comparador.html" class="btn-nav-compare">
          <span>Comparar Modelos</span>
        </a>
      </div>
    </nav>
  </div>
</header>'''

# Root header with currency for index.html
INDEX_HEADER = '''<header class="site-header" id="siteHeader">
  <div class="container nav-wrapper">
    <a href="index.html" class="brand-logo" title="OdontoScore - Portal Odontológico">
      <img src="assets/img/logo-odontoscore.svg" alt="OdontoScore" height="38">
    </a>
    <button type="button" class="mobile-menu-toggle" id="mobileMenuBtn" aria-label="Menú">
      <span></span><span></span><span></span>
    </button>
    <nav class="main-nav" id="mainNav">
      <ul class="nav-links">
        <li><a href="#catalogo" data-nav="catalogo">Catálogo</a></li>
        <li><a href="#estudiantes" data-nav="estudiantes">Estudiantes</a></li>
        <li class="nav-item-dropdown">
          <a href="#academia" class="nav-link-dropdown" data-nav="academia" aria-haspopup="true" aria-expanded="false">
            Academia
            <svg class="dropdown-arrow" width="10" height="6" viewBox="0 0 10 6" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M1 1L5 5L9 1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </a>
          <div class="nav-dropdown-menu">
            <a href="guias/anatomia-dental-3d-por-capas.html" class="dropdown-link">Atlas Anatómico Dental 360°</a>
            <a href="guias/semiologia-pares-craneales-odontologia.html" class="dropdown-link">Semiología y Pares Craneales</a>
            <a href="guias/mejor-cepillo-electrico-encias-sensibles-2026.html" class="dropdown-link">Guía: Encías Sensibles</a>
            <a href="guias/mejor-irrigador-dental-brackets-2026.html" class="dropdown-link">Guía: Higiene en Ortodoncia</a>
            <div class="dropdown-divider"></div>
            <a href="#academia" class="dropdown-link-all">Ver toda la Academia →</a>
          </div>
        </li>
        <li><a href="#comparador" data-nav="comparador">Comparador</a></li>
        <li><a href="#ofertas" data-nav="ofertas">Ofertas</a></li>
        <li><a href="#faq" data-nav="faq">FAQ</a></li>
      </ul>
      <div class="nav-actions">
        <div class="currency-selector-wrapper">
          <select id="globalCurrencySelect" class="currency-select" aria-label="Seleccionar País y Moneda">
            <option value="EUR" data-symbol="€">EUR (€) · España</option>
            <option value="COP" data-symbol="$">COP ($) · Colombia</option>
            <option value="MXN" data-symbol="$">MXN ($) · México</option>
            <option value="USD" data-symbol="$">USD ($) · Estados Unidos</option>
            <option value="PEN" data-symbol="S/.">PEN (S/.) · Perú</option>
            <option value="ARS" data-symbol="$">ARS ($) · Argentina</option>
            <option value="CLP" data-symbol="$">CLP ($) · Chile</option>
            <option value="GBP" data-symbol="£">GBP (£) · Reino Unido</option>
          </select>
        </div>
        <a href="comparador.html" class="btn-nav-compare">
          <span>Comparar Modelos</span>
        </a>
      </div>
    </nav>
  </div>
</header>'''

# Subfolder header HTML
SUB_HEADER = '''<header class="site-header" id="siteHeader">
  <div class="container nav-wrapper">
    <a href="../index.html" class="brand-logo" title="OdontoScore - Portal Odontológico">
      <img src="../assets/img/logo-odontoscore.svg" alt="OdontoScore" height="38">
    </a>
    <button type="button" class="mobile-menu-toggle" id="mobileMenuBtn" aria-label="Menú">
      <span></span><span></span><span></span>
    </button>
    <nav class="main-nav" id="mainNav">
      <ul class="nav-links">
        <li><a href="../index.html#catalogo">Catálogo</a></li>
        <li><a href="../index.html#estudiantes">Estudiantes</a></li>
        <li class="nav-item-dropdown">
          <a href="../index.html#academia" class="nav-link-dropdown" aria-haspopup="true" aria-expanded="false">
            Academia
            <svg class="dropdown-arrow" width="10" height="6" viewBox="0 0 10 6" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M1 1L5 5L9 1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </a>
          <div class="nav-dropdown-menu">
            <a href="../guias/anatomia-dental-3d-por-capas.html" class="dropdown-link">Atlas Anatómico Dental 360°</a>
            <a href="../guias/semiologia-pares-craneales-odontologia.html" class="dropdown-link">Semiología y Pares Craneales</a>
            <a href="../guias/mejor-cepillo-electrico-encias-sensibles-2026.html" class="dropdown-link">Guía: Encías Sensibles</a>
            <a href="../guias/mejor-irrigador-dental-brackets-2026.html" class="dropdown-link">Guía: Higiene en Ortodoncia</a>
            <div class="dropdown-divider"></div>
            <a href="../index.html#academia" class="dropdown-link-all">Ver toda la Academia →</a>
          </div>
        </li>
        <li><a href="../comparador.html">Comparador</a></li>
        <li><a href="../ofertas.html">Ofertas</a></li>
        <li><a href="../index.html#faq">FAQ</a></li>
      </ul>
      <div class="nav-actions">
        <a href="../comparador.html" class="btn-nav-compare">
          <span>Comparar Modelos</span>
        </a>
      </div>
    </nav>
  </div>
</header>'''

header_regex = re.compile(r'<header[^>]*class="[^"]*(?:site-header|header)[^"]*"[^>]*>.*?</header>', re.DOTALL)
css_root_regex = re.compile(r'href="styles\.css(?:\?[^"]*)?"')
css_sub_regex = re.compile(r'href="\.\./styles\.css(?:\?[^"]*)?"')

# 1. Update index.html
idx_path = Path('index.html')
t = idx_path.read_text(encoding='utf-8')
t = header_regex.sub(INDEX_HEADER, t, count=1)
t = css_root_regex.sub(f'href="styles.css?v={VERSION}"', t)
idx_path.write_text(t, encoding='utf-8')
print("[OK] index.html updated")

# 2. Update other root files
root_files = ['comparador.html', 'ofertas.html', 'aviso-afiliados.html', 'privacidad.html', 'sobre-nosotros.html']
for fn in root_files:
    fp = Path(fn)
    if fp.exists():
        t = fp.read_text(encoding='utf-8')
        t = header_regex.sub(ROOT_HEADER, t, count=1)
        t = css_root_regex.sub(f'href="styles.css?v={VERSION}"', t)
        fp.write_text(t, encoding='utf-8')
        print(f"[OK] {fn} updated")

# Mobile nav script for subfolder pages
SUB_MOBILE_SCRIPT = '''<script>
document.addEventListener("DOMContentLoaded", function () {
  var btn = document.getElementById("mobileMenuBtn");
  var nav = document.getElementById("mainNav");
  if (btn && nav) {
    btn.addEventListener("click", function () {
      btn.classList.toggle("open");
      nav.classList.toggle("open");
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
        document.body.style.overflow = "";
      });
    });
  }
});
</script>'''

# 3. Update guias
for fp in Path('guias').glob('*.html'):
    t = fp.read_text(encoding='utf-8')
    t = header_regex.sub(SUB_HEADER, t, count=1)
    t = css_sub_regex.sub(f'href="../styles.css?v={VERSION}"', t)
    # Ensure mobile menu script is present
    if 'mobileMenuBtn' not in t or 'initMobileMenu' not in t:
        if '</body>' in t and 'nav-item-dropdown' not in t:
            t = t.replace('</body>', f'{SUB_MOBILE_SCRIPT}\n</body>')
    fp.write_text(t, encoding='utf-8')
    print(f"[OK] {fp} updated")

# 4. Update producto
for fp in Path('producto').glob('*.html'):
    t = fp.read_text(encoding='utf-8')
    t = header_regex.sub(SUB_HEADER, t, count=1)
    t = css_sub_regex.sub(f'href="../styles.css?v={VERSION}"', t)
    fp.write_text(t, encoding='utf-8')

print(f"[OK] 50 product pages updated with SUB_HEADER and v={VERSION}")
