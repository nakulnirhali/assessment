-- Create tables
CREATE TABLE IF NOT EXISTS symbols (
  id serial PRIMARY KEY,
  symbol text UNIQUE NOT NULL,
  name text,
  is_active boolean DEFAULT true,
  sector text,
  industry text,
  asset_type text
);

CREATE TABLE IF NOT EXISTS prices (
  id serial PRIMARY KEY,
  symbol text NOT NULL,
  timestamp timestamptz NOT NULL,
  net double precision,
  buy double precision,
  sell double precision,
  total double precision
);

-- Insert sample symbols
INSERT INTO symbols (symbol, name, is_active, sector, industry, asset_type)
VALUES
('AAPL','Apple Inc', true, 'Technology', 'Consumer Electronics', 'Equity'),
('MSFT','Microsoft Corp', true, 'Technology', 'Software', 'Equity'),
('TSLA','Tesla Inc', true, 'Automotive', 'Electric Vehicles', 'Equity')
ON CONFLICT (symbol) DO NOTHING;

-- Insert a few sample price rows (timestamps spaced hourly)
INSERT INTO prices (symbol, timestamp, net, buy, sell, total)
VALUES
('AAPL', NOW() - INTERVAL '5 hours', 1.1, 2.0, 0.9, 3.0),
('AAPL', NOW() - INTERVAL '4 hours', 1.2, 2.1, 1.0, 3.1),
('AAPL', NOW() - INTERVAL '3 hours', 0.9, 1.8, 0.8, 2.6),
('MSFT', NOW() - INTERVAL '4 hours', 0.5, 1.0, 0.4, 1.9);

-- Materialized view for demonstration
CREATE MATERIALIZED VIEW IF NOT EXISTS timeseries_mv AS
SELECT
  row_number() OVER () as id,
  symbol,
  '1h'::text as interval,
  date_trunc('hour', timestamp) as timestamp,
  avg(net)::double precision as net,
  avg(buy)::double precision as buy,
  avg(sell)::double precision as sell,
  avg(total)::double precision as total
FROM prices
GROUP BY symbol, date_trunc('hour', timestamp);

CREATE INDEX IF NOT EXISTS idx_timeseries_mv_symbol ON timeseries_mv(symbol);
