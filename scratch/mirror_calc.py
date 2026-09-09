with open('src/pages/calculadora-dosis-pediatrica/index.astro', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('canonicalUrl = "https://odontoscore.com/calculadora-dosis-pediatrica/";', 'canonicalUrl = "https://odontoscore.com/guias/calculadora-dosis-pediatrica-visual.html";')

with open('src/pages/guias/calculadora-dosis-pediatrica-visual.astro', 'w', encoding='utf-8') as f:
    f.write(content)

print("Mirror complete!")
