import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="SwiftPro Navigator", page_icon="🔧", layout="centered")

# --- VISUAL STYLES (LYFT-STYLE CSS) ---
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        font-weight: 600;
        font-size: 16px;
        border: 1px solid #e0e0e0;
        transition: all 0.3s;
    }
    .stButton button:hover {
        border-color: #ff4b4b;
        color: #ff4b4b;
    }
    .big-script {
        font-size: 20px !important;
        font-weight: 500;
        color: #1f1f1f;
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #ff4b4b;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .input-box {
        border: 2px solid #4CAF50;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'step' not in st.session_state:
    st.session_state.step = 'HOME'
if 'customer_concern' not in st.session_state:
    st.session_state.customer_concern = ''
if 'job_type' not in st.session_state:
    st.session_state.job_type = ''

def go_to(step_name):
    st.session_state.step = step_name
    st.rerun()

def restart():
    st.session_state.step = 'HOME'
    st.session_state.customer_concern = ''
    st.session_state.job_type = ''
    st.rerun()

# --- SIDEBAR INFO ---
with st.sidebar:
    st.title("⚡ Quick Info")
    st.info("❄️ HVAC Repair: **$99**")
    st.info("💧 Plumbing Repair: **$49**")
    st.success("🆓 Estimates/Sales: **FREE**")
    st.divider()
    if st.button("🔄 Start Over"):
        restart()

# --- MAIN LOGIC ---

# 1. HOME
if st.session_state.step == 'HOME':
    st.title("🏠 SwiftPro Call Center")
    st.markdown('<div class="big-script">“Thank you for calling SwiftPro Heating, Cooling & Plumbing. This is [Name]—how can I help you today?”</div>', unsafe_allow_html=True)
    st.caption("😊 Remember: Smile and have a great tone of voice.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📞 INBOUND"): go_to('LOCATION_CHECK')
    with col2:
        if st.button("📤 OUTBOUND"): go_to('OUTBOUND_START')

# 2. OUTBOUND FLOW
elif st.session_state.step == 'OUTBOUND_START':
    st.title("📞 Outbound Call")
    st.markdown('<div class="big-script">“Hi [Customer Name], this is [Name] with SwiftPro... I see you reached out about [Issue]. Wanted to make sure we get you taken care of.”</div>', unsafe_allow_html=True)
    if st.button("➡️ Continue"): go_to('LOCATION_CHECK')

# 3. LOCATION GATE
elif st.session_state.step == 'LOCATION_CHECK':
    st.title("📍 Service Area")
    st.markdown('<div class="big-script">“Just to make sure you’re in our service area, what city are you calling from?”</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ IN AREA (NoVA)"): go_to('CLIENT_STATUS')
    with col2:
        if st.button("🚫 OUT OF AREA"): go_to('REFER_OUT')

elif st.session_state.step == 'REFER_OUT':
    st.error("🛑 Out of Service Area")
    st.markdown('<div class="big-script">“I’m really sorry—we don’t service that area, but I’d be happy to point you in the right direction.”</div>', unsafe_allow_html=True)
    if st.button("🏠 Home"): restart()

# 4. CLIENT STATUS
elif st.session_state.step == 'CLIENT_STATUS':
    st.title("👤 Customer Status")
    st.markdown('<div class="big-script">“Have you used us before, or is this your first time calling us?”</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✨ NEW CUSTOMER"): go_to('ACKNOWLEDGE_ISSUE')
    with col2:
        if st.button("📂 EXISTING CLIENT"): 
            st.toast("Search profile in ServiceTitan...")
            go_to('ACKNOWLEDGE_ISSUE')

# 5. ACKNOWLEDGE & LOG ISSUE (Diagram Note: "Add a box")
elif st.session_state.step == 'ACKNOWLEDGE_ISSUE':
    st.title("📝 Understanding the Issue")
    st.markdown('<div class="big-script">“Got it, thank you for explaining that. You’re definitely not alone—we handle situations like this every day. Let me ask a few quick questions...”</div>', unsafe_allow_html=True)
    
    # Input box for note taking
    st.session_state.customer_concern = st.text_area("✍️ Write down the customer's concern here:", height=100)
    
    if st.session_state.customer_concern:
        if st.button("✅ Saved. Continue to Category"):
            go_to('CATEGORY_SELECT')

# 6. CATEGORY SELECTION
elif st.session_state.step == 'CATEGORY_SELECT':
    st.title("🔧 Select Category")
    st.write("What kind of job is this?")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔥 HVAC REPAIR"): go_to('HVAC_JOB_SELECT')
    with col2:
        if st.button("🚿 PLUMBING REPAIR"): go_to('PLUMB_JOB_SELECT')
    with col3:
        if st.button("🆕 SALES / ESTIMATE"): go_to('SALES_JOB_SELECT')

# 7. JOB DROPDOWNS (From Diagram)
elif st.session_state.step == 'HVAC_JOB_SELECT':
    st.title("🔥 HVAC Job Type")
    hvac_options = [
        "Select an option...",
        "AC Repair", "Heat Pump Repair", "Gas/Propane Furnace Repair", "Boiler Repair",
        "Mini-Split Repair", "Maintenance / Tune-Up", "Duct Cleaning", "Thermostat Issue", 
        "Humidifier/Dehumidifier"
    ]
    selection = st.selectbox("Select specific issue:", hvac_options)
    
    if selection != "Select an option...":
        st.session_state.job_type = selection
        if st.button("Continue to Triage"): go_to('HVAC_TRIAGE')

elif st.session_state.step == 'PLUMB_JOB_SELECT':
    st.title("🚿 Plumbing Job Type")
    plumb_options = [
        "Select an option...",
        "Leak (Active)", "Clogged Drain", "Toilet Repair", "Water Heater Repair",
        "Garbage Disposal", "Sump Pump", "Fixture Install", "Well Pump", "Sewer Line"
    ]
    selection = st.selectbox("Select specific issue:", plumb_options)
    
    if selection != "Select an option...":
        st.session_state.job_type = selection
        if st.button("Continue to Triage"): go_to('PLUMB_TRIAGE')

elif st.session_state.step == 'SALES_JOB_SELECT':
    st.title("🆕 Estimate / Replacement")
    sales_options = [
        "Select an option...",
        "Full HVAC System Replacement", "Water Heater Replacement (Tank/Tankless)",
        "Boiler Replacement", "Humidifier Installation"
    ]
    selection = st.selectbox("Select specific issue:", sales_options)
    
    if selection != "Select an option...":
        st.session_state.job_type = selection
        if st.button("Continue to Triage"): go_to('SALES_TRIAGE')

# 8. TRIAGE QUESTIONS
elif st.session_state.step == 'HVAC_TRIAGE':
    st.title("🔥 HVAC Discovery")
    st.write(f"Job Type: **{st.session_state.job_type}**")
    st.markdown("""
    **ASK THESE QUESTIONS:**
    1. 🕒 How long has this been going on?
    2. ⚡ Is it Gas or Electric?
    3. 🏚️ About how old is the system?
    4. 🔊 Any weird noises or smells?
    """)
    st.error("⚠️ EMERGENCY IF: Gas Smell OR No Heat < 32°F")
    
    if st.button("✅ Standard -> Price"): go_to('HVAC_PRICE')
    if st.button("🚨 EMERGENCY"): go_to('EMERGENCY')

elif st.session_state.step == 'PLUMB_TRIAGE':
    st.title("🚿 Plumbing Discovery")
    st.write(f"Job Type: **{st.session_state.job_type}**")
    st.markdown("""
    **ASK THESE QUESTIONS:**
    1. 💧 Is water actively leaking right now?
    2. 🚫 Can you shut the water off?
    3. 🚽 Are drains backing up?
    4. 🏠 Do you have at least one working toilet?
    """)
    st.error("⚠️ EMERGENCY IF: Major flooding or structural damage.")
    
    if st.button("✅ Standard -> Price"): go_to('PLUMB_PRICE')
    if st.button("🚨 EMERGENCY"): go_to('EMERGENCY')

elif st.session_state.step == 'SALES_TRIAGE':
    st.title("🆕 Replacement Discovery")
    st.write(f"Job Type: **{st.session_state.job_type}**")
    st.markdown("""
    **ASK THESE QUESTIONS:**
    1. 🏚️ Is the system working or completely down?
    2. 📅 How old is the current unit?
    3. 🤔 What is driving the replacement? (Age, Bills, Comfort?)
    """)
    if st.button("✅ Ready -> Book Free Estimate"): go_to('SALES_PRICE')

# 9. PRICING / PIVOT
elif st.session_state.step == 'HVAC_PRICE':
    st.title("💰 The Pivot (HVAC)")
    st.markdown('<div class="big-script">“For HVAC, it’s only <b>$99</b> to send a tech out to diagnose the system... Our soonest availability is [Day] between 8-12 or 12-5.”</div>', unsafe_allow_html=True)
    st.warning("🛑 DO NOT PAUSE after the price!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ BOOK ($99)"): go_to('CUSTOMER_INFO')
    with col2:
        if st.button("🛑 OBJECTION"): go_to('OBJECTION')

elif st.session_state.step == 'PLUMB_PRICE':
    st.title("💰 The Pivot (Plumbing)")
    st.markdown('<div class="big-script">“For plumbing, it’s only <b>$49</b> to send a tech out... Our soonest availability is [Day] between 8-12 or 12-5.”</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ BOOK ($49)"): go_to('CUSTOMER_INFO')
    with col2:
        if st.button("🛑 OBJECTION"): go_to('OBJECTION')

elif st.session_state.step == 'SALES_PRICE':
    st.title("🆓 The Pivot (Sales)")
    st.markdown('<div class="big-script">“For replacements, we provide <b>FREE in-home estimates</b> so we can give you accurate options. Our soonest availability is...”</div>', unsafe_allow_html=True)
    if st.button("✅ BOOK ESTIMATE"): go_to('CUSTOMER_INFO')

# 10. CUSTOMER INFO & CLOSE
elif st.session_state.step == 'CUSTOMER_INFO':
    st.title("📝 Customer Details")
    st.write("Collect the following:")
    
    with st.form("booking_form"):
        st.text_input("First & Last Name")
        st.text_input("Service Address")
        st.text_input("Phone Number")
        st.text_input("Email Address")
        st.selectbox("Home Type", ["Single Family", "Townhome", "Condo"])
        st.checkbox("Is Homeowner?")
        
        if st.form_submit_button("✅ COMPLETE BOOKING"):
            go_to('CLOSE_CALL')

elif st.session_state.step == 'CLOSE_CALL':
    st.balloons()
    st.success("🎉 Appointment Booked!")
    st.markdown('<div class="big-script">“Great, everything is confirmed. You’ll receive a text as soon as the technician is on the way. Thank you for choosing SwiftPro!”</div>', unsafe_allow_html=True)
    if st.button("🔄 New Call"): restart()

elif st.session_state.step == 'OBJECTION':
    st.title("🛡️ Handling Objections")
    st.markdown('<div class="big-script">“Totally understand. The fee covers the trip and a full diagnosis by a certified expert. Plus, if you join our Membership ($20/mo), you get 15% off.”</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🤝 SAVED -> BOOK"): go_to('CUSTOMER_INFO')
    with col2:
        if st.button("❌ LOST"): restart()

elif st.session_state.step == 'EMERGENCY':
    st.error("🚨 EMERGENCY PROTOCOL")
    st.write("Consult Manager Immediately.")
    if st.button("🔙 Back"): go_to('CATEGORY_SELECT')