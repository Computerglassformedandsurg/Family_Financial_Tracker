# Family_Financial_Tracker
An automated financial tracking solution. Uses Python and Google Sheets to extract transaction data, clean and load it into a MySQL database, and continuously update progress for key financial goals (debt reduction and savings fund).

💰 **Family Financial Tracker ETL**

This repository contains the Python ETL (Extract, Transform, Load) script that powers our family financial tracking and goal management system.

**It performs the following actions:**

Extracts raw transaction data from a shared Google Sheet.

Transforms the data by standardizing categories, converting expense amounts to negative values, and identifying the Member responsible.

Loads the cleaned data into a central MySQL database.

Updates Goal Progress for our $15,000 Debt Payoff and $10,000 Savings targets based on transaction history.

🛠️ **Project Setup**

**1. Prerequisites**

Before running the script, ensure you have the following installed:

Python (3.8+)

MySQL Server (or equivalent database host)

A Google Cloud Platform Service Account with access to your Google Sheet.

**2. Database Setup**

Create the Database: Run the commands in the financial_schema.sql file (which we prepared earlier) in your MySQL console (or using MySQL Workbench). This creates the transactions, categories, and the crucial goals tables.

# Example of command line execution
mysql -u [your_user] -p [your_database] < financial_schema.sql


**3. Google Sheets Setup**

Create your Ledger: Set up your Google Sheet with the required columns (Date, Description, Category, Member, Amount).

Service Account: Download your Google Service Account JSON key file and place it securely in this project directory (or a safe location). Do not commit this file to GitHub!

**4. Environment Variables**

Create a file named .env in the root of the repository and fill it with your credentials (use the .env.template below as a guide).

**5. Install Dependencies**

pip install python-dotenv mysql-connector-python gspread pandas


🏃 **Running the ETL Script**
Once the setup is complete, you can run the ETL script from your terminal:

python expense_etl.py


The script will handle the full pipeline, printing status updates and the calculated goal progress directly to your console.

**📊 Next Steps: Visualization**

After running the ETL script, your MySQL database will contain all the data needed to build your visualizations, showing:

Spending by Category.

Spending by Member (Me vs. Husband).

Real-time progress towards your Debt and Savings goals.
