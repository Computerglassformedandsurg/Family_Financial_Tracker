# 💰 Family Financial Tracker Dashboard (Deployed)

## 🎯 Project Status: LIVE WEB APPLICATION

**This project is now a live, interactive web dashboard.** The data ETL is complete, and the application provides immediate visualization and analysis of the financial data.

### **View the Live Dashboard!**
[**Click Here to View the Live Streamlit Dashboard**](https://familyfinancialtracker-tqenib8gljrwpwgze6sndy.streamlit.app/)


![Financial Dashboard Preview](assets/dashboard_preview.gif)

---

## 🛠️ Technology Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend/UI** | **Streamlit** | Interactive web dashboard framework. |
| **Data Visualization** | **Plotly** & **Pandas** | Generating dynamic and professional charts (Monthly Trends, Category Breakdown). |
| **Data Storage** | **SQLite** | Serverless, single-file database (`finance.db`) for portable data history. |
| **Data Retrieval** | **Python `sqlite3`** | Custom SQL queries and data fetching directly to the UI. |

---

## 💡 Financial Analysis Features

The deployed dashboard offers the following analysis capabilities powered by the data in `finance.db`:

* **Financial Summary:** Key metrics including Total Income, Total Expenses, and Net Flow (Savings).
* **Monthly Trends:** Line charts showing Income, Expense, and Net Flow over time for historical comparison.
* **Category Breakdown:** Bar charts visualizing spending by category.
* **Transaction Viewer:** Filterable table view of raw transaction details.

---

## ⚙️ Data Pipeline & Structure (The ETL Core)

The original ETL pipeline ensures data quality and completeness before analysis.

* **Goal:** Consolidate raw CSV data into a clean, queryable **`finance.db`** file.
* **Status:** The core ETL logic (Standardization, Duplication Checks, and Loading) is **fully functional** within the `analyzer.py` / `csv_importer.py` scripts.
* **Database Schema:** The `transactions` table includes essential columns: `Date`, `Description`, `Category`, `Amount`, and `Flow`.

### Data Maintenance Note
To update the live dashboard, data must be first inserted into the local `finance.db` file, then committed, and pushed to GitHub, followed by a **redeploy** on Streamlit Cloud.
