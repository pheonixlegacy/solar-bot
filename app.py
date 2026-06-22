import streamlit as st
import requests
import json
from datetime import datetime

# ---------------- UI Styling ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a, #1e3a8a);
}

/* Main title */
h1 {
    text-align: center;
    color: white;
    font-size: 48px;
    font-weight: bold;
}

/* Buttons */
.stButton > button {
    width: 100%;
    height: 55px;
    border-radius: 14px;
    font-weight: bold;
    font-size: 18px;
    background-color: #22c55e;
    color: white;
}

/* Text input boxes */
.stTextInput > div > div > input {
    border-radius: 12px;
    padding: 10px;
}

/* Number input */
.stNumberInput input {
    border-radius: 12px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- Airtable config ----------------
AIRTABLE_TOKEN = "patryhLp1nLG9lPDB.3281b1a26270f1c0b90483155629d9d4acc983e23e3b885889fabd663372fe3b"
BASE_ID = "appQdfXVEYUcfsb4t"
TABLE_NAME = "Table 1"

# Allowed service ZIP codes
ALLOWED_ZIPS = [
    "60037",
    "60199",
    "60522",
    "60699"
]

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
zip_code = st.text_input("ZIP Code")

# Submit
if st.button("Check Qualification"):

    # validation
    if name == "":
        st.error("Please enter your name.")

    elif phone == "":
        st.error("Please enter your phone number.")

    elif zip_code == "":
        st.error("Please enter ZIP code.")

    elif zip_code not in ALLOWED_ZIPS:
        st.error("Sorry, we do not currently service your area.")

    elif q2 != "Yes":
        st.error("Sorry, only homeowners qualify at this time.")

    elif bill < 100:
        st.error("Your electric bill must be over $100 to qualify.")

    elif q4 != "Yes":
        st.error("No problem — reach out if you change your mind.")

    else:
        # qualifies
        st.success("You qualify for a solar consultation.")

        today = datetime.now().strftime("%m/%d/%Y")

        data = {
            "fields": {
                "Name": name,
                "Phone": phone,
                "ZIP": zip_code,
                "Looked into Solar": q1,
                "Homeowner": q2,
                "Monthly bill": bill,
                "interested": q4,
                "Date": today
            }
        }

        url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

        headers = {
            "Authorization": f"Bearer {AIRTABLE_TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(data)
        )

        if response.status_code == 200:
            st.write("Your information has been saved.")
        else:
            st.error("Airtable Error:")
            st.write(response.text)
