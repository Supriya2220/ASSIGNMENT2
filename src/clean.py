# -*- coding: utf-8 -*-
"""1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16hZM3FsPBCo3QFT9gF11IFaaI0uJqrcD
"""

import pandas as pd
from datetime import datetime

data = pd.read_csv('/content/sample_data/train.csv')

"""a)  Look for the missing values in all the columns and either impute them (replace with mean, median, or mode) or drop them. Justify your action for this task.     """

data.info()

missing_values = data.isnull().sum()
print("Missing values in each column:\n", missing_values)

if data['Mileage'].isnull().sum() > 0:
    data['Mileage'] = data['Mileage'].str.extract('(\d+.\d+|\d+)').astype(float)
    data['Mileage'].fillna(data['Mileage'].median(), inplace=True)

# Convert 'Engine' to numeric by removing non-numeric characters
if data['Engine'].isnull().sum() > 0:
    data['Engine'] = data['Engine'].str.extract('(\d+.\d+|\d+)').astype(float)
    data['Engine'].fillna(data['Engine'].median(), inplace=True)

# Convert 'Power' to numeric by removing non-numeric characters
if data['Power'].isnull().sum() > 0:
    data['Power'] = data['Power'].str.extract('(\d+.\d+|\d+)').astype(float)
    data['Power'].fillna(data['Power'].median(), inplace=True)

# Seats - fill missing values with mode (most common seat configuration)
if data['Seats'].isnull().sum() > 0:
    data['Seats'].fillna(data['Seats'].mode()[0], inplace=True)

if data['New_Price'].isnull().sum() > 0:
    data['New_Price'] = data['New_Price'].str.extract('(\d+.\d+|\d+)').astype(float)
    data['New_Price'].fillna(data['New_Price'].median(), inplace=True)
print("Missing values in each column after handling:\n", data.isnull().sum())

data.drop(columns=['New_Price'], inplace=True)

print("Missing values in each column after handling:\n", data.isnull().sum())

"""B)Remove the units from some of the attributes and only keep the numerical values (for example remove kmpl from “Mileage”, CC from “Engine”, bhp from “Power”, and lakh from “New_price”)."""

print("Columns in the dataset:\n", data.columns.tolist())

data.columns = data.columns.str.strip()


data['Mileage'] = data['Mileage'].astype(str).str.replace(' kmpl', '', regex=False).astype(float)  # Removing ' kmpl'
data['Engine'] = data['Engine'].astype(str).str.replace(' CC', '', regex=False).astype(float)      # Removing ' CC'
data['Power'] = data['Power'].astype(str).str.replace(' bhp', '', regex=False).astype(float)       # Removing ' bhp'

print(data[['Mileage', 'Engine', 'Power']].head())

"""C)Change the categorical variables (“Fuel_Type” and “Transmission”) into numerical one hot encoded value"""

data = pd.get_dummies(data, columns=['Fuel_Type', 'Transmission'], drop_first=True)

print(data.head())

duplicates = data.duplicated().sum()
print(f"Number of duplicate columns: {duplicates}")

"""D)Create one more feature and add this column to the dataset (you can use mutate function in R for this). For example, you can calculate the current age of the car by subtracting “Year” value from the current year.   """

current_year = datetime.now().year
data['Car_Age'] = current_year - data['Year']

print(data.head())

"""e)Perform select, filter, rename, mutate, arrange and summarize with group by operations (or their equivalent operations in python) on this dataset."""

print(data.columns)

selected_columns = data[['Name', 'Year', 'Fuel_Type_Petrol', 'Transmission_Manual', 'Price']]
filtered_data = data[data['Year'] > 2015]
renamed_data = data.rename(columns={'Mileage': 'Fuel_Efficiency', 'Power': 'Engine_Power'})
data['Age'] = 2024 - data['Year']
sorted_data = data.sort_values(by='Price', ascending=False)
summary_stats = data.groupby('Fuel_Type_Petrol')['Price'].mean()
summary_stats_complex = data.groupby('Fuel_Type_Petrol').agg({'Price': ['mean', 'min', 'max']})

print("Selected Columns:")
print(selected_columns.head())

print("\nFiltered Data (Year > 2015):")
print(filtered_data.head())

print("\nRenamed Columns:")
print(renamed_data.head())

print("\nNew Column 'Age':")
print(data[['Name', 'Year', 'Age']].head())

print("\nSorted by Price:")
print(sorted_data.head())

print("\nSummary Statistics (Mean Price by Fuel_Type_Petrol):")
print(summary_stats)

print("\nSummary Statistics (Complex):")
print(summary_stats_complex)
data.to_csv("/content/sample_data/train.csv", index=False)