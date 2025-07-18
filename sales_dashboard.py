# ---------------------------------------------
# Sales Data Analysis Dashboard (SQL + EDA)
# ---------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Step 1: Load dataset
df = pd.read_csv("superstore.csv")
print("✅ Data loaded successfully!")

# Step 2: Clean the data
df.dropna(inplace=True)
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
df['order_date'] = pd.to_datetime(df['order_date'])
df['ship_date'] = pd.to_datetime(df['ship_date'])
df.drop_duplicates(inplace=True)

# Step 3: Save to SQLite
conn = sqlite3.connect("sales_data.db")
df.to_sql("sales", conn, if_exists="replace", index=False)

# Step 4: SQL Queries
query1 = """
SELECT category, SUM(sales) AS total_sales
FROM sales
GROUP BY category
ORDER BY total_sales DESC;
"""

query2 = """
SELECT product_name, SUM(quantity) AS total_quantity
FROM sales
GROUP BY product_name
ORDER BY total_quantity DESC
LIMIT 5;
"""

query3 = """
SELECT strftime('%Y-%m', order_date) AS month, SUM(sales) AS total_sales
FROM sales
GROUP BY month
ORDER BY month;
"""

df_cat_sales = pd.read_sql(query1, conn)
df_top_products = pd.read_sql(query2, conn)
df_monthly_sales = pd.read_sql(query3, conn)
conn.close()


