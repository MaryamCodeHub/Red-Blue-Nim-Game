import pandas as pd
import matplotlib.pyplot as plt

file_path = r"C:\Users\User\Downloads\customers-100.xlsx"
df = pd.read_excel(file_path) 

print(df.head())

print(df.tail())

print(df.describe())

print(df.info())

print(df.isnull().sum())

df['Subscription Year'] = pd.to_datetime(df['Subscription Date']).dt.year

year_counts = df['Subscription Year'].value_counts().sort_index()

plt.figure(figsize=(10, 6))
ax = year_counts.plot(kind='bar', color='brown')
ax.set_facecolor('beige')
plt.title('Number of Customers per Subscription Year')
plt.xlabel('Subscription Year')
plt.ylabel('Number of Customers')
plt.tight_layout()
plt.show()

country_counts = df['Country'].value_counts()

plt.figure(figsize=(14, 7))
ax = country_counts.plot(kind='barh', color='darkred')
ax.set_facecolor('pink')
plt.title('Number of Customers per Country')
plt.xlabel('Number of Customers')
plt.ylabel('Country')
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
ax = year_counts.plot(kind='line', marker='o', linestyle='-', color='purple')
ax.set_facecolor('black')  
plt.title('Trend of Subscriptions Over the Years')
plt.xlabel('Subscription Year')
plt.ylabel('Number of Subscriptions')
plt.tight_layout()
plt.show()

