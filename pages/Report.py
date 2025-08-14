#%%
import pandas as pd
import streamlit as st
from datetime import date, datetime, timedelta
import altair as alt

#%%
# FUNCTION
def display_transaction_summary(transaction_df, begin, end, category_map=None):
    """
    Filter transactions by date range and display summary, chart, and detailed table in Streamlit.
    
    Parameters:
        transaction_df (pd.DataFrame): Transaction data containing 'Date' and 'Transaction category'.
        begin (date): Start date for filtering.
        end (date): End date for filtering.
        category_map (dict, optional): Mapping of category names to corresponding amount columns.
    """
    # Default category map
    if category_map is None:
        category_map = {
            "Income": "Money received",
            "Expense": "Payment",
            "Transfer": "Payment"
        }

    # Filter by start and end date
    filtered_start_date = pd.to_datetime(begin)
    filtered_end_date = pd.to_datetime(end)

    filtered_df = transaction_df.copy()
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
    filtered_df = filtered_df[
        (filtered_df['Date'] >= filtered_start_date) &
        (filtered_df['Date'] <= filtered_end_date)
    ].reset_index(drop=True)
    filtered_df.index += 1

    # Calculate totals
    total_data = {
        cat: filtered_df.loc[filtered_df["Transaction category"] == cat, col].sum()
        for cat, col in category_map.items()
    }

    # Tabs in Streamlit
    tab1, tab2, tab3 = st.tabs(["📊 Summary", "📈 Chart", "📄 Detailed Data"])

    with tab1:
        col1, col2, col3 = st.columns(3)
        col1.metric("Income", f"IDR {total_data['Income']:,.0f}")
        col2.metric("Expense", f"IDR {total_data['Expense']:,.0f}")
        col3.metric("Transfer", f"IDR {total_data['Transfer']:,.0f}")

    with tab2:
        total_df = pd.DataFrame({
            "Type": list(total_data.keys()),
            "Amount": list(total_data.values())
        })
        chart = (
            alt.Chart(total_df)
            .mark_bar()
            .encode(
                x=alt.X("Type:N", title="Transaction Type"),
                y=alt.Y("Amount:Q", title="Total Amount"),
                color=alt.Color(
                    "Type:N",
                    scale=alt.Scale(
                        domain=["Income", "Expense", "Transfer"],
                        range=["#2ecc71", "#e74c3c", "#3498db"]
                    )
                )
            )
        )
        st.altair_chart(chart, use_container_width=True)

    with tab3:
        st.dataframe(filtered_df)

#%%
# Account title
st.title("💰 Money Report for Ongoing Year")

# Read transactions
transaction_file = "data/transaction.csv"
transaction_df = pd.read_csv(transaction_file)

#%%
selected_report = st.radio('Select report', ['Weekly', 'Monthly', 'Annual'])

# Find all data related to ongoing year
today = datetime.today()
today_year = datetime.now().year
select_start_year = f"{today_year}-01-01"
select_end_year = f"{today_year}-12-31"

#%%
# Weekly repot
if selected_report == 'Weekly':
    # week interval
    week_interval = st.radio("Week interval", ['Weekly', 'Bi-weekly'])

    weekly_dates = [d.date() for d in pd.date_range(start=select_start_year, end=select_end_year, freq='W-MON')] # Get all weeks in a year
    current_week_start = (today - timedelta(days=today.weekday())).date() # Find the Monday of the current week
    
    # Find the index of the current week in the list
    if current_week_start in weekly_dates:
        default_index = weekly_dates.index(current_week_start)
    else:
        default_index = 0  # fallback

    # select week
    specified_start = st.selectbox("Select week",
                                    weekly_dates,
                                    index=default_index)

    if week_interval == 'Weekly':
        specified_end = specified_start + timedelta(days=6)
        st.markdown(f'**Begin week:** {specified_start}')
        st.markdown(f'**End week:** {specified_end}')

        display_transaction_summary(transaction_df, specified_start, specified_end, category_map=None)

    else: # Bi-weekly
        specified_end = specified_start + timedelta(days=13)
        st.markdown(f'**Begin week:** {specified_start}')
        st.markdown(f'**End week:** {specified_end}')

        display_transaction_summary(transaction_df, specified_start, specified_end, category_map=None)

#%%
if selected_report == 'Monthly':
    # Get all months in a year
    monthly_dates = [
        m.strftime("%b %Y")  # format as string
        for m in pd.date_range(
            start=select_start_year,
            end=select_end_year,
            freq='ME'  # 'M' is month end; 'MS' is month start
        )
    ]
    current_month_start = today.replace(day=1).strftime("%b %Y")

    # Find the index of the current week in the list
    if current_month_start in monthly_dates:
        default_index = monthly_dates.index(current_month_start)
    else:
        default_index = 0  # fallback

    # select week
    specified_str = st.selectbox("Select month",
                                    monthly_dates,
                                    index=default_index)
    
    # Convert to datetime
    specified_start = datetime.strptime(specified_str, "%b %Y").date()
    specified_end = pd.date_range(start=specified_start, periods=1, freq='ME')[0].date()
    
    st.markdown(f'**Begin month:** {specified_start}')
    st.markdown(f'**End month:** {specified_end}')

    display_transaction_summary(transaction_df, specified_start, specified_end, category_map=None)
#%%
if selected_report == 'Annual':
    st.markdown(f'**Begin month:** {select_start_year}')
    st.markdown(f'**End month:** {select_end_year}')

    display_transaction_summary(transaction_df, select_start_year, select_end_year, category_map=None)

weekly_budget_summary = []
weekly_income_category = []
weekly_expense_category = []
