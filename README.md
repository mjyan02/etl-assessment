# Case Study: Sales Data Transformation for Analytical Reporting

This repository contains the implementation of an **ETL pipeline** that processes mock data from CSV files, transforms it, and loads it into an **SQLite database** following a simple **star schema**. The **FactSales**, **DimProduct**, and **DimDate** tables are created to allow for efficient querying and analysis of sales data to evaluate performance.

## Table of Contents

1. [Setup Instructions](#set-up)
2. [Data Modeling (Task 2)](#data-modeling)
3. [SQL Query (Task 3)](#sql-query)
4. [Dashboarding Use Case (Task 4)](#dashboarding-use-case)

### Set Up 🤩

1. Pre-requisites: Ensure **Python 3.6** or above is installed
2. Clone this repo
3. Ensure you are in the correct project directory:

   ```
   cd etl-assessment
   ```

4. Create the virtual environment
   ```
   python -m venv venv
   ```
5. Activate the virtual environment

   ```
   # Windows
   venv\Scripts\activate

   # MacOS
   source venv/bin/activate
   ```

6. Install the requirements

   ```
   pip install -r requirements.txt
   ```

7. Place CSV files (if any is needed) inside the `data` folder

8. Run the ETL script to load data into the SQLite database:

   ```
   python src/etl.py
   ```

9. Run the Query script (if needed):
   ```
   python src/query.py
   ```

## Data Modeling

The data model is designed using a **star schema** with the following tables:

### 1. **DimProduct** (Dimension Table)

- **Purpose**: Stores product details
- **Columns**:
  - **ProductID** (PK): Unique identifier for each product
  - **ProductName**: Name of product (e.g., "Keyboard")
  - **Category**: Product category (e.g., "Peripherals")
  - **Cost**: Cost of product

### 2. **DimDate** (Dimension Table)

- **Purpose**: Stores date related details
- **Columns**:
  - **DateID** (PK): Unique date identifier
  - **OrderYear**: Year of sale
  - **OrderMonth**: Month of sale
  - **OrderDay**: Day of sale

### 3. **FactSales** (Fact Table)

- **Purpose**: Stores transactional sales details
- **Columns**:
  - **OrderID** (PK): Unique order identifier
  - **CustomerID**: Identifier for the customer who made the purchase
  - **Revenue**: Total revenue from the transaction (`Quantity * Price`)
  - **ProductID** (FK): Links to `DimProduct`, indicating which product was sold
  - **DateID** (FK): Links to `DimDate`, indicating when the sale occurred

### Relationships:

- **`FactSales` → `DimProduct`**: `FactSales` contains a `ProductID` that references `DimProduct`. This allows sales to be analyzed by **product attributes** like `Category` and `ProductName`.
- **`FactSales` → `DimDate`**: `FactSales` contains a `DateID` that references `DimDate`. This allows **time based analysis** of sales data, such as total revenue per month or year.

---

## SQL Query

The following SQL query calculates the **total revenue by category and month**, using **`FactSales`**, **`DimProduct`**, and **`DimDate`** tables:

```sql
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
```

This query can also be run using the `query.py` script in `src`:

```
python src/query.py
```

---

## Dashboard Use Case
