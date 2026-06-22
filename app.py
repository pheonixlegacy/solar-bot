import streamlit as st
import requests
import json
import base64
from datetime import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Premium Solar Funnel",
    layout="centered"
)

# ---------- SESSION STATE ----------
if "step" not in st.session_state:
    st.session_state.step = 0

# ---------- LOAD BACKGROUND ----------
def get_base64(file_name):
    with open(file_name, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

bg = get_base64("JPEG image.jpeg")

# ---------- CSS ----------
st.markdown(f"""
<style>

/* Background */
.stApp {{
    background-image:
        linear-gradient(
            rgba(0,0,0,0.78),
            rgba(0,0,0,0.78)
        ),
        url("data:image/jpeg;base64,{bg}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* Hide streamlit junk */
#MainMenu {{visibility:hidden;}}
footer {{visibility:hidden;}}
header {{visibility:hidden;}}

/* Main card */
.main .block-container {{
    max-width: 720px;
    background: rgba(10,15,25,.75);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    padding: 2.5rem;
    margin-top: 3rem;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,.08);
}}

/* Text */
h1 {{
    text-align:center;
    color:white;
    font-size:48px !important;
    font-weight:700 !important;
}}

h2,h3,p,label,div {{
    color:white !important;
    text-align:center;
}}

label {{
    font-weight:500;
}}

/* Inputs */
.stTextInput input,
.stNumberInput input {{
    background: rgba(255,255,255,.08) !important;
    color:white !important;
    border-radius:12px !important;
    border:1px solid rgba(255,255,255,.12) !important;
    padding:12px !important;
}}

/* Buttons */
.stButton > button {{
    width:100%;
    height:65px;
    border:none;
    border-radius:14px;
    font-size:20px;
    font-weight:bold;
    background: linear-gradient(90deg,#f59e0b,#fbbf24);
    color:black;
    box-shadow:0 5px 20px rgba(251,191,36,.25);
}}

/* Progress */
.progress-text {{
    text-align:center;
    color:#d1d5db;
    margin-bottom:10px;
}}

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

# ---------- HERO PAGE ----------
if st.session_state.step == 0:

    st.title("PREMIUM SOLAR FOR MODERN HOMES")

    st.write("""
Lower Your Electric Bill  
Without Changing Your Lifestyle  

Serving Qualified Illinois Homeowners
""")

    st.write("")

    if st.button("CHECK MY SAVINGS"):
        st.session_state.step = 1
        st.rerun()

# ---------- STEP 1 ----------
elif st.session_state.step == 1:

    st.progress(16)
    st.markdown('<div class="progress-text">Step 1 of 6</div>', unsafe_allow_html=True)

    st.subheader("Are you the homeowner?")

    answer = st.radio("", ["Yes", "No"])

    if st.button("CONTINUE"):

        if answer != "Yes":
            st.error("Only homeowners qualify currently.")
        else:
            st.session_state.homeowner = answer
            st.session_state.step = 2
            st.rerun()

# ---------- STEP 2 ----------
elif st.session_state.step == 2:

    st.progress(32)
    st.markdown('<div class="progress-text">Step 2 of 6</div>', unsafe_allow_html=True)

    st.subheader("Have you looked into solar before?")

    answer = st.radio("", ["Yes", "No"])

    if st.button("CONTINUE"):
        st.session_state.looked = answer
        st.session_state.step = 3
        st.rerun()

# ---------- STEP 3 ----------
elif st.session_state.step == 3:

    st.progress(48)
    st.markdown('<div class="progress-text">Step 3 of 6</div>', unsafe_allow_html=True)

    st.subheader("What is your monthly electric bill?")

    bill = st.number_input("", min_value=0)

    if st.button("CONTINUE"):

        if bill < 100:
            st.error("Monthly bill must exceed $100.")
        else:
            st.session_state.bill = bill
            st.session_state.step = 4
            st.rerun()

# ---------- STEP 4 ----------
elif st.session_state.step == 4:

    st.progress(64)
    st.markdown('<div class="progress-text">Step 4 of 6</div>', unsafe_allow_html=True)

    st.subheader("Would reducing that bill interest you?")

    answer = st.radio("", ["Yes", "No"])

    if st.button("CONTINUE"):

        if answer != "Yes":
            st.error("No problem. Reach out anytime.")
        else:
            st.session_state.interested = answer
            st.session_state.step = 5
            st.rerun()

# ---------- STEP 5 ----------
elif st.session_state.step == 5:

    st.progress(80)
    st.markdown('<div class="progress-text">Step 5 of 6</div>', unsafe_allow_html=True)

    st.subheader("What ZIP code are you in?")

    zip_code = st.text_input("")

    if st.button("CONTINUE"):

        if zip_code not in ALLOWED_ZIPS:
            st.error("Sorry. Service unavailable in your area.")
        else:
            st.session_state.zip = zip_code
            st.session_state.step = 6
            st.rerun()

# ---------- FINAL STEP ----------
elif st.session_state.step == 6:

    st.progress(95)
    st.markdown('<div class="progress-text">Final Step</div>', unsafe_allow_html=True)

    st.subheader("You're Pre-Qualified")

    st.write("Where should we send your custom solar estimate?")

    name = st.text_input("Full Name")

    phone = st.text_input("Phone Number")

    if st.button("GET MY SAVINGS REPORT"):

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
                    "Looked into Solar": st.session_state.looked,
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
                st.session_state.step = 7
                st.rerun()

            else:
                st.error("Airtable Error")
                st.write(response.text)

# ---------- SUCCESS ----------
elif st.session_state.step == 7:

    st.progress(100)

    st.title("✓ YOU QUALIFY")

    st.write("""
A solar specialist will contact you shortly.

Thank you for completing your energy assessment.
""")
