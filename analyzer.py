# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 22:44:40 2025

@author: jaisi
"""

# Insert this function into your analyzer.py or a new script like db_export_utility.py


# analyzer.py

import sqlite3
from datetime import datetime
import pandas as pd
import os

DATABASE_NAME = 'finance.db'

def get_db_connection():
    """Returns a connection object to the finance database."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        # Allows accessing columns by name instead of index
        conn.row_factory = sqlite3.Row 
        return conn
    except sqlite3.Error as e:
        print(f"❌ Error connecting to database: {e}")
        return None

# Modified fetch_financial_summary in analyzer.py

def fetch_financial_summary(conn, year_month=None):
    """
    Calculates total Income and total Expense for a given month or all time.
    """
    if not conn:
        return pd.DataFrame()

    # Base SQL query: Added 1 as 'dummy_index'
    query = """
    SELECT 
        1 as dummy_index, -- Added a constant column for the pivot index
        flow,
        SUM(amount) as TotalAmount
    FROM transactions
    WHERE flow IS NOT NULL AND flow != '' -- CRITICAL FILTER: Exclude empty flow values
    """
    
    params = []
    
    # Add filtering if a specific month is requested
    if year_month:
        query += " AND strftime('%Y-%m', date) = ?"
        params.append(year_month)

    query += " GROUP BY dummy_index, flow;" # Group by the new index too
    
    try:
        df = pd.read_sql_query(query, conn, params=params)
        
        if df.empty:
            # Return a default structure with zero totals
            return pd.DataFrame({'Income': [0.0], 'Expense': [0.0], 'Net Flow': [0.0]})
        
        # FIX: Explicitly use the 'dummy_index' column instead of index=None
        summary_df = df.pivot(index='dummy_index', columns='flow', values='TotalAmount')
        
        # Reset index to remove the dummy column label
        summary_df = summary_df.reset_index(drop=True)
        
        # Ensure Income/Expense columns exist
        if 'Income' not in summary_df.columns:
            summary_df['Income'] = 0.0
        if 'Expense' not in summary_df.columns:
            summary_df['Expense'] = 0.0

        summary_df['Net Flow'] = summary_df['Income'].fillna(0) - summary_df['Expense'].fillna(0)
        
        return summary_df[['Income', 'Expense', 'Net Flow']].fillna(0)
        
    except sqlite3.Error as e:
        print(f"❌ Error fetching financial summary: {e}")
        return pd.DataFrame()


def fetch_monthly_trends(conn):
    """
    Calculates total Income and Expense for every recorded month.

    Returns:
        pd.DataFrame: DataFrame with columns: Month (YYYY-MM), Income, Expense, Net Flow.
    """
    if not conn:
        return pd.DataFrame()

    query = """
    SELECT
        -- FIX: Use substr() to reorder the M/D/Y date into YYYY-MM-DD format
        -- and then extract the YYYY-MM string for grouping.
        strftime('%Y-%m', 
            substr(date, 7, 4) || '-' || substr(date, 1, 2) || '-' || substr(date, 4, 2)
        ) as Month,
        flow,
        SUM(amount) as TotalAmount
    FROM transactions
    WHERE flow IS NOT NULL AND flow != '' -- Exclude empty flow values
    GROUP BY Month, flow
    ORDER BY Month;
    """
    
    try:
        df = pd.read_sql_query(query, conn)
        
        # Check if the resulting DataFrame is empty after filtering
        if df.empty:
            return pd.DataFrame()

        # Pivot the data to get separate columns for Income and Expense per month
        monthly_df = df.pivot(index='Month', columns='flow', values='TotalAmount').fillna(0).reset_index()
        
        # Rename columns for consistency
        monthly_df.columns.name = None
        
        # Calculate Net Flow
        if 'Income' not in monthly_df.columns:
            monthly_df['Income'] = 0.0
        if 'Expense' not in monthly_df.columns:
            monthly_df['Expense'] = 0.0

        monthly_df['Net Flow'] = monthly_df['Income'] - monthly_df['Expense']
        
        return monthly_df
        
    except sqlite3.Error as e:
        print(f"❌ Error fetching monthly trends: {e}")
        return pd.DataFrame()


def fetch_category_spending(conn, flow='Expense'):
    """
    Gets the total spending per category (or income per category).

    Args:
        conn (sqlite3.Connection): Active database connection.
        flow (str): 'Expense' (default) or 'Income'.

    Returns:
        pd.DataFrame: DataFrame with columns: Category, Total Amount.
    """
    if not conn:
        return pd.DataFrame()

    query = """
    SELECT
        category,
        SUM(amount) as TotalAmount
    FROM transactions
    WHERE flow = ?
    GROUP BY category
    ORDER BY TotalAmount DESC;
    """
    
    try:
        df = pd.read_sql_query(query, conn, params=(flow,))
        return df
        
    except sqlite3.Error as e:
        print(f"❌ Error fetching category breakdown: {e}")
        return pd.DataFrame()


def fetch_all_transactions(conn, category=None, flow=None, limit=50):
    """
    Fetches raw transaction data for display in a table.

    Returns:
        pd.DataFrame: Raw transaction data.
    """
    if not conn:
        return pd.DataFrame()

    query = "SELECT date, description, category, amount, flow FROM transactions"
    params = []
    conditions = []
    
    if category:
        conditions.append("category = ?")
        params.append(category)
        
    if flow:
        conditions.append("flow = ?")
        params.append(flow)
        
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    query += " ORDER BY date DESC LIMIT ?;"
    params.append(limit)

    try:
        df = pd.read_sql_query(query, conn, params=params)
        return df
    except sqlite3.Error as e:
        print(f"❌ Error fetching raw transactions: {e}")
        return pd.DataFrame()


if __name__ == '__main__':
    # --- Example Usage ---
    print("--- Running Analysis Examples ---")
    
    db_conn = get_db_connection()
    
    if db_conn:
        # 1. Overall Summary
        print("\n**1. Overall Financial Summary (All Time)**")
        summary = fetch_financial_summary(db_conn)
        print(summary)
        
        # 2. Monthly Trends (for Line Charts)
        print("\n**2. Monthly Financial Trends**")
        monthly_trends = fetch_monthly_trends(db_conn)
        print(monthly_trends.tail())
        
        # 3. Top Spending Categories (for Bar/Pie Charts)
        print("\n**3. Top 5 Expense Categories**")
        top_spending = fetch_category_spending(db_conn, flow='Expense').head(5)
        print(top_spending)
        
        # 4. Raw Transaction Data (for tables)
        print("\n**4. Latest 5 Raw Transactions**")
        transactions = fetch_all_transactions(db_conn, limit=5)
        print(transactions)

        db_conn.close()
        print("\n--- Analysis Complete ---")

DATABASE_NAME = 'finance.db'

def export_transactions_to_csv(output_filename='exported_transactions.csv'):
    """
    Connects to the finance database, retrieves all transactions, and saves them
    to a specified CSV file.
    """
    if not os.path.exists(DATABASE_NAME):
        print(f"❌ Error: Database file '{DATABASE_NAME}' not found.")
        return

    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        print(f"Connecting to database: {DATABASE_NAME}")

        # SQL to select all fields from the transactions table
        query = "SELECT * FROM transactions ORDER BY date DESC"

        # Use Pandas to efficiently read the SQL query results directly into a DataFrame
        df = pd.read_sql_query(query, conn)

        # Save the DataFrame to a CSV file
        df.to_csv(output_filename, index=False) # index=False prevents writing the DataFrame index as a column

        print(f"\n🎉 Success! All {len(df)} transactions exported to: **{output_filename}**")
        print("You can now open this CSV file in any spreadsheet program.")

    except sqlite3.Error as e:
        print(f"❌ Database error during export: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()

# Example execution (you can run this block directly to test the export):
if __name__ == '__main__':
    # Make sure you have the 'finance.db' file in the same directory
    export_transactions_to_csv()
