# Trip Expense Analytics

## Objective
# Analyze trip expenditure data to identify spending patterns, major cost drivers, payer contributions, and opportunities for cost optimization using Excel, SQL, Python, and Power BI.

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime
df=pd.read_csv("Trip_expense_cleaned.csv")
print(df.head())
df.info()
print(df.describe())
print(df.isnull().sum())
df['Date']=pd.to_datetime(df['Date'], format='%d-%m-%Y')
df['Month']=df['Date'].dt.month_name()
df['Day']=df['Date'].dt.day
df['Weekday']=df['Date'].dt.day_name()

plt.figure(figsize=(8,5))
sns.histplot(df['Cost'],bins=20)
plt.title("Expense Distribution")
plt.show()

category_spend=df.groupby('Expense Category')['Cost'].sum().reset_index()
print(category_spend)
sns.barplot(data=category_spend,
    x='Expense Category',
    y='Cost')
plt.title("Spending by Category")
plt.show()

category_spend['Percentage'] = (
    category_spend['Cost']
    /
    category_spend['Cost'].sum()
)*100
print(category_spend)
plt.figure(figsize=(7,7))
plt.pie(
    category_spend['Cost'],
    labels=category_spend['Expense Category'],
    autopct='%1.1f%%',
    startangle=90
)
plt.title("Expense Contribution by Category")
plt.show()

daily_spending = (
    df.groupby('Date')['Cost']
      .sum()
      .reset_index()
)
print(daily_spending)
plt.figure(figsize=(10,5))

plt.plot(
    daily_spending['Date'],
    daily_spending['Cost'],
    marker='o'
)
plt.title("Daily Spending Trend")
plt.xlabel("Date")
plt.ylabel("Total Spending")
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

payer = (
    df.groupby('Paid by')['Cost']
      .sum()
      .reset_index()
)
print(payer)
plt.figure(figsize=(8,5))
sns.barplot(
    data=payer,
    x='Paid by',
    y='Cost'
)
plt.title("Contribution by Traveler")
plt.show()

top10 = df.nlargest(10,'Cost')
print(top10)
plt.figure(figsize=(10,6))
sns.barplot(
    data=top10,
    x='Cost',
    y='Description'
)
plt.title("Top 10 Highest Expenses")
plt.show()

pareto = (
    category_spend
    .sort_values(
        by='Cost',
        ascending=False
    )
)
pareto['Contribution %'] = (
    pareto['Cost']
    /
    pareto['Cost'].sum()
)*100
pareto['Cumulative %'] = (
    pareto['Contribution %']
    .cumsum()
)
print(pareto)
plt.figure(figsize=(9,5))
plt.bar(
    pareto['Expense Category'],
    pareto['Cost']
)
plt.plot(
    pareto['Expense Category'],
    pareto['Cumulative %'],
    marker='o'
)
plt.ylabel("Amount / Cumulative %")
plt.title("Pareto Analysis")
plt.show()

df['Expense Level'] = np.where(
    df['Cost']<100,
    'Low',
    np.where(
        df['Cost']<1000,
        'Medium',
        'High'
    )
)
print(df['Expense Level'].value_counts())
sns.countplot(
    data=df,
    x='Expense Level'
)
plt.show()

print("="*50)
print("Total Trip Cost :",df['Cost'].sum())
print("Average Expense :",round(df['Cost'].mean(),2))
print("Highest Expense :",df['Cost'].max())
print("Lowest Expense :",df['Cost'].min())
print("Highest Spending Category :",category_spend.loc[category_spend['Cost'].idxmax(),'Expense Category'])
print("Highest Paying Person :",payer.loc[
payer['Cost'].idxmax(),'Paid by'])

df.to_csv(
    "Trip_expense_python_cleaned.csv",
    index=False
)