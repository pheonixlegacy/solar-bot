import streamlit as st
import requests
import json
from datetime import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Solar Savings Check",
    layout="centered"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>

/* Background */
.stApp {
    background: #0b1120;
}

/* Hero image */
img {
    border-radius: 18px;
}

/* Main card */
.main .block-container {
    max-width: 760px;
    background: rgba(17, 24, 39, 0.88);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 2rem;
    border-radius: 22px;
    margin-top: 1rem;
    box-shadow: 0px 8px 30px rgba(0,0,0,0.35);
}

/* Headings */
h1 {
    text-align: center;
    color: white;
    font-size: 44px !important;
    font-weight: 800 !important;
}

/* Text */
p, label, div {
    color: #f3f4f6 !important;
}

/* Inputs */
.stTextInput > div > div > input {
    background-color: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 12px;
    color: white;
}

.stNumberInput input {
    background-color: rgba(255,255,255,0.08);
    border-radius: 12px;
    color: white;
}

/* Button */
.stButton > button {
    width: 100%;
    height: 65px;
    border-radius: 14px;
    font-weight: bold;
    font-size: 20px;
    background: linear-gradient(90deg, #22c55e, #16a34a);
    color: white;
    border: none;
    box-shadow: 0px 4px 20px rgba(34,197,94,.30);
}

/* Small trust text */
.trust {
    text-align:center;
    color:#9ca3af;
    font-size:14px;
    margin-bottom:20px;
}

.benefits {
    text-align:center;
    font-size:16px;
    margin-bottom:10px;
    line-height:1.8;
}

</style>
""", unsafe_allow_html=True)

# ---------- AIRTABLE ----------
AIRTABLE_TOKEN = "patryhLp1nLG9lPDB.3281b1a26270f1c0b90483155629d9d4acc983e23e3b885889fabd663372fe3b"
BASE_ID = "appQdfXVEYUcfsb4t"
TABLE_NAME = "Table 1"

# ---------- ZIPS ----------
ALLOWED_ZIPS = [
    "60037",
    "60199",
    "60522",
    "60699"
]

# ---------- HERO SECTION ----------
st.image("tesla-house.png", use_container_width=True)

st.title("⚡ Lower Your Electric Bill By Up To 30%")

st.markdown("""
<div class="benefits">
✓ Federal solar incentives available<br>
✓ Zero upfront options may be available<br>
✓ Serving select Illinois homeowners
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="trust">
Check eligibility in under 30 seconds.
</div>
""", unsafe_allow_html=True)

st.subheader("Quick Solar Qualification")

# ---------- FORM ----------
q1 = st.radio(
    "Have you looked into solar before?",
    ["Yes", "No"]
)

q2 = st.radio(
    "Are you the homeowner?",
    ["Yes", "No"]
)

bill = st.number_input(
    "Monthly electric bill ($)",
    min_value=0
)

q4 = st.radio(
    "If we lower your bill, are you interested?",
    ["Yes", "No"]
)

name = st.text_input("Full Name")
phone = st.text_input("Phone Number")
zip_code = st.text_input("ZIP Code")

# ---------- SUBMIT ----------
if st.button("CHECK MY SAVINGS →"):

    if name == "":
        st.error("Please enter your name.")

    elif phone == "":
        st.error("Please enter your phone number.")

    elif zip_code == "":
        st.error("Please enter ZIP code.")

    elif zip_code not in ALLOWED_ZIPS:
        st.error("Sorry, we do not service your area yet.")

    elif q2 != "Yes":
        st.error("Currently only homeowners qualify.")

    elif bill < 100:
        st.error("Minimum electric bill is $100.")

    elif q4 != "Yes":
        st.error("No problem. Reach out anytime.")

    else:

        st.success("🎉 You qualify for a solar consultation.")

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
            st.success("Your information has been saved.")

        else:
            st.error("Airtable Error:")
            st.write(response.text)
