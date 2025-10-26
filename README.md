# JioMart Tier 2/3 Cities Expansion Analysis

## 📊 End-to-End Data Science Portfolio Project

### Business Context
**JioMart**, the digital commerce platform by Reliance Retail Ventures Ltd., is aggressively expanding into non-metro Tier 2 and Tier 3 cities across India. This project analyzes the expansion strategy, focusing on profitability optimization, logistics efficiency, and customer retention in these emerging markets.

---

## 🎯 Problem Statement

**How can JioMart optimize its expansion strategy into Tier 2/3 cities to:**
1. Improve profit margins
2. Reduce logistics and last-mile delivery costs
3. Minimize inventory spoilage
4. Enhance customer retention and repeat purchases

---

## 📋 Hypothesis

**Margin erosion and lower repeat purchase rates in Tier 2/3 cities are driven by:**
- Higher logistics and last-mile delivery costs
- Product assortment mismatch (too many perishables, wrong categories)
- Weaker customer loyalty and digital literacy
- Insufficient cold chain infrastructure leading to spoilage

---

## 📁 Project Structure

```
JIOMART EXPANSION/
│
├── complete_analysis.py          # Main analysis pipeline (data + analysis + ML)
├── README.md                      # This file
├── requirements.txt               # Python dependencies
│
├── data/                          # Generated datasets
│   ├── transactions.csv           # 50K transaction records
│   ├── customers.csv              # 15K customer profiles
│   ├── stores.csv                 # 120 stores across 24 cities
│   ├── products.csv               # 39 product SKUs
│   └── inventory.csv              # 4.5K inventory records
│
├── images/                        # Generated visualizations
│   ├── regional_performance_dashboard.png
│   ├── category_analysis.png
│   ├── logistics_supply_chain.png
│   ├── customer_insights.png
│   ├── feature_importance_margin_risk.png
│   ├── clv_prediction.png
│   ├── clustering_optimization.png
│   └── customer_segmentation.png
│
└── sql_scripts/                   # Database schema and queries
    ├── schema.sql                 # Table definitions
    ├── analytics_queries.sql      # Business intelligence queries
    └── performance_optimization.sql  # Query optimization
```

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
pip install -r requirements.txt
```

### Run Complete Analysis
```bash
python3 complete_analysis.py
```

This will:
1. Generate simulated datasets (stores, customers, products, transactions, inventory)
2. Perform exploratory data analysis
3. Create 8 comprehensive visualizations
4. Train 3 machine learning models
5. Generate business insights and recommendations

**Runtime:** ~3-5 minutes

---

## 📊 Key Metrics

| Metric | Value |
|--------|-------|
| **Total Transactions** | 50,000 |
| **Total Revenue** | ₹190.78M |
| **Total Margin** | ₹21.80M |
| **Overall Margin %** | 11.4% |
| **Unique Customers** | 14,477 |
| **Active Stores** | 120 |
| **Product SKUs** | 39 |

---

## 📈 Analysis Components

### 1. Data Generation & Simulation
Since proprietary JioMart data is unavailable, we simulate realistic transaction data:
- **Cities:** 6 Metro + 9 Tier 2 + 9 Tier 3 cities
- **Product Categories:** Groceries, Fresh Produce, Packaged Foods, Personal Care, Home Care, Electronics, Fashion
- **Customer Demographics:** Age, income bracket, digital literacy score
- **Transaction Attributes:** Revenue, costs (product, logistics, spoilage), margins, delivery metrics

### 2. Exploratory Data Analysis (EDA)
- **Regional Performance:** Revenue, margin %, customer metrics by tier
- **Category Performance:** Revenue and margin % by product category
- **Customer Behavior:** Purchase frequency, repeat rate, lifetime value
- **Logistics Analysis:** Delivery time, distance, cost breakdown
- **Inventory Management:** Stockout frequency by region

### 3. Predictive Modeling

#### Model 1: Margin Risk Classification (Random Forest)
- **Objective:** Identify high-risk stores (margin < 10%)
- **Features:** Revenue, logistics cost, spoilage, delivery time, infrastructure score
- **Performance:** See `feature_importance_margin_risk.png`

#### Model 2: Customer Lifetime Value Prediction (Gradient Boosting)
- **Objective:** Predict total customer revenue
- **Features:** Purchase count, age, income, digital literacy, days since registration
- **Metrics:** MAE, R² score

#### Model 3: Customer Segmentation (K-Means Clustering)
- **Objective:** Segment customers into actionable groups
- **Segments:** High Value, Frequent Buyers, Moderate, Low Engagement
- **Optimal K:** 4 clusters (elbow method + silhouette score)

---

## 🔍 Key Findings

### Regional Performance Summary

| Region | Transactions | Revenue (₹M) | Margin % | Avg Delivery Time | Avg Logistics Cost |
|--------|-------------|--------------|----------|-------------------|-------------------|
| Metro | 27,221 | 136.19 | 13.40% | 1.75 hrs | ₹27.89 |
| Tier 2 | 15,203 | 41.81 | 8.61% | 5.08 hrs | ₹53.68 |
| Tier 3 | 7,576 | 12.78 | -4.04% | 9.58 hrs | ₹124.58 |

### Critical Insights

1. **📊 Margin Gap:** Tier 3 cities have 17.4% lower margins than Metro (-4.04% vs 13.40%)
2. **🚚 Logistics Challenge:** Tier 3 logistics costs are 346% higher than Metro (₹124.58 vs ₹27.89)
3. **🔄 Retention Gap:** Tier 3 repeat purchase rate is lower despite similar customer counts
4. **⏱️ Delivery Delay:** Tier 3 deliveries take 7.8 hours longer than Metro (9.58h vs 1.75h)
5. **📦 Spoilage Issue:** Tier 3 spoilage costs are significantly higher due to longer transit times
6. **💰 Growth Potential:** 5,500+ customers in Tier 2/3 represent untapped revenue opportunity

---

## 💡 Strategic Recommendations

### 1. Optimize Last-Mile Logistics
- Establish micro-fulfillment centers in Tier 2/3 city clusters to reduce delivery distances
- Partner with local logistics providers familiar with regional terrain
- Implement hub-and-spoke distribution model for better cost efficiency

### 2. Improve Inventory Management
- Deploy predictive analytics for demand forecasting in smaller markets
- Reduce perishable inventory in Tier 3 stores (focus on non-perishables initially)
- Implement FIFO (First-In-First-Out) strictly for fresh produce

### 3. Tailor Product Assortment
- Focus on high-margin, non-perishable categories for Tier 3 (Groceries, Home Care)
- Gradually introduce premium products based on customer digital literacy scores
- Create region-specific bundles (e.g., festive packs, local preferences)

### 4. Enhance Customer Retention
- Launch loyalty programs with tier-based rewards
- Offer free delivery for repeat customers to boost retention in Tier 2/3
- Use targeted WhatsApp marketing (high penetration in Tier 2/3)

### 5. Reduce Costs Through Technology
- Deploy route optimization software to reduce delivery time and fuel costs
- Implement IoT sensors for cold chain monitoring to reduce spoilage
- Use AI chatbots for customer support to reduce operational overhead

### 6. Payment Method Optimization
- Incentivize UPI payments in Tier 3 (currently COD-heavy) to reduce collection costs
- Partner with fintech for Buy-Now-Pay-Later options to increase basket sizes
- Educate customers on digital payment benefits through in-app tutorials

### 7. Dynamic Pricing Strategy
- Implement location-based pricing to offset higher logistics costs
- Offer strategic discounts during off-peak seasons to move inventory
- Test subscription models (JioMart Plus) for guaranteed delivery slots

---

## 🛠️ Technologies Used

- **Data Processing:** pandas, numpy
- **Visualization:** matplotlib, seaborn
- **Machine Learning:** scikit-learn (RandomForest, GradientBoosting, KMeans)
- **Statistical Analysis:** Python datetime, scipy (implicit)

---

## 📚 Data Dictionary

See `DATA_DICTIONARY.md` for detailed field descriptions of all datasets.

---

## 🔗 SQL Database Design

For enterprise deployment, SQL schemas and analytical queries are provided in `sql_scripts/`:
- `schema.sql`: Table definitions with constraints
- `analytics_queries.sql`: Pre-built business intelligence queries
- `performance_optimization.sql`: Indexing and query optimization

---

## 📧 Contact

**Project Author:** Data Science Portfolio  
**Purpose:** Demonstrating end-to-end data science capabilities for retail analytics

---

## 📄 License

This project is for educational and portfolio purposes. Data is simulated and does not represent actual JioMart operations.

---

## 🙏 Acknowledgments

- JioMart expansion data publicly available through news reports
- Indian city demographics from Census 2011
- Retail industry benchmarks from IBEF reports

---

## 🔄 Future Enhancements

1. **Real-time Dashboard:** Build Streamlit/Dash app for interactive analysis
2. **Time Series Forecasting:** Predict future revenue trends using Prophet/ARIMA
3. **Geospatial Analysis:** Heatmaps showing delivery efficiency by location
4. **A/B Testing Framework:** Simulate discount experiments
5. **Churn Prediction:** Identify at-risk customers before they churn
