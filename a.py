import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

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
