import streamlit as st
import pandas as pd

# Load CSV file
df = pd.read_csv("sales_data.csv")

st.title("📊 Sales Data Dashboard")

# Show dataset
st.subheader("Dataset")
st.write(df)

# Total revenue
total_revenue = df['Total_Sales'].sum()

st.success(f"Total Revenue: ₹{total_revenue:,.2f}")

# Best product
best_product = df.groupby('Product')['Quantity'].sum().idxmax()

st.info(f"Best Selling Product: {best_product}")

# Average sales
average_sales = df['Total_Sales'].mean()

st.warning(f"Average Sales: ₹{average_sales:,.2f}")