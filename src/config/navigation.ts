export interface NavLink {
  label: string;
  href: string;
  badge?: string;
  highlight?: boolean;
  isDivider?: boolean;
}

export interface NavMenuItem {
  label: string;
  href: string;
  navKey?: string;
  children?: NavLink[];
  viewAll?: {
    label: string;
    href: string;
  };
}

export interface FooterColumn {
  title: string;
  links: Array<{
    label: string;
    href: string;
    highlight?: boolean;
    color?: string;
  }>;
}

/**
 * Configuración centralizada de navegación de OdontoScore.
 * Edita este archivo para agregar, quitar o modificar enlaces del menú superior y del pie de página.
 */
export const mainNavigation: NavMenuItem[] = [
  {
    label: 'Catálogo',
    href: '/#catalogo',
    navKey: 'catalogo'
  },
  {
    label: 'Estudiantes',
    href: '/#estudiantes',
    navKey: 'estudiantes'
  },
  {
    label: 'Academia',
    href: '/#academia',
    navKey: 'academia',
    children: [
      {
        label: 'Atlas Anatómico Dental 360°',
        href: '/guias/anatomia-dental-3d-por-capas.html'
      },
      {
        label: 'Biofilm y Endodoncia 3D',
        href: '/guias/biofilm-microbiologia-endodoncia-3d.html'
      },
      {
        label: 'Semiología y Pares Craneales',
        href: '/guias/semiologia-pares-craneales-odontologia.html'
      },
      {
        label: 'Farmacología & Calculadora Pediátrica',
        href: '/guias/farmacologia-dolor-trigeminal-inflamacion-pediatrica.html'
      },
      {
        label: 'Longitud de Trabajo en Endodoncia',
        href: '/guias/longitud-trabajo-endodoncia.html',
        highlight: true
      },
      {
        label: 'Simulador 3D de Endodoncia',
        href: '/guias/simulador-endodoncia-3d.html',
        highlight: true
      },
      {
        label: 'Calculadora Visual de Dosis',
        href: '/calculadora-dosis-pediatrica/',
        highlight: true
      },
      {
        label: 'Guía: Encías Sensibles',
        href: '/guias/mejor-cepillo-electrico-encias-sensibles-2026.html'
      },
      {
        label: 'Guía: Higiene en Ortodoncia',
        href: '/guias/mejor-irrigador-dental-brackets-2026.html'
      }
    ],
    viewAll: {
      label: 'Ver toda la Academia →',
      href: '/#academia'
    }
  },
  {
    label: 'Comparador',
    href: '/comparador.html',
    navKey: 'comparador'
  },
  {
    label: 'Ofertas',
    href: '/ofertas.html',
    navKey: 'ofertas'
  },
  {
    label: 'FAQ',
    href: '/#faq',
    navKey: 'faq'
  }
];

export const footerNavigation: FooterColumn[] = [
  {
    title: 'Especialidades',
    links: [
      { label: 'Estudiantes y Prácticas', href: '/categoria/estudiantes-odontologia.html' },
      { label: 'Cepillos Eléctricos', href: '/categoria/cepillos-electricos.html' },
      { label: 'Irrigadores Dentales', href: '/categoria/irrigadores-dentales.html' },
      { label: 'Blanqueamiento Dental', href: '/categoria/blanqueamiento-dental.html' },
      { label: 'Ortodoncia y Brackets', href: '/categoria/ortodoncia-brackets.html' },
      { label: 'Instrumental Clínico', href: '/categoria/instrumental-basico.html' }
    ]
  },
  {
    title: 'Herramientas & Academia',
    links: [
      { label: 'Longitud de Trabajo Endo', href: '/guias/longitud-trabajo-endodoncia.html', highlight: true, color: '#0066FF' },
      { label: 'Simulador 3D Endodoncia', href: '/guias/simulador-endodoncia-3d.html', highlight: true, color: '#0066FF' },
      { label: 'Atlas Anatómico Dental 360°', href: '/guias/anatomia-dental-3d-por-capas.html' },
      { label: 'Biofilm y Endodoncia 3D', href: '/guias/biofilm-microbiologia-endodoncia-3d.html' },
      { label: 'Semiología Pares Craneales', href: '/guias/semiologia-pares-craneales-odontologia.html', highlight: true },
      { label: 'Farmacología & Calculadora', href: '/guias/farmacologia-dolor-trigeminal-inflamacion-pediatrica.html', highlight: true },
      { label: 'Tutor Visual de Dosis Pediátrica', href: '/calculadora-dosis-pediatrica/', color: '#0284C7', highlight: true },
      { label: 'Comparador de 7 Ejes', href: '/comparador.html' },
      { label: 'Ofertas y Descuentos', href: '/ofertas.html' },
      { label: 'Guía Irrigadores', href: '/guias/mejor-irrigador-dental-brackets-2026.html' },
      { label: 'Guía Encías Sensibles', href: '/guias/mejor-cepillo-electrico-encias-sensibles-2026.html' }
    ]
  },
  {
    title: 'Transparencia',
    links: [
      { label: 'Aviso de Afiliación', href: '/aviso-afiliados.html' },
      { label: 'Privacidad y Cookies', href: '/privacidad.html' },
      { label: 'Metodología OdontoScore', href: '/sobre-nosotros.html' }
    ]
  }
];
