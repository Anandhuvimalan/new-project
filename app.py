import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Sales Data Analysis API", layout="wide")
sns.set_theme(style="whitegrid")

st.title("📊 Sales and Product Data Dashboard")
st.markdown("This dashboard analyzes our raw sales transactions and product datasets to derive actionable business insights.")

@st.cache_data
def load_data():
    # Load the datasets
    sales = pd.read_csv('sales_transactions.csv')
    products = pd.read_csv('product_master.csv')
    
    # 1. Data Cleaning
    sales['order_date'] = pd.to_datetime(sales['order_date'], format='mixed')
    sales['discount_pct'] = sales['discount_pct'].str.replace('%', '', regex=False).astype(float) / 100
    
    # 2. Feature Engineering
    sales['order_month'] = sales['order_date'].dt.to_period('M')
    
    # 3. Merge Datasets
    master_df = sales.merge(products, on='product_id', how='left')
    
    # Calculate Financials
    master_df['revenue'] = master_df['quantity'] * master_df['unit_price'] * (1 - master_df['discount_pct'])
    master_df['profit'] = master_df['revenue'] - (master_df['quantity'] * master_df['unit_cost'])
    
    return master_df

# Load data utilizing Streamlit's caching
master_df = load_data()

# Extract Year for filtering
master_df['order_year'] = master_df['order_date'].dt.year
available_years = sorted(master_df['order_year'].dropna().unique().tolist())

# Sidebar Filter
st.sidebar.header("Filters")
selected_year = st.sidebar.selectbox("Select Year", ["All Years"] + available_years)

if selected_year != "All Years":
    master_df = master_df[master_df['order_year'] == selected_year]

# --- KPI SECTION ---
st.header(f"Key Performance Indicators {'(All Years)' if selected_year == 'All Years' else f'({selected_year})'}")
col1, col2, col3, col4 = st.columns(4)

total_revenue = master_df['revenue'].sum()
total_profit = master_df['profit'].sum()
total_orders = master_df['order_id'].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Avg Order Value", f"${avg_order_value:,.2f}")

st.divider()

# --- CHARTS SECTION ---
st.header("Data Visualizations")
tab1, tab2, tab3 = st.tabs(["Revenue by Category", "Monthly Trend", "Order Quantities"])

with tab1:
    st.subheader("Total Revenue by Product Category")
    st.markdown("Easily identify which product categories bring in the most money.")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    cat_rev = master_df.groupby('category')['revenue'].sum().sort_values(ascending=False).reset_index()
    sns.barplot(data=cat_rev, x='category', y='revenue', palette='viridis', ax=ax1)
    ax1.set_xlabel('Category')
    ax1.set_ylabel('Revenue ($)')
    st.pyplot(fig1)

with tab2:
    st.subheader("Monthly Revenue Trend")
    st.markdown("Spot peaks and valleys in sales throughout the year.")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    monthly_rev = master_df.groupby('order_month')['revenue'].sum()
    # Convert period index to string so pyplot can graph it
    monthly_rev.index = monthly_rev.index.astype(str)
    ax2.plot(monthly_rev.index, monthly_rev.values, marker='o', linestyle='-', color='b')
    plt.xticks(rotation=45)
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Revenue ($)')
    st.pyplot(fig2)

with tab3:
    st.subheader("Distribution of Order Quantities")
    st.markdown("Understand whether customers typically buy in bulk or order single items at a time.")
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    sns.histplot(master_df['quantity'], bins=20, kde=True, color='purple', ax=ax3)
    ax3.set_xlabel('Quantity Ordered')
    ax3.set_ylabel('Frequency (Number of Orders)')
    st.pyplot(fig3)

# Data Preview Feature
st.divider()
if st.checkbox("Show Raw Master Data"):
    st.subheader("Raw Data View")
    st.dataframe(master_df)

# Sidebar
st.sidebar.header("About")
st.sidebar.info("This dashboard translates the Data Analysis originally generated in our Jupyter Notebook into an interactive Streamlit application.")
