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

💰 Simple Finance CSV to SQLite Importer

A utility script to reliably transform raw financial transaction data from a structured CSV file into a queryable SQLite database.

✅ Current Status: Core Import Functional

The primary goal of transforming CSV data into a structured database is complete.

What's Done:

Python Script (csv_importer.py): Handles file reading, data validation, type conversion, and efficient bulk insertion into SQLite.

Database Creation: Automatically creates finance_tracker.db.

Schema Enforcement: Ensures the transactions table is properly structured with columns for Date, Description, Category, Amount, and Flow.

How to Run:

Place your transaction data in a file named finance_data.csv in the project root.

Ensure your CSV includes the exact headers: Date, Description, Category, Amount, Flow.

Execute the script in your terminal:

python csv_importer.py


🚀 Project Roadmap (Next Steps)

The next steps will focus on making the data useful by adding a front-end interface and advanced reporting capabilities.

Phase 2: Data Analysis & UI

Database Query Layer: Add dedicated functions to csv_importer.py for retrieving summary data (e.g., total income, total expenses, balance by month).

Web Visualization: Implement a single-file React or HTML application to read the finance_tracker.db contents and display charts/tables.

Filtering: Add basic user controls to filter transactions by Category or Flow.

Phase 3: Advanced Reporting

Implement more complex analytics, such as:

Calculating net worth over time.

Generating budget variance reports.

**Connecting to Power BI (via ODBC)**

Power BI has excellent native support for SQLite. The most reliable method is typically using an ODBC (Open Database Connectivity) driver.

Install ODBC Driver: Ensure you have a suitable SQLite ODBC driver installed on your system (e.g., SQLiteODBC).

Get Data: In Power BI Desktop, select "Get Data" -> "ODBC".

Connection String: In the ODBC dialogue, use the Connection String option and provide the path to your database file:

Driver={SQLite3 ODBC Driver};Database=C:\path\to\your\finance.db;


**Load Data: **Power BI will connect and allow you to select the transactions table to begin building your reports.

**Connecting to Streamlit (Native Python)**

Since the ETL is Python-based, connecting to SQLite from Streamlit is straightforward using the built-in sqlite3 library and Pandas. 


