-- =============================================================================
-- JioMart Expansion Analysis - Database Schema
-- =============================================================================

-- Drop existing tables (in dependency order)
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS inventory CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS stores CASCADE;

-- =============================================================================
-- STORES TABLE
-- =============================================================================
CREATE TABLE stores (
    store_id VARCHAR(10) PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL,
    region_tier VARCHAR(10) NOT NULL CHECK (region_tier IN ('Metro', 'Tier 2', 'Tier 3')),
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    city_population INTEGER,
    infrastructure_score DECIMAL(3,1) CHECK (infrastructure_score BETWEEN 0 AND 10),
    warehouse_distance_km DECIMAL(6,2),
    opening_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- PRODUCTS TABLE
-- =============================================================================
CREATE TABLE products (
    product_id VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    unit_cost DECIMAL(10,2) NOT NULL CHECK (unit_cost >= 0),
    list_price DECIMAL(10,2) NOT NULL CHECK (list_price >= 0),
    target_margin_pct DECIMAL(5,2),
    is_perishable BOOLEAN NOT NULL DEFAULT FALSE,
    avg_shelf_life_days INTEGER CHECK (avg_shelf_life_days > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- CUSTOMERS TABLE
-- =============================================================================
CREATE TABLE customers (
    customer_id VARCHAR(15) PRIMARY KEY,
    primary_store_id VARCHAR(10) NOT NULL REFERENCES stores(store_id),
    region_tier VARCHAR(10) NOT NULL CHECK (region_tier IN ('Metro', 'Tier 2', 'Tier 3')),
    age INTEGER CHECK (age BETWEEN 18 AND 100),
    income_bracket VARCHAR(20),
    digital_literacy_score DECIMAL(3,1) CHECK (digital_literacy_score BETWEEN 0 AND 10),
    registration_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- TRANSACTIONS TABLE
-- =============================================================================
CREATE TABLE transactions (
    transaction_id VARCHAR(15) PRIMARY KEY,
    transaction_date DATE NOT NULL,
    customer_id VARCHAR(15) NOT NULL REFERENCES customers(customer_id),
    product_id VARCHAR(10) NOT NULL REFERENCES products(product_id),
    store_id VARCHAR(10) NOT NULL REFERENCES stores(store_id),
    region_tier VARCHAR(10) NOT NULL CHECK (region_tier IN ('Metro', 'Tier 2', 'Tier 3')),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
    revenue DECIMAL(12,2) NOT NULL CHECK (revenue >= 0),
    product_cost DECIMAL(12,2) NOT NULL CHECK (product_cost >= 0),
    logistics_cost DECIMAL(10,2) NOT NULL CHECK (logistics_cost >= 0),
    spoilage_cost DECIMAL(10,2) DEFAULT 0 CHECK (spoilage_cost >= 0),
    total_cost DECIMAL(12,2) NOT NULL,
    margin DECIMAL(12,2) NOT NULL,
    margin_pct DECIMAL(6,2),
    discount_pct INTEGER DEFAULT 0 CHECK (discount_pct BETWEEN 0 AND 100),
    delivery_time_hours DECIMAL(5,2),
    delivery_distance_km DECIMAL(6,2),
    payment_method VARCHAR(20),
    is_perishable BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- INVENTORY TABLE
-- =============================================================================
CREATE TABLE inventory (
    inventory_id VARCHAR(15) PRIMARY KEY,
    store_id VARCHAR(10) NOT NULL REFERENCES stores(store_id),
    product_id VARCHAR(10) NOT NULL REFERENCES products(product_id),
    current_stock INTEGER NOT NULL CHECK (current_stock >= 0),
    reorder_point INTEGER NOT NULL CHECK (reorder_point >= 0),
    stockout_days_last_month INTEGER DEFAULT 0 CHECK (stockout_days_last_month >= 0),
    avg_daily_sales DECIMAL(8,2),
    last_restock_date DATE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (store_id, product_id)
);

-- =============================================================================
-- INDEXES FOR PERFORMANCE
-- =============================================================================

-- Stores indexes
CREATE INDEX idx_stores_region ON stores(region_tier);
CREATE INDEX idx_stores_city ON stores(city);

-- Products indexes
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_perishable ON products(is_perishable);

-- Customers indexes
CREATE INDEX idx_customers_region ON customers(region_tier);
CREATE INDEX idx_customers_store ON customers(primary_store_id);
CREATE INDEX idx_customers_reg_date ON customers(registration_date);

-- Transactions indexes (most queried table)
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_customer ON transactions(customer_id);
CREATE INDEX idx_transactions_product ON transactions(product_id);
CREATE INDEX idx_transactions_store ON transactions(store_id);
CREATE INDEX idx_transactions_region ON transactions(region_tier);
CREATE INDEX idx_transactions_date_region ON transactions(transaction_date, region_tier);
CREATE INDEX idx_transactions_margin ON transactions(margin_pct);

-- Inventory indexes
CREATE INDEX idx_inventory_store ON inventory(store_id);
CREATE INDEX idx_inventory_product ON inventory(product_id);
CREATE INDEX idx_inventory_stockouts ON inventory(stockout_days_last_month);

-- =============================================================================
-- COMMENTS FOR DOCUMENTATION
-- =============================================================================

COMMENT ON TABLE stores IS 'JioMart store locations across Metro, Tier 2, and Tier 3 cities';
COMMENT ON TABLE products IS 'Product catalog with pricing and category information';
COMMENT ON TABLE customers IS 'Customer demographics and profile data';
COMMENT ON TABLE transactions IS 'Transaction records with revenue, cost, and margin details';
COMMENT ON TABLE inventory IS 'Store-level inventory tracking and stockout monitoring';

COMMENT ON COLUMN transactions.margin_pct IS 'Calculated as (margin / revenue) * 100';
COMMENT ON COLUMN transactions.total_cost IS 'Sum of product_cost + logistics_cost + spoilage_cost';
COMMENT ON COLUMN stores.infrastructure_score IS 'Score from 0-10 indicating logistics infrastructure quality';
COMMENT ON COLUMN customers.digital_literacy_score IS 'Score from 0-10 indicating comfort with digital platforms';
