#%%
import os
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

#%%
# Page title
st.set_page_config(page_title="BATS Money manger", layout="wide")

# Sidebar
money_manager_option = st.sidebar.selectbox("Choose category", ["Home", "Budget", "Accounts", "Transactions", "Report", "Goals"])

#%%
# GENERAL DATA
# Account, income and expense categories
account_list = ['Checking BRI', 'Checking BCA', 'Checking JAGO', 'Checking Walet', 'Debt', 'Receivable', 'Saving JAGO', 'Saving Bibit']
income_category = ['Dividends', 'Financial Aid', 'Gifts Received', 'Interest Income', 'Other Income', 'Refunds/Reimbursements', 'Teaching Income', 'Wages & Tips']
expense_category = ['Alimony', 'Car Insurance', 'Car Payment', 'Car Repair / Licenses', 'Car Replacement Fund', 'Charity', 'Child Care', 'Cleaning', 'Clothing', 'Debt',
                    'Dining', 'Discretionary', 'Doctor / Dentist', 'Education', 'Emergency Fund', 'E-Money', 'Family', 'Food & Drink', 'Fuel', 'Fun / Entertainment',
                    'Furniture / Appliances', 'Gifts Given', 'Gopay', 'Groceries', 'Haircare', 'Health Insurance', 'Home Insurance', 'Home Supplies', 'Interest Expense', 'Life Insurance',
                    'Medicine', 'Miscellaneous', 'Mortgage / Rent', 'Other Savings', 'OVO', 'Personal Supplies', 'Playing and Entertaining', 'Retirement Fund', 'Shopee Pay', 'Sport',
                    'Subscriptions/Dues', 'Taxes', 'Transfer', 'Transportation', 'Util. Electricity', 'Util. Gas', 'Util. Phone(s)', 'Util. TV / Internet', 'Util. Water', 'Work Bills']

#%%
# HOME
if money_manager_option == "Home":
    # Homepage title
    st.title("💰 Money Manager")

    # Daily transaction
    with st.container():
        st.subheader('📄 Daily Transaction')

        # Load existing data
        transaction_file = "transaction.csv"

        if os.path.exists(transaction_file):
            transaction_df = pd.read_csv(transaction_file)
        else:
            transaction_df = pd.DataFrame(columns=["Date", "Payee", "Account", "Transaction category", "Income category", "Expense category", "Money received", "Payment"])

        # Input form
        date = st.date_input("Date")
        st.caption("Specific date on which a financial transaction occur")

        payee = st.text_input("Transaction name", placeholder="Enter the transaction name")
        st.caption("The recipient of funds, whether it's for a bill, a service, or any other type of financial transfer")

        account = st.selectbox("Account", account_list)
        st.caption("A record used to track financial transactions and manage financial activities")

        transaction_category = st.selectbox("Transaction category", ["Income", "Expense", "Transfer"])
        st.caption("The specific category of a financial transaction")

        # Conditional of transaction category
        selected_income = ""
        selected_expense = ""
        received_account = ""
        deposit = 0.00
        payment = 0.00
        if transaction_category == "Income":
            selected_income = st.selectbox("Income category", income_category)
            selected_expense = ""
            deposit = st.number_input("Amount (IDR)", min_value=0.00, step=500.00, format="%.0f")
            payment = 0.00

        elif transaction_category == "Expense":
            selected_income = ""
            selected_expense = st.selectbox("Expense category", expense_category)
            deposit = 0.00
            payment = st.number_input("Amount (IDR)", min_value=0.00, step=500.00, format="%.0f")

        else: # transaction category is transfer
            received_account = st.selectbox("Received account", [i for i in account_list if i != account])
            selected_income = "Transfer"
            selected_expense = "Transfer"
            payment = st.number_input("Amount (IDR)", min_value=0.0, step=500.00, format="%.0f")
            deposit = payment

        # Dataframe analysis after submit a transaction
        if st.button("Submit"):
            if transaction_category == "Income" or transaction_category == "Expense":
                new_data = pd.DataFrame([[date, payee, account, transaction_category, selected_income, selected_expense, deposit, payment]], columns=df.columns)
                transaction_df = pd.concat([transaction_df, new_data], ignore_index=True)
                transaction_df.to_csv(transaction_file, index=False)

            else: # transaction category is transfer
                new_data1 = pd.DataFrame([[date, payee, account, transaction_category, '', selected_expense, 0.00, payment]], columns=df.columns)
                transaction_df = pd.concat([transaction_df, new_data1], ignore_index=True)
                transaction_df.to_csv(transaction_file, index=False)

                new_data2 = pd.DataFrame([[date, payee, received_account, transaction_category, selected_income, '', deposit, 0.00]], columns=df.columns)
                transaction_df = pd.concat([transaction_df, new_data2], ignore_index=True)
                transaction_df.to_csv(transaction_file, index=False)

            st.success("Entry added!")

            formatted_amount = f"{(deposit or payment):,.0f}".replace(",", ".")
            st.write(f"📅 **{date}** — 💳 **{account}** — {transaction_category} of **Rp {formatted_amount}**")

    # Show last 10 transactions
    with st.container():
        st.subheader("📄 Last 10 transactions")
        last_transactional_df = transaction_df.copy()
        last_transactional_df['Sub-category'] = last_transactional_df['Income category'].fillna('') + last_transactional_df['Expense category'].fillna('')
        last_transactional_df['Amonut (IDR)'] = last_transactional_df['Money received'].fillna('') + last_transactional_df['Payment'].fillna('')
        last_transactional_df = last_transactional_df.drop(columns=['Income category', 'Expense category', 'Money received', 'Payment'])
        last_transactional_df = last_transactional_df.tail(10)  # Get last 10
        last_transactional_df.index = range(1, len(transaction_df) + 1)  # Set index from 1
        st.dataframe(last_transactional_df, hide_index=False)  # Show the index

#%%
# BUDGET
if money_manager_option == "Budget":
    # Account title
    st.title("💰 Money Manager")

    with st.container():
        # Dudget data
        income_budget_file = "income_monthly_budget.csv"
        expense_budget_file = "expense_monthly_budget.csv"
        month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        # Load existing data
        if os.path.exists(income_budget_file):
            income_budget_df = pd.read_csv(income_budget_file)
            expense_budget_df = pd.read_csv(expense_budget_file)
        else:
            income_budget_df = pd.DataFrame(index=income_category, columns=month)
            expense_budget_df = pd.DataFrame(index=expense_category, columns=month)

        st.subheader('📄 Monthly budget')
        with st.expander("**Income budget**"):
            # Income budget editor
            edited_income_budget_df = st.data_editor(income_budget_df, num_rows="fixed", use_container_width=True)

            if st.button("Save income budget"):
                edited_income_budget_df.to_csv(income_budget_file, index=True)
                st.success("Saved to income budget")

        with st.expander("**Expense budget**"):
            # Expense budget editor
            edited_expense_budget_df = st.data_editor(expense_budget_df, num_rows="fixed", use_container_width=True)

            if st.button("Save expense budget"):
                edited_expense_budget_df.to_csv(expense_budget_file, index=True)
                st.success("Saved to expense budget")

#%%
# ACCOUNTS
if money_manager_option == "Accounts":
    # Account title
    st.title("💰 Money Manager")

    with st.container():
        st.subheader("📄 Accounts net balance")

        # Read transactions
        transaction_file = "transaction.csv"
        transaction_df = pd.read_csv(transaction_file)

        # Calculate accounts money
        income_expense_accounts = pd.pivot_table(transaction_df, index="Account", values=['Money received', 'Payment'], aggfunc='sum')
        income_expense_accounts.reset_index(inplace=True)
        income_expense_accounts['Net balance'] = income_expense_accounts['Money received'] - income_expense_accounts['Payment']

        account_total = income_expense_accounts[['Net balance']].sum()
        account_total['Account'] = 'Total'
        income_expense_total_acounts = pd.concat([income_expense_accounts, pd.DataFrame([account_total])], ignore_index=True)

        accounts_summary = income_expense_total_acounts[['Account', 'Net balance']]
        accounts_summary.columns = ['Account', 'Net balance (IDR)']
        st.dataframe(accounts_summary, hide_index=True)

#%%
# TRANSACTIONS
if money_manager_option == "Transactions":
    data = {
        "Month": ["Jan", "Feb", "Mar", "Apr"],
        "Sales": [100, 120, 140, 160],
        "Profit": [20, 30, 35, 50]
    }
    df = pd.DataFrame(data)

    # Dashboard Title
    st.title("📊 Monthly Sales Dashboard")

    # KPI Metrics
    col1, col2 = st.columns(2)
    col1.metric("Total Sales", f"${df['Sales'].sum()}K")
    col2.metric("Total Profit", f"${df['Profit'].sum()}K")

    # Tabs
    tab1, tab2 = st.tabs(["📈 Chart", "📄 Raw Data"])
    with tab1:
        st.bar_chart(df.set_index("Month"))
    with tab2:
        st.dataframe(df)

    ############################################
    st.title("🔍 Product Filter Tool")

    # Sample data
    df = pd.DataFrame({
        "Product": ["A", "B", "C", "D"],
        "Category": ["Food", "Drink", "Food", "Drink"],
        "Price": [10, 20, 15, 25]
    })

    # Sidebar filters
    category = st.sidebar.selectbox("Select Category", options=["All"] + df["Category"].unique().tolist())
    max_price = st.sidebar.slider("Max Price", 0, 30, 30)

    # Filter logic
    filtered_df = df.copy()
    if category != "All":
        filtered_df = filtered_df[filtered_df["Category"] == category]
    filtered_df = filtered_df[filtered_df["Price"] <= max_price]

    # Display
    st.subheader("Filtered Products")

    ############################################
    # Sample data
    df = pd.DataFrame({
        "Product": ["Apple", "Banana", "Milk", "Soda", "Bread"],
        "Category": ["Fruit", "Fruit", "Dairy", "Drink", "Bakery"],
        "Price": [5, 3, 10, 7, 4],
        "In Stock": [True, False, True, True, False]
    })

    # Filters
    category = st.selectbox("Choose a category", ["All"] + df["Category"].unique().tolist())
    max_price = st.slider("Max Price", 0, 15, 10)
    only_available = st.checkbox("Only show products in stock")

    # Apply filters
    filtered_df = df.copy()
    if category != "All":
        filtered_df = filtered_df[filtered_df["Category"] == category]
    filtered_df = filtered_df[filtered_df["Price"] <= max_price]
    if only_available:
        filtered_df = filtered_df[filtered_df["In Stock"] == True]

    # Show result
    st.subheader("Filtered Products")
    st.dataframe(filtered_df)

    ###########################
    st.title("📊 Regional Sales Filter")

    # Sample sales data
    df = pd.DataFrame({
        "Region": ["East", "West", "North", "South", "East", "West"],
        "Month": ["Jan", "Jan", "Jan", "Jan", "Feb", "Feb"],
        "Sales": [120, 90, 100, 80, 140, 110]
    })

    # Filters
    selected_regions = st.multiselect("Select regions", df["Region"].unique(), default=["East", "West"])
    selected_month = st.radio("Select month", df["Month"].unique())

    # Apply filters
    filtered = df[(df["Region"].isin(selected_regions)) & (df["Month"] == selected_month)]

    # Show results
    st.subheader("Filtered Sales")
    st.dataframe(filtered)
    st.bar_chart(filtered.set_index("Region")["Sales"])

    ####################
    st.title("📅 Filter Orders by Date")

    # Create sample date data
    dates = pd.date_range(start="2025-01-01", periods=10, freq="D")
    df = pd.DataFrame({
        "Order ID": range(1, 11),
        "Order Date": dates,
        "Amount": [50, 80, 40, 70, 90, 60, 75, 55, 85, 100]
    })

    # Date filter
    start_date, end_date = st.date_input("Select date range", [dates.min(), dates.max()])

    # Filter
    filtered_df = df[(df["Order Date"] >= pd.to_datetime(start_date)) &
                    (df["Order Date"] <= pd.to_datetime(end_date))]

    # Show result
    st.subheader("Filtered Orders")
    st.dataframe(filtered_df)

#%%
# REPORT
if money_manager_option == "Report":
    # Account title
    st.title("💰 Money Manager")
    st.subheader("📄 Report")

    # Weekly repot   
    with st.expander("**Weekly report**"):
        week_mode = st.selectbox("Week mode", ['Ongoing week', 'Specified week'])

        if week_mode == 'Specified week':
            today_year = datetime.now().year
            select_week_start_year = f"{today_year}-01-01"
            select_week_end_year = f"{today_year}-12-31"
            weekly_dates = [d.date() for d in pd.date_range(start=select_week_start_year, end=select_week_end_year, freq='W-MON')]
            specified_start = st.selectbox("Choose week", weekly_dates)

        # 
        week_interval = st.selectbox("Week interval", ['Weekly', 'Bi-weekly'])

        if week_mode == 'Ongoing week':
            today_datetime = datetime.now()
            start_of_week = today_datetime - timedelta(days=today_datetime.weekday())
            begin = start_of_week.date()

            if week_interval == 'Weekly':
                end = begin + timedelta(days=6)
                st.markdown(f'**Begin week:** {begin}')
                st.markdown(f'**End week:** {end}')
            else:
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

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Sales", "$100K")
            
        with col2:
            st.metric("Profit", "$25K")
        
        data = {
        "Month": ["January", "February", "March", "April"],
        "Sales": [100, 150, 200, 170],
        "Profit": [30, 50, 70, 60]
        }
        df = pd.DataFrame(data)

        # Create Tabs
        tab1, tab2, tab3 = st.tabs(["📊 Summary", "📈 Chart", "📄 Detailed Data"])

        with tab1:
            st.subheader("Summary Statistics")
            st.write(df.describe())

        with tab2:
            st.subheader("Sales Line Chart")
            st.line_chart(df.set_index("Month")[["Sales", "Profit"]])
        
        with tab3:
            st.subheader("Raw Data")
            st.dataframe(df)

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

