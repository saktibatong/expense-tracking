#%%
import os
import pandas as pd
from datetime import datetime
import streamlit as st
import matplotlib.pyplot as plt

current_dir = os.getcwd()
os.chdir(current_dir)

#%%
def accounts(account_df: str) -> list:
    all_accounts = account_df['Accounts']
    return all_accounts

def income_categories():
    return

def input_transaction():
    selected_acc = input('Acount name:')
    transaction_datetime = datetime.now()
    transaction_type = 'a'
    payee = input('Transaction name:')
    payment = input('Price:')
    deposit = input('Payment received:')

    transaction_list = [selected_acc, payee, transaction_datetime, payment, deposit]
    return transaction_list

def transaction_analysis(transaction_df, input):
    return

#%%
accounts_df = pd.read_excel(r"./Database/Money Manager.xlsx", sheet_name='Accounts')
accounts_df

# %%
transaction_df = pd.read_excel(r"./Database/Money Manager.xlsx", sheet_name='Transactions')
transaction_df

# %%
accounts(accounts_df)

# %%
# Transaction calculation
input_transaction()

# %%
st.title("Questionnaire")

# Define questions
questions = {
    "How satisfied are you?": ["Very satisfied", "Satisfied", "Neutral", "Dissatisfied"],
    "What is your favorite color?": ["Red", "Blue", "Green", "Other"],
    "How often do you exercise?": ["Daily", "Weekly", "Rarely", "Never"]
}

# Store answers
answers = {}

for q, opts in questions.items():
    answers[q] = st.selectbox(q, opts)

# Button to submit
if st.button("Submit"):
    df = pd.DataFrame([answers])
    st.write("Your answers:")
    st.dataframe(df)
    
# %%

# File to save the data
DATA_FILE = "money_data.csv"

# Load existing data
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Date", "Type", "Category", "Amount"])

st.title("💰 Money Tracker")

# Input form
with st.form("money_form"):
    date = st.date_input("Date")
    entry_type = st.selectbox("Type", ["Income", "Expense"])
    category = st.selectbox("Category", ["Food", "Transport", "Salary", "Shopping", "Other"])
    amount = st.number_input("Amount (IDR)", min_value=0.0, step=1000.0)

    submitted = st.form_submit_button("Submit")
    if submitted:
        new_data = pd.DataFrame([[date, entry_type, category, amount]], columns=df.columns)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Entry added!")

# Show data
st.subheader("📄 All Entries")
st.dataframe(df)

# Analysis
if not df.empty:
    st.subheader("📊 Total Income and Expenses")
    totals = df.groupby("Type")["Amount"].sum()
    st.bar_chart(totals)

    st.subheader("📂 Breakdown by Category")
    category_totals = df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum()
    fig, ax = plt.subplots()
    category_totals.plot.pie(autopct="%1.1f%%", ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)
