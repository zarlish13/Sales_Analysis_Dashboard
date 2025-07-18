import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from Google Sheets
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vROprV7Ojc9h4AaVF_tfrwVqPuFh1yGWfnuAOMBFTCMbzBGbu4gElFDYFxmm_8rgvJYB2I-qsKmg17y/pub?output=csv"
df = pd.read_csv(url)

# Set page config
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Title
st.title("📊 Sales Data Analysis Dashboard")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("🛍️ Total Sales", f"${df['Sales'].sum():,.0f}")
col2.metric("💰 Total Profit", f"${df['Profit'].sum():,.0f}")
col3.metric("📦 Total Orders", f"{df.shape[0]}")

st.markdown("---")

st.subheader("📉 Sales vs Profit")

# Create centered layout using columns
col1, col2, col3 = st.columns([1, 2, 1])  # middle column is wider

with col2:  # only plot in the center
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(x="Sales", y="Profit", data=df, ax=ax)
    ax.set_title("Sales vs Profit")
    st.pyplot(fig)


st.subheader("🏆 Top 10 Products by Sales")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    top_products = df.groupby("Product")["Sales"].sum().reset_index().sort_values("Sales", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x="Sales", y="Product", data=top_products, ax=ax, palette="viridis")
    ax.set_title("Top Products by Sales")
    st.pyplot(fig)



st.subheader("📦 Sales by Category")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    category_sales = df.groupby("Category")["Sales"].sum().reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x="Category", y="Sales", data=category_sales, ax=ax, palette="magma")
    ax.set_title("Sales by Category")
    st.pyplot(fig)



st.subheader("📅 Monthly Sales Trend")

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
monthly_sales = df.groupby("Month")["Sales"].sum().reset_index()

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.lineplot(x="Month", y="Sales", data=monthly_sales, marker="o", ax=ax)
    ax.set_title("Monthly Sales Over Time")
    plt.xticks(rotation=45)
    st.pyplot(fig)


st.subheader("💰 Profit by Category")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    category_profit = df.groupby("Category")["Profit"].sum().reset_index().sort_values("Profit", ascending=False)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x="Category", y="Profit", data=category_profit, ax=ax, palette="coolwarm")
    ax.set_title("Profit by Category")
    st.pyplot(fig)


df.columns = df.columns.str.strip()

st.markdown("---")


# Raw Data
with st.expander("🔍 View Raw Data"):
    st.dataframe(df)
