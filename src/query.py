import sqlite3


def query(db_name="sales_data.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    query = """
    SELECT 
        p.Category,
        d.OrderYear,
        d.OrderMonth,
        SUM(f.Revenue) AS TotalRevenue
    FROM 
        FactSales f
    JOIN 
        DimProduct p ON f.ProductID = p.ProductID
    JOIN 
        DimDate d ON f.DateID = d.DateID
    GROUP BY 
        p.Category, d.OrderYear, d.OrderMonth
    ORDER BY 
        p.Category, d.OrderYear, d.OrderMonth;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    print("Category\tYear\tMonth\tRevenue")
    print("-" * 40)

    for row in results:
        category, year, month, revenue = row
        print(f"{category}\t{year}\t{month}\t${revenue:.2f}")

    conn.close()


query()
