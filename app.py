# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 22:48:29 2025

@author: jaisi
"""

# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from analyzer import get_db_connection, fetch_financial_summary, fetch_monthly_trends, fetch_category_spending, fetch_all_transactions

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Local Financial Tracker",
    layout="wide",
    initial_sidebar_state="expanded"
)

def run_app():
    """Main function to run the Streamlit application."""
    
    st.title("💰 Local Financial Tracker Dashboard")
    st.markdown("---")

    # Get connection and load data
    conn = get_db_connection()
    if not conn:
        st.error("Cannot connect to finance.db. Please ensure the file exists and is accessible.")
        return

    # --- 1. OVERVIEW METRICS (Key Performance Indicators) ---
    st.header("1. Financial Summary Overview")
    
    # Fetch overall summary
    summary_df = fetch_financial_summary(conn)

    if summary_df.empty:
        st.warning("No transaction data found in the database.")
        conn.close()
        return

    # Extract single values for metrics
    income = summary_df['Income'].iloc[0]
    expense = summary_df['Expense'].iloc[0]
    net_flow = summary_df['Net Flow'].iloc[0]
    
    # Format for display
    def format_currency(value):
        return f"${value:,.2f}"

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Income (All Time)", value=format_currency(income))

    with col2:
        st.metric(label="Total Expenses (All Time)", value=format_currency(expense))
        
    with col3:
        # Change color based on positive/negative net flow
        delta_color = "normal" if net_flow >= 0 else "inverse"
        st.metric(label="Net Flow / Savings", value=format_currency(net_flow), delta_color=delta_color)

    st.markdown("---")

    # --- 2. MONTHLY TRENDS (Line Chart) ---
    st.header("2. Monthly Net Flow & Trends")
    
    monthly_df = fetch_monthly_trends(conn)
    
    if not monthly_df.empty:
        # Create a line chart showing Income and Expense trends
        fig_trend = px.line(
            monthly_df,
            x='Month',
            y=['Income', 'Expense', 'Net Flow'],
            title='Monthly Income, Expense, and Net Flow Over Time',
            labels={'value': 'Amount ($)', 'variable': 'Type'},
            height=400
        )
        # Highlight Net Flow for clarity
        fig_trend.update_traces(
            selector=dict(name='Net Flow'), 
            line=dict(dash='dash', width=3, color='orange')
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    st.markdown("---")

    # --- 3. CATEGORY BREAKDOWN (Bar Chart) ---
    st.header("3. Expense Breakdown by Category")
    
    # Fetch category spending
    category_df = fetch_category_spending(conn, flow='Expense')

    if not category_df.empty:
        # Bar chart for spending
        fig_cat = px.bar(
            category_df,
            x='TotalAmount',
            y='category',
            orientation='h',
            title='Spending by Category',
            labels={'TotalAmount': 'Total Spent ($)', 'category': 'Category'},
            color='TotalAmount',
            color_continuous_scale=px.colors.sequential.Reds_r 
        )
        fig_cat.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown("---")

    # --- 4. RAW DATA TABLE & FILTERING ---
    st.header("4. Transaction Detail Viewer")
    
    # Sidebar Filters
    st.sidebar.header("Filter Transactions")
    
    all_categories = ['All'] + sorted(category_df['category'].tolist() if not category_df.empty else [])
    
    selected_category = st.sidebar.selectbox(
        "Select Category:",
        options=all_categories
    )
    
    selected_flow = st.sidebar.radio(
        "Select Flow Type:",
        options=['All', 'Income', 'Expense'],
        index=0
    )
    
    limit = st.sidebar.slider("Number of transactions to display:", 10, 500, 100)
    
    # Prepare filter arguments
    filter_category = selected_category if selected_category != 'All' else None
    filter_flow = selected_flow if selected_flow != 'All' else None
    
    # Fetch filtered data
    raw_transactions_df = fetch_all_transactions(
        conn, 
        category=filter_category, 
        flow=filter_flow, 
        limit=limit
    )

    st.dataframe(raw_transactions_df, use_container_width=True)

    # Close the database connection
    conn.close()

if __name__ == '__main__':
    run_app()