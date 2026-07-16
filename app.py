import pandas as pd 
# Load the CSV file
df = pd.read_csv("sales_data.csv")
# Look at the first 5 rows
print(df.head())
# Basic info about columns and data types
print(df.info())
# Total sales
print("Total Sales:", df["Net_Sales"].sum())

# Sales grouped by Region
print(df.groupby("Region")["Net_Sales"].sum())

import numpy as np
# Find outlier orders using the IQR method
Q1 = np.percentile(df["Net_Sales"], 25)
Q3 = np.percentile(df["Net_Sales"], 75)
IQR = Q3 - Q1
upper_bound = Q3 + 1.5 * IQR
lower_bound = Q1 - 1.5 * IQR

outliers = df[(df["Net_Sales"] > upper_bound) | (df["Net_Sales"] < lower_bound)]
print("Number of outlier orders:", len(outliers))

# Correlation between Discount % and Quantity sold
correlation = df["Discount_Pct"].corr(df["Quantity"])
print("Correlation:", correlation)
# Q1 — Total & average sales
print("Q1. Total Net Sales:", df["Net_Sales"].sum())
print("Q1. Average Order Value:", df["Net_Sales"].mean())
#Q3 — Sales by Category
category_sales = df.groupby("Category")["Net_Sales"].sum().sort_values(ascending=False)
print("Q3. Sales by Category:\n", category_sales)
#Q4 — Top 10 best-selling products
top_products = df.groupby("Product")["Net_Sales"].sum().sort_values(ascending=False).head(10)
print("Q4. Top 10 Products:\n", top_products)
#Q6 — Average profit margin
df["Profit_Margin_Pct"] = (df["Profit"] / df["Net_Sales"]) * 100
print("Q6. Average Profit Margin:", df["Profit_Margin_Pct"].mean())
#Q7 — Most profitable category
category_profit = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
print("Q7. Profit by Category:\n", category_profit)
#Q8 -Sales by customer segment
segment_sales = df.groupby("Customer_Segment")["Net_Sales"].sum()
print("Q8. Sales by Segment:\n", segment_sales)
#Q9 — Popular payment methods
payment_counts = df["Payment_Method"].value_counts()
print("Q9. Payment Method Popularity:\n", payment_counts)
#Q10 — Sales rep performance
rep_sales = df.groupby("Sales_Rep")["Net_Sales"].sum().sort_values(ascending=False)
print("Q10. Sales Rep Performance:\n", rep_sales)
#Q11 — Sales by weekday
rep_sales = df.groupby("Sales_Rep")["Net_Sales"].sum().sort_values(ascending=False)
print("Q11. Sales Rep Performance:\n", rep_sales)
#Q12 — Rating vs average sales
rating_sales = df.groupby("Customer_Rating")["Net_Sales"].mean()
print("Q12. Avg Sales by Rating:\n", rating_sales)
######################################################################
import matplotlib.pyplot as plt

# Chart 1: Sales by Region (bar chart)
region_sales = df.groupby("Region")["Net_Sales"].sum().sort_values(ascending=False)
plt.figure(figsize=(7,5))
plt.bar(region_sales.index, region_sales.values, color="steelblue")
plt.title("Total Sales by Region")
plt.ylabel("Net Sales")
plt.xlabel("Region")
plt.savefig("region_sales_chart.png")   # saves the chart as an image file
plt.show()                               # opens a window showing the chart
# Chart 2: Monthly sales trend (line chart)
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
monthly_sales = df.groupby("Month")["Net_Sales"].sum()

plt.figure(figsize=(10,5))
plt.plot(monthly_sales.index, monthly_sales.values, marker="o", color="darkorange")
plt.title("Monthly Sales Trend")
plt.xticks(rotation=45)
plt.ylabel("Net Sales")
plt.tight_layout()
plt.savefig("monthly_trend_chart.png")
plt.show()
###################################################################################################################
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# ----------------------------- PAGE CONFIG -----------------------------
st.set_page_config(page_title="Sales Analytics Dashboard", page_icon="📊", layout="wide")

"""
Sales Analytics Dashboard
Built with Streamlit + Pandas + NumPy + Matplotlib
Run with:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------- PAGE CONFIG -----------------------------
st.set_page_config(page_title="Sales Analytics Dashboard", page_icon="📊", layout="wide")

# ----------------------------- LOAD DATA -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv", parse_dates=["Order_Date"])
    df["Customer_Rating"] = df["Customer_Rating"].fillna(df["Customer_Rating"].median())
    df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
    df["Weekday"] = df["Order_Date"].dt.day_name()
    df["Profit_Margin_Pct"] = (df["Profit"] / df["Net_Sales"]) * 100
    bins = [17, 25, 35, 45, 55, 65]
    labels = ["18-25", "26-35", "36-45", "46-55", "56-65"]
    df["Age_Group"] = pd.cut(df["Customer_Age"], bins=bins, labels=labels)
    return df

df = load_data()

# ----------------------------- SIDEBAR FILTERS -----------------------------
st.sidebar.header("🔎 Filters")

date_min, date_max = df["Order_Date"].min(), df["Order_Date"].max()
date_range = st.sidebar.date_input("Order Date Range", [date_min, date_max],
                                    min_value=date_min, max_value=date_max)

regions = st.sidebar.multiselect("Region", sorted(df["Region"].unique()),
                                  default=sorted(df["Region"].unique()))
categories = st.sidebar.multiselect("Category", sorted(df["Category"].unique()),
                                     default=sorted(df["Category"].unique()))
segments = st.sidebar.multiselect("Customer Segment", sorted(df["Customer_Segment"].unique()),
                                   default=sorted(df["Customer_Segment"].unique()))

if len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    mask = (
        (df["Order_Date"] >= start) & (df["Order_Date"] <= end)
        & (df["Region"].isin(regions))
        & (df["Category"].isin(categories))
        & (df["Customer_Segment"].isin(segments))
    )
    fdf = df[mask]
else:
    fdf = df.copy()

if fdf.empty:
    st.warning("No data matches the selected filters. Please broaden your selection.")
    st.stop()

# ----------------------------- HEADER -----------------------------
st.title("📊 Sales Analytics Dashboard")
st.caption("Interactive dashboard answering 15 key business questions from a medium-sized sales dataset.")

# ----------------------------- KPI ROW (Q1) -----------------------------
st.subheader("1️⃣ Overall Performance (Q1)")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Net Sales", f"₹{fdf['Net_Sales'].sum():,.0f}")
k2.metric("Total Orders", f"{len(fdf):,}")
k3.metric("Avg Order Value", f"₹{fdf['Net_Sales'].mean():,.0f}")
k4.metric("Avg Profit Margin", f"{fdf['Profit_Margin_Pct'].mean():.1f}%")

st.divider()

# ----------------------------- Q2 & Q3: Region / Category -----------------------------
st.subheader("2️⃣ & 3️⃣ Sales by Region and Category")
c1, c2 = st.columns(2)

with c1:
    region_sales = fdf.groupby("Region")["Net_Sales"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(region_sales.index, region_sales.values, color="steelblue")
    ax.set_title("Total Sales by Region")
    ax.set_ylabel("Net Sales (Rs.)")
    plt.xticks(rotation=30)
    st.pyplot(fig)

with c2:
    cat_sales = fdf.groupby("Category")["Net_Sales"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(cat_sales.index, cat_sales.values, color="seagreen")
    ax.set_title("Total Sales by Category")
    ax.set_ylabel("Net Sales (Rs.)")
    plt.xticks(rotation=30)
    st.pyplot(fig)

st.divider()

# ----------------------------- Q4: Top Products -----------------------------
st.subheader("4️⃣ Top 10 Products by Sales")
top_products = fdf.groupby("Product")["Net_Sales"].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_products)

st.divider()

# ----------------------------- Q5: Monthly Trend -----------------------------
st.subheader("5️⃣ Monthly Sales Trend")
monthly = fdf.groupby("Month")["Net_Sales"].sum()
st.line_chart(monthly)

st.divider()

# ----------------------------- Q6 & Q7: Profit -----------------------------
st.subheader("6️⃣ & 7️⃣ Profit Margin & Profit by Category")
c3, c4 = st.columns(2)
with c3:
    st.metric("Average Profit Margin", f"{fdf['Profit_Margin_Pct'].mean():.2f}%")
    st.write("Profit margin distribution:")
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.hist(fdf["Profit_Margin_Pct"], bins=20, color="orange", edgecolor="black")
    ax.set_xlabel("Profit Margin (%)")
    st.pyplot(fig)

with c4:
    profit_cat = fdf.groupby("Category")["Profit"].sum().sort_values(ascending=False)
    st.write("Total Profit by Category:")
    st.bar_chart(profit_cat)

st.divider()

# ----------------------------- Q8: Discount vs Quantity -----------------------------
st.subheader("8️⃣ Discount % vs Quantity Sold (Correlation)")
corr = fdf["Discount_Pct"].corr(fdf["Quantity"])
st.write(f"**Correlation coefficient:** `{corr:.3f}` "
         f"({'weak/no' if abs(corr) < 0.2 else 'moderate' if abs(corr) < 0.5 else 'strong'} relationship)")
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(fdf["Discount_Pct"], fdf["Quantity"], alpha=0.3, color="purple")
ax.set_xlabel("Discount %")
ax.set_ylabel("Quantity Sold")
st.pyplot(fig)

st.divider()

# ----------------------------- Q9 & Q10: Segment / Payment -----------------------------
st.subheader("9️⃣ & 🔟 Customer Segment & Payment Method")
c5, c6 = st.columns(2)
with c5:
    seg = fdf.groupby("Customer_Segment")["Net_Sales"].sum()
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(seg.values, labels=seg.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Sales Share by Customer Segment")
    st.pyplot(fig)

with c6:
    pay = fdf["Payment_Method"].value_counts()
    st.write("Payment Method Popularity:")
    st.bar_chart(pay)

st.divider()

# ----------------------------- Q11: Sales Rep -----------------------------
st.subheader("1️⃣1️⃣ Sales Rep Performance")
rep = fdf.groupby("Sales_Rep")["Net_Sales"].sum().sort_values(ascending=False)
st.bar_chart(rep)

st.divider()

# ----------------------------- Q12: Weekday -----------------------------
st.subheader("1️⃣2️⃣ Sales by Weekday")
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
wk = fdf.groupby("Weekday")["Net_Sales"].sum().reindex(weekday_order)
st.bar_chart(wk)

st.divider()

# ----------------------------- Q13: Rating vs Sales -----------------------------
st.subheader("1️⃣3️⃣ Avg Net Sales by Customer Rating")
rating = fdf.groupby("Customer_Rating")["Net_Sales"].mean()
st.bar_chart(rating)

st.divider()

# ----------------------------- Q14: Age group -----------------------------
st.subheader("1️⃣4️⃣ Sales by Customer Age Group")
age = fdf.groupby("Age_Group", observed=True)["Net_Sales"].sum()
st.bar_chart(age)

st.divider()

# ----------------------------- Q15: Outlier detection -----------------------------
st.subheader("1️⃣5️⃣ Outlier Detection in Net Sales (IQR Method - NumPy)")
Q1 = np.percentile(fdf["Net_Sales"], 25)
Q3 = np.percentile(fdf["Net_Sales"], 75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = fdf[(fdf["Net_Sales"] < lower_bound) | (fdf["Net_Sales"] > upper_bound)]

o1, o2, o3 = st.columns(3)
o1.metric("Outlier Orders", f"{len(outliers):,}")
o2.metric("% of Data", f"{100*len(outliers)/len(fdf):.2f}%")
o3.metric("Upper Bound (Rs.)", f"{upper_bound:,.0f}")

fig, ax = plt.subplots(figsize=(6, 4))
ax.boxplot(fdf["Net_Sales"], vert=False)
ax.set_xlabel("Net Sales (Rs.)")
ax.set_title("Net Sales Distribution with Outliers")
st.pyplot(fig)

with st.expander("View outlier records"):
    st.dataframe(outliers[["Order_ID", "Order_Date", "Region", "Category", "Product", "Net_Sales"]])

st.divider()

# ----------------------------- RAW DATA -----------------------------
with st.expander("📄 View Filtered Raw Data"):
    st.dataframe(fdf)
    st.download_button("Download filtered data as CSV",
                        fdf.to_csv(index=False).encode("utf-8"),
                        "filtered_sales_data.csv", "text/csv")

st.caption("Dashboard built using Python, Pandas, NumPy, Matplotlib and Streamlit.")
