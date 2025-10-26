-- =============================================================================
-- JioMart Expansion Analysis - Analytics Queries
-- Business Intelligence & KPI Queries
-- =============================================================================

-- =============================================================================
-- 1. REGIONAL PERFORMANCE ANALYSIS
-- =============================================================================

-- Overall regional performance summary
SELECT 
    region_tier,
    COUNT(DISTINCT transaction_id) as total_transactions,
    COUNT(DISTINCT customer_id) as unique_customers,
    SUM(revenue) as total_revenue,
    SUM(margin) as total_margin,
    ROUND(AVG(margin_pct), 2) as avg_margin_pct,
    ROUND(AVG(delivery_time_hours), 2) as avg_delivery_hours,
    ROUND(AVG(delivery_distance_km), 2) as avg_delivery_distance,
    ROUND(AVG(logistics_cost), 2) as avg_logistics_cost
FROM transactions
GROUP BY region_tier
ORDER BY total_revenue DESC;

-- =============================================================================
-- 2. CATEGORY PERFORMANCE BY REGION
-- =============================================================================

-- Revenue and margin by category and region
SELECT 
    t.region_tier,
    p.category,
    COUNT(t.transaction_id) as transaction_count,
    SUM(t.revenue) as total_revenue,
    SUM(t.margin) as total_margin,
    ROUND(AVG(t.margin_pct), 2) as avg_margin_pct,
    ROUND(SUM(t.revenue) * 100.0 / SUM(SUM(t.revenue)) OVER (PARTITION BY t.region_tier), 2) as pct_of_regional_revenue
FROM transactions t
JOIN products p ON t.product_id = p.product_id
GROUP BY t.region_tier, p.category
ORDER BY t.region_tier, total_revenue DESC;

-- =============================================================================
-- 3. CUSTOMER BEHAVIOR ANALYSIS
-- =============================================================================

-- Customer purchase frequency and lifetime value
SELECT 
    c.region_tier,
    COUNT(DISTINCT c.customer_id) as total_customers,
    ROUND(AVG(txn_stats.purchase_count), 2) as avg_purchases_per_customer,
    ROUND(AVG(txn_stats.total_revenue), 2) as avg_customer_lifetime_value,
    ROUND(AVG(txn_stats.total_margin), 2) as avg_customer_margin,
    COUNT(CASE WHEN txn_stats.purchase_count >= 3 THEN 1 END) as repeat_customers,
    ROUND(COUNT(CASE WHEN txn_stats.purchase_count >= 3 THEN 1 END) * 100.0 / COUNT(DISTINCT c.customer_id), 2) as repeat_rate_pct
FROM customers c
LEFT JOIN (
    SELECT 
        customer_id,
        COUNT(*) as purchase_count,
        SUM(revenue) as total_revenue,
        SUM(margin) as total_margin
    FROM transactions
    GROUP BY customer_id
) txn_stats ON c.customer_id = txn_stats.customer_id
GROUP BY c.region_tier
ORDER BY total_customers DESC;

-- =============================================================================
-- 4. TOP PERFORMING PRODUCTS
-- =============================================================================

-- Top 20 products by revenue
SELECT 
    p.product_name,
    p.category,
    COUNT(t.transaction_id) as times_sold,
    SUM(t.quantity) as total_units_sold,
    ROUND(SUM(t.revenue), 2) as total_revenue,
    ROUND(AVG(t.margin_pct), 2) as avg_margin_pct,
    ROUND(SUM(t.revenue) / SUM(t.quantity), 2) as avg_selling_price
FROM transactions t
JOIN products p ON t.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 20;

-- =============================================================================
-- 5. STORE PERFORMANCE RANKING
-- =============================================================================

-- Store performance with rankings
SELECT 
    s.store_id,
    s.store_name,
    s.region_tier,
    s.city,
    COUNT(t.transaction_id) as total_transactions,
    ROUND(SUM(t.revenue), 2) as total_revenue,
    ROUND(AVG(t.margin_pct), 2) as avg_margin_pct,
    ROUND(AVG(t.delivery_time_hours), 2) as avg_delivery_time,
    RANK() OVER (PARTITION BY s.region_tier ORDER BY SUM(t.revenue) DESC) as revenue_rank_in_tier
FROM stores s
LEFT JOIN transactions t ON s.store_id = t.store_id
GROUP BY s.store_id, s.store_name, s.region_tier, s.city
ORDER BY total_revenue DESC;

-- =============================================================================
-- 6. HIGH-RISK STORES (Low Margin)
-- =============================================================================

-- Stores with margin % < 10% (high risk)
SELECT 
    s.store_id,
    s.store_name,
    s.region_tier,
    s.city,
    COUNT(t.transaction_id) as total_transactions,
    ROUND(AVG(t.margin_pct), 2) as avg_margin_pct,
    ROUND(AVG(t.logistics_cost), 2) as avg_logistics_cost,
    ROUND(AVG(t.spoilage_cost), 2) as avg_spoilage_cost,
    s.warehouse_distance_km
FROM stores s
JOIN transactions t ON s.store_id = t.store_id
GROUP BY s.store_id, s.store_name, s.region_tier, s.city, s.warehouse_distance_km
HAVING AVG(t.margin_pct) < 10
ORDER BY avg_margin_pct ASC;

-- =============================================================================
-- 7. LOGISTICS COST ANALYSIS
-- =============================================================================

-- Average costs breakdown by region
SELECT 
    region_tier,
    ROUND(AVG(product_cost), 2) as avg_product_cost,
    ROUND(AVG(logistics_cost), 2) as avg_logistics_cost,
    ROUND(AVG(spoilage_cost), 2) as avg_spoilage_cost,
    ROUND(AVG(total_cost), 2) as avg_total_cost,
    ROUND(AVG(logistics_cost) * 100.0 / AVG(total_cost), 2) as logistics_pct_of_cost
FROM transactions
GROUP BY region_tier
ORDER BY avg_logistics_cost DESC;

-- =============================================================================
-- 8. INVENTORY STOCKOUT ANALYSIS
-- =============================================================================

-- Products with frequent stockouts by region
SELECT 
    s.region_tier,
    p.product_name,
    p.category,
    COUNT(i.inventory_id) as stores_carrying,
    ROUND(AVG(i.stockout_days_last_month), 2) as avg_stockout_days,
    SUM(CASE WHEN i.stockout_days_last_month > 5 THEN 1 ELSE 0 END) as stores_with_high_stockouts
FROM inventory i
JOIN stores s ON i.store_id = s.store_id
JOIN products p ON i.product_id = p.product_id
GROUP BY s.region_tier, p.product_id, p.product_name, p.category
HAVING AVG(i.stockout_days_last_month) > 3
ORDER BY s.region_tier, avg_stockout_days DESC;

-- =============================================================================
-- 9. PAYMENT METHOD ANALYSIS
-- =============================================================================

-- Payment method distribution by region
SELECT 
    region_tier,
    payment_method,
    COUNT(*) as transaction_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY region_tier), 2) as pct_of_regional_txns,
    ROUND(AVG(revenue), 2) as avg_transaction_value
FROM transactions
GROUP BY region_tier, payment_method
ORDER BY region_tier, transaction_count DESC;

-- =============================================================================
-- 10. MONTH-OVER-MONTH GROWTH
-- =============================================================================

-- Monthly revenue and transaction trends
SELECT 
    TO_CHAR(transaction_date, 'YYYY-MM') as month,
    region_tier,
    COUNT(*) as transactions,
    ROUND(SUM(revenue), 2) as total_revenue,
    ROUND(AVG(margin_pct), 2) as avg_margin_pct,
    COUNT(DISTINCT customer_id) as active_customers
FROM transactions
GROUP BY TO_CHAR(transaction_date, 'YYYY-MM'), region_tier
ORDER BY month, region_tier;

-- =============================================================================
-- 11. PERISHABLE vs NON-PERISHABLE ANALYSIS
-- =============================================================================

-- Perishable product performance by region
SELECT 
    region_tier,
    is_perishable,
    COUNT(*) as transaction_count,
    ROUND(SUM(revenue), 2) as total_revenue,
    ROUND(AVG(margin_pct), 2) as avg_margin_pct,
    ROUND(AVG(spoilage_cost), 2) as avg_spoilage_cost,
    ROUND(AVG(CASE WHEN is_perishable THEN spoilage_cost ELSE 0 END), 2) as avg_spoilage_if_perishable
FROM transactions
GROUP BY region_tier, is_perishable
ORDER BY region_tier, is_perishable DESC;

-- =============================================================================
-- 12. CUSTOMER ACQUISITION TRENDS
-- =============================================================================

-- New customer registrations over time
SELECT 
    TO_CHAR(registration_date, 'YYYY-MM') as month,
    region_tier,
    COUNT(*) as new_customers,
    ROUND(AVG(age), 1) as avg_age,
    ROUND(AVG(digital_literacy_score), 2) as avg_digital_score
FROM customers
GROUP BY TO_CHAR(registration_date, 'YYYY-MM'), region_tier
ORDER BY month, region_tier;

-- =============================================================================
-- 13. DISCOUNT EFFECTIVENESS
-- =============================================================================

-- Impact of discounts on margin and volume
SELECT 
    discount_pct,
    COUNT(*) as transaction_count,
    ROUND(AVG(quantity), 2) as avg_quantity_per_txn,
    ROUND(AVG(revenue), 2) as avg_revenue_per_txn,
    ROUND(AVG(margin_pct), 2) as avg_margin_pct
FROM transactions
GROUP BY discount_pct
ORDER BY discount_pct;
