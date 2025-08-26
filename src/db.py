import sqlite3


def create_tables(conn):
    cursor = conn.cursor()

    # DimProduct table for product details
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DimProduct (
        ProductID TEXT PRIMARY KEY,
        ProductName TEXT,
        Category TEXT,
        Cost REAL
    );
    """)

    # DimDate table for date related details
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DimDate (
        DateID INTEGER PRIMARY KEY AUTOINCREMENT,
        OrderYear INTEGER,
        OrderMonth INTEGER,
        OrderDay INTEGER
    );
    """)

    # FactSales table for transactional sales data
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS FactSales (
        OrderID INTEGER PRIMARY KEY,
        CustomerID TEXT,
        Revenue REAL,
        ProductID TEXT,
        DateID INTEGER,
        FOREIGN KEY (ProductID) REFERENCES DimProduct (ProductID),
        FOREIGN KEY (DateID) REFERENCES DimDate (DateID)
    );
    """)

    # Commit the changes
    conn.commit()


def insert_product(conn, product_data):
    cursor = conn.cursor()
    cursor.executemany(
        """
    INSERT INTO DimProduct (ProductID, ProductName, Category, Cost)
    VALUES (?, ?, ?, ?)
    """,
        product_data,
    )
    conn.commit()


def insert_date(conn, date_data):
    cursor = conn.cursor()
    cursor.executemany(
        """
    INSERT INTO DimDate (OrderYear, OrderMonth, OrderDay)
    VALUES (?, ?, ?)
    """,
        date_data,
    )
    conn.commit()


def insert_sales(conn, sales_data):
    cursor = conn.cursor()
    cursor.executemany(
        """
    INSERT INTO FactSales (OrderID, CustomerID, Revenue, ProductID, DateID)
    VALUES (?, ?, ?, ?, ?)
    """,
        sales_data,
    )
    conn.commit()


def db(db_name="sales_data.db"):
    return sqlite3.connect(db_name)
