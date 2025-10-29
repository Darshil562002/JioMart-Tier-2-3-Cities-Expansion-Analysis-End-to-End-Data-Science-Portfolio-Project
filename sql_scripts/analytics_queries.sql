JioMart Expansion Analysis - Analytics Queries
Business Intelligence & KPI Queries
________________________________________________________________________________

1. REGIONAL PERFORMANCE ANALYSIS
________________________________________________________________________________

Overall regional performance summary

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

________________________________________________________________________________

2. CATEGORY PERFORMANCE BY REGION
________________________________________________________________________________

Revenue and margin by category and region

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

________________________________________________________________________________

3. CUSTOMER BEHAVIOR ANALYSIS
________________________________________________________________________________

Customer purchase frequency and lifetime value

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

________________________________________________________________________________

4. TOP PERFORMING PRODUCTS
________________________________________________________________________________

Top 20 products by revenue

SELECT 
    p.product_name,
    p.category,
    COUNT(t.transaction_id) as transactions,
    ROUND(SUM(t.revenue), 2) as total_revenue,
    ROUND(AVG(t.margin_pct), 2) as avg_margin_pct,
    COUNT(DISTINCT t.customer_id) as active_customers
FROM transactions t
JOIN products p ON t.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 20;

________________________________________________________________________________

5. DELIVERY & LOGISTICS EFFICIENCY
________________________________________________________________________________

Delivery performance metrics by region and delivery type

SELECT 
    region_tier,
    delivery_type,
    COUNT(*) as total_deliveries,
    ROUND(AVG(delivery_time_hours), 2) as avg_delivery_hours,
    ROUND(AVG(delivery_distance_km), 2) as avg_distance_km,
    ROUND(AVG(logistics_cost), 2) as avg_cost,
    ROUND(AVG(delivery_time_hours) OVER (PARTITION BY region_tier), 2) as region_avg_hours
FROM transactions
GROUP BY region_tier, delivery_type
ORDER BY region_tier, avg_delivery_hours DESC;

________________________________________________________________________________

6. PAYMENT METHOD ANALYSIS
________________________________________________________________________________

Payment method preferences and performance by region

SELECT 
    region_tier,
    payment_method,
    COUNT(*) as transaction_count,
    ROUND(SUM(revenue), 2) as total_revenue,
    ROUND(AVG(revenue), 2) as avg_transaction_value,
    ROUND(AVG(margin_pct), 2) as avg_margin_pct
FROM transactions
GROUP BY region_tier, payment_method
ORDER BY region_tier, total_revenue DESC;

________________________________________________________________________________

7. SEASONAL & MONTHLY TRENDS
________________________________________________________________________________

Monthly revenue and customer trends by region

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

________________________________________________________________________________

8. CUSTOMER SEGMENTATION
________________________________________________________________________________

Customer segments by value and purchase behavior

SELECT 
    CASE 
        WHEN txn_stats.total_revenue >= 10000 THEN 'High Value'
        WHEN txn_stats.total_revenue >= 5000 THEN 'Medium Value'
        ELSE 'Low Value'
    END as customer_segment,
    COUNT(DISTINCT c.customer_id) as customer_count,
    ROUND(AVG(c.age), 1) as avg_age,
    ROUND(AVG(c.digital_literacy_score), 2) as avg_digital_score,
    c.region_tier
FROM customers c
LEFT JOIN (
    SELECT 
        customer_id,
        SUM(revenue) as total_revenue
    FROM transactions
    GROUP BY customer_id
) txn_stats ON c.customer_id = txn_stats.customer_id
GROUP BY customer_segment, c.region_tier
ORDER BY c.region_tier, customer_segment;

________________________________________________________________________________

9. PRODUCT CATEGORY PERFORMANCE
________________________________________________________________________________

Detailed category performance metrics

SELECT 
    p.category,
    COUNT(DISTINCT t.product_id) as unique_products,
    COUNT(DISTINCT t.transaction_id) as total_transactions,
    ROUND(SUM(t.revenue), 2) as total_revenue,
    ROUND(SUM(t.margin), 2) as total_margin,
    ROUND(AVG(t.margin_pct), 2) as avg_margin_pct,
    COUNT(DISTINCT t.customer_id) as active_customers
FROM transactions t
JOIN products p ON t.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

________________________________________________________________________________

10. INVENTORY & STOCKOUTS
________________________________________________________________________________

Inventory turnover and stockout analysis by region

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

________________________________________________________________________________

11. PERISHABLE vs NON-PERISHABLE ANALYSIS
________________________________________________________________________________

Perishable product performance by region

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

________________________________________________________________________________

12. CUSTOMER ACQUISITION TRENDS
________________________________________________________________________________

New customer registrations over time

SELECT 
    TO_CHAR(registration_date, 'YYYY-MM') as month,
    region_tier,
    COUNT(*) as new_customers,
    ROUND(AVG(age), 1) as avg_age,
    ROUND(AVG(digital_literacy_score), 2) as avg_digital_score
FROM customers
GROUP BY TO_CHAR(registration_date, 'YYYY-MM'), region_tier
ORDER BY month, region_tier;

________________________________________________________________________________

13. DISCOUNT EFFECTIVENESS
________________________________________________________________________________

Impact of discounts on margin and volume

SELECT 
    discount_pct,
    COUNT(*) as transaction_count,
    ROUND(AVG(quantity), 2) as avg_quantity_per_txn,
    ROUND(AVG(revenue), 2) as avg_revenue_per_txn,
    ROUND(AVG(margin_pct), 2) as avg_margin_pct
FROM transactions
GROUP BY discount_pct
ORDER BY discount_pct;
