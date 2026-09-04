import re

def clean_main_js():
    with open('main.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update CURRENCY_CONFIG without flag emojis
    currency_config_old = re.search(r'var CURRENCY_CONFIG = \{[^}]+\};', content, re.DOTALL)
    if currency_config_old:
        currency_config_new = """var CURRENCY_CONFIG = {
    EUR: { symbol: "€", name: "Euros (EUR)", position: "after", decimals: 2, flag: "EUR" },
    COP: { symbol: "$", name: "Pesos Colombianos (COP)", position: "before", decimals: 0, flag: "COP" },
    MXN: { symbol: "$", name: "Pesos Mexicanos (MXN)", position: "before", decimals: 2, flag: "MXN" },
    USD: { symbol: "$", name: "Dólares USA (USD)", position: "before", decimals: 2, flag: "USD" },
    PEN: { symbol: "S/.", name: "Soles Peruanos (PEN)", position: "before", decimals: 2, flag: "PEN" },
    ARS: { symbol: "$", name: "Pesos Argentinos (ARS)", position: "before", decimals: 0, flag: "ARS" },
    CLP: { symbol: "$", name: "Pesos Chilenos (CLP)", position: "before", decimals: 0, flag: "CLP" },
    GBP: { symbol: "£", name: "Libras Esterlinas (GBP)", position: "before", decimals: 2, flag: "GBP" }
  };"""
        content = content.replace(currency_config_old.group(0), currency_config_new)

    # 2. Clean 🎬 from all buttons and labels
    content = content.replace("'🎬 Vídeo & Tiendas'", "'Vídeo y Tiendas'")
    content = content.replace('"🎬 Con Vídeo (', '"Con Vídeo (')
    content = content.replace('(hasVideo(prod) ? "🎬 " : "")', '(hasVideo(prod) ? "▶ " : "")')
    content = content.replace("'🎬 Ver Vídeo & Tiendas'", "'Ver Vídeo y Tiendas'")
    content = content.replace('🎬', '')

    with open('main.js', 'w', encoding='utf-8') as f:
        f.write(content)

    print("main.js cleaned of all emojis successfully!")

if __name__ == '__main__':
    clean_main_js()
