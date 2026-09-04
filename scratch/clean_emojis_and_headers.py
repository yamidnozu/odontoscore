import os
import re
from pathlib import Path

# Common emoji regex
emoji_pattern = re.compile(
    r'[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50\u2b55]'
)

# 1. Update guias/anatomia-dental-3d-por-capas.html
anatomia_path = Path('guias/anatomia-dental-3d-por-capas.html')
if anatomia_path.exists():
    text = anatomia_path.read_text(encoding='utf-8')
    
    # Replace header
    old_header_pat = re.compile(r'<!-- Top Header -->\s*<header class="header">.*?</header>', re.DOTALL)
    new_header = '''<!-- Top Header -->
  <header class="site-header" id="siteHeader">
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
              <a href="../guias/anatomia-dental-3d-por-capas.html" class="dropdown-item">
                <div class="dropdown-item-title">
                  <span>Atlas Anatómico Dental 360°</span>
                  <span class="dropdown-item-badge">Activo</span>
                </div>
                <div class="dropdown-item-desc">Visor orbital en 8 planos, cortes sagitales y atlas histológico.</div>
              </a>
              <a href="../guias/semiologia-pares-craneales-odontologia.html" class="dropdown-item">
                <div class="dropdown-item-title">
                  <span>Semiología y Pares Craneales</span>
                  <span class="dropdown-item-badge">Clínico</span>
                </div>
                <div class="dropdown-item-desc">Neuroanatomía orofacial, 5 capas de disección y casos clínicos.</div>
              </a>
              <a href="../guias/mejor-cepillo-electrico-encias-sensibles-2026.html" class="dropdown-item">
                <div class="dropdown-item-title">
                  <span>Guía: Encías Sensibles</span>
                </div>
                <div class="dropdown-item-desc">Protocolos periodontales y control atraumático de placa.</div>
              </a>
              <a href="../guias/mejor-irrigador-dental-brackets-2026.html" class="dropdown-item">
                <div class="dropdown-item-title">
                  <span>Guía: Higiene en Ortodoncia</span>
                </div>
                <div class="dropdown-item-desc">Mantenimiento de aparatología e irrigación subgingival.</div>
              </a>
              <div class="dropdown-footer-link">
                <a href="../index.html#academia">Ver todo el catálogo de Academia →</a>
              </div>
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
    text = old_header_pat.sub(new_header, text)

    # Footer logo replacement
    footer_logo_pat = re.compile(r'<a href="\.\./index\.html" class="logo"[^>]*>.*?</a>', re.DOTALL)
    text = footer_logo_pat.sub('<a href="../index.html" class="brand-logo" style="margin-bottom:0.75rem;display:inline-flex;"><img src="../assets/img/logo-odontoscore.svg" alt="OdontoScore" height="34" style="filter: brightness(0) invert(1);"></a>', text)

    # Specific text cleanups
    text = text.replace('◀ Paso Anterior', 'Paso Anterior').replace('Paso Siguiente ▶', 'Paso Siguiente')
    text = text.replace('◀ Ángulo Anterior', 'Ángulo Anterior').replace('Ángulo Siguiente ▶', 'Ángulo Siguiente')
    text = text.replace('⏸ Pausar Rotación', 'Pausar Rotación').replace('▶ Rotación Continua 360°', 'Rotación Continua 360°')
    text = text.replace('🩻 Alternar Filtro Rayos X (Negativo)', 'Filtro Radiográfico Rayos X')
    text = text.replace('☀️ Modo Histológico Realista', 'Modo Histológico Realista')

    # Remove all emojis
    text = emoji_pattern.sub('', text)

    # Add mobileMenuBtn handler if not present
    if 'mobileMenuBtn' in text and 'mobileMenuBtn.addEventListener' not in text:
        text = text.replace('renderStep(0);', '''var mobileMenuBtn = document.getElementById("mobileMenuBtn");
    var mainNav = document.getElementById("mainNav");
    if (mobileMenuBtn && mainNav) {
      mobileMenuBtn.addEventListener("click", function() {
        mainNav.classList.toggle("open");
      });
    }
    renderStep(0);''')

    anatomia_path.write_text(text, encoding='utf-8')
    print("[OK] anatomia-dental-3d-por-capas.html updated and cleaned")


# 2. Update guias/semiologia-pares-craneales-odontologia.html
semiologia_path = Path('guias/semiologia-pares-craneales-odontologia.html')
if semiologia_path.exists():
    text = semiologia_path.read_text(encoding='utf-8')

    old_header_pat = re.compile(r'<header class="site-header">.*?</header>', re.DOTALL)
    new_header_semi = '''<header class="site-header" id="siteHeader">
  <div class="container nav-wrapper">
    <a href="../index.html" class="brand-logo" title="OdontoScore - Portal Odontológico">
      <img src="../assets/img/logo-odontoscore.svg" alt="OdontoScore Logo" height="38">
    </a>
    <button type="button" class="mobile-menu-toggle" id="mobileMenuBtn" aria-label="Menú">
      <span></span><span></span><span></span>
    </button>
    <nav class="main-nav" id="mainNav">
      <ul class="nav-links">
        <li><a href="../index.html#catalogo">Catálogo</a></li>
        <li><a href="../index.html#estudiantes">Estudiantes</a></li>
        <li class="nav-item-dropdown">
          <a href="../index.html#academia" class="nav-link-dropdown" aria-haspopup="true" aria-expanded="false" style="color:var(--color-primary);font-weight:700;">
            Academia
            <svg class="dropdown-arrow" width="10" height="6" viewBox="0 0 10 6" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M1 1L5 5L9 1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </a>
          <div class="nav-dropdown-menu">
            <a href="../guias/anatomia-dental-3d-por-capas.html" class="dropdown-item">
              <div class="dropdown-item-title">
                <span>Atlas Anatómico Dental 360°</span>
                <span class="dropdown-item-badge">Activo</span>
              </div>
              <div class="dropdown-item-desc">Visor orbital en 8 planos, cortes sagitales y atlas histológico.</div>
            </a>
            <a href="../guias/semiologia-pares-craneales-odontologia.html" class="dropdown-item">
              <div class="dropdown-item-title">
                <span>Semiología y Pares Craneales</span>
                <span class="dropdown-item-badge">Clínico</span>
              </div>
              <div class="dropdown-item-desc">Neuroanatomía orofacial, 5 capas de disección y casos clínicos.</div>
            </a>
            <a href="../guias/mejor-cepillo-electrico-encias-sensibles-2026.html" class="dropdown-item">
              <div class="dropdown-item-title">
                <span>Guía: Encías Sensibles</span>
              </div>
              <div class="dropdown-item-desc">Protocolos periodontales y control atraumático de placa.</div>
            </a>
            <a href="../guias/mejor-irrigador-dental-brackets-2026.html" class="dropdown-item">
              <div class="dropdown-item-title">
                <span>Guía: Higiene en Ortodoncia</span>
              </div>
              <div class="dropdown-item-desc">Mantenimiento de aparatología e irrigación subgingival.</div>
            </a>
            <div class="dropdown-footer-link">
              <a href="../index.html#academia">Ver todo el catálogo de Academia →</a>
            </div>
          </div>
        </li>
        <li><a href="../comparador.html">Comparador</a></li>
        <li><a href="../ofertas.html">Ofertas</a></li>
        <li><a href="../index.html#faq">FAQ</a></li>
      </ul>
      <div class="nav-actions">
        <a href="../index.html#catalogo" class="btn-nav-compare">
          <span>Instrumental Clínico</span>
        </a>
      </div>
    </nav>
  </div>
</header>'''
    text = old_header_pat.sub(new_header_semi, text)

    # Clean specific buttons/badges
    text = text.replace('➖ Eliminar Capa (Pelar)', 'Remover Capa').replace('➕ Reponer Capa', 'Restaurar Capa').replace('🔄 Todas (5)', 'Todas (5)')
    text = text.replace('🔬 Instrumental Clínico', 'Instrumental Clínico')
    text = text.replace('🧠 Academia Clínica OdontoScore', 'Academia Clínica OdontoScore')

    # Remove all emojis
    text = emoji_pattern.sub('', text)

    semiologia_path.write_text(text, encoding='utf-8')
    print("[OK] semiologia-pares-craneales-odontologia.html updated and cleaned")


# 3. Update comparador.html, ofertas.html, aviso-afiliados.html, privacidad.html, sobre-nosotros.html
root_header_dropdown = '''      <ul class="nav-links">
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
            <a href="guias/anatomia-dental-3d-por-capas.html" class="dropdown-item">
              <div class="dropdown-item-title">
                <span>Atlas Anatómico Dental 360°</span>
                <span class="dropdown-item-badge">Activo</span>
              </div>
              <div class="dropdown-item-desc">Visor orbital en 8 planos, cortes sagitales y atlas histológico.</div>
            </a>
            <a href="guias/semiologia-pares-craneales-odontologia.html" class="dropdown-item">
              <div class="dropdown-item-title">
                <span>Semiología y Pares Craneales</span>
                <span class="dropdown-item-badge">Clínico</span>
              </div>
              <div class="dropdown-item-desc">Neuroanatomía orofacial, 5 capas de disección y casos clínicos.</div>
            </a>
            <a href="guias/mejor-cepillo-electrico-encias-sensibles-2026.html" class="dropdown-item">
              <div class="dropdown-item-title">
                <span>Guía: Encías Sensibles</span>
              </div>
              <div class="dropdown-item-desc">Protocolos periodontales y control atraumático de placa.</div>
            </a>
            <a href="guias/mejor-irrigador-dental-brackets-2026.html" class="dropdown-item">
              <div class="dropdown-item-title">
                <span>Guía: Higiene en Ortodoncia</span>
              </div>
              <div class="dropdown-item-desc">Mantenimiento de aparatología e irrigación subgingival.</div>
            </a>
            <div class="dropdown-footer-link">
              <a href="index.html#academia">Ver todo el catálogo de Academia →</a>
            </div>
          </div>
        </li>
        <li><a href="comparador.html">Comparador</a></li>
        <li><a href="ofertas.html">Ofertas</a></li>
        <li><a href="index.html#faq">FAQ</a></li>
      </ul>'''

for fname in ['comparador.html', 'ofertas.html', 'aviso-afiliados.html', 'privacidad.html', 'sobre-nosotros.html']:
    fpath = Path(fname)
    if fpath.exists():
        t = fpath.read_text(encoding='utf-8')
        # Replace nav-links
        old_ul = re.compile(r'<ul class="nav-links">.*?</ul>', re.DOTALL)
        t = old_ul.sub(root_header_dropdown, t)
        # Remove emojis like ⚡
        t = t.replace('⚡ Comparar', 'Comparar').replace('⚡', '')
        # Clean any remaining emojis
        t = emoji_pattern.sub('', t)
        fpath.write_text(t, encoding='utf-8')
        print(f"[OK] {fname} updated")

# 4. Update other guides in guias/
sub_header_dropdown = '''      <ul class="nav-links">
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
            <a href="../guias/anatomia-dental-3d-por-capas.html" class="dropdown-item">
              <div class="dropdown-item-title">
                <span>Atlas Anatómico Dental 360°</span>
                <span class="dropdown-item-badge">Activo</span>
              </div>
              <div class="dropdown-item-desc">Visor orbital en 8 planos, cortes sagitales y atlas histológico.</div>
            </a>
            <a href="../guias/semiologia-pares-craneales-odontologia.html" class="dropdown-item">
              <div class="dropdown-item-title">
                <span>Semiología y Pares Craneales</span>
                <span class="dropdown-item-badge">Clínico</span>
              </div>
              <div class="dropdown-item-desc">Neuroanatomía orofacial, 5 capas de disección y casos clínicos.</div>
            </a>
            <a href="../guias/mejor-cepillo-electrico-encias-sensibles-2026.html" class="dropdown-item">
              <div class="dropdown-item-title">
                <span>Guía: Encías Sensibles</span>
              </div>
              <div class="dropdown-item-desc">Protocolos periodontales y control atraumático de placa.</div>
            </a>
            <a href="../guias/mejor-irrigador-dental-brackets-2026.html" class="dropdown-item">
              <div class="dropdown-item-title">
                <span>Guía: Higiene en Ortodoncia</span>
              </div>
              <div class="dropdown-item-desc">Mantenimiento de aparatología e irrigación subgingival.</div>
            </a>
            <div class="dropdown-footer-link">
              <a href="../index.html#academia">Ver todo el catálogo de Academia →</a>
            </div>
          </div>
        </li>
        <li><a href="../comparador.html">Comparador</a></li>
        <li><a href="../ofertas.html">Ofertas</a></li>
        <li><a href="../index.html#faq">FAQ</a></li>
      </ul>'''

for fname in ['guias/mejor-cepillo-electrico-encias-sensibles-2026.html', 'guias/mejor-irrigador-dental-brackets-2026.html']:
    fpath = Path(fname)
    if fpath.exists():
        t = fpath.read_text(encoding='utf-8')
        old_ul = re.compile(r'<ul class="nav-links">.*?</ul>', re.DOTALL)
        t = old_ul.sub(sub_header_dropdown, t)
        t = t.replace('⚡ Comparar', 'Comparar').replace('📖', '').replace('⚡', '')
        t = emoji_pattern.sub('', t)
        fpath.write_text(t, encoding='utf-8')
        print(f"[OK] {fname} updated")

print("\nALL FILES SUCCESSFULLY UPDATED WITH DROPDOWN AND ZERO EMOJIS!")
