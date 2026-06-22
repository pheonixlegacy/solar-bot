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

# ---------- SESSION ----------
if "step" not in st.session_state:
    st.session_state.step = 0

if "selection" not in st.session_state:
    st.session_state.selection = None

# ---------- LOAD IMAGE ----------
def get_base64(file_name):
    with open(file_name, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

bg = get_base64("JPEG image.jpeg")

# ---------- CSS ----------
st.markdown(f"""
<style>

.stApp {{
    background-image:
        linear-gradient(
            rgba(0,0,0,.84),
            rgba(0,0,0,.84)
        ),
        url("data:image/jpeg;base64,{bg}");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

#MainMenu {{visibility:hidden;}}
footer {{visibility:hidden;}}
header {{visibility:hidden;}}

.main .block-container {{
    max-width:760px;
    background:rgba(10,15,25,.72);
    backdrop-filter:blur(18px);
    -webkit-backdrop-filter:blur(18px);

    padding:3rem;
    margin-top:2rem;

    border-radius:28px;

    border:1px solid rgba(255,255,255,.08);
}}

h1 {{
    color:white !important;
    text-align:center;
    font-size:54px !important;
}}

h2,h3,p,label {{
    color:white !important;
    text-align:center;
}}

p {{
    color:#d1d5db !important;
    line-height:1.8;
}}

.card {{
    background:rgba(255,255,255,.04);
    padding:25px;
    border-radius:18px;
    margin-bottom:15px;
    border:1px solid rgba(255,255,255,.08);
    text-align:center;
}}

.stButton > button {{
    width:100%;
    height:68px;

    background:
        linear-gradient(
            90deg,
            #f59e0b,
            #fbbf24
        );

    color:black;

    font-size:20px;
    font-weight:bold;

    border:none;
    border-radius:16px;
}}

.stTextInput input,
.stNumberInput input {{
    background: rgba(255,255,255,.08) !important;
    color: white !important;
    border-radius:12px !important;
}}

</style>
""", unsafe_allow_html=True)

# ---------- AIRTABLE ----------
AIRTABLE_TOKEN = "patryhLp1nLG9lPDB.3281b1a26270f1c0b90483155629d9d4acc983e23e3b885889fabd663372fe3b"

BASE_ID = "appQdfXVEYUcfsb4t"

TABLE_NAME = "Table 1"

# ---------- ZIP PREFIXES ----------
ALLOWED_PREFIXES = [
    "90","91","92","93","94","95","96",
    "60","61","62"
]

# ---------- HERO ----------
if st.session_state.step == 0:

    st.title("PREMIUM SOLAR FOR MODERN HOMES")

    st.write("""
Take control of rising electricity costs  
with premium residential solar solutions.

Federal incentives may currently be available.
""")

    st.write("""
⭐⭐⭐⭐⭐ Trusted by homeowners nationwide

✓ Premium Installation Options  
✓ Long-Term Utility Savings  
✓ Professional Solar Consultation
""")

    if st.button("CHECK MY SAVINGS →"):

        st.session_state.step = 1

        st.rerun()


# ---------- STEP 1 HOMEOWNER ----------
elif st.session_state.step == 1:

    st.progress(10)

    st.subheader("Do you own this property?")

    col1,col2 = st.columns(2)

    with col1:

        st.markdown("""
<div class="card">

### YES

I Own My Home

</div>
""", unsafe_allow_html=True)

        if st.button("HOMEOWNER YES"):

            st.session_state.selection = "Yes"

    with col2:

        st.markdown("""
<div class="card">

### NO

I Rent Property

</div>
""", unsafe_allow_html=True)

        if st.button("HOMEOWNER NO"):

            st.session_state.selection = "No"

    if st.button("CONTINUE STEP 1"):

        if st.session_state.selection == "No":

            st.error("Currently only homeowners qualify.")

        elif st.session_state.selection == "Yes":

            st.session_state.homeowner = "Yes"

            st.session_state.selection = None

            st.session_state.step = 2

            st.rerun()


# ---------- STEP 2 UTILITY ----------
elif st.session_state.step == 2:

    st.progress(20)

    st.subheader("Who is your electricity provider?")

    utility = st.selectbox(
        "",
        [
            "SDG&E",
            "PG&E",
            "Southern California Edison",
            "ComEd",
            "Other"
        ]
    )

    if st.button("CONTINUE STEP 2"):

        st.session_state.utility = utility

        st.session_state.step = 3

        st.rerun()


# ---------- STEP 3 SOLAR EXPERIENCE ----------
elif st.session_state.step == 3:

    st.progress(30)

    st.subheader(
        "Have you previously explored residential solar options?"
    )

    col1,col2 = st.columns(2)

    with col1:

        if st.button("SOLAR YES"):

            st.session_state.selection = "Yes"

    with col2:

        if st.button("SOLAR NO"):

            st.session_state.selection = "No"

    if st.button("CONTINUE STEP 3"):

        if st.session_state.selection:

            st.session_state.looked = st.session_state.selection

            st.session_state.selection = None

            st.session_state.step = 4

            st.rerun()
            # ---------- STEP 4 MONTHLY BILL ----------
elif st.session_state.step == 4:

    st.progress(40)

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

            st.session_state.step = 5

            st.rerun()


# ---------- STEP 5 SAVINGS CALCULATOR ----------
elif st.session_state.step == 5:

    st.progress(55)

    monthly = st.session_state.bill * 0.30
    yearly = monthly * 12
    twentyfive = yearly * 25

    st.title("Estimated Savings")

    st.write(f"### ${monthly:.0f} / month")

    st.write(f"### ${yearly:.0f} / year")

    st.write(f"### ${twentyfive:,.0f} over 25 years")

    if st.button("CONTINUE TO QUALIFY →"):

        st.session_state.step = 6

        st.rerun()


# ---------- STEP 6 ROOF EXPOSURE ----------
elif st.session_state.step == 6:

    st.progress(65)

    st.subheader(
        "How much direct sunlight does your roof receive?"
    )

    roof = st.selectbox(
        "",
        [
            "Full Sun Most Of Day",
            "Partial Shade",
            "Heavy Shade",
            "Not Sure"
        ]
    )

    if st.button("CONTINUE STEP 6"):

        st.session_state.roof = roof

        st.session_state.step = 7

        st.rerun()


# ---------- STEP 7 INTEREST ----------
elif st.session_state.step == 7:

    st.progress(75)

    st.subheader(
        "Would lowering your monthly energy costs be valuable to you?"
    )

    col1,col2 = st.columns(2)

    with col1:

        st.markdown("""
<div class="card">

### YES

Lower My Monthly Bills

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

    if st.button("CONTINUE STEP 7"):

        if st.session_state.selection == "No":

            st.error("Reach back out anytime.")

        elif st.session_state.selection == "Yes":

            st.session_state.interested = "Yes"

            st.session_state.selection = None

            st.session_state.step = 8

            st.rerun()


# ---------- STEP 8 ZIP ----------
elif st.session_state.step == 8:

    st.progress(85)

    st.subheader("Enter your ZIP code")

    zip_code = st.text_input("")

    if st.button("CONTINUE STEP 8"):

        if not zip_code.startswith(tuple(ALLOWED_PREFIXES)):

            st.error("Sorry — service unavailable in your area.")

        else:

            st.session_state.zip = zip_code

            st.session_state.step = 9

            st.rerun()
            # ---------- STEP 9 LEAD CAPTURE ----------
elif st.session_state.step == 9:

    st.progress(95)

    st.title("Your Home May Qualify")

    st.write("""
Where should we send your personalized solar savings estimate?
""")

    name = st.text_input("Full Name")

    phone = st.text_input("Phone Number")

    email = st.text_input("Email Address")

    st.write("""
🔒 Your information remains private.

A solar advisor may contact you shortly.
""")

   if st.button("GET MY SAVINGS REPORT →"):

    if name == "":
        st.error("Please enter your name.")

    elif phone == "":
        st.error("Please enter your phone number.")

    elif len(phone) != 10 or not phone.isdigit():
        st.error("Please enter a valid 10 digit phone number.")

    elif email == "":
        st.error("Please enter email address.")

    else:
    # homeowner
    score += 3

    # high electric bill
    if st.session_state.bill > 250:
        score += 3

    # roof exposure
    if st.session_state.roof == "Full Sun Most Of Day":
        score += 2

    # interested
    if st.session_state.interested == "Yes":
        score += 3


            today = datetime.now().strftime("%m/%d/%Y")

            data = {
                "fields": {
                    "Name": name,
                    "Phone": phone,
                    "Email": email,
                    "ZIP": st.session_state.zip,
                    "Homeowner": st.session_state.homeowner,
                    "Utility Provider": st.session_state.utility,
                    "Looked into Solar": st.session_state.looked,
                    "Monthly bill": st.session_state.bill,
                    "Roof Exposure": st.session_state.roof,
                    "interested": st.session_state.interested,
                    "Lead Score": score,
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

                st.session_state.step = 10

                st.rerun()

            else:

                st.error("Airtable Error")

                st.write(response.text)


# ---------- SUCCESS ----------
elif st.session_state.step == 10:

    st.progress(100)

    st.title("Congratulations")

    st.write("""
Based on your responses, your property may qualify  
for premium residential solar installation options.

A solar advisor will contact you shortly.

Thank you for completing your energy assessment.
""")

    st.write("")

    st.write("★★★★★ Premium Residential Solar Solutions")

    st.write("")

    if st.button("START OVER"):

        for key in list(st.session_state.keys()):

            del st.session_state[key]

        st.rerun()
