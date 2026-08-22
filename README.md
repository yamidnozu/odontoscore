# 🦷 OdontoScore — Dental Affiliate & Clinical Comparison Platform

> **Dominio Oficial:** [https://odontoscore.com/](https://odontoscore.com/)  
> **Arquitectura:** Supabase (Source of Truth) + Amazon PA-API 5.0 / Rainforest API Fallback + Static Site Generator (Python) + Hostinger Deployment.

---

## 🌟 Características Principales

- **Fichas Técnicas Clínicas (E-E-A-T):** Especificaciones normalizadas (presión en PSI, pulsaciones/minuto, decibelios, sellado IPX, batería y aplicaciones con IA).
- **Radar Clínico de 7 Ejes (SVG):** Eficacia Limpieza Biofilm, Cuidado Gingival, Durabilidad, Ergonomía, Nivel Sonoro, Tecnología y Relación Calidad-Precio.
- **Comparador Clínico Intra-Categoría:** Enfrentamiento de 2 a 4 dispositivos lado a lado con matrices de características y superposición de gráficos radar.
- **Motor GEO para Inteligencia Artificial:** Bloques estructurados de preguntas clínicas para motores generativos (ChatGPT Search, Perplexity, Gemini).
- **Actualización de Precios Híbrida:** Páginas HTML pre-horneadas para SEO con actualización en vivo en cliente (`main.js`) vía Supabase REST.

---

## 🛠️ Stack Tecnológico

- **Frontend:** Vanilla HTML5, CSS3 moderno (Design System Clínico: `#0E76BC` + `#0F172A` + `#F8FAFC`), Vanilla JS (IIFE sin frameworks).
- **Backend / Datos:** Supabase PostgreSQL con Row Level Security (RLS).
- **Sincronización:** Amazon PA-API 5.0 (`paapi5-python-sdk`) + Rainforest API.
- **Compilador:** Python Static Site Builder (`tools/build_site.py`).
- **CI/CD:** GitHub Actions (`.github/workflows/sync.yml`) programado cada 6 horas.

---

## 📁 Estructura del Proyecto

```text
├── .github/workflows/sync.yml    # Pipeline CI/CD cada 6h
├── assets/                       # Gráficos vectoriales y logotipos SVG
├── categoria/                    # Hubs de las 6 especialidades dentales
├── datos/productos.json          # Caché local estructurado de productos
├── guias/                        # Guías clínicas y artículos de autoridad SEO
├── lib/                          # Manifest y DB en cliente
├── producto/                     # Fichas técnicas individuales
├── supabase/                     # Esquema SQL (schema.sql y price_history.sql)
├── tools/
│   ├── build_site.py             # Generador estático de HTML
│   └── sync_supabase.py          # Sincronizador Supabase y Amazon PA-API 5.0
├── asins.json                    # Catálogo de ASINs a procesar
├── requirements.txt              # Dependencias Python
└── styles.css                    # Sistema de diseño clínico OdontoScore
```

---

## 🚀 Guía de Inicio Local

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno
Copia `.env.example` a `.env` y completa tus credenciales:
```bash
cp .env.example .env
```

### 3. Sincronizar y Compilar
```bash
# Sincronización con Amazon y Supabase
python tools/sync_supabase.py

# Compilación estática
python tools/build_site.py

# Servidor de previsualización local
python -m http.server 8000
```

---

## 📄 Licencia y Descargos

- **Aviso de Afiliación:** Participante del Programa de Afiliados de Amazon EU con el tag oficial `odontoscore-21`.
- **Descargo Médico:** La información técnica publicada en OdontoScore es meramente divulgativa y no sustituye el diagnóstico u orientación de un odontólogo colegiado.
