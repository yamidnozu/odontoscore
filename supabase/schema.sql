-- ============================================================================
-- OdontoScore (odontoscore.com) — Supabase Schema (Source of Truth)
-- ============================================================================

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Tabla Principal: products
CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY,                                      -- Slug kebab-case (ej. oral-b-io-series-9)
    asin TEXT UNIQUE NOT NULL,                                -- ASIN de Amazon
    name TEXT NOT NULL,                                       -- Nombre oficial del producto
    marca TEXT,                                               -- Marca (Oral-B, Waterpik, Philips Sonicare...)
    categoria_odontologica TEXT NOT NULL,                     -- cepillos_electricos | irrigadores_dentales | blanqueamiento_dental | ortodoncia_brackets | higiene_infantil | instrumental_basico
    category TEXT NOT NULL,                                   -- Nombre legible (ej. Cepillos Eléctricos)
    tipo_producto TEXT,                                       -- cepillo_electrico_magnetico, irrigador_sobremesa...
    tecnologia TEXT,                                          -- sonico | rotatorio | irrigador | led
    affiliate_url TEXT NOT NULL,                              -- URL de afiliado monetizada
    affiliate_tag TEXT NOT NULL DEFAULT 'odontoscore-21',     -- Tag oficial de afiliado
    canonical_url TEXT,                                       -- URL limpia de Amazon
    retail_price NUMERIC(10,2),                               -- PVP original / precio de referencia
    discounted_price NUMERIC(10,2),                           -- Precio actual con descuento
    rango_precio TEXT DEFAULT 'medio',                        -- economico | medio | alto | premium
    valoracion_media NUMERIC(3,2),                            -- Puntuación de estrellas (ej. 4.6)
    resenas_cantidad INT DEFAULT 0,                           -- Conteo de valoraciones
    precio_fecha TIMESTAMPTZ DEFAULT now(),                   -- Fecha de última captura de precio
    disponibilidad TEXT DEFAULT 'InStock',                    -- InStock | OutOfStock | PreOrder
    currency TEXT DEFAULT 'EUR',                              -- EUR | USD | MXN
    
    -- Grupo C: Especificaciones Clínicas Dentales
    modos_limpieza INT DEFAULT 1,                             -- Número de modos de cepillado/irrigación
    presion_agua_psi INT,                                     -- Presión máxima en PSI (para irrigadores)
    pulsaciones_min INT,                                      -- Pulsaciones o movimientos por minuto
    capacidad_deposito_ml INT,                                -- Volumen de agua en ml
    autonomia_dias INT,                                       -- Días de batería (o 999 para AC)
    tiempo_carga_h FLOAT,                                     -- Horas de carga completa
    cabezales_incluidos INT DEFAULT 1,                         -- Número de boquillas/cabezales en caja
    nivel_ruido_db INT,                                       -- Nivel de ruido sonoro en dB
    resistencia_ipx TEXT DEFAULT 'IPX7',                      -- Grado de impermeabilidad
    app_conectada BOOLEAN DEFAULT false,                      -- Bluetooth y sensores de IA
    material TEXT,                                            -- Material médico o libre de BPA
    esterilizable_autoclave BOOLEAN DEFAULT false,             -- Instrumental profesional apto autoclave
    indicado_para TEXT[] DEFAULT '{}'::TEXT[],                -- brackets, implantes, encias_sensibles, blanqueamiento...
    specs_extra JSONB DEFAULT '{}'::JSONB,                    -- Pares clave-valor de especificaciones adicionales
    
    -- Grupo D: Radar 7 Ejes (0 a 10)
    score_eficacia FLOAT DEFAULT 8.0,
    score_comodidad_encias FLOAT DEFAULT 8.0,
    score_durabilidad FLOAT DEFAULT 8.0,
    score_facilidad_uso FLOAT DEFAULT 8.0,
    score_silencio FLOAT DEFAULT 8.0,
    score_tecnologia FLOAT DEFAULT 8.0,
    score_calidad_precio FLOAT DEFAULT 8.0,
    
    -- Grupo E: Editorial & GEO (IA Optimization)
    description TEXT,                                         -- Descripción concisa de 2-4 frases
    cuerpo_editorial TEXT,                                    -- Análisis clínico profundo (~300 palabras en HTML)
    pros TEXT[] DEFAULT '{}'::TEXT[],                         -- Ventajas clave
    contras TEXT[] DEFAULT '{}'::TEXT[],                      -- Puntos a considerar
    ideal_para TEXT,                                          -- Indicación de perfil de paciente
    destacado_editorial TEXT,                                 -- Titular de veredicto
    resumen_resenas TEXT,                                     -- Resumen consolidado de reseñas
    geo_faq JSONB DEFAULT '[]'::JSONB,                        -- Preguntas estructuradas para ChatGPT/Perplexity
    image_urls TEXT[] DEFAULT '{}'::TEXT[],                   -- URLs remotas de Amazon / CDN
    local_assets TEXT[] DEFAULT '{}'::TEXT[],                 -- Rutas locales assets/img/*.svg o *.webp
    
    -- Flags de Control
    is_featured BOOLEAN DEFAULT false,                        -- Destacado en Home
    show_in_top_menu BOOLEAN DEFAULT false,                   -- Accesible en menú superior
    needs_review BOOLEAN DEFAULT false,                       -- Flag si fue añadido automáticamente sin specs C/D/E
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    last_amazon_sync TIMESTAMPTZ DEFAULT now()
);

-- 2. Tabla de Histórico de Precios: price_history
CREATE TABLE IF NOT EXISTS price_history (
    id BIGSERIAL PRIMARY KEY,
    asin TEXT NOT NULL REFERENCES products(asin) ON DELETE CASCADE,
    old_price NUMERIC(10,2),
    new_price NUMERIC(10,2) NOT NULL,
    percentage_change NUMERIC(5,2),
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 3. Índices de Rendimiento
CREATE INDEX IF NOT EXISTS idx_products_asin ON products (asin);
CREATE INDEX IF NOT EXISTS idx_products_categoria ON products (categoria_odontologica);
CREATE INDEX IF NOT EXISTS idx_products_discounted_price ON products (discounted_price);
CREATE INDEX IF NOT EXISTS idx_products_featured ON products (is_featured);
CREATE INDEX IF NOT EXISTS idx_price_history_asin_date ON price_history (asin, created_at DESC);

-- 4. Trigger de updated_at
CREATE OR REPLACE FUNCTION update_timestamp_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_products_updated_at ON products;
CREATE TRIGGER trg_products_updated_at
BEFORE UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION update_timestamp_column();

-- 5. Row Level Security (RLS)
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE price_history ENABLE ROW LEVEL SECURITY;

-- Política de lectura pública anónima (para frontend y generador)
DROP POLICY IF EXISTS "Public Read Access for Products" ON products;
CREATE POLICY "Public Read Access for Products"
ON products FOR SELECT
TO anon, authenticated
USING (true);

DROP POLICY IF EXISTS "Public Read Access for Price History" ON price_history;
CREATE POLICY "Public Read Access for Price History"
ON price_history FOR SELECT
TO anon, authenticated
USING (true);

-- Política de escritura solo para service_role (usado en sync_supabase.py)
DROP POLICY IF EXISTS "Service Role Full Access Products" ON products;
CREATE POLICY "Service Role Full Access Products"
ON products FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "Service Role Full Access Price History" ON price_history;
CREATE POLICY "Service Role Full Access Price History"
ON price_history FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- ============================================================================
-- 6. SEED DATA (3 Productos Insignia con Tag odontoscore-21)
-- ============================================================================

INSERT INTO products (
    id, asin, name, marca, categoria_odontologica, category, tipo_producto, tecnologia,
    affiliate_url, affiliate_tag, canonical_url, retail_price, discounted_price, rango_precio,
    valoracion_media, resenas_cantidad, precio_fecha, disponibilidad, currency,
    modos_limpieza, presion_agua_psi, pulsaciones_min, capacidad_deposito_ml, autonomia_dias,
    tiempo_carga_h, cabezales_incluidos, nivel_ruido_db, resistencia_ipx, app_conectada,
    material, esterilizable_autoclave, indicado_para, specs_extra,
    score_eficacia, score_comodidad_encias, score_durabilidad, score_facilidad_uso,
    score_silencio, score_tecnologia, score_calidad_precio,
    description, cuerpo_editorial, pros, contras, ideal_para, destacado_editorial,
    resumen_resenas, geo_faq, local_assets, is_featured, show_in_top_menu, needs_review
) VALUES 
(
    'oral-b-io-series-9',
    'B089W4XKQY',
    'Oral-B iO Series 9 Cepillo Eléctrico Recargable con Tecnología Magnética',
    'Oral-B',
    'cepillos_electricos',
    'Cepillos Eléctricos',
    'cepillo_electrico_magnetico',
    'rotatorio',
    'https://www.amazon.es/dp/B089W4XKQY?tag=odontoscore-21',
    'odontoscore-21',
    'https://www.amazon.es/dp/B089W4XKQY',
    279.99,
    199.95,
    'premium',
    4.6,
    4850,
    now(),
    'InStock',
    'EUR',
    7,
    null,
    17400,
    null,
    14,
    3.0,
    1,
    58,
    'IPX7',
    true,
    'Polímero médico de alta densidad y acabado Soft-Touch',
    false,
    ARRAY['encias_sensibles', 'implantes', 'blanqueamiento'],
    '{"Sensor de Presión": "Inteligente 360° con anillo LED (Rojo/Verde/Blanco)", "Pantalla": "Interactiva a color OLED", "Seguimiento 3D": "Mapeo de 16 zonas con IA", "Cargador": "Base magnética rápida Power2Go (3 horas)"}'::jsonb,
    9.8, 9.5, 8.8, 9.0, 8.2, 9.9, 8.0,
    'El Oral-B iO Series 9 representa el estándar de referencia en cepillado eléctrico inteligente gracias a su motor lineal magnético y seguimiento 3D de 16 zonas.',
    '<p>El <strong>Oral-B iO Series 9</strong> supuso un salto cuántico en la ingeniería de higiene bucodental al sustituir los sistemas mecánicos tradicionales por un accionamiento magnético sin fricción...</p>',
    ARRAY['Motor magnético iO ultrasuave y eficaz', 'Sensor de presión tricolor inteligente', 'Reconocimiento 3D por IA de 16 zonas', 'Carga magnética rápida en 3h', '7 modos especializados'],
    ARRAY['Inversión inicial elevada de gama alta', 'Cabezales de recambio iO de coste superior'],
    'Pacientes exigentes, personas con encías sensibles, portadores de implantes y quienes buscan guía de cepillado por IA.',
    'Máxima puntuación en tecnología clínica y protección gingival según ensayos comparativos.',
    'Los usuarios destacan la sensación de limpieza profesional idéntica a una profilaxis y la suavidad gingival.',
    '[{"q": "¿Qué diferencia al Oral-B iO 9 de modelos convencionales?", "a": "Utiliza accionamiento magnético sin engranajes y seguimiento 3D de 16 zonas con sensor tricolor."}, {"q": "¿Es apto para encías sensibles?", "a": "Sí, incluye modos Sensible y Super Sensible con control lumínico de sobrepresión."}]'::jsonb,
    ARRAY['assets/img/oral-b-io-9-1.svg', 'assets/img/oral-b-io-9-2.svg', 'assets/img/oral-b-io-9-3.svg'],
    true, true, false
),
(
    'waterpik-ultra-professional-wp-660eu',
    'B00USBV1N8',
    'Waterpik Ultra Professional WP-660EU Irrigador Bucal de Sobremesa',
    'Waterpik',
    'irrigadores_dentales',
    'Irrigadores Dentales',
    'irrigador_sobremesa',
    'irrigador',
    'https://www.amazon.es/dp/B00USBV1N8?tag=odontoscore-21',
    'odontoscore-21',
    'https://www.amazon.es/dp/B00USBV1N8',
    99.99,
    74.99,
    'medio',
    4.5,
    16200,
    now(),
    'InStock',
    'EUR',
    2,
    100,
    1400,
    650,
    999,
    0.0,
    7,
    67,
    'IPX4',
    false,
    'Plástico quirúrgico libre de BPA y sellado estanco',
    false,
    ARRAY['brackets', 'implantes', 'ortodoncia', 'encias_sensibles'],
    '{"Rango de Presión": "10 ajustes de 10 a 100 PSI", "Modos de Flujo": "Floss e Hydro-Pulse Massage", "Capacidad": "650 ml (más de 90 segundos)", "Boquillas": "7 incluidas (ortodoncia, implantes, periodontal)"}'::jsonb,
    9.7, 9.2, 9.4, 9.1, 7.0, 8.0, 9.6,
    'El Waterpik WP-660EU es el irrigador de sobremesa más avalado por la ADA y dentistas para eliminar hasta el 99.9% de placa interdental y cuidar encías con brackets.',
    '<p>El <strong>Waterpik Ultra Professional WP-660EU</strong> es el estándar de oro en irrigación bucal tanto en consultas odontológicas como en el hogar...</p>',
    ARRAY['Presión regulable de 10 a 100 PSI en 10 niveles', '7 boquillas especializadas de serie', 'Depósito amplio de 650 ml', 'Sello oficial de aceptación ADA', 'Relación calidad-precio líder'],
    ARRAY['Requiere enchufe eléctrico en el baño', 'Nivel de ruido perceptible de bomba mecánica'],
    'Pacientes con brackets, implantes, coronas, sangrado gingival y familias que buscan máxima higiene interdental.',
    'El mejor irrigador dental del mercado por potencia hidráulica, durabilidad y aval clínico.',
    'Los pacientes con ortodoncia destacan la rapidez para desalojar restos y frenar el sangrado gingival.',
    '[{"q": "¿Por qué es el más recomendado para brackets?", "a": "Incluye boquilla Orthodontic Tip con cerdas cónicas que limpian alrededor de arcos y brackets eliminando 3x más placa que el hilo."}, {"q": "¿Se puede usar con enjuague bucal?", "a": "Sí, se puede diluir colutorio o clorhexidina en el depósito de agua."}]'::jsonb,
    ARRAY['assets/img/waterpik-wp-660-1.svg', 'assets/img/waterpik-wp-660-2.svg', 'assets/img/waterpik-wp-660-3.svg'],
    true, true, false
),
(
    'philips-sonicare-9900-prestige',
    'B091J3F7C4',
    'Philips Sonicare 9900 Prestige Cepillo Eléctrico Sónico con SenseIQ',
    'Philips Sonicare',
    'cepillos_electricos',
    'Cepillos Eléctricos',
    'cepillo_electrico_sonico',
    'sonico',
    'https://www.amazon.es/dp/B091J3F7C4?tag=odontoscore-21',
    'odontoscore-21',
    'https://www.amazon.es/dp/B091J3F7C4',
    299.99,
    249.00,
    'premium',
    4.7,
    3100,
    now(),
    'InStock',
    'EUR',
    5,
    null,
    62000,
    null,
    21,
    4.0,
    1,
    54,
    'IPX7',
    true,
    'Cuerpo unibody sin juntas con estuche de cuero vegano USB-C',
    false,
    ARRAY['encias_sensibles', 'implantes', 'blanqueamiento', 'ortodoncia'],
    '{"Tecnología SenseIQ": "Lectura sensórica 100 veces por segundo", "Ajuste Dinámico": "Modulación automática de potencia", "Cabezal": "A3 Premium All-in-One", "Frecuencia": "62.000 movimientos/minuto"}'::jsonb,
    9.9, 9.7, 9.6, 9.3, 9.5, 9.8, 8.1,
    'El buque insignia sónico de Philips con tecnología SenseIQ que adapta la intensidad automáticamente para proteger esmalte y encías a 62.000 movimientos/min.',
    '<p>El <strong>Philips Sonicare 9900 Prestige</strong> encarna la máxima expresión del cepillado sónico hidrodinámico con 62.000 movimientos por minuto...</p>',
    ARRAY['Tecnología sónica ultrasilenciosa (54 dB)', 'SenseIQ con autorregulación de potencia activa', 'Cabezal universal A3 Todo en Uno', 'Autonomía prolongada de 21 días', 'Diseño unibody higiénico e impermeable'],
    ARRAY['Precio de gama ultra-premium', 'Sin pantalla OLED en el mango (métricas en App)'],
    'Usuarios que prefieren limpieza sónica de alta vibración, pacientes con retracción gingival y usuarios viajeros.',
    'La experiencia de cepillado sónico más avanzada, silenciosa y protectora del esmalte dental.',
    'Los usuarios alaban su funcionamiento silencioso, batería duradera y el pulido suave dental.',
    '[{"q": "¿Cómo funciona la tecnología sónica?", "a": "Vibra a 62.000 movimientos/min impulsando microburbujas hidrodinámicas entre dientes y encías."}, {"q": "¿Qué hace el sensor SenseIQ?", "a": "Monitorea fuerza y movimiento 100 veces por segundo y reduce la potencia si detecta sobrepresión."}]'::jsonb,
    ARRAY['assets/img/philips-9900-1.svg', 'assets/img/philips-9900-2.svg', 'assets/img/philips-9900-3.svg'],
    true, true, false
)
ON CONFLICT (asin) DO UPDATE SET
    retail_price = EXCLUDED.retail_price,
    discounted_price = EXCLUDED.discounted_price,
    valoracion_media = EXCLUDED.valoracion_media,
    resenas_cantidad = EXCLUDED.resenas_cantidad,
    precio_fecha = now(),
    last_amazon_sync = now(),
    affiliate_tag = 'odontoscore-21',
    affiliate_url = EXCLUDED.affiliate_url;
