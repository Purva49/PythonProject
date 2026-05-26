import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Customer Sales Analysis", layout="wide")

st.title("📊 Customer Sales Analysis Dashboard")
st.write("Advanced pandas project with merging, aggregation, pivot tables and visualizations.")

try:
    sales = pd.read_csv("sales_data.csv")
    customers = pd.read_csv("customer_churn.csv")

    st.subheader("1. Data Loading & Exploration")
    st.write("Sales Data")
    st.dataframe(sales)

    st.write("Customer Data")
    st.dataframe(customers)

    required_sales_cols = ["Order_ID", "Date", "Customer_ID", "Product", "Category", "Quantity", "Price"]
    required_customer_cols = ["Customer_ID", "Customer_Name", "Region", "Age", "Gender"]

    if not all(col in sales.columns for col in required_sales_cols):
        st.error("Sales dataset has missing columns.")
        st.stop()

    if not all(col in customers.columns for col in required_customer_cols):
        st.error("Customer dataset has missing columns.")
        st.stop()

    st.subheader("2. Data Cleaning & Preparation")

    sales = sales.drop_duplicates()
    customers = customers.drop_duplicates()

    sales["Date"] = pd.to_datetime(sales["Date"], errors="coerce")
    sales["Quantity"] = pd.to_numeric(sales["Quantity"], errors="coerce")
    sales["Price"] = pd.to_numeric(sales["Price"], errors="coerce")

    sales["Quantity"] = sales["Quantity"].fillna(sales["Quantity"].mean())
    sales["Price"] = sales["Price"].fillna(sales["Price"].mean())

    sales["Total_Sales"] = sales["Quantity"] * sales["Price"]
    sales["Month"] = sales["Date"].dt.month_name()

    df = pd.merge(sales, customers, on="Customer_ID", how="left")

    st.success("Data cleaned and merged successfully!")
    st.dataframe(df)

    st.subheader("3. Key Metrics")

    total_revenue = df["Total_Sales"].sum()
    total_customers = df["Customer_ID"].nunique()
    avg_order_value = df["Total_Sales"].mean()

    top_customer_data = df.groupby("Customer_Name")["Total_Sales"].sum().idxmax()
    top_customer_sales = df.groupby("Customer_Name")["Total_Sales"].sum().max()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue", f"₹ {total_revenue:,.0f}")
    col2.metric("Total Customers", total_customers)
    col3.metric("Average Order Value", f"₹ {avg_order_value:,.0f}")
    col4.metric("Top Customer", top_customer_data)

    st.subheader("4. Aggregations")

    st.write("### Aggregation 1: Revenue by Customer")
    customer_sales = df.groupby("Customer_Name")["Total_Sales"].sum().sort_values(ascending=False)
    st.dataframe(customer_sales)

    st.write("### Aggregation 2: Revenue by Product")
    product_sales = df.groupby("Product")["Total_Sales"].sum().sort_values(ascending=False)
    st.dataframe(product_sales)

    st.write("### Aggregation 3: Revenue by Region")
    region_sales = df.groupby("Region")["Total_Sales"].sum().sort_values(ascending=False)
    st.dataframe(region_sales)

    st.subheader("5. Pivot Table Summary")

    pivot_table = pd.pivot_table(
        df,
        values="Total_Sales",
        index="Region",
        columns="Category",
        aggfunc="sum",
        fill_value=0
    )

    st.dataframe(pivot_table)

    st.subheader("6. Professional Visualizations")

    st.write("### Chart 1: Revenue by Region")
    fig1, ax1 = plt.subplots()
    ax1.bar(region_sales.index, region_sales.values)
    ax1.set_xlabel("Region")
    ax1.set_ylabel("Revenue")
    ax1.set_title("Revenue by Region")
    st.pyplot(fig1)

    st.write("### Chart 2: Product-wise Sales")
    fig2, ax2 = plt.subplots()
    ax2.pie(product_sales.values, labels=product_sales.index, autopct="%1.1f%%")
    ax2.set_title("Product-wise Sales Distribution")
    st.pyplot(fig2)

    st.write("### Chart 3: Monthly Sales Trend")
    monthly_sales = df.groupby("Month")["Total_Sales"].sum()

    fig3, ax3 = plt.subplots()
    ax3.plot(monthly_sales.index, monthly_sales.values, marker="o")
    ax3.set_xlabel("Month")
    ax3.set_ylabel("Revenue")
    ax3.set_title("Monthly Sales Trend")
    plt.xticks(rotation=45)
    st.pyplot(fig3)

    st.write("### Chart 4: Category-wise Sales")
    category_sales = df.groupby("Category")["Total_Sales"].sum()

    fig4, ax4 = plt.subplots()
    ax4.bar(category_sales.index, category_sales.values)
    ax4.set_xlabel("Category")
    ax4.set_ylabel("Revenue")
    ax4.set_title("Category-wise Sales")
    st.pyplot(fig4)

    st.subheader("7. Business Insights & Recommendations")

    best_region = region_sales.idxmax()
    best_product = product_sales.idxmax()
    best_category = category_sales.idxmax()

    st.success(f"✅ Total Revenue: ₹ {total_revenue:,.0f}")
    st.success(f"✅ Total Customers: {total_customers}")
    st.success(f"✅ Average Order Value: ₹ {avg_order_value:,.0f}")
    st.success(f"✅ Top Customer: {top_customer_data} - ₹ {top_customer_sales:,.0f}")

    st.write(f"✅ Best performing region is **{best_region}**.")
    st.write(f"✅ Best selling product is **{best_product}**.")
    st.write(f"✅ Best performing category is **{best_category}**.")
    st.write("✅ Business should focus more marketing on high-revenue regions.")
    st.write("✅ Top customers can be targeted with loyalty offers.")
    st.write("✅ Low-selling products can be improved through discounts or promotions.")

except FileNotFoundError:
    st.error("CSV file not found. Please check sales_data.csv and customer_churn.csv.")

except Exception as e:
    st.error(f"Error: {e}")