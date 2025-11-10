# -*- coding: utf-8 -*-
"""
This script reads financial transaction data from a local CSV file,
processes it, and loads it into the 'finance.db' SQLite database.
"""

import csv
import finance_db # Import the database utility functions (initialize_db, import_transactions)
import os

# --- CONFIGURATION (UPDATE THESE VALUES) ---
# 1. CSV File Path: The location of your downloaded spreadsheet data (e.g., 'budget_data.csv')
CSV_FILE_PATH = 'My Weekly Budget Data - Weekly.csv' 

# 2. Column Indices: Define the columns in your CSV (0-indexed)
# Based on your data, the columns are mapped as follows:
COLUMN_MAP = {
    'DATE': 0,
    'DESCRIPTION': 1,
    'CATEGORY': 2, # <-- Category is now at index 2
    'AMOUNT': 3,   # <-- Amount is now at index 3
    'FLOW': 4,     # <-- Flow (Income/Expense) is now at index 4
}

# Set to True if your CSV file has a header row that should be skipped
HAS_HEADER = True
# ---------------------

def fetch_data_from_csv():
    """
    Reads all records from the specified CSV file, processes the rows, cleans the 
    amount, and reads the flow (Income/Expense) directly.
    
    Returns:
        list: A list of transaction tuples (date, description, category, amount, flow)
              ready for database insertion.
    """
    if not os.path.exists(CSV_FILE_PATH):
        print(f"❌ Error: CSV file not found at path: '{CSV_FILE_PATH}'")
        return []

    print(f"Attempting to read data from CSV file: '{CSV_FILE_PATH}'...")
    
    processed_data = []
    
    try:
        with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            
            if HAS_HEADER:
                next(reader, None) # Skip the header row
            
            records = list(reader)
            print(f"✅ Successfully read {len(records)} rows from CSV.")

            for i, row in enumerate(records):
                # Ensure the row has enough columns (at least up to the FLOW index)
                if len(row) < max(COLUMN_MAP.values()) + 1 or not any(cell.strip() for cell in row):
                    continue

                try:
                    # --- 1. Extract and Clean Values ---
                    date = row[COLUMN_MAP['DATE']].strip()
                    description = row[COLUMN_MAP['DESCRIPTION']].strip()
                    category = row[COLUMN_MAP['CATEGORY']].strip()
                    flow = row[COLUMN_MAP['FLOW']].strip() # Read flow directly from the 5th column
                    
                    # Clean amount string (remove $, commas, and whitespace)
                    amount_str = row[COLUMN_MAP['AMOUNT']].replace('$', '').replace(',', '').strip()
                    
                    if not amount_str:
                        continue 
                    
                    # Convert amount to float (it must be a number now)
                    amount = float(amount_str) 

                    # --- 2. Normalize Data for DB ---
                    # Ensure amount is positive, as the 'flow' column defines direction.
                    normalized_amount = abs(amount)
                    
                    # Ensure flow is standardized
                    normalized_flow = flow.title() 

                    # The tuple order must match DB columns: (date, description, category, amount, flow)
                    processed_data.append((date, description, category, normalized_amount, normalized_flow))

                except ValueError as ve:
                    # Report which row caused the number conversion error
                    # Use 1-based indexing for user clarity (i+2 because we skip the header)
                    print(f"⚠️ Skipping row {i+2} (CSV Line {i+2}) due to data conversion error. Check if the Amount column (Index {COLUMN_MAP['AMOUNT']}) contains non-numeric data in row: {row}")
                except Exception as row_e:
                    print(f"⚠️ Skipping row {i+2} (CSV Line {i+2}) due to unexpected error in row processing: {row_e}")
        
        return processed_data

    except Exception as e:
        print(f"❌ An unexpected error occurred during CSV read process: {e}")
        return []


def main():
    """
    Main function to orchestrate data import.
    """
    # 1. Fetch data from the CSV file
    data_to_import = fetch_data_from_csv()
    
    if not data_to_import:
        print("\nStopping: No valid data fetched from CSV file.")
        return

    # 2. Connect to the SQLite database
    # Requires finance_db.py to be in the same folder.
    db_conn = finance_db.initialize_db()
    
    if db_conn:
        # 3. Load data into the database
        print("\n--- Starting Data Load into SQLite ---")
        finance_db.import_transactions(db_conn, data_to_import)
        
        # 4. Close the connection
        finance_db.close_db(db_conn)


if __name__ == '__main__':
    main()
