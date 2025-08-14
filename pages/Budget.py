#%%
import os
import pandas as pd
import streamlit as st

#%%
# BUDGET
# Account title
st.title("📄 Monthly budget")

with st.container():
    # Dudget data
    income_budget_file = "data/income_monthly_budget.csv"
    expense_budget_file = "data/expense_monthly_budget.csv"
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Load income budget
    if os.path.exists(income_budget_file):
        income_budget_df = pd.read_csv(income_budget_file, index_col="Income Category")
    else:
        income_budget_df = pd.DataFrame(index=st.session_state["income_category"], columns=month)
        income_budget_df.index.name = "Income Category"
    
    # Load expense budget
    if os.path.exists(expense_budget_file):
        expense_budget_df = pd.read_csv(expense_budget_file, index_col="Expense Category")
    else:
        expense_budget_df = pd.DataFrame(index=st.session_state["expense_category"], columns=month)
        expense_budget_df.index.name = "Expense Category"

    # Fill budget
    with st.expander("**Income budget**"):
        # Income budget editor
        edited_income_budget_df = st.data_editor(income_budget_df, num_rows="fixed", use_container_width=True)

        if st.button("Save income budget", key="save_income_budget"):
            edited_income_budget_df.to_csv(income_budget_file, index_label=edited_income_budget_df.index.name)
            st.success("Saved to income budget")
            st.rerun()

    with st.expander("**Expense budget**"):
        # Expense budget editor
        edited_expense_budget_df = st.data_editor(expense_budget_df, num_rows="fixed", use_container_width=True)

        if st.button("Save expense budget", key="save_expense_budget"):
            edited_expense_budget_df.to_csv(expense_budget_file, index_label=edited_expense_budget_df.index.name)
            st.success("Saved to expense budget")
            st.rerun()