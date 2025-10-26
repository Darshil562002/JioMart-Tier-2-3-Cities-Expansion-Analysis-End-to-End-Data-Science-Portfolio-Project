#!/usr/bin/env python3
"""
JioMart Tier 2/3 Cities Expansion Analysis
Complete Data Generation, Analysis, and Visualization Pipeline
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report, silhouette_score, mean_absolute_error, r2_score
import os

# Configuration
np.random.seed(42)
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("="*80)
print("JIOMART TIER 2/3 EXPANSION ANALYSIS - COMPLETE PIPELINE")
print("="*80)

# ==============================================================================
# SECTION 1: DATA GENERATION
# ==============================================================================

print("\n[1/8] GENERATING SIMULATION DATA...")
print("-" * 80)

# City definitions with population and infrastructure scores
metro_cities = [
    ('Mumbai', 'Maharashtra', 20_400_000, 9.5),
    ('Delhi', 'Delhi', 16_750_000, 9.2),
    ('Bangalore', 'Karnataka', 12_330_000, 9.0),
    ('Hyderabad', 'Telangana', 10_000_000, 8.8),
    ('Pune', 'Maharashtra', 6_430_000, 8.5),
    ('Chennai', 'Tamil Nadu', 10_970_000, 8.7)
]

tier2_cities = [
    ('Jaipur', 'Rajasthan', 3_050_000, 7.5),
    ('Lucknow', 'Uttar Pradesh', 2_900_000, 7.2),
    ('Coimbatore', 'Tamil Nadu', 2_150_000, 7.8),
    ('Indore', 'Madhya Pradesh', 2_170_000, 7.4),
    ('Bhopal', 'Madhya Pradesh', 1_800_000, 6.9),
    ('Nagpur', 'Maharashtra', 2_400_000, 7.3),
    ('Vadodara', 'Gujarat', 1_670_000, 7.6),
    ('Ludhiana', 'Punjab', 1_620_000, 7.1),
    ('Visakhapatnam', 'Andhra Pradesh', 1_730_000, 7.0)
]

tier3_cities = [
    ('Raipur', 'Chhattisgarh', 1_010_000, 6.2),
    ('Jamshedpur', 'Jharkhand', 630_000, 6.5),
    ('Guwahati', 'Assam', 960_000, 6.0),
    ('Ranchi', 'Jharkhand', 1_070_000, 6.3),
    ('Agra', 'Uttar Pradesh', 1_590_000, 5.8),
    ('Nashik', 'Maharashtra', 1_480_000, 6.4),
    ('Udaipur', 'Rajasthan', 475_000, 6.1),
    ('Ajmer', 'Rajasthan', 550_000, 5.9),
    ('Mysore', 'Karnataka', 920_000, 6.7)
]

# Product categories with pricing and margins
product_categories = {
    'Groceries': {
        'items': ['Basmati Rice 5kg', 'Wheat Flour 10kg', 'Sunflower Oil 1L', 'Sugar 1kg', 'Toor Dal 1kg', 'Spices Mix'],
        'cost_range': (40, 250),
        'margin_range': (12, 20),
        'perishable': False
    },
    'Fresh Produce': {
        'items': ['Seasonal Vegetables', 'Fresh Fruits', 'Milk 1L', 'Eggs Dozen', 'Paneer 200g', 'Fresh Chicken'],
        'cost_range': (30, 180),
        'margin_range': (18, 28),
        'perishable': True
    },
    'Packaged Foods': {
        'items': ['Biscuits Assorted', 'Namkeen Mix', 'Instant Noodles', 'Sauces', 'Beverages', 'Bread'],
        'cost_range': (25, 150),
        'margin_range': (15, 25),
        'perishable': False
    },
    'Personal Care': {
        'items': ['Shampoo 200ml', 'Soap Bar', 'Toothpaste', 'Face Wash', 'Body Lotion', 'Hair Oil'],
        'cost_range': (50, 300),
        'margin_range': (20, 35),
        'perishable': False
    },
    'Home Care': {
        'items': ['Detergent 1kg', 'Floor Cleaner', 'Dishwash Liquid', 'Toilet Cleaner', 'Air Freshener'],
        'cost_range': (40, 200),
        'margin_range': (18, 28),
        'perishable': False
    },
    'Electronics': {
        'items': ['Mobile Phones', 'TWS Earbuds', 'Phone Chargers', 'Power Banks', 'Smart Watches'],
        'cost_range': (500, 15000),
        'margin_range': (8, 15),
        'perishable': False
    },
    'Fashion': {
        'items': ['T-Shirts', 'Jeans', 'Footwear', 'Accessories', 'Kids Wear'],
        'cost_range': (200, 2000),
        'margin_range': (25, 45),
        'perishable': False
    }
}

# Generate Stores
print("\n  → Generating Stores Data...")
stores_data = []
store_id = 1

for cities, tier_name, num_stores in [(metro_cities, 'Metro', 40), (tier2_cities, 'Tier 2', 45), (tier3_cities, 'Tier 3', 35)]:
    
    for i in range(num_stores):
        city_info = cities[i % len(cities)]
        city, state, population, infra_score = city_info
        
        stores_data.append({
            'store_id': f'STR{store_id:04d}',
            'store_name': f'JioMart {city} Store {(i % len(cities)) + 1}',
            'region_tier': tier_name,
            'city': city,
            'state': state,
            'city_population': population,
            'infrastructure_score': infra_score,
            'warehouse_distance_km': np.random.uniform(2, 8) if tier_name == 'Metro' else np.random.uniform(10, 40),
            'opening_date': datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 365))
        })
        store_id += 1

stores_df = pd.DataFrame(stores_data)
print(f"     ✓ Created {len(stores_df)} stores across {len(stores_df['city'].unique())} cities")

# Generate Products
print("\n  → Generating Products Catalog...")
products_data = []
prod_id = 1

for category, details in product_categories.items():
    for item in details['items']:
        cost = np.random.uniform(*details['cost_range'])
        margin_pct = np.random.uniform(*details['margin_range'])
        list_price = cost / (1 - margin_pct/100)
        
        products_data.append({
            'product_id': f'PRD{prod_id:04d}',
            'product_name': item,
            'category': category,
            'unit_cost': round(cost, 2),
            'list_price': round(list_price, 2),
            'target_margin_pct': round(margin_pct, 2),
            'is_perishable': details['perishable'],
            'avg_shelf_life_days': np.random.randint(1, 7) if details['perishable'] else np.random.randint(180, 730)
        })
        prod_id += 1

products_df = pd.DataFrame(products_data)
print(f"     ✓ Created {len(products_df)} products across {len(products_df['category'].unique())} categories")

# Generate Customers
print("\n  → Generating Customer Base...")
n_customers = 15_000
customers_data = []

for i in range(1, n_customers + 1):
    tier = np.random.choice(['Metro', 'Tier 2', 'Tier 3'], p=[0.55, 0.30, 0.15])
    tier_stores = stores_df[stores_df['region_tier'] == tier]
    primary_store = tier_stores.sample(1).iloc[0]
    
    # Customer demographics vary by tier
    if tier == 'Metro':
        age = int(np.random.normal(32, 8))
        income_bracket = np.random.choice(['25-50K', '50-75K', '75K+'], p=[0.3, 0.4, 0.3])
    elif tier == 'Tier 2':
        age = int(np.random.normal(35, 10))
        income_bracket = np.random.choice(['15-25K', '25-50K', '50-75K'], p=[0.4, 0.4, 0.2])
    else:
        age = int(np.random.normal(37, 12))
        income_bracket = np.random.choice(['10-15K', '15-25K', '25-50K'], p=[0.5, 0.4, 0.1])
    
    age = max(18, min(age, 70))
    
    customers_data.append({
        'customer_id': f'CUST{i:06d}',
        'primary_store_id': primary_store['store_id'],
        'region_tier': tier,
        'age': age,
        'income_bracket': income_bracket,
        'digital_literacy_score': np.random.uniform(4, 10) if tier == 'Metro' else np.random.uniform(3, 8),
        'registration_date': datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 450))
    })

customers_df = pd.DataFrame(customers_data)
print(f"     ✓ Created {len(customers_df)} customers")

# Generate Transactions
print("\n  → Generating Transaction History...")
n_transactions = 50_000
transactions_data = []

for i in range(1, n_transactions + 1):
    # Sample customer
    customer = customers_df.sample(1).iloc[0]
    tier = customer['region_tier']
    
    # Select store (80% primary, 20% nearby)
    if np.random.random() < 0.8:
        store_id = customer['primary_store_id']
        store = stores_df[stores_df['store_id'] == store_id].iloc[0]
    else:
        store = stores_df[stores_df['region_tier'] == tier].sample(1).iloc[0]
    
    # Select product with tier preferences
    if tier == 'Metro':
        # Metro prefers all categories
        product = products_df.sample(1).iloc[0]
    elif tier == 'Tier 2':
        # Tier 2 has less electronics/fashion
        if np.random.random() < 0.2:
            product = products_df[products_df['category'].isin(['Electronics', 'Fashion'])].sample(1).iloc[0]
        else:
            product = products_df[~products_df['category'].isin(['Electronics', 'Fashion'])].sample(1).iloc[0]
    else:
        # Tier 3 focuses on essentials
        if np.random.random() < 0.1:
            product = products_df[products_df['category'].isin(['Electronics', 'Fashion'])].sample(1).iloc[0]
        else:
            product = products_df[~products_df['category'].isin(['Electronics', 'Fashion'])].sample(1).iloc[0]
    
    # Transaction characteristics by tier
    if tier == 'Metro':
        qty = int(np.random.lognormal(1.2, 0.6))
        discount = np.random.choice([0, 5, 10, 15], p=[0.6, 0.25, 0.10, 0.05])
        delivery_time = np.random.uniform(0.5, 3)
        delivery_distance = np.random.uniform(1, 15)
        payment_method = np.random.choice(['UPI', 'Card', 'Wallet', 'COD'], p=[0.4, 0.35, 0.2, 0.05])
    elif tier == 'Tier 2':
        qty = int(np.random.lognormal(0.9, 0.6))
        discount = np.random.choice([0, 5, 10, 15, 20], p=[0.4, 0.3, 0.15, 0.10, 0.05])
        delivery_time = np.random.uniform(2, 8)
        delivery_distance = np.random.uniform(3, 30)
        payment_method = np.random.choice(['UPI', 'Card', 'Wallet', 'COD'], p=[0.35, 0.20, 0.15, 0.30])
    else:
        qty = int(np.random.lognormal(0.7, 0.5))
        discount = np.random.choice([0, 5, 10, 15, 20], p=[0.3, 0.25, 0.20, 0.15, 0.10])
        delivery_time = np.random.uniform(4, 16)
        delivery_distance = np.random.uniform(5, 60)
        payment_method = np.random.choice(['UPI', 'Card', 'Wallet', 'COD'], p=[0.25, 0.10, 0.10, 0.55])
    
    qty = max(1, min(qty, 10))
    
    # Pricing and costs
    unit_price = product['list_price'] * (1 - discount/100)
    revenue = unit_price * qty
    product_cost = product['unit_cost'] * qty
    
    # Logistics cost increases with distance and tier
    if tier == 'Metro':
        logistics_cost = delivery_distance * 2.5 + 15
    elif tier == 'Tier 2':
        logistics_cost = delivery_distance * 3.5 + 25
    else:
        logistics_cost = delivery_distance * 4.5 + 35
    
    # Spoilage cost for perishables in lower tiers
    spoilage_cost = 0
    if product['is_perishable']:
        if tier == 'Tier 2':
            spoilage_cost = product_cost * np.random.uniform(0, 0.08)
        elif tier == 'Tier 3':
            spoilage_cost = product_cost * np.random.uniform(0, 0.15)
    
    total_cost = product_cost + logistics_cost + spoilage_cost
    margin = revenue - total_cost
    margin_pct = (margin / revenue * 100) if revenue > 0 else 0
    
    # Transaction date
    days_since_registration = (datetime(2024, 9, 30) - customer['registration_date']).days
    days_back = np.random.randint(0, min(days_since_registration, 365))
    transaction_date = datetime(2024, 9, 30) - timedelta(days=days_back)
    
    transactions_data.append({
        'transaction_id': f'TXN{i:07d}',
        'transaction_date': transaction_date.date(),
        'customer_id': customer['customer_id'],
        'product_id': product['product_id'],
        'store_id': store['store_id'],
        'region_tier': tier,
        'quantity': qty,
        'unit_price': round(unit_price, 2),
        'revenue': round(revenue, 2),
        'product_cost': round(product_cost, 2),
        'logistics_cost': round(logistics_cost, 2),
        'spoilage_cost': round(spoilage_cost, 2),
        'total_cost': round(total_cost, 2),
        'margin': round(margin, 2),
        'margin_pct': round(margin_pct, 2),
        'discount_pct': discount,
        'delivery_time_hours': round(delivery_time, 2),
        'delivery_distance_km': round(delivery_distance, 2),
        'payment_method': payment_method,
        'is_perishable': product['is_perishable']
    })

transactions_df = pd.DataFrame(transactions_data)
print(f"     ✓ Created {len(transactions_df)} transactions")

# Generate Inventory Data
print("\n  → Generating Inventory Records...")
inventory_data = []
inv_id = 1

for _, store in stores_df.iterrows():
    for _, product in products_df.iterrows():
        # Not all stores carry all products (especially Tier 3)
        if store['region_tier'] == 'Tier 3' and product['category'] in ['Electronics', 'Fashion']:
            if np.random.random() < 0.6:  # 60% skip rate
                continue
        
        # Stock levels based on tier and product type
        if store['region_tier'] == 'Metro':
            stock_level = np.random.randint(50, 300)
            reorder_point = int(stock_level * 0.3)
        elif store['region_tier'] == 'Tier 2':
            stock_level = np.random.randint(20, 150)
            reorder_point = int(stock_level * 0.25)
        else:
            stock_level = np.random.randint(10, 80)
            reorder_point = int(stock_level * 0.20)
        
        # Stockout frequency
        stockout_days = np.random.randint(0, 15) if store['region_tier'] != 'Metro' else np.random.randint(0, 5)
        
        inventory_data.append({
            'inventory_id': f'INV{inv_id:06d}',
            'store_id': store['store_id'],
            'product_id': product['product_id'],
            'current_stock': stock_level,
            'reorder_point': reorder_point,
            'stockout_days_last_month': stockout_days,
            'avg_daily_sales': round(stock_level / 30, 2),
            'last_restock_date': datetime(2024, 9, 30) - timedelta(days=np.random.randint(1, 30))
        })
        inv_id += 1

inventory_df = pd.DataFrame(inventory_data)
print(f"     ✓ Created {len(inventory_df)} inventory records")

# Save all data
print("\n  → Saving datasets to CSV...")
os.makedirs('data', exist_ok=True)
transactions_df.to_csv('data/transactions.csv', index=False)
stores_df.to_csv('data/stores.csv', index=False)
products_df.to_csv('data/products.csv', index=False)
customers_df.to_csv('data/customers.csv', index=False)
inventory_df.to_csv('data/inventory.csv', index=False)
print("     ✓ All datasets saved to 'data/' folder")

# ==============================================================================
# SECTION 2: EXPLORATORY DATA ANALYSIS
# ==============================================================================

print("\n\n[2/8] EXPLORATORY DATA ANALYSIS...")
print("-" * 80)

# Regional Performance
print("\n  → Analyzing Regional Performance...")
regional_perf = transactions_df.groupby('region_tier').agg({
    'transaction_id': 'count',
    'revenue': 'sum',
    'margin': 'sum',
    'customer_id': 'nunique',
    'delivery_time_hours': 'mean',
    'delivery_distance_km': 'mean',
    'logistics_cost': 'mean',
    'spoilage_cost': 'mean'
}).round(2)

regional_perf.columns = ['Transactions', 'Total Revenue', 'Total Margin', 'Unique Customers', 
                          'Avg Delivery Time (hrs)', 'Avg Delivery Distance (km)', 
                          'Avg Logistics Cost', 'Avg Spoilage Cost']
regional_perf['Margin %'] = ((regional_perf['Total Margin'] / regional_perf['Total Revenue']) * 100).round(2)
regional_perf['Revenue per Customer'] = (regional_perf['Total Revenue'] / regional_perf['Unique Customers']).round(2)

print("\nRegional Performance Summary:")
print(regional_perf)

# Category Performance
print("\n  → Analyzing Category Performance by Region...")
txn_with_product = transactions_df.merge(products_df[['product_id', 'category']], on='product_id')
category_perf = txn_with_product.groupby(['region_tier', 'category']).agg({
    'revenue': 'sum',
    'margin': 'sum',
    'transaction_id': 'count'
}).reset_index()
category_perf['margin_pct'] = ((category_perf['margin'] / category_perf['revenue']) * 100).round(2)
print(category_perf.sort_values(['region_tier', 'revenue'], ascending=[True, False]).head(20))

# Customer Behavior
print("\n  → Analyzing Customer Behavior...")
customer_behavior = transactions_df.groupby(['customer_id', 'region_tier']).agg({
    'transaction_id': 'count',
    'revenue': 'sum',
    'margin': 'sum'
}).reset_index()
customer_behavior.columns = ['customer_id', 'region_tier', 'purchase_count', 'total_revenue', 'total_margin']

behavior_summary = customer_behavior.groupby('region_tier').agg({
    'purchase_count': 'mean',
    'total_revenue': 'mean',
    'customer_id': 'count'
}).round(2)
behavior_summary.columns = ['Avg Purchases per Customer', 'Avg Revenue per Customer', 'Total Customers']

# Repeat purchase rate
repeat_customers = customer_behavior[customer_behavior['purchase_count'] >= 3].groupby('region_tier').size()
total_customers = customer_behavior.groupby('region_tier').size()
behavior_summary['Repeat Rate %'] = ((repeat_customers / total_customers) * 100).round(2)

print("\nCustomer Behavior Summary:")
print(behavior_summary)

# ==============================================================================
# SECTION 3: VISUALIZATIONS
# ==============================================================================

print("\n\n[3/8] GENERATING VISUALIZATIONS...")
print("-" * 80)

os.makedirs('images', exist_ok=True)

# Viz 1: Regional Performance Dashboard
print("  → Creating regional performance dashboard...")
fig = plt.figure(figsize=(18, 10))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Revenue by region
ax1 = fig.add_subplot(gs[0, :])
revenue_data = regional_perf['Total Revenue'] / 1_000_000
ax1.bar(revenue_data.index, revenue_data.values, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
ax1.set_title('Total Revenue by Region (in Millions ₹)', fontsize=14, fontweight='bold')
ax1.set_ylabel('Revenue (₹M)')
for i, v in enumerate(revenue_data.values):
    ax1.text(i, v + 0.1, f'₹{v:.1f}M', ha='center', fontweight='bold')

# Margin %
ax2 = fig.add_subplot(gs[1, 0])
margin_data = regional_perf['Margin %']
ax2.bar(margin_data.index, margin_data.values, color=['#d62728', '#9467bd', '#8c564b'])
ax2.set_title('Profit Margin %', fontsize=12, fontweight='bold')
ax2.set_ylabel('Margin %')
ax2.axhline(y=margin_data.mean(), color='red', linestyle='--', label='Average')
ax2.legend()

# Delivery Time
ax3 = fig.add_subplot(gs[1, 1])
delivery_data = regional_perf['Avg Delivery Time (hrs)']
ax3.bar(delivery_data.index, delivery_data.values, color=['#e377c2', '#7f7f7f', '#bcbd22'])
ax3.set_title('Avg Delivery Time (hours)', fontsize=12, fontweight='bold')
ax3.set_ylabel('Hours')

# Logistics Cost
ax4 = fig.add_subplot(gs[1, 2])
logistics_data = regional_perf['Avg Logistics Cost']
ax4.bar(logistics_data.index, logistics_data.values, color=['#17becf', '#1f77b4', '#ff7f0e'])
ax4.set_title('Avg Logistics Cost (₹)', fontsize=12, fontweight='bold')
ax4.set_ylabel('Cost (₹)')

# Transactions by payment method
ax5 = fig.add_subplot(gs[2, 0])
payment_data = transactions_df.groupby(['region_tier', 'payment_method']).size().unstack()
payment_data.plot(kind='bar', ax=ax5, stacked=True)
ax5.set_title('Payment Methods by Region', fontsize=12, fontweight='bold')
ax5.set_ylabel('Transaction Count')
ax5.legend(title='Payment Method', bbox_to_anchor=(1.05, 1))

# Perishable vs Non-Perishable
ax6 = fig.add_subplot(gs[2, 1])
perishable_data = transactions_df.groupby(['region_tier', 'is_perishable']).size().unstack()
perishable_data_pct = (perishable_data.div(perishable_data.sum(axis=1), axis=0) * 100)
perishable_data_pct.plot(kind='bar', ax=ax6, color=['#2ca02c', '#d62728'])
ax6.set_title('Product Mix: Perishable vs Non-Perishable', fontsize=12, fontweight='bold')
ax6.set_ylabel('Percentage (%)')
ax6.legend(['Non-Perishable', 'Perishable'])

# Revenue per customer
ax7 = fig.add_subplot(gs[2, 2])
rpc_data = regional_perf['Revenue per Customer']
ax7.bar(rpc_data.index, rpc_data.values, color=['#9467bd', '#8c564b', '#e377c2'])
ax7.set_title('Revenue per Customer (₹)', fontsize=12, fontweight='bold')
ax7.set_ylabel('Revenue (₹)')

plt.savefig('images/regional_performance_dashboard.png', dpi=300, bbox_inches='tight')
print("     ✓ Saved: regional_performance_dashboard.png")
plt.close()

# Viz 2: Category Deep Dive
print("  → Creating category analysis...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Category revenue by tier
category_revenue = txn_with_product.pivot_table(values='revenue', index='category', columns='region_tier', aggfunc='sum') / 1000
category_revenue.plot(kind='barh', ax=axes[0, 0], color=['#1f77b4', '#ff7f0e', '#2ca02c'])
axes[0, 0].set_title('Revenue by Category & Region (₹ Thousands)', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Revenue (₹K)')
axes[0, 0].legend(title='Region')

# Category margin %
category_margins = category_perf.pivot_table(values='margin_pct', index='category', columns='region_tier')
category_margins.plot(kind='bar', ax=axes[0, 1], color=['#d62728', '#9467bd', '#8c564b'])
axes[0, 1].set_title('Margin % by Category & Region', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Margin %')
axes[0, 1].set_xticklabels(axes[0, 1].get_xticklabels(), rotation=45, ha='right')
axes[0, 1].legend(title='Region')

# Top products by revenue
txn_with_full_product = txn_with_product.merge(products_df[['product_id', 'product_name']], on='product_id')
top_products = txn_with_full_product.groupby('product_name')['revenue'].sum().nlargest(15) / 1000
top_products.plot(kind='barh', ax=axes[1, 0], color='teal')
axes[1, 0].set_title('Top 15 Products by Revenue (₹ Thousands)', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Revenue (₹K)')

# Discount impact on margin
discount_impact = transactions_df.groupby('discount_pct').agg({'margin_pct': 'mean', 'transaction_id': 'count'})
ax_main = axes[1, 1]
ax_main.plot(discount_impact.index, discount_impact['margin_pct'], marker='o', color='red', linewidth=2)
ax_main.set_title('Impact of Discount on Margin %', fontsize=12, fontweight='bold')
ax_main.set_xlabel('Discount %')
ax_main.set_ylabel('Avg Margin %', color='red')
ax_main.tick_params(axis='y', labelcolor='red')
ax_twin = ax_main.twinx()
ax_twin.bar(discount_impact.index, discount_impact['transaction_id'], alpha=0.3, color='gray')
ax_twin.set_ylabel('Transaction Count', color='gray')
ax_twin.tick_params(axis='y', labelcolor='gray')

plt.tight_layout()
plt.savefig('images/category_analysis.png', dpi=300, bbox_inches='tight')
print("     ✓ Saved: category_analysis.png")
plt.close()

# Viz 3: Logistics & Supply Chain
print("  → Creating logistics analysis...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Delivery distance distribution
for tier in ['Metro', 'Tier 2', 'Tier 3']:
    data = transactions_df[transactions_df['region_tier'] == tier]['delivery_distance_km']
    axes[0, 0].hist(data, bins=30, alpha=0.6, label=tier)
axes[0, 0].set_title('Delivery Distance Distribution', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Distance (km)')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].legend()

# Delivery time vs distance
for tier, color in [('Metro', 'blue'), ('Tier 2', 'orange'), ('Tier 3', 'green')]:
    data = transactions_df[transactions_df['region_tier'] == tier]
    axes[0, 1].scatter(data['delivery_distance_km'], data['delivery_time_hours'], alpha=0.3, s=5, label=tier, color=color)
axes[0, 1].set_title('Delivery Time vs Distance', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Distance (km)')
axes[0, 1].set_ylabel('Time (hours)')
axes[0, 1].legend()

# Logistics cost breakdown
logistics_breakdown = transactions_df.groupby('region_tier').agg({
    'product_cost': 'mean',
    'logistics_cost': 'mean',
    'spoilage_cost': 'mean'
})
logistics_breakdown.plot(kind='bar', stacked=True, ax=axes[1, 0], color=['#8c564b', '#e377c2', '#d62728'])
axes[1, 0].set_title('Cost Breakdown by Region', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('Avg Cost (₹)')
axes[1, 0].set_xticklabels(axes[1, 0].get_xticklabels(), rotation=0)
axes[1, 0].legend(['Product Cost', 'Logistics Cost', 'Spoilage Cost'])

# Stockout analysis
stockout_data = inventory_df.merge(stores_df[['store_id', 'region_tier']], on='store_id')
stockout_summary = stockout_data.groupby('region_tier')['stockout_days_last_month'].mean()
axes[1, 1].bar(stockout_summary.index, stockout_summary.values, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
axes[1, 1].set_title('Avg Stockout Days per Month', fontsize=12, fontweight='bold')
axes[1, 1].set_ylabel('Days')
for i, v in enumerate(stockout_summary.values):
    axes[1, 1].text(i, v + 0.2, f'{v:.1f}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('images/logistics_supply_chain.png', dpi=300, bbox_inches='tight')
print("     ✓ Saved: logistics_supply_chain.png")
plt.close()

# Viz 4: Customer Insights
print("  → Creating customer insights...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Purchase frequency distribution
for tier in ['Metro', 'Tier 2', 'Tier 3']:
    tier_cust = customer_behavior[customer_behavior['region_tier'] == tier]['purchase_count']
    axes[0, 0].hist(tier_cust, bins=20, alpha=0.6, label=tier)
axes[0, 0].set_title('Purchase Frequency Distribution', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Number of Purchases')
axes[0, 0].set_ylabel('Number of Customers')
axes[0, 0].legend()
axes[0, 0].set_xlim(0, 20)

# Customer lifetime value
cust_with_demo = customer_behavior.merge(customers_df[['customer_id', 'income_bracket', 'digital_literacy_score']], on='customer_id')
clv_data = cust_with_demo.groupby(['region_tier', 'income_bracket'])['total_revenue'].mean().unstack()
clv_data.plot(kind='bar', ax=axes[0, 1])
axes[0, 1].set_title('Avg Customer Revenue by Income Bracket', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('Avg Revenue (₹)')
axes[0, 1].set_xticklabels(axes[0, 1].get_xticklabels(), rotation=0)
axes[0, 1].legend(title='Income Bracket', bbox_to_anchor=(1.05, 1))

# Repeat rate by region
repeat_rate_data = behavior_summary['Repeat Rate %']
axes[1, 0].bar(repeat_rate_data.index, repeat_rate_data.values, color=['#2ca02c', '#ff7f0e', '#d62728'])
axes[1, 0].set_title('Customer Repeat Purchase Rate (3+ orders)', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('Repeat Rate %')
for i, v in enumerate(repeat_rate_data.values):
    axes[1, 0].text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold')

# Digital literacy impact
digital_bins = pd.cut(cust_with_demo['digital_literacy_score'], bins=[0, 4, 7, 10], labels=['Low', 'Medium', 'High'])
cust_with_demo['digital_literacy_bracket'] = digital_bins
digital_impact = cust_with_demo.groupby(['region_tier', 'digital_literacy_bracket'])['purchase_count'].mean().unstack()
digital_impact.plot(kind='bar', ax=axes[1, 1])
axes[1, 1].set_title('Avg Purchases by Digital Literacy', fontsize=12, fontweight='bold')
axes[1, 1].set_ylabel('Avg Purchase Count')
axes[1, 1].set_xticklabels(axes[1, 1].get_xticklabels(), rotation=0)
axes[1, 1].legend(title='Digital Literacy')

plt.tight_layout()
plt.savefig('images/customer_insights.png', dpi=300, bbox_inches='tight')
print("     ✓ Saved: customer_insights.png")
plt.close()

# ==============================================================================
# SECTION 4: PREDICTIVE MODELING - MARGIN RISK CLASSIFICATION
# ==============================================================================

print("\n\n[4/8] BUILDING PREDICTIVE MODELS...")
print("-" * 80)

print("\n  → Model 1: Margin Risk Classification (Low vs High Risk Stores)")

# Aggregate store performance
store_perf = transactions_df.groupby('store_id').agg({
    'revenue': 'sum',
    'margin': 'sum',
    'margin_pct': 'mean',
    'logistics_cost': 'mean',
    'spoilage_cost': 'mean',
    'delivery_time_hours': 'mean',
    'is_perishable': 'mean',
    'transaction_id': 'count'
}).reset_index()

store_perf = store_perf.merge(stores_df[['store_id', 'region_tier', 'infrastructure_score', 
                                          'warehouse_distance_km']], on='store_id')

# Define high risk: margin % < 10%
store_perf['high_risk'] = (store_perf['margin_pct'] < 10).astype(int)

print(f"     High Risk Stores: {store_perf['high_risk'].sum()} / {len(store_perf)}")

# Prepare features
X = store_perf[['revenue', 'logistics_cost', 'spoilage_cost', 'delivery_time_hours', 
                'is_perishable', 'infrastructure_score', 'warehouse_distance_km', 'transaction_id']]
y = store_perf['high_risk']

# Encode region
le = LabelEncoder()
store_perf['region_code'] = le.fit_transform(store_perf['region_tier'])
X['region_code'] = store_perf['region_code']

# Train-test split
if len(y.unique()) > 1:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    rf_model.fit(X_train_scaled, y_train)
    
    y_pred = rf_model.predict(X_test_scaled)
    
    print("\n  Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Low Risk', 'High Risk']))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n  Top Feature Importances:")
    print(feature_importance.head(10))
    
    # Save feature importance visualization
    plt.figure(figsize=(10, 6))
    plt.barh(feature_importance['feature'][:10], feature_importance['importance'][:10])
    plt.xlabel('Importance')
    plt.title('Top 10 Features for Margin Risk Prediction', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('images/feature_importance_margin_risk.png', dpi=300, bbox_inches='tight')
    print("     ✓ Saved: feature_importance_margin_risk.png")
    plt.close()

else:
    print("  ⚠ Insufficient class diversity for training")

# ==============================================================================
# SECTION 5: PREDICTIVE MODELING - CUSTOMER LIFETIME VALUE
# ==============================================================================

print("\n  → Model 2: Customer Lifetime Value Prediction")

# Prepare customer features
cust_features = customer_behavior.merge(customers_df[['customer_id', 'age', 'income_bracket', 
                                                       'digital_literacy_score', 'registration_date']], 
                                        on='customer_id')
cust_features['days_since_registration'] = (datetime(2024, 9, 30) - pd.to_datetime(cust_features['registration_date'])).dt.days

# Encode income bracket
income_mapping = {'10-15K': 1, '15-25K': 2, '25-50K': 3, '50-75K': 4, '75K+': 5}
cust_features['income_code'] = cust_features['income_bracket'].map(income_mapping)

# Features and target
X_clv = cust_features[['purchase_count', 'age', 'income_code', 'digital_literacy_score', 'days_since_registration']]
X_clv['region_code'] = le.transform(cust_features['region_tier'])
y_clv = cust_features['total_revenue']

# Train-test split
X_train_clv, X_test_clv, y_train_clv, y_test_clv = train_test_split(X_clv, y_clv, test_size=0.25, random_state=42)

# Scale
scaler_clv = StandardScaler()
X_train_clv_scaled = scaler_clv.fit_transform(X_train_clv)
X_test_clv_scaled = scaler_clv.transform(X_test_clv)

# Train Gradient Boosting
gb_model = GradientBoostingRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
gb_model.fit(X_train_clv_scaled, y_train_clv)

y_pred_clv = gb_model.predict(X_test_clv_scaled)

mae = mean_absolute_error(y_test_clv, y_pred_clv)
r2 = r2_score(y_test_clv, y_pred_clv)

print(f"\n  Model Performance:")
print(f"     MAE: ₹{mae:.2f}")
print(f"     R² Score: {r2:.4f}")

# Predicted vs Actual
plt.figure(figsize=(10, 6))
plt.scatter(y_test_clv, y_pred_clv, alpha=0.5, s=20)
plt.plot([y_test_clv.min(), y_test_clv.max()], [y_test_clv.min(), y_test_clv.max()], 'r--', lw=2)
plt.xlabel('Actual Revenue (₹)')
plt.ylabel('Predicted Revenue (₹)')
plt.title('Customer Lifetime Value: Predicted vs Actual', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('images/clv_prediction.png', dpi=300, bbox_inches='tight')
print("     ✓ Saved: clv_prediction.png")
plt.close()

# ==============================================================================
# SECTION 6: CUSTOMER SEGMENTATION
# ==============================================================================

print("\n\n[5/8] CUSTOMER SEGMENTATION (K-MEANS CLUSTERING)...")
print("-" * 80)

# Prepare clustering features
cluster_data = cust_features[['purchase_count', 'total_revenue', 'total_margin', 
                               'age', 'income_code', 'digital_literacy_score']].copy()

# Scale for clustering
scaler_cluster = StandardScaler()
cluster_scaled = scaler_cluster.fit_transform(cluster_data)

# Determine optimal k using elbow method
inertias = []
silhouette_scores = []
K_range = range(2, 8)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(cluster_scaled)
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(cluster_scaled, kmeans.labels_))

# Plot elbow curve
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].plot(K_range, inertias, marker='o')
axes[0].set_xlabel('Number of Clusters')
axes[0].set_ylabel('Inertia')
axes[0].set_title('Elbow Method', fontsize=12, fontweight='bold')

axes[1].plot(K_range, silhouette_scores, marker='o', color='green')
axes[1].set_xlabel('Number of Clusters')
axes[1].set_ylabel('Silhouette Score')
axes[1].set_title('Silhouette Score', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('images/clustering_optimization.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: clustering_optimization.png")
plt.close()

# Choose k=4
optimal_k = 4
kmeans_final = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
cust_features['cluster'] = kmeans_final.fit_predict(cluster_scaled)

# Cluster profiles
cluster_profiles = cust_features.groupby('cluster').agg({
    'customer_id': 'count',
    'purchase_count': 'mean',
    'total_revenue': 'mean',
    'total_margin': 'mean',
    'age': 'mean',
    'income_code': 'mean',
    'digital_literacy_score': 'mean'
}).round(2)

cluster_profiles.columns = ['Customer Count', 'Avg Purchases', 'Avg Revenue', 'Avg Margin', 
                             'Avg Age', 'Avg Income Code', 'Avg Digital Score']

print("\nCluster Profiles:")
print(cluster_profiles)

# Name clusters based on characteristics
cluster_names = {
    cluster_profiles['Avg Revenue'].idxmax(): 'High Value',
    cluster_profiles['Avg Purchases'].idxmax(): 'Frequent Buyers',
    cluster_profiles['Avg Revenue'].idxmin(): 'Low Engagement',
}
# The remaining cluster
remaining = [i for i in range(optimal_k) if i not in cluster_names.keys()]
if remaining:
    cluster_names[remaining[0]] = 'Moderate'

cust_features['cluster_name'] = cust_features['cluster'].map(cluster_names)

# Visualize clusters
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Cluster distribution
cluster_counts = cust_features['cluster_name'].value_counts()
axes[0].pie(cluster_counts.values, labels=cluster_counts.index, autopct='%1.1f%%', startangle=90)
axes[0].set_title('Customer Segment Distribution', fontsize=12, fontweight='bold')

# Revenue by cluster
cluster_revenue = cust_features.groupby('cluster_name')['total_revenue'].sum().sort_values(ascending=False)
axes[1].bar(cluster_revenue.index, cluster_revenue.values / 1000, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
axes[1].set_title('Total Revenue by Customer Segment (₹ Thousands)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Revenue (₹K)')
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45, ha='right')

plt.tight_layout()
plt.savefig('images/customer_segmentation.png', dpi=300, bbox_inches='tight')
print("  ✓ Saved: customer_segmentation.png")
plt.close()

# ==============================================================================
# SECTION 7: KEY INSIGHTS AND RECOMMENDATIONS
# ==============================================================================

print("\n\n[6/8] GENERATING KEY INSIGHTS...")
print("-" * 80)

insights = []

# Insight 1: Regional Margin Gap
metro_margin = regional_perf.loc['Metro', 'Margin %']
tier3_margin = regional_perf.loc['Tier 3', 'Margin %']
margin_gap = metro_margin - tier3_margin
insights.append(f"📊 Margin Gap: Tier 3 cities have {margin_gap:.1f}% lower margins than Metro ({tier3_margin:.1f}% vs {metro_margin:.1f}%)")

# Insight 2: Logistics Cost Impact
metro_logistics = regional_perf.loc['Metro', 'Avg Logistics Cost']
tier3_logistics = regional_perf.loc['Tier 3', 'Avg Logistics Cost']
logistics_increase = ((tier3_logistics - metro_logistics) / metro_logistics) * 100
insights.append(f"🚚 Logistics Challenge: Tier 3 logistics costs are {logistics_increase:.0f}% higher than Metro (₹{tier3_logistics:.2f} vs ₹{metro_logistics:.2f})")

# Insight 3: Customer Retention
metro_repeat = behavior_summary.loc['Metro', 'Repeat Rate %']
tier3_repeat = behavior_summary.loc['Tier 3', 'Repeat Rate %']
retention_gap = metro_repeat - tier3_repeat
insights.append(f"🔄 Retention Gap: Tier 3 repeat purchase rate is {retention_gap:.1f}% lower than Metro ({tier3_repeat:.1f}% vs {metro_repeat:.1f}%)")

# Insight 4: Delivery Time
metro_delivery = regional_perf.loc['Metro', 'Avg Delivery Time (hrs)']
tier3_delivery = regional_perf.loc['Tier 3', 'Avg Delivery Time (hrs)']
time_increase = tier3_delivery - metro_delivery
insights.append(f"⏱️ Delivery Delay: Tier 3 deliveries take {time_increase:.1f} hours longer than Metro ({tier3_delivery:.1f}h vs {metro_delivery:.1f}h)")

# Insight 5: Spoilage Cost
tier3_spoilage = regional_perf.loc['Tier 3', 'Avg Spoilage Cost']
metro_spoilage = regional_perf.loc['Metro', 'Avg Spoilage Cost']
spoilage_ratio = tier3_spoilage / metro_spoilage if metro_spoilage > 0 else 0
insights.append(f"📦 Spoilage Issue: Tier 3 spoilage costs are {spoilage_ratio:.1f}x higher than Metro (₹{tier3_spoilage:.2f} vs ₹{metro_spoilage:.2f})")

# Insight 6: Revenue Potential
tier2_customers = regional_perf.loc['Tier 2', 'Unique Customers']
tier3_customers = regional_perf.loc['Tier 3', 'Unique Customers']
total_untapped = tier2_customers + tier3_customers
insights.append(f"💰 Growth Potential: {total_untapped:,.0f} customers in Tier 2/3 represent untapped revenue potential")

print("\nKey Insights:")
for i, insight in enumerate(insights, 1):
    print(f"  {i}. {insight}")

# ==============================================================================
# SECTION 8: BUSINESS RECOMMENDATIONS
# ==============================================================================

print("\n\n[7/8] BUSINESS RECOMMENDATIONS...")
print("-" * 80)

recommendations = {
    "1. Optimize Last-Mile Logistics": [
        "• Establish micro-fulfillment centers in Tier 2/3 city clusters to reduce delivery distances",
        "• Partner with local logistics providers familiar with regional terrain",
        "• Implement hub-and-spoke distribution model for better cost efficiency"
    ],
    
    "2. Improve Inventory Management": [
        "• Deploy predictive analytics for demand forecasting in smaller markets",
        "• Reduce perishable inventory in Tier 3 stores (focus on non-perishables initially)",
        "• Implement FIFO (First-In-First-Out) strictly for fresh produce"
    ],
    
    "3. Tailor Product Assortment": [
        "• Focus on high-margin, non-perishable categories for Tier 3 (Groceries, Home Care)",
        "• Gradually introduce premium products based on customer digital literacy scores",
        "• Create region-specific bundles (e.g., festive packs, local preferences)"
    ],
    
    "4. Enhance Customer Retention": [
        "• Launch loyalty programs with tier-based rewards",
        "• Offer free delivery for repeat customers to boost retention in Tier 2/3",
        "• Use targeted WhatsApp marketing (high penetration in Tier 2/3)"
    ],
    
    "5. Reduce Costs Through Technology": [
        "• Deploy route optimization software to reduce delivery time and fuel costs",
        "• Implement IoT sensors for cold chain monitoring to reduce spoilage",
        "• Use AI chatbots for customer support to reduce operational overhead"
    ],
    
    "6. Payment Method Optimization": [
        "• Incentivize UPI payments in Tier 3 (currently COD-heavy) to reduce collection costs",
        "• Partner with fintech for Buy-Now-Pay-Later options to increase basket sizes",
        "• Educate customers on digital payment benefits through in-app tutorials"
    ],
    
    "7. Dynamic Pricing Strategy": [
        "• Implement location-based pricing to offset higher logistics costs",
        "• Offer strategic discounts during off-peak seasons to move inventory",
        "• Test subscription models (JioMart Plus) for guaranteed delivery slots"
    ]
}

print("\nStrategic Recommendations:")
for key, actions in recommendations.items():
    print(f"\n{key}:")
    for action in actions:
        print(f"  {action}")

# ==============================================================================
# FINAL SUMMARY
# ==============================================================================

print("\n\n[8/8] ANALYSIS SUMMARY")
print("=" * 80)

print("\n📁 Generated Files:")
print("  Data:")
print("    • data/transactions.csv")
print("    • data/stores.csv")
print("    • data/products.csv")
print("    • data/customers.csv")
print("    • data/inventory.csv")
print("\n  Visualizations:")
print("    • images/regional_performance_dashboard.png")
print("    • images/category_analysis.png")
print("    • images/logistics_supply_chain.png")
print("    • images/customer_insights.png")
print("    • images/feature_importance_margin_risk.png")
print("    • images/clv_prediction.png")
print("    • images/clustering_optimization.png")
print("    • images/customer_segmentation.png")

print("\n📊 Key Metrics:")
print(f"  • Total Transactions: {len(transactions_df):,}")
print(f"  • Total Revenue: ₹{transactions_df['revenue'].sum()/1_000_000:.2f}M")
print(f"  • Total Margin: ₹{transactions_df['margin'].sum()/1_000_000:.2f}M")
print(f"  • Unique Customers: {transactions_df['customer_id'].nunique():,}")
print(f"  • Active Stores: {len(stores_df)}")
print(f"  • Product SKUs: {len(products_df)}")

print("\n✅ COMPLETE ANALYSIS PIPELINE EXECUTED SUCCESSFULLY")
print("=" * 80)
