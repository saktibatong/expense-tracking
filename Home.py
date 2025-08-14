#%%
import os
import pandas as pd
import streamlit as st
import altair as alt

#%% PAGE CONFIG
st.set_page_config(page_title="Home - Money Manager", layout="wide")
st.title("🏠 Home")
st.write("Welcome! Use the sidebar to navigate through your accounts, budgets, and reports.")

#%% SESSION STATE INITIALIZATION
if "account_list" not in st.session_state:
    st.session_state["account_list"] = [
        'Checking BRI', 'Checking BCA', 'Checking JAGO', 'Checking Walet',
        'Debt', 'Receivable', 'Saving JAGO', 'Saving Bibit'
    ]

if "income_category" not in st.session_state:
    st.session_state["income_category"] = [
        'Dividends', 'Financial Aid', 'Gifts Received', 'Interest Income', 'Other Income',
        'Refunds/Reimbursements', 'Teaching Income', 'Wages & Tips'
    ]

if "expense_category" not in st.session_state:
    st.session_state["expense_category"] = [
        'Alimony', 'Car Insurance', 'Car Payment', 'Car Repair / Licenses', 'Car Replacement Fund',
        'Charity', 'Child Care', 'Cleaning', 'Clothing', 'Debt', 'Dining', 'Discretionary',
        'Doctor / Dentist', 'Education', 'Emergency Fund', 'E-Money', 'Family', 'Food & Drink',
        'Fuel', 'Fun / Entertainment', 'Furniture / Appliances', 'Gifts Given', 'Gopay', 'Groceries',
        'Haircare', 'Health Insurance', 'Home Insurance', 'Home Supplies', 'Interest Expense',
        'Life Insurance', 'Medicine', 'Miscellaneous', 'Mortgage / Rent', 'Other Savings', 'OVO',
        'Personal Supplies', 'Playing and Entertaining', 'Retirement Fund', 'Shopee Pay', 'Sport',
        'Subscriptions/Dues', 'Taxes', 'Transfer', 'Transportation', 'Util. Electricity', 'Util. Gas',
        'Util. Phone(s)', 'Util. TV / Internet', 'Util. Water', 'Work Bills'
    ]

#%% LOAD TRANSACTIONS
transaction_file = "data/transaction.csv"
if os.path.exists(transaction_file):
    transaction_df = pd.read_csv(transaction_file)
else:
    transaction_df = pd.DataFrame(columns=[
        "Date", "Payee", "Account", "Transaction category",
        "Income category", "Expense category", "Money received", "Payment"
    ])

#%% DAILY TRANSACTION
with st.container():
    st.subheader('📄 Daily Transaction')

    date = st.date_input("Date")
    st.caption("Specific date on which a financial transaction occurs")

    payee = st.text_input("Transaction name", placeholder="Enter the transaction name")
    st.caption("The recipient of funds, whether it's for a bill, a service, or another transfer")

    account = st.selectbox("Account", st.session_state["account_list"])
    st.caption("A record used to track financial transactions")

    transaction_category = st.selectbox("Transaction category", ["Income", "Expense", "Transfer"])
    st.caption("The specific category of a financial transaction")

    selected_income, selected_expense, received_account = "", "", ""
    deposit, payment = 0.00, 0.00

    if transaction_category == "Income":
        selected_income = st.selectbox("Income category", st.session_state["income_category"])
        deposit = st.number_input("Amount (IDR)", min_value=0.00, step=500.00, format="%.0f")

    elif transaction_category == "Expense":
        selected_expense = st.selectbox("Expense category", st.session_state["expense_category"])
        payment = st.number_input("Amount (IDR)", min_value=0.00, step=500.00, format="%.0f")

    else:  # Transfer
        received_account = st.selectbox(
            "Received account",
            [i for i in st.session_state["account_list"] if i != account]
        )
        payment = st.number_input("Amount (IDR)", min_value=0.0, step=500.00, format="%.0f")
        deposit = payment
        selected_income = selected_expense = "Transfer"

    if st.button("Submit"):
        rows_to_add = []

        if transaction_category == "Income":
            rows_to_add.append([date, payee, account, transaction_category, selected_income, "", deposit, 0.00])
        elif transaction_category == "Expense":
            rows_to_add.append([date, payee, account, transaction_category, "", selected_expense, 0.00, payment])
        else:  # Transfer
            rows_to_add.extend([
                [date, payee, account, transaction_category, "", "Transfer", 0.00, payment],
                [date, payee, received_account, transaction_category, "Transfer", "", deposit, 0.00]
            ])

        transaction_df = pd.concat([transaction_df, pd.DataFrame(rows_to_add, columns=transaction_df.columns)], ignore_index=True)
        transaction_df.to_csv(transaction_file, index=False)

        formatted_amount = f"{(deposit or payment):,.0f}".replace(",", ".")
        st.success(f"Entry added! 📅 **{date}** — 💳 **{account}** — {transaction_category} of **Rp {formatted_amount}**")

#%% FILTER DATA BY TODAY
today = date.today()

# Filter for today's transactions
filtered_df = transaction_df.copy()
filtered_df = filtered_df[pd.to_datetime(filtered_df["Date"]).dt.date == today]

# Reset index for table display
filtered_df = filtered_df.reset_index(drop=True)
filtered_df.index += 1

# Category mapping for amounts
category_map = {
    "Income": "Money received",
    "Expense": "Payment",
    "Transfer": "Payment"  # Assuming Transfer amounts are in Payment
}

# Always calculate totals for all categories
total_data = {}
for cat, col in category_map.items():
    total_data[cat] = filtered_df.loc[
        filtered_df["Transaction category"] == cat, col
    ].sum()

#%% VISUALIZATION OF TODAY'S TRANSACTION
st.subheader('📄 Transactions of today')

# Present data
tab1, tab2, tab3 = st.tabs(["📊 Summary", "📈 Chart", "📄 Detailed Data"])

# Tab 1: Summary
with tab1:
    col1, col2, col3 = st.columns(3)
    col1.metric("Income", f"IDR {total_data['Income']:,.0f}")
    col2.metric("Expense", f"IDR {total_data['Expense']:,.0f}")
    col3.metric("Transfer", f"IDR {total_data['Transfer']:,.0f}")

# Tab 2: Charts
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

# Tab 3: Data Table
with tab3:
    st.dataframe(filtered_df)
