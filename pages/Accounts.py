#%%
import os
import pandas as pd
import streamlit as st
import numpy as np

#%%
# PAGE STATE CONTROL
if "current_page" not in st.session_state:
    st.session_state.current_page = "main"
if "edit_df" not in st.session_state:
    st.session_state.edit_df = pd.DataFrame()

# Files
transaction_file = "data/transaction.csv"
accounts_file = "data/accounts.csv"

COL_MONEY_IN = "Money received"
COL_MONEY_OUT = "Payment"

#%%
# PAGE 1 — MAIN OVERVIEW
if st.session_state.current_page == "main":
    st.title("💰 Accounts")

    # Read transactions
    if os.path.exists(transaction_file) and os.path.getsize(transaction_file) > 0:
        transaction_df = pd.read_csv(transaction_file)
    else:
        st.warning("No transaction data found.")
        transaction_df = pd.DataFrame(columns=["Account", COL_MONEY_IN, COL_MONEY_OUT])

    # Load saved accounts
    if os.path.exists(accounts_file):
        accounts_df = pd.read_csv(accounts_file)
    else:
        accounts_df = pd.DataFrame(columns=['Account', 'Balance (IDR)', 'Goal', '%'])

    if not transaction_df.empty:
        # Calculate balances
        income_expense_accounts = pd.pivot_table(
            transaction_df,
            index="Account",
            values=[COL_MONEY_IN, COL_MONEY_OUT],
            aggfunc='sum'
        ).reset_index()

        income_expense_accounts['Net balance'] = (
            income_expense_accounts[COL_MONEY_IN] - income_expense_accounts[COL_MONEY_OUT]
        )

        accounts_summary = income_expense_accounts[['Account', 'Net balance']].copy()
        accounts_summary.columns = ['Account', 'Balance (IDR)']

        # Merge with goals
        accounts_summary = accounts_summary.merge(
            accounts_df[['Account', 'Goal']], on='Account', how='left'
        ) if not accounts_df.empty else accounts_summary.assign(Goal=None)

        # Calculate %
        accounts_summary['%'] = np.where(
            (accounts_summary['Goal'].notna()) & (accounts_summary['Goal'] != 0),
            round(100 * accounts_summary['Balance (IDR)'] / accounts_summary['Goal'], 2),
            None
        )

        # Add total row
        total_balance = accounts_summary['Balance (IDR)'].sum()
        total_goal = accounts_summary['Goal'].sum(skipna=True)
        total_percent = (
            round(100 * total_balance / total_goal, 2)
            if pd.notnull(total_goal) and total_goal != 0 else None
        )

        total_row = pd.DataFrame([{
            'Account': 'Total',
            'Balance (IDR)': total_balance,
            'Goal': total_goal,
            '%': total_percent
        }])

        account_total_summary = pd.concat([accounts_summary, total_row], ignore_index=True)

        # Show table
        st.dataframe(account_total_summary, hide_index=True)

    # Edit button → switch page
    if st.button("Edit Goals"):
        st.session_state.edit_df = accounts_summary.copy()
        st.session_state.current_page = "edit"
        st.rerun()

#%%
# PAGE 2 — EDIT GOALS
elif st.session_state.current_page == "edit":
    st.title("✏ Edit Goals")

    edited_goals = st.data_editor(
        st.session_state.edit_df,
        num_rows="fixed",
        use_container_width=True,
        column_config={
            'Account': st.column_config.TextColumn(disabled=True),
            'Balance (IDR)': st.column_config.NumberColumn(disabled=True),
            '%': st.column_config.NumberColumn(disabled=True)
        }
    )

    if st.button("Save"):
        edited_goals.to_csv(accounts_file, index=False)
        st.success("Goals updated!")
        st.session_state.current_page = "main"
        st.rerun()
