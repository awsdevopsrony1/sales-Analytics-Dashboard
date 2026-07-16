"""
Sales Data Analysis - 15 Business Questions
Libraries: pandas, numpy, matplotlib
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-darkgrid') if 'seaborn-v0_8-darkgrid' in plt.style.available else None

df = pd.read_csv('sales_data.csv', parse_dates=['Order_Date'])
df['Customer_Rating'] = df['Customer_Rating'].fillna(df['Customer_Rating'].median())
df['Month'] = df['Order_Date'].dt.to_period('M').astype(str)
df['Year'] = df['Order_Date'].dt.year
df['Weekday'] = df['Order_Date'].dt.day_name()

results = {}

# Q1: Total & average net sales
results['Q1_total_net_sales'] = df['Net_Sales'].sum()
results['Q1_avg_order_value'] = df['Net_Sales'].mean()
print("Q1. Total Net Sales: Rs. {:,.2f} | Avg Order Value: Rs. {:,.2f}".format(
    results['Q1_total_net_sales'], results['Q1_avg_order_value']))

# Q2: Sales by Region
q2 = df.groupby('Region')['Net_Sales'].sum().sort_values(ascending=False)
print("\nQ2. Sales by Region:\n", q2)
plt.figure(figsize=(7,5))
q2.plot(kind='bar', color='steelblue')
plt.title('Total Sales by Region'); plt.ylabel('Net Sales (Rs. )'); plt.tight_layout()
plt.savefig('charts/q2_sales_by_region.png'); plt.close()

# Q3: Sales by Category
q3 = df.groupby('Category')['Net_Sales'].sum().sort_values(ascending=False)
print("\nQ3. Sales by Category:\n", q3)
plt.figure(figsize=(7,5))
q3.plot(kind='bar', color='seagreen')
plt.title('Total Sales by Category'); plt.ylabel('Net Sales (Rs. )'); plt.tight_layout()
plt.savefig('charts/q3_sales_by_category.png'); plt.close()

# Q4: Top 10 products by sales
q4 = df.groupby('Product')['Net_Sales'].sum().sort_values(ascending=False).head(10)
print("\nQ4. Top 10 Products:\n", q4)

# Q5: Monthly sales trend
q5 = df.groupby('Month')['Net_Sales'].sum()
print("\nQ5. Monthly Sales Trend (first 5):\n", q5.head())
plt.figure(figsize=(10,5))
q5.plot(kind='line', marker='o', color='darkorange')
plt.title('Monthly Sales Trend'); plt.xticks(rotation=45); plt.ylabel('Net Sales (Rs. )'); plt.tight_layout()
plt.savefig('charts/q5_monthly_trend.png'); plt.close()

# Q6: Profit margin overall
df['Profit_Margin_Pct'] = (df['Profit'] / df['Net_Sales']) * 100
q6 = df['Profit_Margin_Pct'].mean()
print("\nQ6. Average Profit Margin: {:.2f}%".format(q6))

# Q7: Most profitable category
q7 = df.groupby('Category')['Profit'].sum().sort_values(ascending=False)
print("\nQ7. Profit by Category:\n", q7)

# Q8: Effect of discount on quantity sold (correlation)
q8_corr = df['Discount_Pct'].corr(df['Quantity'])
print("\nQ8. Correlation between Discount% and Quantity sold: {:.3f}".format(q8_corr))

# Q9: Customer segment contribution
q9 = df.groupby('Customer_Segment')['Net_Sales'].sum().sort_values(ascending=False)
print("\nQ9. Sales by Customer Segment:\n", q9)
plt.figure(figsize=(6,6))
plt.pie(q9.values, labels=q9.index, autopct='%1.1f%%', startangle=90)
plt.title('Sales Share by Customer Segment'); plt.tight_layout()
plt.savefig('charts/q9_segment_pie.png'); plt.close()

# Q10: Preferred payment method
q10 = df['Payment_Method'].value_counts()
print("\nQ10. Payment Method Popularity:\n", q10)

# Q11: Sales rep performance (top 5)
q11 = df.groupby('Sales_Rep')['Net_Sales'].sum().sort_values(ascending=False)
print("\nQ11. Sales Rep Performance:\n", q11)
plt.figure(figsize=(8,5))
q11.plot(kind='barh', color='purple')
plt.title('Sales by Sales Rep'); plt.xlabel('Net Sales (Rs. )'); plt.tight_layout()
plt.savefig('charts/q11_rep_performance.png'); plt.close()

# Q12: Weekday sales pattern
q12 = df.groupby('Weekday')['Net_Sales'].sum().reindex(
    ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
print("\nQ12. Sales by Weekday:\n", q12)

# Q13: Customer rating distribution & its relation with sales
q13 = df.groupby('Customer_Rating')['Net_Sales'].mean()
print("\nQ13. Avg Net Sales by Customer Rating:\n", q13)

# Q14: Age group analysis using numpy binning
bins = [17, 25, 35, 45, 55, 65]
labels = ['18-25','26-35','36-45','46-55','56-65']
df['Age_Group'] = pd.cut(df['Customer_Age'], bins=bins, labels=labels)
q14 = df.groupby('Age_Group', observed=True)['Net_Sales'].sum()
print("\nQ14. Sales by Age Group:\n", q14)
plt.figure(figsize=(7,5))
q14.plot(kind='bar', color='crimson')
plt.title('Sales by Customer Age Group'); plt.ylabel('Net Sales (Rs. )'); plt.tight_layout()
plt.savefig('charts/q14_age_group.png'); plt.close()

# Q15: Outlier detection in Net_Sales using numpy (IQR method)
Q1 = np.percentile(df['Net_Sales'], 25)
Q3 = np.percentile(df['Net_Sales'], 75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['Net_Sales'] < lower_bound) | (df['Net_Sales'] > upper_bound)]
print("\nQ15. Number of Outlier Orders (IQR method): {} ({:.2f}% of data)".format(
    len(outliers), 100*len(outliers)/len(df)))

print("\nAll 15 analyses complete. Charts saved in /charts folder.")
