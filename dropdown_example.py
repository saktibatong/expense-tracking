import streamlit as st
import pandas as pd

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