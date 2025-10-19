_**Local Financial Data ETL Pipeline (SQLite)**
_
💰 **Project Overview**

This repository contains a lightweight, serverless Python ETL (Extract, Transform, Load) script designed for consolidating personal or family financial data. It is optimized for monthly data uploads from various sources (like bank exports or local spreadsheets).

By using SQLite, the entire data history is stored in a single, portable file (finance.db), allowing for rapid, local SQL analysis without the complexity of managing a separate database server.

**The pipeline performs the following actions:**

**Extract:** Reads raw transaction data from a local CSV file.

**Transform:** Standardizes categories, converts expense amounts to negative values, and performs cleanup.

**Load:** Loads the cleaned data into the central SQLite database, performing checks to avoid importing duplicate transactions across monthly runs.

**Goal Tracking:** Updates Goal Progress for financial targets (e.g., Debt Payoff, Savings) based on the consolidated transaction history.

🛠️** Getting Started**

1. **Prerequisites**

You only need Python (3.8+) installed. The SQLite database module (sqlite3) is standard and built into Python.

2. **Install Dependencies**

You'll need the pandas library for efficient data handling and transformation.

pip install pandas streamlit


3. **Project Structure**

This project relies on a simple folder structure. The finance.db file will be created automatically upon the first successful run.

.
├── expense_etl.py    # The main ETL script
├── finance.db        # The consolidated SQLite database (generated)
└── monthly_exports/  # Folder for your input CSV files
    ├── 2024_01_transactions.csv
    └── 2024_02_transactions.csv


4. **Database Setup (Automatic)**

No external database server is required. The Python script handles the creation of the finance.db file and the necessary tables automatically when it is run for the first time.

🏃 **Running the ETL Script**

**Prepare Your Data**

Ensure your new monthly financial data is saved as a clean CSV file. The required columns are: Date, Flow, Description, Category, and positive Amount.

**Execute the Script**

Run the ETL script from your terminal, passing the path to the new CSV file as an argument:

python expense_etl.py monthly_exports/latest_export.csv


The script will handle the full pipeline, printing status updates and confirmation messages to your console.

📊 **Analysis and Visualization**

The core strength of using a portable SQLite database is its ease of connectivity with virtually any modern BI or data analysis tool. Once the finance.db file is populated by the ETL script, you can connect to it directly.

**Connecting to Power BI (via ODBC)**

Power BI has excellent native support for SQLite. The most reliable method is typically using an ODBC (Open Database Connectivity) driver.

Install ODBC Driver: Ensure you have a suitable SQLite ODBC driver installed on your system (e.g., SQLiteODBC).

Get Data: In Power BI Desktop, select "Get Data" -> "ODBC".

Connection String: In the ODBC dialogue, use the Connection String option and provide the path to your database file:

Driver={SQLite3 ODBC Driver};Database=C:\path\to\your\finance.db;


**Load Data: **Power BI will connect and allow you to select the transactions table to begin building your reports.

**Connecting to Streamlit (Native Python)**

Since the ETL is Python-based, connecting to SQLite from Streamlit is straightforward using the built-in sqlite3 library and Pandas. 


