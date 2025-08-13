#%%
import os
import pandas as pd
import streamlit as st

#%%
# PAGE STATE CONTROL
if "current_page" not in st.session_state:
    st.session_state.current_page = "main"

# Files
transaction_file = "data/transaction.csv"
accounts_file = "data/accounts.csv"

#%%
# PAGE 1 — MAIN OVERVIEW
if st.session_state.current_page == "main":
    st.title("💰 Accounts")

    # Read transactions
    transaction_df = pd.read_csv(transaction_file)

    # Load saved accounts
    if os.path.exists(accounts_file):
        accounts_df = pd.read_csv(accounts_file)
    else:
        accounts_df = pd.DataFrame(columns=['Account', 'Balance (IDR)', 'Goal', '%'])

    # Calculate balances
    income_expense_accounts = pd.pivot_table(
        transaction_df,
        index="Account",
        values=['Money received', 'Payment'],
        aggfunc='sum'
    ).reset_index()

    income_expense_accounts['Net balance'] = (
        income_expense_accounts['Money received'] - income_expense_accounts['Payment']
    )

    accounts_summary = income_expense_accounts[['Account', 'Net balance']].copy()
    accounts_summary.columns = ['Account', 'Balance (IDR)']

    # Merge with goals
    if not accounts_df.empty:
        accounts_summary = accounts_summary.merge(accounts_df[['Account', 'Goal']], on='Account', how='left')
    else:
        accounts_summary['Goal'] = None

    # Calculate %
    accounts_summary['%'] = accounts_summary.apply(
        lambda row: round(100 * row['Balance (IDR)'] / row['Goal'], 2)
        if pd.notnull(row['Goal']) and row['Goal'] != 0
        else None,
        axis=1
    )

    # Add total row
    total_balance = accounts_summary['Balance (IDR)'].sum()
    total_goal = accounts_summary['Goal'].sum(skipna=True)

    if accounts_summary[['Balance (IDR)', 'Goal']].notna().all().all(): # Only calculate if there are no NaNs in both columns
        total_percent = round(100 * total_balance / total_goal, 2) if total_goal else None
    else:
        total_percent = None

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
        # store editable data
        st.session_state.edit_df = accounts_summary.copy()  

        # go to page 2 - edit goals
        st.session_state.current_page = "edit"
        st.rerun()

#%%
# PAGE 2 — EDIT GOALS
elif st.session_state.current_page == "edit":
    st.title("✏ Edit Goals")

    # Editable table from session
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

    # Save button → go back to main
    if st.button("Save"):
        # save without index
        edited_goals.to_csv(accounts_file, index=False)  
        st.success("Goals updated!")

        # return to main page
        st.session_state.current_page = "main"  
        st.rerun()
