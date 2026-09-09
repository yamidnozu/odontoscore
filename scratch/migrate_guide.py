import re
import os
import json

def migrate_html_to_astro(html_path, astro_path, canonical_url):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Title
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1).strip() if title_match else "OdontoScore Guía Clínica"

    # 2. Description
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE | re.DOTALL)
    desc = desc_match.group(1).strip() if desc_match else ""

    # 3. JSON-LD scripts
    json_lds = []
    for m in re.finditer(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', content, re.IGNORECASE | re.DOTALL):
        raw_json = m.group(1).strip()
        try:
            parsed = json.loads(raw_json)
            json_lds.append(parsed)
        except Exception as e:
            print(f"Error parsing JSON-LD in {html_path}: {e}")

    # 4. Extract styles inside <head>
    styles = []
    # Match <style> tags
    for m in re.finditer(r'<style\b[^>]*>(.*?)</style>', content, re.IGNORECASE | re.DOTALL):
        styles.append(m.group(1).strip())
    combined_styles = "\n\n".join(styles)

    # 5. Extract <main>...</main> or body content between header and footer
    # Remove header: <header ... id="siteHeader">...</header>
    # Also <footer ...>...</footer>
    body_match = re.search(r'<body\b[^>]*>(.*?)</body>', content, re.IGNORECASE | re.DOTALL)
    if body_match:
        body_content = body_match.group(1)
    else:
        body_content = content

    # Remove site header
    body_content = re.sub(r'<header\s+class=["\'](?:site-header|header)["\'][^>]*>.*?</header>', '', body_content, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove site footer
    body_content = re.sub(r'<footer\s+class=["\'](?:site-footer|footer)["\'][^>]*>.*?</footer>', '', body_content, flags=re.IGNORECASE | re.DOTALL)

    # Extract scripts at the end of body
    scripts = []
    # Find all <script ...>...</script> inside remaining body_content
    # Note: external scripts like <script src="..."></script> vs inline scripts
    ext_scripts = []
    def script_repl(m):
        full_tag = m.group(0)
        src_match = re.search(r'src=["\'](.*?)["\']', full_tag)
        if src_match:
            src = src_match.group(1)
            # ignore manifest.js, db.js, main.js if already in BaseLayout
            if any(x in src for x in ['manifest.js', 'main.js', 'adsbygoogle.js']):
                return ''
            ext_scripts.append(src)
            return ''
        else:
            inner_script = m.group(1)
            scripts.append(inner_script)
            return ''

    cleaned_body = re.sub(r'<script\b[^>]*>(.*?)</script>', script_repl, body_content, flags=re.IGNORECASE | re.DOTALL)

    # Replace <main with <div and </main> with </div> to avoid duplicate <main> tags (BaseLayout already has <main id="mainContent">)
    cleaned_body = re.sub(r'<main\b', '<div', cleaned_body, flags=re.IGNORECASE)
    cleaned_body = re.sub(r'</main>', '</div>', cleaned_body, flags=re.IGNORECASE)

    # Clean relative URLs
    cleaned_body = cleaned_body.replace('../assets/', '/assets/')
    cleaned_body = cleaned_body.replace('../index.html', '/')
    cleaned_body = cleaned_body.replace('../guias/', '/guias/')
    cleaned_body = cleaned_body.replace('../categoria/', '/categoria/')
    cleaned_body = cleaned_body.replace('../producto/', '/producto/')
    cleaned_body = cleaned_body.replace('../comparador.html', '/comparador.html')
    cleaned_body = cleaned_body.replace('../ofertas.html', '/ofertas.html')
    cleaned_body = cleaned_body.replace('../aviso-afiliados.html', '/aviso-afiliados.html')
    cleaned_body = cleaned_body.replace('../privacidad.html', '/privacidad.html')
    cleaned_body = cleaned_body.replace('../sobre-nosotros.html', '/sobre-nosotros.html')
    cleaned_body = cleaned_body.replace('../lib/', '/lib/')

    # External scripts clean url
    clean_ext_scripts = []
    for s in ext_scripts:
        s_clean = s.replace('../', '/')
        clean_ext_scripts.append(s_clean)

    # Format JSON-LD for Astro frontmatter
    json_ld_str = json.dumps(json_lds, indent=2, ensure_ascii=False) if json_lds else "null"

    # Assemble Astro file
    astro_content = f"""---
import BaseLayout from '../../layouts/BaseLayout.astro';

const pageTitle = {json.dumps(title, ensure_ascii=False)};
const pageDesc = {json.dumps(desc, ensure_ascii=False)};
const canonicalUrl = "{canonical_url}";
const jsonLd = {json_ld_str};
---

<BaseLayout
  title={{pageTitle}}
  description={{pageDesc}}
  canonicalUrl={{canonicalUrl}}
  jsonLd={{jsonLd}}
>
{cleaned_body.strip()}
</BaseLayout>

"""
    if clean_ext_scripts:
        for s in clean_ext_scripts:
            astro_content += f'<script is:inline src="{s}"></script>\n'

    if scripts:
        combined_inline_scripts = "\n\n".join(scripts)
        astro_content += f"""
<script is:inline>
{combined_inline_scripts}
</script>
"""

    if combined_styles:
        astro_content += f"""
<style is:global>
{combined_styles}
</style>
"""

    os.makedirs(os.path.dirname(astro_path), exist_ok=True)
    with open(astro_path, 'w', encoding='utf-8') as f:
        f.write(astro_content)

    print(f"Successfully generated {astro_path}")

if __name__ == '__main__':
    guides = [
        ("guias/semiologia-pares-craneales-odontologia.html", "src/pages/guias/semiologia-pares-craneales-odontologia.astro", "https://odontoscore.com/guias/semiologia-pares-craneales-odontologia.html"),
        ("guias/farmacologia-dolor-trigeminal-inflamacion-pediatrica.html", "src/pages/guias/farmacologia-dolor-trigeminal-inflamacion-pediatrica.astro", "https://odontoscore.com/guias/farmacologia-dolor-trigeminal-inflamacion-pediatrica.html"),
        ("guias/anatomia-dental-3d-por-capas.html", "src/pages/guias/anatomia-dental-3d-por-capas.astro", "https://odontoscore.com/guias/anatomia-dental-3d-por-capas.html"),
        ("guias/biofilm-microbiologia-endodoncia-3d.html", "src/pages/guias/biofilm-microbiologia-endodoncia-3d.astro", "https://odontoscore.com/guias/biofilm-microbiologia-endodoncia-3d.html"),
        ("guias/calculadora-dosis-pediatrica-visual.html", "src/pages/calculadora-dosis-pediatrica/index.astro", "https://odontoscore.com/calculadora-dosis-pediatrica/"),
        ("guias/calculadora-dosis-pediatrica-visual.html", "src/pages/guias/calculadora-dosis-pediatrica-visual.astro", "https://odontoscore.com/guias/calculadora-dosis-pediatrica-visual.html"),
    ]
    for src, dst, url in guides:
        migrate_html_to_astro(src, dst, url)
