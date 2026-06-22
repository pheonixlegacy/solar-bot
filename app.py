import streamlit as st
import requests
import json

AIRTABLE_TOKEN = "HIDDEN"
BASE_ID = "appQdfXVEYUcfsb4t"
TABLE_NAME = "Solar leads"

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
        # Airtable save
        url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

        headers = {
            "Authorization": f"Bearer {AIRTABLE_TOKEN}",
            "Content-Type": "application/json"
        }

        data = {
            "fields": {
                "Name": name,
                "Phone": phone,
                "Looked into Solar": q1,
                "Homeowner": q2,
                "Monthly bill": bill,
                "interested": q4
            }
        }

        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(data)
        )

        if response.status_code == 200:
            if q1 == "Yes" and q2 == "Yes" and bill > 120 and q4 == "Yes":
                st.success("✅ You qualify for a solar consultation.")
                st.write("Your information has been saved.")
            else:
                st.warning("⚠️ Saved, but customer may not qualify.")
        else:
            st.error("Error saving lead.")
