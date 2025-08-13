#%%
import os
import pandas as pd
import streamlit as st

#%%
st.title("💰 Money Manager")
transaction_account = st.selectbox('Account', ['All accounts'] + st.session_state["account_list"])
transaction_start_date = st.date_input('Start date')
transaction_end_date = st.date_input('End date')
transaction_category = st.selectbox('Transaction category', ['All categories', 'Income', 'Expense', 'Transfer'])

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
