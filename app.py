import streamlit as st

st.title("Solar Qualification Bot")

st.write("Answer a few quick questions below.")

# Questions
q1 = st.radio(
    "Have you looked into solar for your home before?",
    ["Yes", "No"]
)

q2 = st.radio(
    "Are you the homeowner there?",
    ["Yes", "No"]
)

bill = st.number_input(
    "About what do you normally pay for electricity each month? ($)",
    min_value=0
)

q4 = st.radio(
    "If we could lower that bill, is that something you'd want to explore?",
    ["Yes", "No"]
)

name = st.text_input("Your name")
phone = st.text_input("Best phone number")

# Button
if st.button("Check Qualification"):

    if q1 == "Yes" and q2 == "Yes" and bill > 120 and q4 == "Yes":
        st.success("You qualify for a solar consultation.")
        st.write("Lead captured successfully.")

    else:
        st.error("Based on your answers, you do not qualify at this time.")
