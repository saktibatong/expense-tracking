#%%
import os
import pandas as pd
from datetime import datetime
import streamlit as st

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
