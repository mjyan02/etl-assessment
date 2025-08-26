import pandas as pd

# Data files
orders = pd.read_csv("data/orders.csv")
products = pd.read_csv("data/products.csv")

# Test log
print(orders.head())
print(products.head())

# Calculate revenue
orders["Revenue"] = orders["Quantity"] * orders["Price"]

# Extract fields
orders["OrderYear"] = pd.to_datetime(orders["OrderDate"]).dt.year
orders["OrderMonth"] = pd.to_datetime(orders["OrderDate"]).dt.month
orders["OrderDay"] = pd.to_datetime(orders["OrderDate"]).dt.day

# Test log
print(orders.head())
