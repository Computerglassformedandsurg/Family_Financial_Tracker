import sqlite3
import os

DATABASE_NAME = 'finance.db'

def initialize_db():
    """
    Establishes a connection to the SQLite database and ensures the necessary
    'transactions' table exists with the correct schema.
    
    Returns:
        sqlite3.Connection: The database connection object, or None if connection fails.
    """
    print(f"Connecting to database: {DATABASE_NAME}")
    try:
        # Connect to the database file (it will be created if it doesn't exist)
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # SQL to create the transactions table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            flow TEXT NOT NULL -- 'Income' or 'Expense'
        );
        """
        cursor.execute(create_table_sql)
        conn.commit()
        print("✅ Database connection established and 'transactions' table ensured.")
        return conn

    except sqlite3.Error as e:
        print(f"❌ Database error during initialization: {e}")
        return None

def import_transactions(conn, transactions_data):
    """
    Inserts a list of financial transactions into the database.

    Args:
        conn (sqlite3.Connection): The active database connection.
        transactions_data (list): A list of tuples, where each tuple is a 
                                  transaction record: 
                                  (date, description, category, amount, flow).
    """
    if not conn:
        print("❌ Cannot import data: Database connection is not available.")
        return

    insert_sql = """
    INSERT INTO transactions (date, description, category, amount, flow)
    VALUES (?, ?, ?, ?, ?);
    """
    
    try:
        cursor = conn.cursor()
        # Execute the INSERT statement for all records at once for efficiency
        cursor.executemany(insert_sql, transactions_data)
        conn.commit()
        print(f"🎉 Successfully imported {len(transactions_data)} transactions into the database.")
    
    except sqlite3.Error as e:
        print(f"❌ Database error during data insertion: {e}")
        print("Rolling back changes...")
        conn.rollback()

def close_db(conn):
    """
    Closes the database connection.

    Args:
        conn (sqlite3.Connection): The database connection object to close.
    """
    if conn:
        conn.close()
        print("✅ Database connection closed.")

# if __name__ == '__main__':
#     # Example usage when running finance_db.py directly
#     print("--- Testing finance_db.py functionality ---")
    
#     # 1. Initialize DB
#     db_conn = initialize_db()
    
#     if db_conn:
#         # 2. Sample data to insert
#         sample_data = [
#             ('2025-10-01', 'Initial Salary Deposit', 'Salary', 5000.00, 'Income'),
#             ('2025-10-02', 'Monthly Rent', 'Housing', 1500.00, 'Expense'),
#             ('2025-10-03', 'Groceries', 'Food', 85.50, 'Expense'),
#         ]
        
#         # 3. Import data
#         import_transactions(db_conn, sample_data)
        
#         # 4. Read back data to verify (optional)
#         print("\nVerifying imported data:")
#         cursor = db_conn.cursor()
#         cursor.execute("SELECT * FROM transactions ORDER BY id DESC LIMIT 3")
#         for row in cursor.fetchall():
#             print(row)
            
#         # 5. Close connection
#         close_db(db_conn)
    
