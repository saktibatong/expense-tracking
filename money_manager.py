#%%
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

#%%
# File to save the data
transaction_file = "transaction.csv"

# Load existing data
if os.path.exists(transaction_file):
    df = pd.read_csv(transaction_file)
else:
    df = pd.DataFrame(columns=["Date", "Payee", "Account", "Transaction category", "Income category", "Expense category", "Money received", "Payment"])

#%%
st.title("💰 Money Manager")

st.subheader('📄 Daily Transaction')
account_list = ['Checking BRI', 'Checking BCA', 'Checking JAGO', 'Checking Walet', 'Debt', 'Receivable', 'Saving JAGO', 'Saving Bibit']
income_category = ['Dividends', 'Financial Aid', 'Gifts Received', 'Interest Income', 'Other Income', 'Refunds/Reimbursements', 'Teaching Income', 'Wages & Tips']
expense_category = ['Alimony', 'Car Insurance', 'Car Payment', 'Car Repair / Licenses', 'Car Replacement Fund', 'Charity', 'Child Care', 'Cleaning', 'Clothing', 'Debt',
                    'Dining', 'Discretionary', 'Doctor / Dentist', 'Education', 'Emergency Fund', 'E-Money', 'Family', 'Food & Drink', 'Fuel', 'Fun / Entertainment',
                    'Furniture / Appliances', 'Gifts Given', 'Gopay', 'Groceries', 'Haircare', 'Health Insurance', 'Home Insurance', 'Home Supplies', 'Interest Expense', 'Life Insurance',
                    'Medicine', 'Miscellaneous', 'Mortgage / Rent', 'Other Savings', 'OVO', 'Personal Supplies', 'Playing and Entertaining', 'Retirement Fund', 'Shopee Pay', 'Sport',
                    'Subscriptions/Dues', 'Taxes', 'Transfer', 'Transportation', 'Util. Electricity', 'Util. Gas', 'Util. Phone(s)', 'Util. TV / Internet', 'Util. Water', 'Work Bills']

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
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(transaction_file, index=False)

    else: # transaction category is transfer
        new_data1 = pd.DataFrame([[date, payee, account, transaction_category, '', selected_expense, 0.00, payment]], columns=df.columns)
        df = pd.concat([df, new_data1], ignore_index=True)
        df.to_csv(transaction_file, index=False)

        new_data2 = pd.DataFrame([[date, payee, received_account, transaction_category, selected_income, '', deposit, 0.00]], columns=df.columns)
        df = pd.concat([df, new_data2], ignore_index=True)
        df.to_csv(transaction_file, index=False)

    st.success("Entry added!")

    formatted_amount = f"{(deposit or payment):,.0f}".replace(",", ".")
    st.write(f"📅 **{date}** — 💳 **{account}** — {transaction_category} of **Rp {formatted_amount}**")

#%%
# Show last 10 transactions
st.subheader("📄 Last 10 transactions")
last_transactional_df = df.copy()
last_transactional_df['Sub-category'] = last_transactional_df['Income category'].fillna('') + last_transactional_df['Expense category'].fillna('')
last_transactional_df['Amonut (IDR)'] = last_transactional_df['Money received'].fillna('') + last_transactional_df['Payment'].fillna('')
last_transactional_df = last_transactional_df.drop(columns=['Income category', 'Expense category', 'Money received', 'Payment'])
last_transactional_df = last_transactional_df.tail(10)  # Get last 10
last_transactional_df.index = range(1, len(df) + 1)  # Set index from 1
st.dataframe(last_transactional_df, hide_index=False)  # Show the index

#%%
# Account
st.subheader("📄 Accounts net balance")
income_expense_accounts = pd.pivot_table(df, index="Account", values=['Money received', 'Payment'], aggfunc='sum')
income_expense_accounts.reset_index(inplace=True)
income_expense_accounts['Net balance'] = income_expense_accounts['Money received'] - income_expense_accounts['Payment']

account_total = income_expense_accounts[['Net balance']].sum()
account_total['Account'] = 'Total'
income_expense_total_acounts = pd.concat([income_expense_accounts, pd.DataFrame([account_total])], ignore_index=True)

accounts_summary = income_expense_total_acounts[['Account', 'Net balance']]
accounts_summary.columns = ['Account', 'Net balance (IDR)']
st.dataframe(accounts_summary, hide_index=True)

#%%
# Analysis

