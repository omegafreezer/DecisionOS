-- PostgreSQL-ready logical schema for the production extension of DecisionOS.
CREATE TABLE IF NOT EXISTS customers (customer_id BIGINT PRIMARY KEY, segment TEXT);
CREATE TABLE IF NOT EXISTS products (product_id TEXT PRIMARY KEY, category TEXT, base_price NUMERIC(12,2));
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id BIGSERIAL PRIMARY KEY,
    transaction_date DATE NOT NULL,
    customer_id BIGINT,
    product_id TEXT,
    region TEXT,
    channel TEXT,
    units_sold INT,
    price NUMERIC(12,2),
    revenue NUMERIC(14,2),
    returns INT DEFAULT 0
);
CREATE TABLE IF NOT EXISTS model_runs (
    run_id UUID PRIMARY KEY,
    model_name TEXT NOT NULL,
    metric_name TEXT,
    metric_value DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS decision_audit (
    decision_id UUID PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    decision_json JSONB NOT NULL
);
