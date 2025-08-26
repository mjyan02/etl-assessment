import pandas as pd
from db import db, create_tables, insert_product, insert_sales

# Data files
orders = pd.read_csv("data/orders.csv")
products = pd.read_csv("data/products.csv")

# Test logs
# print(orders.head())
# print(products.head())

# Calculate revenue
orders["Revenue"] = orders["Quantity"] * orders["Price"]

# Extract year, month, day from OrderDate
orders["OrderYear"] = pd.to_datetime(orders["OrderDate"]).dt.year
orders["OrderMonth"] = pd.to_datetime(orders["OrderDate"]).dt.month
orders["OrderDay"] = pd.to_datetime(orders["OrderDate"]).dt.day
orders["OrderDate"] = pd.to_datetime(orders["OrderDate"])

# Connect to db
conn = db()

# Start with a clean slate by dropping existing tables
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS FactSales")
cursor.execute("DROP TABLE IF EXISTS DimDate")
cursor.execute("DROP TABLE IF EXISTS DimProduct")
conn.commit()

# Populate db with data from CSV into their respective tables
create_tables(conn)

# Insert product data
product_data = [
    (row["ProductID"], row["ProductName"], row["Category"], row["Cost"])
    for _, row in products.iterrows()
]
insert_product(conn, product_data)

# Insert date data using a mapping of (Year, Month, Day) to DateID
date_mapping = {}

for _, row in orders.iterrows():
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DateID FROM DimDate WHERE OrderYear = ? AND OrderMonth = ? AND OrderDay = ?",
        (row["OrderYear"], row["OrderMonth"], row["OrderDay"]),
    )
    result = cursor.fetchone()

    if result:
        date_id = result[0]
    else:
        cursor.execute(
            "INSERT INTO DimDate (OrderYear, OrderMonth, OrderDay) VALUES (?, ?, ?)",
            (row["OrderYear"], row["OrderMonth"], row["OrderDay"]),
        )
        date_id = cursor.lastrowid

    date_mapping[(row["OrderYear"], row["OrderMonth"], row["OrderDay"])] = date_id

# Insert sales data
sales_data = []
for _, row in orders.iterrows():
    date_id = date_mapping[(row["OrderYear"], row["OrderMonth"], row["OrderDay"])]
    sales_data.append(
        (row["OrderID"], row["CustomerID"], row["Revenue"], row["ProductID"], date_id)
    )
insert_sales(conn, sales_data)

# Commit changes and close connection to db
conn.commit()
conn.close()

print("Data loaded into the database successfully.")
