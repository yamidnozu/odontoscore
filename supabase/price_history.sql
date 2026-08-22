-- ============================================================================
-- OdontoScore — Price History & Analytics Table
-- ============================================================================

CREATE TABLE IF NOT EXISTS price_history (
    id BIGSERIAL PRIMARY KEY,
    asin TEXT NOT NULL REFERENCES products(asin) ON DELETE CASCADE,
    old_price NUMERIC(10,2),
    new_price NUMERIC(10,2) NOT NULL,
    percentage_change NUMERIC(5,2),
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_price_history_asin_date ON price_history (asin, created_at DESC);

ALTER TABLE price_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public Read Access for Price History"
ON price_history FOR SELECT
TO anon, authenticated
USING (true);

CREATE POLICY "Service Role Full Access Price History"
ON price_history FOR ALL
TO service_role
USING (true)
WITH CHECK (true);
