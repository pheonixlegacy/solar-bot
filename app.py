import streamlit as st

# Page title
st.title("Free Solar Savings Check")

st.write("Answer a few quick questions to see if you qualify.")

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
    "About what do you normally pay for electricity each month ($)",
    min_value=0
)

q4 = st.radio(
    "If we could lower that bill, would you be interested?",
    ["Yes", "No"]
)

name = st.text_input("Your name")
phone = st.text_input("Best phone number")

# Submit button
if st.button("Check Qualification"):

    # Basic validation
    if name == "":
        st.error("Please enter your name.")
    
    elif len(phone) < 10:
        st.error("Please enter a valid phone number.")

    else:
        # Qualification logic
        if q1 == "Yes" and q2 == "Yes" and bill > 120 and q4 == "Yes":
            st.success("✅ You qualify for a solar consultation.")
            st.write("Our team will contact you shortly.")

        else:
            st.warning("⚠️ Based on your answers, you may not qualify at this time.")
