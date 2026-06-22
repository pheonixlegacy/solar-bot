import streamlit as st
import requests
import json
import base64
from datetime import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Premium Solar Savings",
    layout="centered"
)

# ---------- LOAD LOCAL BACKGROUND IMAGE ----------
def get_base64(file_name):
    with open(file_name, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Must match your GitHub uploaded file exactly
bg = get_base64("JPEG image.jpeg")

# ---------- PREMIUM UI CSS ----------
st.markdown(f"""
<style>

/* Full page luxury background */
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

/* Hide Streamlit menu/footer */
#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

header {{
    visibility: hidden;
}}

/* Glass card */
.main .block-container {{
    max-width: 720px;
    background: rgba(10, 15, 25, 0.72);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    padding: 2.5rem;
    border-radius: 24px;
    margin-top: 2rem;
    border: 1px solid rgba(255,255,255,0.08);
}}

/* Main title */
h1 {{
    text-align: center;
    color: white;
    font-size: 48px;
    font-weight: 700;
    margin-bottom: 10px;
}}

/* Text */
p {{
    color: #d1d5db !important;
    text-align: center;
    font-size: 17px;
}}

label {{
    color: white !important;
    font-weight: 500;
}}

/* Inputs */
.stTextInput input {{
    background: rgba(255,255,255,0.08);
    color: white;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.12);
}}

.stNumberInput input {{
    background: rgba(255,255,255,0.08);
    color: white;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.12);
}}

/* Button */
.stButton > button {{
    width: 100%;
    height: 65px;
    background: linear-gradient(90deg,#f59e0b,#fbbf24);
    color: black;
    font-size: 20px;
    font-weight: bold;
    border: none;
    border-radius: 14px;
    box-shadow: 0 5px 20px rgba(251,191,36,.25);
}}

/* Success/Error boxes */
.stSuccess, .stError {{
    border-radius: 14px;
}}

</style>
""", unsafe_allow_html=True)

# ---------- AIRTABLE CONFIG ----------
AIRTABLE_TOKEN = "patryhLp1nLG9lPDB.3281b1a26270f1c0b90483155629d9d4acc983e23e3b885889fabd663372fe3b"
BASE_ID = "appQdfXVEYUcfsb4t"
TABLE_NAME = "Table 1"

# ---------- ALLOWED ZIPS ----------
ALLOWED_ZIPS = [
    "60037",
    "60199",
    "60522",
    "60699"
]

# ---------- HERO SECTION ----------
st.title("Premium Solar For Modern Homes")

st.markdown("""
### Start Saving On Electricity Without Changing Your Lifestyle  

⭐⭐⭐⭐⭐ Trusted by qualified homeowners  

✓ Reduce monthly utility costs  
✓ Premium home solar installation  
✓ Increase long-term property value  
✓ Fast 30-second qualification process  

**Get your personalized solar savings estimate below.**
""")

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
    "Would reducing that bill interest you?",
    ["Yes", "No"]
)

name = st.text_input("Full Name")

phone = st.text_input("Best Phone Number")

zip_code = st.text_input("ZIP Code")

# ---------- SUBMIT ----------
if st.button("Check My Savings"):

    if name == "":
        st.error("Please enter your name.")

    elif phone == "":
        st.error("Please enter your phone number.")

    elif zip_code == "":
        st.error("Please enter ZIP code.")

    elif zip_code not in ALLOWED_ZIPS:
        st.error("Sorry — service unavailable in your area.")

    elif q2 != "Yes":
        st.error("Currently only homeowners qualify.")

    elif bill < 100:
        st.error("Monthly electric bill must be above $100.")

    elif q4 != "Yes":
        st.error("No problem — reach back out anytime.")

    else:

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
            st.success("Your information has been submitted.")

        else:
            st.error("Airtable Error")
            st.write(response.text)
