import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# PAGE SETTINGS
st.set_page_config(page_title="Sales Data Analysis Dashboard", layout="wide")

# TITLE
st.title("📊 Sales Data Analysis Dashboard")
st.write("Complete data analysis pipeline: Load, Clean, Analyze, Visualize and Insights")

try:
    # LOAD DATA
    df = pd.read_csv("student_data.csv")

    # CLEAN COLUMN NAMES
    df.columns = df.columns.str.strip().str.replace(" ", "_")

    st.subheader("1. Dataset Preview")
    st.dataframe(df)

    # REQUIRED COLUMNS
    required_cols = [
        "Date",
        "Product",
        "Quantity",
        "Price",
        "Customer_ID",
        "Region",
        "Total_Sales"
    ]

    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        st.error(f"Missing columns: {missing_cols}")
        st.stop()

    # DATA CLEANING
    st.subheader("2. Data Cleaning")

    st.write("Missing Values:")
    st.write(df.isnull().sum())

    # REMOVE DUPLICATES
    df = df.drop_duplicates()

    # CONVERT TO NUMERIC
    numeric_cols = ["Quantity", "Price", "Total_Sales"]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # FILL MISSING VALUES
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    st.success("Data cleaned successfully!")

    # BASIC ANALYSIS
    st.subheader("3. Basic Analysis")

    total_sales = df["Total_Sales"].sum()
    avg_sales = df["Total_Sales"].mean()
    total_products = df["Product"].nunique()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Sales", f"₹ {round(total_sales,2)}")
    col2.metric("Average Sales", f"₹ {round(avg_sales,2)}")
    col3.metric("Total Products", total_products)

    # VISUALIZATIONS
    st.subheader("4. Visualizations")

    # BAR CHART
    st.write("### Chart 1: Total Sales by Product")

    product_sales = df.groupby("Product")["Total_Sales"].sum()

    fig1, ax1 = plt.subplots()

    ax1.bar(product_sales.index, product_sales.values)

    ax1.set_xlabel("Products")
    ax1.set_ylabel("Total Sales")
    ax1.set_title("Total Sales by Product")

    plt.xticks(rotation=45)

    st.pyplot(fig1)

    # PIE CHART
    st.write("### Chart 2: Sales Distribution by Region")

    region_sales = df.groupby("Region")["Total_Sales"].sum()

    fig2, ax2 = plt.subplots()

    ax2.pie(
        region_sales.values,
        labels=region_sales.index,
        autopct='%1.1f%%'
    )

    ax2.set_title("Sales Distribution by Region")

    st.pyplot(fig2)

    # INSIGHTS
    st.subheader("5. Insights")

    best_product = product_sales.idxmax()
    best_region = region_sales.idxmax()

    st.success(f"✅ Highest selling product: {best_product}")

    st.success(f"✅ Region with highest sales: {best_region}")

    st.write("✅ Sales trends can help businesses improve decision making.")

    st.write("✅ Product-wise analysis helps identify top-performing products.")

    st.write("✅ Regional analysis helps target profitable markets.")

except FileNotFoundError:
    st.error("CSV file not found.")

except Exception as e:
    st.error(f"Error: {e}")