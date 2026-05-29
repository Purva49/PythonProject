import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm

st.set_page_config(page_title="Statistical Business Analysis", layout="wide")

st.title("📊 Statistical Business Analysis Dashboard")
st.write("Hypothesis testing, correlation analysis, confidence intervals, and regression analysis")

try:
    df = pd.read_csv("sales_data.csv")

    df.columns = df.columns.str.strip().str.replace(" ", "_")

    if "Total_Sales" not in df.columns:
        df["Total_Sales"] = df["Quantity"] * df["Price"]

    if "Marketing_Spend" not in df.columns:
        df["Marketing_Spend"] = df["Total_Sales"] * 0.12

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Month"] = df["Date"].dt.month_name()

    numeric_cols = ["Quantity", "Price", "Total_Sales", "Marketing_Spend"]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    st.subheader("1. Dataset Preview")
    st.dataframe(df)

    st.subheader("2. Descriptive Statistics")
    st.dataframe(df[numeric_cols].describe())

    mean_sales = df["Total_Sales"].mean()
    median_sales = df["Total_Sales"].median()
    mode_sales = df["Total_Sales"].mode()[0]
    std_sales = df["Total_Sales"].std()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mean Sales", f"₹ {mean_sales:,.2f}")
    col2.metric("Median Sales", f"₹ {median_sales:,.2f}")
    col3.metric("Mode Sales", f"₹ {mode_sales:,.2f}")
    col4.metric("Std Deviation", f"₹ {std_sales:,.2f}")

    st.subheader("3. Distribution Analysis")

    fig1, ax1 = plt.subplots()
    sns.histplot(df["Total_Sales"], kde=True, ax=ax1)
    ax1.set_title("Sales Distribution")
    st.pyplot(fig1)

    shapiro_stat, shapiro_p = stats.shapiro(df["Total_Sales"])

    if shapiro_p > 0.05:
        st.success(f"Normality Test: p = {shapiro_p:.4f}. Sales data looks normally distributed.")
    else:
        st.warning(f"Normality Test: p = {shapiro_p:.4f}. Sales data may not be normally distributed.")

    st.subheader("4. Correlation Analysis")

    corr = df[numeric_cols].corr()

    fig2, ax2 = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="viridis", ax=ax2)
    ax2.set_title("Correlation Heatmap")
    st.pyplot(fig2)

    pearson_corr, pearson_p = stats.pearsonr(df["Marketing_Spend"], df["Total_Sales"])

    st.write(f"**Correlation between Marketing Spend and Sales:** {pearson_corr:.2f}")
    st.write(f"**P-value:** {pearson_p:.4f}")

    st.subheader("5. Hypothesis Testing")

    st.write("### Test 1: One Sample T-Test")
    t_stat, p_value = stats.ttest_1samp(df["Total_Sales"], 45000)
    st.write(f"T-statistic: {t_stat:.4f}")
    st.write(f"P-value: {p_value:.4f}")

    if p_value < 0.05:
        st.success("Result: Average sales are significantly different from ₹45,000.")
    else:
        st.info("Result: Average sales are not significantly different from ₹45,000.")

    st.write("### Test 2: Independent T-Test by Quantity Group")

    low_qty = df[df["Quantity"] <= df["Quantity"].median()]["Total_Sales"]
    high_qty = df[df["Quantity"] > df["Quantity"].median()]["Total_Sales"]

    if len(low_qty) > 1 and len(high_qty) > 1:
        t_stat2, p_value2 = stats.ttest_ind(low_qty, high_qty)
        st.write(f"T-statistic: {t_stat2:.4f}")
        st.write(f"P-value: {p_value2:.4f}")
    else:
        st.warning("Not enough data for independent t-test.")

    st.write("### Test 3: ANOVA Test by Product")

    product_groups = [
        group["Total_Sales"].values
        for name, group in df.groupby("Product")
        if len(group) > 1
    ]

    if len(product_groups) >= 2:
        f_stat, anova_p = stats.f_oneway(*product_groups)
        st.write(f"F-statistic: {f_stat:.4f}")
        st.write(f"P-value: {anova_p:.4f}")
    else:
        st.warning("Not enough repeated product data for ANOVA.")

    st.subheader("6. 95% Confidence Interval")

    confidence = 0.95
    n = len(df["Total_Sales"])
    margin_error = stats.sem(df["Total_Sales"]) * stats.t.ppf((1 + confidence) / 2, n - 1)

    ci_lower = mean_sales - margin_error
    ci_upper = mean_sales + margin_error

    st.success(f"Average Sales: ₹ {mean_sales:,.2f} ± ₹ {margin_error:,.2f}")
    st.write(f"95% Confidence Interval: ₹ {ci_lower:,.2f} to ₹ {ci_upper:,.2f}")

    st.subheader("7. Regression Analysis")

    X = df["Marketing_Spend"]
    y = df["Total_Sales"]

    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()

    st.write("### Regression Summary")
    st.text(model.summary())

    r_squared = model.rsquared
    regression_p = model.pvalues["Marketing_Spend"]

    st.metric("R-squared", round(r_squared, 4))
    st.metric("Marketing Spend P-value", round(regression_p, 4))

    fig3, ax3 = plt.subplots()
    sns.regplot(x="Marketing_Spend", y="Total_Sales", data=df, ax=ax3)
    ax3.set_title("Regression: Marketing Spend vs Sales")
    st.pyplot(fig3)

    st.subheader("8. Statistical Analysis Report")

    st.success(f"Average Sales: ₹ {mean_sales:,.2f} ± ₹ {margin_error:,.2f} 95% CI")
    st.success(f"Correlation Sales-Marketing: {pearson_corr:.2f}")

    if regression_p < 0.05:
        st.success(f"Marketing affects sales: p = {regression_p:.4f} ✓ Significant")
    else:
        st.warning(f"Marketing effect is not statistically significant: p = {regression_p:.4f}")

    st.subheader("9. Business Recommendations")

    st.write("✅ Increase marketing investment if correlation remains strong.")
    st.write("✅ Focus on products with consistently higher sales.")
    st.write("✅ Use regression results to predict future revenue.")
    st.write("✅ Monitor sales distribution to detect unusual business patterns.")
    st.write("✅ Use confidence intervals for realistic sales forecasting.")

except FileNotFoundError:
    st.error("CSV file not found. Please check sales_data.csv.")

except Exception as e:
    st.error(f"Error: {e}")