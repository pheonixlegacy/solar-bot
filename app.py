import streamlit as st
import requests
import json
import base64
from datetime import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Premium Solar Experience",
    layout="centered"
)

# ---------- SESSION STATE ----------
if "step" not in st.session_state:
    st.session_state.step = 0

if "selection" not in st.session_state:
    st.session_state.selection = None


# ---------- LOAD BACKGROUND IMAGE ----------
def get_base64(file_name):
    with open(file_name, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

bg = get_base64("JPEG image.jpeg")


# ---------- PREMIUM CSS ----------
st.markdown(f"""
<style>

/* BACKGROUND */
.stApp {{
    background-image:
        linear-gradient(
            rgba(0,0,0,.82),
            rgba(0,0,0,.82)
        ),
        url("data:image/jpeg;base64,{bg}");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* HIDE STREAMLIT DEFAULTS */
#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

header {{
    visibility: hidden;
}}

/* MAIN CARD */
.main .block-container {{
    max-width: 760px;
    background: rgba(10,15,25,.72);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);

    padding: 3rem;
    margin-top: 2rem;

    border-radius: 28px;

    border: 1px solid rgba(255,255,255,.08);

    box-shadow: 0 10px 40px rgba(0,0,0,.35);
}}

/* HEADINGS */
h1 {{
    color: white !important;
    text-align: center;
    font-size: 54px !important;
    font-weight: 700 !important;
    margin-bottom: 10px;
}}

h2, h3 {{
    color: white !important;
    text-align: center;
}}

p {{
    color: #d1d5db !important;
    text-align: center;
    font-size: 17px;
    line-height: 1.8;
}}

label {{
    color: white !important;
}}

/* TRUST TEXT */
.trust {{
    text-align: center;
    color: #d1d5db;
    margin-top: 12px;
    line-height: 2;
}}

/* BUTTONS */
.stButton > button {{
    width: 100%;
    height: 68px;

    background:
        linear-gradient(
            90deg,
            #f59e0b,
            #fbbf24
        );

    color: black;

    font-size: 20px;
    font-weight: bold;

    border: none;
    border-radius: 16px;

    box-shadow:
        0 6px 25px rgba(251,191,36,.30);
}}

/* BIG SELECTION CARDS */
.card {{
    background: rgba(255,255,255,.04);
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 15px;
    border: 1px solid rgba(255,255,255,.08);
    text-align: center;
}}

/* INPUTS */
.stTextInput input,
.stNumberInput input {{
    background: rgba(255,255,255,.08) !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,.12) !important;
    padding: 12px !important;
}}

/* PROGRESS TEXT */
.progress-text {{
    text-align:center;
    color:#d1d5db;
    margin-bottom:15px;
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
Take control of rising electricity costs  
with premium residential solar solutions.

Federal incentives may currently be available.
""")

    st.markdown("""
<div class="trust">

⭐⭐⭐⭐⭐ Trusted by homeowners nationwide

✓ Premium Installation Options  
✓ Long-Term Utility Savings  
✓ Professional Solar Consultation  

</div>
""", unsafe_allow_html=True)

    st.write("")

    if st.button("CHECK MY SAVINGS →"):
        st.session_state.step = 1
        st.rerun()


# ---------- STEP 1 ----------
elif st.session_state.step == 1:

    st.progress(15)

    st.markdown(
        '<div class="progress-text">15% Complete</div>',
        unsafe_allow_html=True
    )

    st.subheader("Do you own this property?")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
<div class="card">

### YES

I Own My Home

</div>
""", unsafe_allow_html=True)

        if st.button("SELECT YES"):

            st.session_state.selection = "Yes"

    with col2:

        st.markdown("""
<div class="card">

### NO

I Rent Property

</div>
""", unsafe_allow_html=True)

        if st.button("SELECT NO"):

            st.session_state.selection = "No"

    if st.button("CONTINUE"):

        if st.session_state.selection == "No":

            st.error("Currently only homeowners qualify.")

        elif st.session_state.selection == "Yes":

            st.session_state.homeowner = "Yes"

            st.session_state.selection = None

            st.session_state.step = 2

            st.rerun()
            # ---------- STEP 2 ----------
elif st.session_state.step == 2:

    st.progress(30)

    st.markdown(
        '<div class="progress-text">30% Complete</div>',
        unsafe_allow_html=True
    )

    st.subheader("Have you previously explored residential solar options?")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
<div class="card">

### YES

I’ve Looked Into Solar

</div>
""", unsafe_allow_html=True)

        if st.button("SOLAR YES"):

            st.session_state.selection = "Yes"

    with col2:

        st.markdown("""
<div class="card">

### NO

First Time Exploring

</div>
""", unsafe_allow_html=True)

        if st.button("SOLAR NO"):

            st.session_state.selection = "No"

    if st.button("CONTINUE STEP 2"):

        if st.session_state.selection:

            st.session_state.looked = st.session_state.selection

            st.session_state.selection = None

            st.session_state.step = 3

            st.rerun()


# ---------- STEP 3 ----------
elif st.session_state.step == 3:

    st.progress(45)

    st.markdown(
        '<div class="progress-text">45% Complete</div>',
        unsafe_allow_html=True
    )

    st.subheader("What is your average monthly electric bill?")

    bill = st.number_input(
        "",
        min_value=0
    )

    if st.button("SEE MY ESTIMATE →"):

        if bill < 100:

            st.error("Monthly electric bill must exceed $100.")

        else:

            st.session_state.bill = bill

            st.session_state.step = 4

            st.rerun()


# ---------- SAVINGS CALCULATOR ----------
elif st.session_state.step == 4:

    st.progress(60)

    st.markdown(
        '<div class="progress-text">60% Complete</div>',
        unsafe_allow_html=True
    )

    monthly = st.session_state.bill * 0.30
    yearly = monthly * 12
    twentyfive = yearly * 25

    st.title("Estimated Savings")

    st.write(f"### ${monthly:.0f} / month")

    st.write(f"### ${yearly:.0f} / year")

    st.write(f"### ${twentyfive:,.0f} over 25 years")

    st.write("")

    if st.button("CONTINUE TO QUALIFY →"):

        st.session_state.step = 5

        st.rerun()


# ---------- STEP 4 ----------
elif st.session_state.step == 5:

    st.progress(75)

    st.markdown(
        '<div class="progress-text">75% Complete</div>',
        unsafe_allow_html=True
    )

    st.subheader(
        "Would lowering your monthly energy costs be valuable to you?"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
<div class="card">

### YES

I Want Lower Bills

</div>
""", unsafe_allow_html=True)

        if st.button("INTEREST YES"):

            st.session_state.selection = "Yes"

    with col2:

        st.markdown("""
<div class="card">

### NO

Not Interested

</div>
""", unsafe_allow_html=True)

        if st.button("INTEREST NO"):

            st.session_state.selection = "No"

    if st.button("CONTINUE STEP 4"):

        if st.session_state.selection == "No":

            st.error("Reach back out anytime.")

        elif st.session_state.selection == "Yes":

            st.session_state.interested = "Yes"

            st.session_state.selection = None

            st.session_state.step = 6

            st.rerun()
            # ---------- STEP 5 ----------
elif st.session_state.step == 6:

    st.progress(85)

    st.markdown(
        '<div class="progress-text">85% Complete</div>',
        unsafe_allow_html=True
    )

    st.subheader("Enter your ZIP code")

    zip_code = st.text_input("")

    if st.button("CONTINUE STEP 5"):

        if zip_code not in ALLOWED_ZIPS:

            st.error("Sorry — service unavailable in your area.")

        else:

            st.session_state.zip = zip_code

            st.session_state.step = 7

            st.rerun()


# ---------- FINAL LEAD CAPTURE ----------
elif st.session_state.step == 7:

    st.progress(95)

    st.markdown(
        '<div class="progress-text">Final Qualification Step</div>',
        unsafe_allow_html=True
    )

    st.title("You May Qualify")

    st.write("""
Where should we send your personalized solar savings estimate?
""")

    name = st.text_input("Full Name")

    phone = st.text_input("Phone Number")

    st.markdown("""
<div class="trust">

🔒 Your information remains private.

A solar advisor may contact you shortly.

</div>
""", unsafe_allow_html=True)

    if st.button("GET MY SAVINGS REPORT →"):

        if name == "":

            st.error("Please enter your name.")

        elif phone == "":

            st.error("Please enter your phone number.")

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

                st.session_state.step = 8

                st.rerun()

            else:

                st.error("Airtable Error")

                st.write(response.text)


# ---------- SUCCESS PAGE ----------
elif st.session_state.step == 8:

    st.progress(100)

    st.title("Congratulations")

    st.write("""
Based on your responses, your property may qualify  
for premium residential solar installation options.

A solar advisor will contact you shortly.

Thank you for completing your energy assessment.
""")

    st.markdown("""
<div class="trust">

★★★★★ Premium Residential Solar Solutions

</div>
""", unsafe_allow_html=True)


# ---------- RESET OPTION ----------
    st.write("")

    if st.button("START OVER"):

        for key in list(st.session_state.keys()):

            del st.session_state[key]

        st.rerun()
