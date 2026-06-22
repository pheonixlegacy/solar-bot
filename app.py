import streamlit as st
import requests
import json
from datetime import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Solar Savings",
    page_icon="⚡",
    layout="centered"
)

# ---------- CSS ----------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #06111f, #0f2350, #173d8f);
}

/* Container */
.main .block-container {
    max-width: 650px;
    padding-top: 2rem;
}

/* Title */
h1 {
    text-align:center;
    color:white;
    font-size:52px;
    font-weight:800;
}

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background-color: rgba(255,255,255,.08);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,.15);
    color: white;
    padding: 12px;
}

/* Button */
.stButton > button {
    width:100%;
    height:65px;
    border-radius:16px;
    font-size:22px;
    font-weight:bold;
    background:#22c55e;
    color:white;
    border:none;
    box-shadow:0px 5px 20px rgba(34,197,94,.35);
}

/* Text */
label, p {
    color:white !important;
}

</style>
""", unsafe_allow_html=True)

# ---------- AIRTABLE ----------
AIRTABLE_TOKEN = "patryhLp1nLG9lPDB.3281b1a26270f1c0b90483155629d9d4acc983e23e3b885889fabd663372fe3b"
BASE_ID = "appQdfXVEYUcfsb4t"
TABLE_NAME = "Table 1"

ALLOWED_ZIPS = [
    "60037",
    "60199",
    "60522",
    "60699"
]

# ---------- SESSION STATE ----------
if "step" not in st.session_state:
    st.session_state.step = 1

# ---------- HEADER ----------
st.title("⚡ Lower Your Electric Bill")

st.write("See if your home qualifies for solar savings in under 30 seconds.")

st.success("Limited installation availability in your area")

# progress
progress = {
    1: 20,
    2: 40,
    3: 60,
    4: 80,
    5: 100
}

st.progress(progress[st.session_state.step])
st.caption(f"Step {st.session_state.step} of 5")

# ---------- STEP 1 ----------
if st.session_state.step == 1:

    homeowner = st.radio(
        "Do you own your home?",
        ["Yes", "No"]
    )

    if st.button("Continue"):

        if homeowner != "Yes":
            st.error("Only homeowners qualify at this time.")
        else:
            st.session_state.homeowner = homeowner
            st.session_state.step = 2
            st.rerun()

# ---------- STEP 2 ----------
elif st.session_state.step == 2:

    zip_code = st.text_input("Enter your ZIP Code")

    if st.button("Continue"):

        if zip_code not in ALLOWED_ZIPS:
            st.error("Sorry, we do not currently service your area.")
        else:
            st.session_state.zip = zip_code
            st.session_state.step = 3
            st.rerun()

# ---------- STEP 3 ----------
elif st.session_state.step == 3:

    bill = st.number_input(
        "What is your average monthly electric bill?",
        min_value=0
    )

    if st.button("Calculate Savings"):

        if bill < 100:
            st.error("Monthly bill must be over $100.")
        else:
            st.session_state.bill = bill
            st.session_state.step = 4
            st.rerun()

# ---------- STEP 4 ----------
elif st.session_state.step == 4:

    savings = round(st.session_state.bill * 0.30)

    st.success("Estimated Savings Potential")

    st.markdown(f"""
### Monthly Savings: **${savings}**
### Yearly Savings: **${savings * 12}**
### 25 Year Savings: **${savings * 12 * 25}**
""")

    interested = st.radio(
        "Would you like to see if you qualify?",
        ["Yes", "No"]
    )

    if st.button("Continue"):

        if interested != "Yes":
            st.error("No worries — maybe another time.")
        else:
            st.session_state.interested = interested
            st.session_state.step = 5
            st.rerun()

# ---------- STEP 5 ----------
elif st.session_state.step == 5:

    name = st.text_input("Full Name")
    phone = st.text_input("Best Phone Number")

    st.write("✓ No upfront cost options")
    st.write("✓ Free solar consultation")
    st.write("✓ No obligation quote")

    if st.button("Get My Free Consultation"):

        if name == "":
            st.error("Please enter your name.")

        elif phone == "":
            st.error("Please enter phone number.")

        else:

            today = datetime.now().strftime("%m/%d/%Y")

            data = {
                "fields": {
                    "Name": name,
                    "Phone": phone,
                    "ZIP": st.session_state.zip,
                    "Looked into Solar": "Yes",
                    "Homeowner": st.session_state.homeowner,
                    "Monthly bill": st.session_state.bill,
                    "interested": st.session_state.interested,
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

                st.balloons()

                st.success("🎉 Congratulations!")

                st.write("Your home may qualify for reduced electricity costs.")

                st.write("A solar advisor will contact you shortly.")

            else:
                st.error("Airtable Error")
                st.write(response.text)
