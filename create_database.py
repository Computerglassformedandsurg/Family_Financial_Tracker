# -*- coding: utf-8 -*-
"""
@author: jaisi
"""

import sqlite3
import os
from datetime import datetime

Database_File = 'finance.db'

def create_table():
    """
    Connects to the SQLite database and creates the 'transactions' and 'goals' tables
    if they do not already exist.
    """
    conn = None
    try:
        conn = sqlite3.connect(Database_File)
        cursor = conn.cursor()
        
        # --- 1. Create the Transactions Table (for raw monthly data) ---
        transactions_table_sql = """
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            flow TEXT NOT NULL
        );
        """
        cursor.execute(transactions_table_sql)
        
        # --- 2. Create the Goals Table (for aggregated savings/debt targets) ---
        goals_table_sql = """
        CREATE TABLE IF NOT EXISTS goals (
            goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_name TEXT UNIQUE NOT NULL,
            target_amount REAL NOT NULL,
            current_progress REAL NOT NULL DEFAULT 0.0,
            last_updated TEXT
        );
        """
        cursor.execute(goals_table_sql)
        
        conn.commit()
        print("✅ Tables ensured: 'transactions' and 'goals'.")

    except sqlite3.Error as e:
        print(f"An error occurred during database setup: {e}")
    finally:
        if conn:
            conn.close()


def insert_sample_data():
    """
    Inserts a few rows into the transactions and goals tables for demonstration.
    This function is now COMMENTED OUT in the main execution block below.
    """
    conn = None
    try:
        conn = sqlite3.connect(Database_File)
        cursor = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        transactions_data = [
            ('2024-07-01', 'Monthly Paycheck', 'Income', 4500.00, 'Income'),
            ('2024-07-02', 'Rent Payment', 'Housing', 1200.00, 'Expense'),
        ]
        
        cursor.execute("SELECT COUNT(*) FROM transactions;")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("""
                INSERT INTO transactions (date, description, category, amount, flow)
                VALUES (?, ?, ?, ?, ?)
            """, transactions_data)
            
        cursor.execute("SELECT COUNT(*) FROM goals;")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO goals (goal_name, target_amount, current_progress, last_updated)
                VALUES (?, ?, ?, ?)
            """, ('Emergency Fund', 5000.00, 1500.00, now))

        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred during data insertion: {e}")
    finally:
        if conn:
            conn.close()


def delete_all_data():
    """
    Deletes ALL rows from the 'transactions' and 'goals' tables.
    This function is now COMMENTED OUT in the main execution block below.
    """
    conn = None
    try:
        conn = sqlite3.connect(Database_File)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM transactions;")
        cursor.execute("DELETE FROM goals;")

        conn.commit()
        
    except sqlite3.Error as e:
        print(f"An error occurred during data deletion: {e}")
    finally:
        if conn:
            conn.close()


def view_tables_contents(table_name):
    """
    Connects to the database and displays the schema and contents of a given table.
    """
    conn = None
    try:
        conn = sqlite3.connect(Database_File)
        cursor = conn.cursor()

        print(f"\n" + "="*50)
        print(f"VIEWING TABLE: {table_name.upper()}")
        print("="*50)

        # 1. Display Schema (Structure)
        print(f"\n--- Schema (Structure of '{table_name}') ---")
        cursor.execute(f"PRAGMA table_info({table_name});")
        schema = cursor.fetchall()
        
        print("{:<5} {:<20} {:<10} {:<8}".format("ID", "Name", "Type", "PK"))
        print("-" * 45)
        for col in schema:
            print("{:<5} {:<20} {:<10} {:<8}".format(col[0], col[1], col[2], col[5]))
        
        # 2. Display Contents (Actual Data)
        print(f"\n--- Data Contents of '{table_name}' ---")
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()

        if not rows:
            print(f"The '{table_name}' table has 0 rows.")
        else:
            column_names = [description[0] for description in cursor.description]
            print(column_names)
            for row in rows:
                print(row)
                
    except sqlite3.Error as e:
        print(f"\nAn error occurred while querying the table: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    if os.path.exists(Database_File):
        print(f"Database file '{Database_File}' already exists.")
    else:
        print(f"Creating new database file '{Database_File}'.")

    # 1. Ensure tables exist
    create_table()
    
    # --- As requested, skipping data insertion to view empty tables ---
    # insert_sample_data() 
    
    print("\n" + "#"*60)
    print("      Viewing tables to show schema and confirm they are empty.")
    print("#"*60)

    # 2. View the contents of the tables (which will be empty)
    view_tables_contents('transactions')
    view_tables_contents('goals')
    
    print("\nDatabase setup complete. Ready for new operations.")

