import streamlit as st
import requests
import json
from datetime import datetime

# ---------------- UI Styling ----------------
st.markdown("""
<style>

/* Tesla Style Background */
.stApp {
    background-image: url("https://images.unsplash.com/photo-1592833159155-c62df1b65634");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Floating Glass Card */
.main .block-container {
    max-width: 650px;
    background: rgba(0, 0, 0, 0.55);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    padding: 2rem;
    border-radius: 24px;
    margin-top: 2rem;
}

/* Main Title */
h1 {
    text-align: center;
    color: white;
    font-size: 48px;
    font-weight: bold;
}

/* Paragraph text */
p, label {
    color: white !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    height: 65px;
    border-radius: 14px;
    font-weight: bold;
    font-size: 22px;
    background-color: #22c55e;
    color: white;
    border: none;
    box-shadow: 0px 4px 15px rgba(34,197,94,0.35);
}

/* Text Input */
.stTextInput > div > div > input {
    background-color: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 12px;
    padding: 10px;
    color: white;
}

/* Number Input */
.stNumberInput input {
    background-color: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 12px;
    padding: 10px;
    color: white;
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
st.title("⚡ See If Your Home Qualifies For Solar Savings")
st.write("Save up to 30% on electricity in under 30 seconds.")

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
