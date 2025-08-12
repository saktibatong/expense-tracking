#%%
import os
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

#%%
# Account title
st.title("💰 Money Report")
selected_report = st.selectbox('Select report', ['Weekly', 'Monthly', 'Annual'])

# Read transactions
transaction_file = "data/transaction.csv"
transaction_df = pd.read_csv(transaction_file)

# Weekly repot
if selected_report == 'Weekly':
    # week mode
    week_mode = st.selectbox("Week mode", ['Ongoing week', 'Specified week'])

    # specified week condition
    if week_mode == 'Specified week':
        today_year = datetime.now().year
        select_week_start_year = f"{today_year}-01-01"
        select_week_end_year = f"{today_year}-12-31"
        weekly_dates = [d.date() for d in pd.date_range(start=select_week_start_year, end=select_week_end_year, freq='W-MON')]
        specified_start = st.selectbox("Choose week", weekly_dates)

    # week interval
    week_interval = st.selectbox("Week interval", ['Weekly', 'Bi-weekly'])

    # start and end week of week mode and interval
    if week_mode == 'Ongoing week':
        today_datetime = datetime.now()
        start_of_week = today_datetime - timedelta(days=today_datetime.weekday())
        begin = start_of_week.date()

        if week_interval == 'Weekly':
            end = begin + timedelta(days=6)
            st.markdown(f'**Begin week:** {begin}')
            st.markdown(f'**End week:** {end}')

            # convert date to pandas date
            transaction_df['Date'] = pd.to_datetime(transaction_df['Date'])
            filtered_start_date = pd.to_datetime(begin)
            filtered_end_date = pd.to_datetime(end)
            transaction_filtered_df = transaction_df[(transaction_df['Date'] >= filtered_start_date) & (transaction_df['Date'] <= filtered_end_date)]
            ongoing_weekly_summary = pd.pivot_table(transaction_filtered_df, index="Transaction category", values=['Money received', 'Payment'], aggfunc='sum')

            # Create Tabs
            tab1, tab2, tab3 = st.tabs(["📊 Summary", "📈 Chart", "📄 Detailed Data"])
            with tab1:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Income", f"IDR {ongoing_weekly_summary['Money received'].sum()}")          
                with col2:
                    st.metric("Expense", f"IDR {ongoing_weekly_summary['Payment'].sum()}")

                # add budget

            with tab2:
                # Overall graph
                # Detailed graph
                pass
            
            with tab3:
                st.dataframe(transaction_filtered_df)    
        
        else: # Biweekly
            end = begin + timedelta(days=13)
            st.markdown(f'**Begin week:** {begin}')
            st.markdown(f'**End week:** {end}')

    else:
        if week_interval == 'Weekly':
            specified_end = specified_start + timedelta(days=6)
            st.markdown(f'**Begin week:** {specified_start}')
            st.markdown(f'**End week:** {specified_end}')
        else:
            specified_end = specified_start + timedelta(days=13)
            st.markdown(f'**Begin week:** {specified_start}')
            st.markdown(f'**End week:** {specified_end}')

with st.expander("**Monthly report**"):
    pass

with st.expander("**Annual report**"):
    pass

weekly_budget_summary = []
weekly_graph = []
weekly_income_category = []
weekly_expense_category = []

#%%
# Monthly report
# Annual report
