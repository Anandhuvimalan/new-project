# Sales and Product Data Analysis Project

Welcome to the Sales and Product Data Analysis project! This repository contains sales transaction data, product details, and a comprehensive Jupyter Notebook that performs exploratory data analysis (EDA) to derive business insights.

## 📂 Project Structure

- **`sales_transactions.csv`**: Contains detailed, row-level sales transaction records, including order dates, customer information, product identifiers, quantities, and discounts.
- **`product_master.csv`**: Contains product catalog information, including product names, categories, brands, unit costs, and unit prices.
- **`Sales_Data_Analysis.ipynb`**: A complete, step-by-step Jupyter Notebook that ingests the datasets, cleans the data, engineers new features, merges the tables, and calculates Key Performance Indicators (KPIs). It also includes several visualizations using `matplotlib` and `seaborn`.
- **`Data_Analysis_Master_Prompt.md`**: The original prompt instructions detailing the required analysis steps and notebook structure.

## 📊 Notebook Contents

The `Sales_Data_Analysis.ipynb` notebook is designed to be accessible and easy to follow. Key sections include:

1. **Basic Inspection:** Viewing data shapes and sample rows.
2. **Data Cleaning:** Converting dates and formatting numerical values like discount percentages.
3. **Feature Engineering:** Creating a monthly tracking column to analyze trends over time.
4. **Data Merging:** Joining the sales and product tables on `product_id` to form a unified master dataset.
5. **KPI Calculation:** Calculating essential metrics such as **Total Revenue**, **Total Profit**, and **Average Order Value**.
6. **Data Visualization:**
   - Bar Chart: Total Revenue by Product Category
   - Line Chart: Monthly Revenue Trend
   - Histogram: Distribution of Order Quantities

## 🚀 Getting Started

To run the analysis locally, ensure you have Python installed along with the required libraries:

```bash
pip install pandas matplotlib seaborn jupyter
```

Then, launch Jupyter and open the notebook:

```bash
jupyter notebook Sales_Data_Analysis.ipynb
```

