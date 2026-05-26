import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Advanced Sales Visualization Dashboard", layout="wide")

st.title("📊 Advanced Sales Visualization Dashboard")
st.write("Seaborn statistical plots + Plotly interactive charts + professional dashboard layout")

sns.set_theme(style="whitegrid", palette="viridis")

try:
    sales = pd.read_csv("sales_data.csv")
    customers = pd.read_csv("customer_churn.csv")

    sales.columns = sales.columns.str.strip().str.replace(" ", "_")
    customers.columns = customers.columns.str.strip().str.replace(" ", "_")

    if "CustomerID" in sales.columns:
        sales.rename(columns={"CustomerID": "Customer_ID"}, inplace=True)

    if "CustomerID" in customers.columns:
        customers.rename(columns={"CustomerID": "Customer_ID"}, inplace=True)

    if "Customer_Id" in sales.columns:
        sales.rename(columns={"Customer_Id": "Customer_ID"}, inplace=True)

    if "Customer_Id" in customers.columns:
        customers.rename(columns={"Customer_Id": "Customer_ID"}, inplace=True)

    if "Category" not in sales.columns:
        sales["Category"] = sales["Product"]

    if "Customer_ID" not in sales.columns:
        st.error("Customer_ID column not found in sales_data.csv")
        st.write(sales.columns.tolist())
        st.stop()

    if "Customer_ID" not in customers.columns:
        st.error("Customer_ID column not found in customer_data.csv")
        st.write(customers.columns.tolist())
        st.stop()

    sales["Date"] = pd.to_datetime(sales["Date"], errors="coerce")
    sales["Quantity"] = pd.to_numeric(sales["Quantity"], errors="coerce")
    sales["Price"] = pd.to_numeric(sales["Price"], errors="coerce")

    sales = sales.drop_duplicates()
    customers = customers.drop_duplicates()

    sales["Quantity"] = sales["Quantity"].fillna(sales["Quantity"].mean())
    sales["Price"] = sales["Price"].fillna(sales["Price"].mean())

    sales["Total_Sales"] = sales["Quantity"] * sales["Price"]
    sales["Month"] = sales["Date"].dt.month_name()

    df = pd.merge(sales, customers, on="Customer_ID", how="left")

    if "Region" not in df.columns:
        df["Region"] = "Unknown"

    if "Age" not in df.columns:
        df["Age"] = 25

    st.sidebar.header("Filters")

    selected_region = st.sidebar.multiselect(
        "Select Region",
        df["Region"].dropna().unique(),
        default=df["Region"].dropna().unique()
    )

    selected_category = st.sidebar.multiselect(
        "Select Category",
        df["Category"].dropna().unique(),
        default=df["Category"].dropna().unique()
    )

    filtered_df = df[
        (df["Region"].isin(selected_region)) &
        (df["Category"].isin(selected_category))
    ]

    total_revenue = filtered_df["Total_Sales"].sum()
    total_customers = filtered_df["Customer_ID"].nunique()
    avg_order_value = filtered_df["Total_Sales"].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Revenue", f"₹ {total_revenue:,.0f}")
    col2.metric("Total Customers", total_customers)
    col3.metric("Average Order Value", f"₹ {avg_order_value:,.0f}")

    st.subheader("Dataset Preview")
    st.dataframe(filtered_df)

    st.subheader("1. Box Plot: Price Distribution by Category")
    fig1, ax1 = plt.subplots()
    sns.boxplot(x="Category", y="Price", data=filtered_df, ax=ax1)
    ax1.set_title("Price Distribution by Category")
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    st.subheader("2. Violin Plot: Sales Distribution by Region")
    fig2, ax2 = plt.subplots()
    sns.violinplot(x="Region", y="Total_Sales", data=filtered_df, ax=ax2)
    ax2.set_title("Sales Distribution by Region")
    st.pyplot(fig2)

    st.subheader("3. Correlation Heatmap")
    numeric_df = filtered_df[["Quantity", "Price", "Total_Sales", "Age"]]

    fig3, ax3 = plt.subplots()
    sns.heatmap(numeric_df.corr(), annot=True, cmap="viridis", ax=ax3)
    ax3.set_title("Correlation Heatmap")
    st.pyplot(fig3)

    st.subheader("4. Interactive Bar Chart: Revenue by Product")
    product_sales = filtered_df.groupby("Product")["Total_Sales"].sum().reset_index()

    fig4 = px.bar(
        product_sales,
        x="Product",
        y="Total_Sales",
        color="Product",
        title="Interactive Revenue by Product"
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("5. Interactive Scatter Plot: Price vs Total Sales")
    fig5 = px.scatter(
        filtered_df,
        x="Price",
        y="Total_Sales",
        color="Category",
        size="Quantity",
        hover_data=["Product", "Customer_ID", "Region"],
        title="Price vs Total Sales"
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("6. Interactive Pie Chart: Regional Revenue Share")
    region_sales = filtered_df.groupby("Region")["Total_Sales"].sum().reset_index()

    fig6 = px.pie(
        region_sales,
        names="Region",
        values="Total_Sales",
        title="Regional Revenue Share"
    )
    st.plotly_chart(fig6, use_container_width=True)

    st.subheader("Business Insights")

    if not product_sales.empty:
        best_product = product_sales.loc[product_sales["Total_Sales"].idxmax(), "Product"]
        st.success(f"✅ Best-selling product is {best_product}.")

    if not region_sales.empty:
        best_region = region_sales.loc[region_sales["Total_Sales"].idxmax(), "Region"]
        st.success(f"✅ Highest revenue region is {best_region}.")

    st.write("✅ Box plot compares price distribution across categories.")
    st.write("✅ Violin plot shows sales distribution across regions.")
    st.write("✅ Heatmap shows correlation between numerical columns.")
    st.write("✅ Plotly charts provide hover effects and interactive visualization.")

except FileNotFoundError:
    st.error("CSV files not found. Please check sales_data.csv and customer_data.csv.")

except Exception as e:
    st.error(f"Error: {e}")