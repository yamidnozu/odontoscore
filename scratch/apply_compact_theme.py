import re

def update_styles():
    with open('styles.css', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update :root tokens
    old_root = re.search(r':root\s*\{[^}]+\}', content, re.DOTALL)
    if not old_root:
        print("ERROR: :root not found")
        return

    new_root = """:root {
  --color-bg: #F8FAFC;
  --color-surface: #F1F5F9;
  --color-surface-hover: #E2E8F0;
  --color-surface-card: #FFFFFF;
  --color-primary: #0284C7;
  --color-primary-dark: #0369A1;
  --color-primary-light: #F0F9FF;
  --color-primary-glow: rgba(2, 132, 199, 0.12);
  --color-navy: #0F172A;
  --color-slate-dark: #1E293B;
  --color-slate: #334155;
  --color-slate-light: #64748B;
  --color-muted: #94A3B8;
  --color-border: #E2E8F0;
  --color-border-subtle: #F1F5F9;
  --color-border-focus: var(--color-primary);
  --color-success: #059669;
  --color-success-bg: #ECFDF5;
  --color-danger: #E11D48;
  --color-danger-bg: #FFF1F2;
  --color-accent: #0284C7;
  --color-warm: #D97706;

  --font-sans: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-display: 'Inter', system-ui, sans-serif;

  --shadow-xs: 0 1px 2px rgba(15, 23, 42, 0.04);
  --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.05), 0 1px 2px rgba(15, 23, 42, 0.03);
  --shadow-md: 0 4px 12px -2px rgba(15, 23, 42, 0.07), 0 2px 4px rgba(15, 23, 42, 0.02);
  --shadow-lg: 0 10px 24px -4px rgba(15, 23, 42, 0.08);
  --shadow-xl: 0 16px 36px -6px rgba(15, 23, 42, 0.12);

  --radius-xs: 3px;
  --radius-sm: 5px;
  --radius-md: 7px;
  --radius-lg: 9px;
  --radius-xl: 12px;
  --radius-2xl: 14px;
  --radius-full: 9999px;

  --container-max: 1360px;
  --header-height: 52px;
  --transition-smooth: cubic-bezier(0.22, 1, 0.36, 1);
}"""
    content = content.replace(old_root.group(0), new_root)

    # 2. Container
    content = re.sub(
        r'\.container\s*\{[^}]+\}',
        """.container {
  width: 100%;
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 1.25rem;
}""",
        content
    )

    # 3. Brand Logo
    content = re.sub(
        r'\.brand-logo img\s*\{[^}]+\}',
        '.brand-logo img { height: 28px; width: auto; }',
        content
    )

    # 4. Nav Links
    content = re.sub(
        r'\.nav-links\s*\{[^}]+\}',
        """.nav-links {
  display: flex;
  list-style: none;
  gap: 0.15rem;
  align-items: center;
}""",
        content
    )

    content = re.sub(
        r'\.nav-links a\s*\{[^}]+\}',
        """.nav-links a {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--color-slate);
  padding: 0.35rem 0.65rem;
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;
  position: relative;
}""",
        content
    )

    # 5. Nav Link Dropdown
    content = re.sub(
        r'\.nav-link-dropdown\s*\{[^}]+\}',
        """.nav-link-dropdown {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--color-slate);
  padding: 0.35rem 0.65rem;
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;
  cursor: pointer;
  text-decoration: none;
}""",
        content
    )

    # 6. Nav Dropdown Menu
    content = re.sub(
        r'\.nav-dropdown-menu\s*\{[^}]+\}',
        """.nav-dropdown-menu {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 235px;
  background: #FFFFFF;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  padding: 0.3rem;
  flex-direction: column;
  gap: 0.15rem;
  z-index: 1000;
}""",
        content
    )

    # 7. Hero Section
    content = re.sub(
        r'\.hero-section\s*\{[^}]+\}',
        """.hero-section {
  padding: 2.25rem 0 2rem;
  background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
  border-bottom: 1px solid var(--color-border);
  position: relative;
  overflow: hidden;
}""",
        content
    )

    content = re.sub(
        r'\.hero-grid\s*\{[^}]+\}',
        """.hero-grid {
  display: grid;
  grid-template-columns: 1.4fr 0.6fr;
  gap: 2.5rem;
  align-items: center;
}""",
        content
    )

    content = re.sub(
        r'\.hero-badge\s*\{[^}]+\}',
        """.hero-badge {
  display: inline-flex;
  align-items: center;
  background: #FFFFFF;
  border: 1px solid var(--color-border);
  color: var(--color-slate-dark);
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 0.2rem 0.65rem;
  border-radius: var(--radius-full);
  margin-bottom: 0.75rem;
  box-shadow: var(--shadow-xs);
}""",
        content
    )

    content = re.sub(
        r'\.hero-title\s*\{[^}]+\}',
        """.hero-title {
  font-size: clamp(1.75rem, 2.8vw, 2.35rem);
  line-height: 1.15;
  margin-bottom: 0.75rem;
  color: var(--color-navy);
  letter-spacing: -0.03em;
  animation: fadeSlideUp 0.5s var(--transition-smooth) both;
}""",
        content
    )

    content = re.sub(
        r'\.hero-subtitle\s*\{[^}]+\}',
        """.hero-subtitle {
  font-size: 0.92rem;
  color: var(--color-slate-light);
  line-height: 1.55;
  margin-bottom: 1.25rem;
  max-width: 580px;
  animation: fadeSlideUp 0.5s 0.08s var(--transition-smooth) both;
}""",
        content
    )

    content = re.sub(
        r'\.hero-actions\s*\{[^}]+\}',
        """.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.65rem;
  margin-bottom: 1.25rem;
  animation: fadeSlideUp 0.5s 0.15s var(--transition-smooth) both;
}""",
        content
    )

    content = re.sub(
        r'\.btn-primary\s*\{[^}]+\}',
        """.btn-primary {
  background: var(--color-primary);
  color: #FFFFFF !important;
  font-weight: 600;
  font-size: 0.85rem;
  padding: 0.55rem 1.25rem;
  border-radius: var(--radius-sm);
  box-shadow: 0 2px 8px var(--color-primary-glow);
  transition: all 0.2s var(--transition-smooth);
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}""",
        content
    )

    content = re.sub(
        r'\.btn-secondary\s*\{[^}]+\}',
        """.btn-secondary {
  background: #FFFFFF;
  color: var(--color-navy) !important;
  border: 1px solid var(--color-border);
  font-weight: 600;
  font-size: 0.85rem;
  padding: 0.55rem 1.25rem;
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}""",
        content
    )

    content = re.sub(
        r'\.hero-trust-bullets\s*\{[^}]+\}',
        """.hero-trust-bullets {
  display: flex;
  flex-wrap: wrap;
  gap: 1.25rem;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--color-slate);
  animation: fadeSlideUp 0.5s 0.2s var(--transition-smooth) both;
}""",
        content
    )

    content = re.sub(
        r'\.hero-visual img\s*\{[^}]+\}',
        """.hero-visual img {
  max-height: 190px;
  width: auto;
}""",
        content
    )

    # 8. Section Blocks
    content = re.sub(
        r'\.section-block\s*\{[^}]+\}',
        """.section-block {
  padding: 2.25rem 0;
}""",
        content
    )

    content = re.sub(
        r'\.section-header\s*\{[^}]+\}',
        """.section-header {
  text-align: center;
  max-width: 640px;
  margin: 0 auto 1.5rem;
}""",
        content
    )

    content = re.sub(
        r'\.section-title\s*\{[^}]+\}',
        """.section-title {
  font-size: 1.55rem;
  margin-bottom: 0.45rem;
}""",
        content
    )

    content = re.sub(
        r'\.section-desc\s*\{[^}]+\}',
        """.section-desc {
  font-size: 0.88rem;
  color: var(--color-slate-light);
  line-height: 1.5;
}""",
        content
    )

    # 9. Catalog Toolbar
    content = re.sub(
        r'\.catalog-toolbar-wrapper\s*\{[^}]+\}',
        """.catalog-toolbar-wrapper {
  background: #FFFFFF;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 0.75rem 1rem;
  box-shadow: var(--shadow-xs);
  margin-bottom: 1.25rem;
}""",
        content
    )

    content = re.sub(
        r'\.catalog-search-row\s*\{[^}]+\}',
        """.catalog-search-row {
  display: flex;
  gap: 0.65rem;
  margin-bottom: 0.65rem;
  align-items: center;
}""",
        content
    )

    content = re.sub(
        r'\.search-input-field\s*\{[^}]+\}',
        """.search-input-field {
  width: 100%;
  padding: 0.4rem 0.85rem 0.4rem 2.2rem;
  font-size: 0.84rem;
  font-family: var(--font-sans);
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-bg);
  color: var(--color-navy);
  transition: all 0.2s ease;
  height: 36px;
}""",
        content
    )

    content = re.sub(
        r'\.catalog-sort-select\s*\{[^}]+\}',
        """.catalog-sort-select {
  padding: 0.4rem 0.85rem;
  font-size: 0.82rem;
  font-family: var(--font-sans);
  font-weight: 600;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-bg);
  color: var(--color-navy);
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 190px;
  height: 36px;
}""",
        content
    )

    content = re.sub(
        r'\.filter-pill-btn\s*\{[^}]+\}',
        """.filter-pill-btn {
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  color: var(--color-slate);
  font-size: 0.76rem;
  font-weight: 600;
  padding: 0.3rem 0.65rem;
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}""",
        content
    )

    # 10. Product Grid & Cards
    content = re.sub(
        r'\.product-grid\s*\{[^}]+\}',
        """.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1.1rem;
}""",
        content
    )

    content = re.sub(
        r'\.product-card\s*\{[^}]+\}',
        """.product-card {
  background: #FFFFFF;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-xs);
  display: flex;
  flex-direction: column;
  transition: all 0.25s var(--transition-smooth);
  position: relative;
}""",
        content
    )

    content = re.sub(
        r'\.card-media\s*\{[^}]+\}',
        """.card-media {
  height: 165px;
  background: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem;
  position: relative;
}""",
        content
    )

    content = re.sub(
        r'\.card-thumbs-strip\s*\{[^}]+\}',
        """.card-thumbs-strip {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.35rem 0.55rem;
  background: var(--color-bg);
  border-top: 1px solid var(--color-border-subtle);
  overflow-x: auto;
  scrollbar-width: thin;
}""",
        content
    )

    content = re.sub(
        r'\.card-thumb-mini\s*\{[^}]+\}',
        """.card-thumb-mini {
  width: 32px;
  height: 32px;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  background: #FFFFFF;
  padding: 2px;
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.15s ease;
  position: relative;
}""",
        content
    )

    content = re.sub(
        r'\.card-body\s*\{[^}]+\}',
        """.card-body {
  padding: 0.85rem 0.95rem 1rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}""",
        content
    )

    content = re.sub(
        r'\.card-title\s*\{[^}]+\}',
        """.card-title {
  font-size: 0.9rem;
  font-weight: 600;
  line-height: 1.35;
  margin-bottom: 0.4rem;
  color: var(--color-navy);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 2.45em;
}""",
        content
    )

    content = re.sub(
        r'\.card-specs-matrix\s*\{[^}]+\}',
        """.card-specs-matrix {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.25rem;
  background: var(--color-bg);
  padding: 0.45rem 0.65rem;
  border-radius: var(--radius-sm);
  margin-bottom: 0.65rem;
  font-size: 0.74rem;
  border: 1px solid var(--color-border-subtle);
}""",
        content
    )

    content = re.sub(
        r'\.card-price-row\s*\{[^}]+\}',
        """.card-price-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-top: auto;
  padding-top: 0.5rem;
  border-top: 1px solid var(--color-border-subtle);
  margin-bottom: 0.65rem;
}""",
        content
    )

    content = re.sub(
        r'\.price-main-val\s*\{[^}]+\}',
        """.price-main-val {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--color-navy);
  font-family: var(--font-display);
}""",
        content
    )

    content = re.sub(
        r'\.card-actions-grid\s*\{[^}]+\}',
        """.card-actions-grid {
  display: grid;
  grid-template-columns: 1fr 1.15fr;
  gap: 0.4rem;
}""",
        content
    )

    content = re.sub(
        r'\.btn-card-quick\s*\{[^}]+\}',
        """.btn-card-quick {
  background: var(--color-bg);
  color: var(--color-navy);
  font-weight: 600;
  font-size: 0.78rem;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 0.45rem 0.6rem;
  cursor: pointer;
  font-family: var(--font-sans);
  transition: all 0.2s ease;
  text-align: center;
}""",
        content
    )

    content = re.sub(
        r'\.btn-card-prime\s*\{[^}]+\}',
        """.btn-card-prime {
  background: var(--color-navy);
  color: #FFFFFF !important;
  font-weight: 600;
  font-size: 0.78rem;
  border-radius: var(--radius-sm);
  padding: 0.45rem 0.6rem;
  text-align: center;
  transition: all 0.2s ease;
}""",
        content
    )

    # 11. Modal Video Badge emoji removal!
    content = content.replace('content: "🎬";', 'content: "▶"; font-size: 0.75rem; color: #38BDF8;')

    # 12. Quick Modal
    content = re.sub(
        r'\.quick-modal\s*\{[^}]+\}',
        """.quick-modal {
  background: #FFFFFF;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  max-width: 920px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  padding: 1.5rem 1.75rem;
  position: relative;
  box-shadow: var(--shadow-xl);
}""",
        content
    )

    content = re.sub(
        r'\.modal-gallery-main\s*\{[^}]+\}',
        """.modal-gallery-main {
  background: #FFFFFF;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 1rem;
  text-align: center;
  margin-bottom: 0.65rem;
  height: 240px;
  display: flex;
  align-items: center;
  justify-content: center;
}""",
        content
    )

    content = re.sub(
        r'\.modal-thumb-btn\s*\{[^}]+\}',
        """.modal-thumb-btn {
  width: 44px; height: 44px;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-xs);
  background: #FFFFFF;
  padding: 2px;
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.15s;
}""",
        content
    )

    content = re.sub(
        r'\.btn-buy-amazon-large\s*\{[^}]+\}',
        """.btn-buy-amazon-large {
  background: var(--color-navy);
  color: #FFFFFF !important;
  font-weight: 700;
  font-size: 0.88rem;
  padding: 0.65rem 1.25rem;
  border-radius: var(--radius-sm);
  text-align: center;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}""",
        content
    )

    # 13. Skeleton Card
    content = re.sub(
        r'\.skeleton-card\s*\{[^}]+\}',
        """.skeleton-card {
  background: #FFFFFF;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
  min-height: 380px;
  position: relative;
}""",
        content
    )

    content = re.sub(
        r'\.skeleton-card::before\s*\{[^}]+\}',
        """.skeleton-card::before {
  content: "";
  display: block;
  height: 165px;
  background: linear-gradient(110deg, var(--color-surface) 30%, #E8EDF2 50%, var(--color-surface) 70%);
  background-size: 300% 100%;
  animation: shimmer 1.8s infinite linear;
}""",
        content
    )

    # 14. Academia Home
    content = re.sub(
        r'\.academy-featured-card\s*\{[^}]+\}',
        """.academy-featured-card {
  display: grid;
  grid-template-columns: 1.3fr 0.7fr;
  gap: 1.75rem;
  background: linear-gradient(135deg, #0B1426 0%, #17253D 100%);
  color: #FFFFFF;
  padding: 1.75rem 2rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  margin-bottom: 1.5rem;
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
}""",
        content
    )

    content = re.sub(
        r'\.academy-featured-title\s*\{[^}]+\}',
        """.academy-featured-title {
  font-size: 1.55rem;
  color: #FFFFFF;
  line-height: 1.2;
  margin-bottom: 0.65rem;
}""",
        content
    )

    content = re.sub(
        r'\.academy-featured-desc\s*\{[^}]+\}',
        """.academy-featured-desc {
  font-size: 0.88rem;
  color: #CBD5E1;
  line-height: 1.5;
  margin-bottom: 1.15rem;
}""",
        content
    )

    content = re.sub(
        r'\.academy-featured-bullets\s*\{[^}]+\}',
        """.academy-featured-bullets {
  list-style: none;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.45rem;
  margin-bottom: 1.25rem;
}""",
        content
    )

    content = re.sub(
        r'\.btn-academy-primary\s*\{[^}]+\}',
        """.btn-academy-primary {
  display: inline-flex;
  align-items: center;
  gap: 0.65rem;
  background: var(--color-primary);
  color: #FFFFFF !important;
  font-weight: 700;
  font-size: 0.85rem;
  padding: 0.6rem 1.35rem;
  border-radius: var(--radius-sm);
  box-shadow: 0 3px 12px rgba(2, 132, 199, 0.35);
  transition: all 0.2s ease;
}""",
        content
    )

    content = re.sub(
        r'\.academy-subgrid\s*\{[^}]+\}',
        """.academy-subgrid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
}""",
        content
    )

    content = re.sub(
        r'\.academy-subcard\s*\{[^}]+\}',
        """.academy-subcard {
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 1.15rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: all 0.2s ease;
}""",
        content
    )

    content = re.sub(
        r'\.academy-subcard h4\s*\{[^}]+\}',
        """.academy-subcard h4 {
  font-size: 1.05rem;
  margin: 0.35rem 0;
  color: var(--color-navy);
}""",
        content
    )

    content = re.sub(
        r'\.academy-subcard p\s*\{[^}]+\}',
        """.academy-subcard p {
  font-size: 0.82rem;
  color: var(--color-slate);
  line-height: 1.45;
  margin-bottom: 0.85rem;
}""",
        content
    )

    # 15. Site Footer
    content = re.sub(
        r'\.site-footer\s*\{[^}]+\}',
        """.site-footer {
  background: var(--color-navy);
  color: var(--color-muted);
  padding: 2.5rem 0 1.5rem;
  border-top: 1px solid #1E293B;
  font-size: 0.84rem;
}""",
        content
    )

    content = re.sub(
        r'\.footer-grid\s*\{[^}]+\}',
        """.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 2rem;
  margin-bottom: 1.75rem;
}""",
        content
    )

    # 16. Append global compact overrides if not already appended
    global_overrides = """
/* ==========================================================================
   GLOBAL PRODUCT DETAIL (FICHA TÉCNICA) COMPACT OVERRIDES
   ========================================================================== */
.ficha-layout,
.product-detail-container,
.product-page-container {
  max-width: 1200px !important;
  margin: 0 auto !important;
  padding: 1.25rem 1rem !important;
}

.ficha-hero-grid,
.product-hero-grid {
  display: grid !important;
  grid-template-columns: 1fr 1.15fr !important;
  gap: 1.5rem !important;
  align-items: start !important;
  margin-bottom: 1.5rem !important;
}

.ficha-gallery-wrapper > div:first-child,
.main-image-container,
.gallery-featured {
  height: 270px !important;
  max-height: 270px !important;
  padding: 0.75rem !important;
  background: #FFFFFF !important;
  border-radius: var(--radius-md) !important;
  border: 1px solid var(--color-border) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.ficha-gallery-wrapper img,
.main-image-container img,
.gallery-featured img {
  max-height: 100% !important;
  max-width: 100% !important;
  object-fit: contain !important;
}

.ficha-title,
.product-title {
  font-size: 1.35rem !important;
  line-height: 1.25 !important;
  margin-bottom: 0.45rem !important;
}

.ficha-spec-table,
.product-specs-table,
.specs-table {
  font-size: 0.82rem !important;
}

.ficha-spec-table td,
.ficha-spec-table th,
.product-specs-table td,
.product-specs-table th {
  padding: 0.45rem 0.65rem !important;
}

/* ==========================================================================
   ACADEMIA & ATLAS 360 COMPACT OVERRIDES
   ========================================================================== */
.atlas-master-box {
  border-radius: var(--radius-lg) !important;
  margin: 1.25rem 0 !important;
}

.mode-nav-tabs {
  padding: 0.35rem 0.75rem 0 !important;
  gap: 0.35rem !important;
}

.mode-tab-btn {
  padding: 0.55rem 0.95rem !important;
  font-size: 0.84rem !important;
  border-radius: var(--radius-sm) var(--radius-sm) 0 0 !important;
}

.atlas-content-grid {
  gap: 1.25rem !important;
  padding: 1.25rem !important;
}

.step-viewport {
  max-height: 380px !important;
  border-radius: var(--radius-md) !important;
}

.step-hud {
  top: 0.6rem !important;
  left: 0.6rem !important;
  right: 0.6rem !important;
}

.hud-chip {
  padding: 0.2rem 0.55rem !important;
  font-size: 0.72rem !important;
  border-radius: var(--radius-full) !important;
}

.step-panel-title {
  font-size: 1.15rem !important;
  margin-bottom: 0.35rem !important;
}

.step-panel-desc {
  font-size: 0.84rem !important;
  line-height: 1.45 !important;
  margin-bottom: 0.65rem !important;
}

.angle-chips-row {
  gap: 0.3rem !important;
  margin-bottom: 0.65rem !important;
}

.angle-chip-btn {
  padding: 0.2rem 0.5rem !important;
  font-size: 0.74rem !important;
  border-radius: var(--radius-sm) !important;
}

.turntable-scrubber-bar {
  height: 6px !important;
}

.turntable-handle {
  width: 16px !important;
  height: 16px !important;
}

.layers-table,
.atlas-table,
.anatomical-table {
  font-size: 0.82rem !important;
}

.layers-table th,
.layers-table td,
.atlas-table th,
.atlas-table td,
.anatomical-table th,
.anatomical-table td {
  padding: 0.45rem 0.65rem !important;
}
"""
    if "GLOBAL PRODUCT DETAIL (FICHA TÉCNICA) COMPACT OVERRIDES" not in content:
        content += "\n" + global_overrides

    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(content)

    print("styles.css successfully updated with compact styling!")

if __name__ == '__main__':
    update_styles()
