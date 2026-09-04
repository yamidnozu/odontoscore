import re
from pathlib import Path

prod_header_dropdown = '''      <ul class="nav-links">
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

old_ul = re.compile(r'<ul class="nav-links">.*?</ul>', re.DOTALL)
count = 0
for f in Path('producto').glob('*.html'):
    t = f.read_text(encoding='utf-8')
    if old_ul.search(t):
        t = old_ul.sub(prod_header_dropdown, t)
        f.write_text(t, encoding='utf-8')
        count += 1

print(f'Successfully updated {count} product pages with Academia dropdown!')
