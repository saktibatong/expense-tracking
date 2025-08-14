#%%
from datetime import date, timedelta
import pandas as pd
import streamlit as st
import altair as alt

#%%
st.title("💰 Transactions")

# Read transactions
transaction_file = "data/transaction.csv"
transaction_df = pd.read_csv(transaction_file)

# Ensure proper date type
transaction_df["Date"] = pd.to_datetime(transaction_df["Date"], errors="coerce")
transaction_df = transaction_df.dropna(subset=["Date"])

#%%
st.subheader('📄 Select Transactions')

# Account and transaction category
transaction_account = st.selectbox(
'Account', 
    ['All accounts'] + st.session_state["account_list"]
)

transaction_category = st.multiselect(
    "Transaction category",
    transaction_df["Transaction category"].unique(),
    default=['Income', 'Expense']
)
# Default display dates
today = date.today()
yesterday = today - timedelta(days=1)

transaction_start_date = st.date_input('Start date', value=yesterday)
transaction_end_date = st.date_input('End date', value=today)

#%%
# Filtering
filtered_df = transaction_df.copy()

if transaction_account != "All accounts":
    filtered_df = filtered_df.query("Account == @transaction_account")

if transaction_category:
    filtered_df = filtered_df[filtered_df["Transaction category"].isin(transaction_category)]

filtered_df = filtered_df[
    (filtered_df["Date"] >= pd.to_datetime(transaction_start_date)) &
    (filtered_df["Date"] <= pd.to_datetime(transaction_end_date))
]

# Reset index for table display
filtered_df = filtered_df.reset_index(drop=True)
filtered_df.index += 1

#%%
# Prepare totals (always include all categories for consistent colors)
category_map = {
    "Income": "Money received",
    "Expense": "Payment",
    "Transfer": "Payment"
}
total_data = {
    cat: filtered_df.loc[filtered_df["Transaction category"] == cat, col].sum()
    if cat in transaction_category else 0
    for cat, col in category_map.items()
}

#%%
st.subheader('📄 Transaction data')

tab1, tab2, tab3 = st.tabs(["📊 Summary", "📈 Chart", "📄 Detailed Data"])

# Tab 1: Summary
with tab1:
    st.subheader("Total Money Over Time")
    col1, col2, col3 = st.columns(3)
    col1.metric("Income", f"IDR {total_data['Income']:,.0f}")
    col2.metric("Expense", f"IDR {total_data['Expense']:,.0f}")
    col3.metric("Transfer", f"IDR {total_data['Transfer']:,.0f}")

# Tab 2: Charts
with tab2:
    if transaction_category:
        # Total Money Chart
        st.subheader("Total Money Over Time")
        total_df = pd.DataFrame({
            "Type": list(total_data.keys()),
            "Amount": list(total_data.values())
        })

        if total_df["Amount"].sum() == 0:
            st.info("No data available")
        else:
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

        # Detailed Money Chart
        st.subheader("Detailed Money Over Time")

        chart_df = (
            filtered_df.groupby(["Date", "Transaction category"])
            .agg({"Money received": "sum", "Payment": "sum"})
            .reset_index()
        )

        # Merge Income & Expense amounts into one column
        chart_df["Amount"] = chart_df.apply(
            lambda row: row["Money received"] if row["Transaction category"] == "Income" else row["Payment"],
            axis=1
        )

        chart_df = chart_df[["Date", "Transaction category", "Amount"]]
        chart_df["Date"] = chart_df["Date"].dt.strftime("%Y-%m-%d")

        if chart_df.empty:
            st.info("No data available")
        else:
            chart = (
                alt.Chart(chart_df)
                .mark_bar()
                .encode(
                    x=alt.X("Date:N", axis=alt.Axis(title="Date", labelAngle=-45)),
                    y=alt.Y("Amount:Q", axis=alt.Axis(title="Amount")),
                    color=alt.Color(
                        "Transaction category:N",
                        title="Category",
                        scale=alt.Scale(
                            domain=["Income", "Expense", "Transfer"],
                            range=["#2ecc71", "#e74c3c", "#3498db"]
                        )
                    ),
                    xOffset="Transaction category:N"
                )
            )
            st.altair_chart(chart, use_container_width=True)

    else:
        st.info("No category selected")

# Tab 3: Data Table
with tab3:
    if transaction_category:
        st.dataframe(filtered_df)
    else:
        st.info("No data available")
