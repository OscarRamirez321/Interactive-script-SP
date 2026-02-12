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
        font-size: 22px !important;
        font-weight: 500;
        color: #1f1f1f;
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 12px;
        border-left: 6px solid #ff4b4b;
        margin-bottom: 25px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .note {
        font-size: 14px;
        color: #666;
        font-style: italic;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'step' not in st.session_state:
    st.session_state.step = 'HOME'

def go_to(step_name):
    st.session_state.step = step_name
    st.rerun()

def restart():
    st.session_state.step = 'HOME'
    st.rerun()

# --- SIDEBAR (QUICK INFO) ---
with st.sidebar:
    st.title("⚡ Quick Info")
    st.markdown("### 💰 Dispatch Fees")
    st.info("❄️ HVAC: **$99**")
    st.info("💧 Plumbing: **$49**")
    st.markdown("### 💳 Membership")
    st.success("**$20/mo** (Priority + 15% off)")
    st.divider()
    if st.button("🔄 Reset App"):
        restart()

# --- MAIN INTERFACE ---

# 1. HOME SCREEN
if st.session_state.step == 'HOME':
    st.title("🏠 SwiftPro Call Center")
    
    st.markdown('<div class="big-script">“Thank you for calling SwiftPro Heating, Cooling & Plumbing. This is ___ how can I help you today?”</div>', unsafe_allow_html=True)
    st.caption("😊 Remember: Smile and verify the customer's name.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📞 INBOUND (New Call)"): go_to('LOCATION_CHECK')
    with col2:
        if st.button("❌ CANCEL / RE-BOOK/ UPDATE"): go_to('CANCEL_FLOW')
    
    if st.button("📤 OUTBOUND (Leads)"): go_to('OUTBOUND_START')

# 2. LOCATION GATE
elif st.session_state.step == 'LOCATION_CHECK':
    st.title("📍 Location Check")
    st.progress(20)
    
    st.markdown('<div class="big-script">“Just to make sure you’re in our service area, what city are you calling from?”</div>', unsafe_allow_html=True)
    st.info("ℹ️ Valid Areas: Fairfax, Arlington, Prince William, Loudoun.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ IN AREA"): go_to('NEW_CLIENT_CHECK')
    with col2:
        if st.button("🚫 OUT OF AREA"): go_to('REFER_OUT')

# 3. CLIENT STATUS
elif st.session_state.step == 'NEW_CLIENT_CHECK':
    st.title("👤 Client Status")
    st.progress(40)
    
    st.markdown('<div class="big-script">“Have you used us before, or is this your first time calling us?”</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✨ NEW CLIENT"): go_to('TRADE_SELECT')
    with col2:
        if st.button("📂 EXISTING CLIENT"): 
            st.toast("Search profile in ServiceTitan...")
            go_to('TRADE_SELECT')

# 4. TRADE SELECTOR
elif st.session_state.step == 'TRADE_SELECT':
    st.title("🔧 Trade Selection")
    st.progress(60)

    st.markdown('<div class="big-script">“Perfect. To get you to the right expert, is this regarding your Heating/Cooling or Plumbing?”</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔥 HVAC (Heat/Cool)"): go_to('HVAC_DISCO')
    with col2:
        if st.button("🚿 PLUMBING (Water/Drain)"): go_to('PLUMB_DISCO')

# 5. HVAC FLOW
elif st.session_state.step == 'HVAC_DISCO':
    st.title("🔥 HVAC Triage")
    
    st.error("⚠️ EMERGENCY CHECK: Gas Smell OR No Heat < 32°F")
    
    st.markdown("""
    **MANDATORY QUESTIONS:**
    1. How long has this been going on?
    2. Is it Gas or Electric?
    3. How old is the system?
    4. Any weird noises or smells?
    """)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ STANDARD ISSUE"): go_to('HVAC_PRICE')
    with col2:
        if st.button("🚨 IT IS AN EMERGENCY"): go_to('EMERGENCY')

elif st.session_state.step == 'HVAC_PRICE':
    st.title("💰 The Pivot (HVAC)")
    st.progress(90)
    
    st.markdown('<div class="big-script">“For HVAC, it’s only <b>$99</b> to send a tech out to diagnose the system... Our soonest availability is [DAY] between 8-12 or 12-5.”</div>', unsafe_allow_html=True)
    st.warning("🛑 DO NOT SPEAK! Wait for the customer to respond.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ BOOK IT ($99)"): go_to('BOOKING')
    with col2:
        if st.button("🤔 PRICE OBJECTION"): go_to('OBJ_PRICE')

# 6. PLUMBING FLOW
elif st.session_state.step == 'PLUMB_DISCO':
    st.title("🚿 Plumbing Triage")

    st.error("⚠️ EMERGENCY CHECK: Major flooding OR Structural risk")

    st.markdown("""
    **MANDATORY QUESTIONS:**
    1. Is there an active leak?
    2. Can you shut the water off?
    3. Are drains backing up?
    4. Age of the home?
    """)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ STANDARD ISSUE"): go_to('PLUMB_PRICE')
    with col2:
        if st.button("🚨 IT IS AN EMERGENCY"): go_to('EMERGENCY')

elif st.session_state.step == 'PLUMB_PRICE':
    st.title("💰 The Pivot (Plumbing)")
    st.progress(90)
    
    st.markdown('<div class="big-script">“For plumbing, it’s only <b>$49</b> to send a tech out to diagnose the issue... Our soonest availability is [DAY] between 8-12 or 12-5.”</div>', unsafe_allow_html=True)
    st.warning("🛑 DO NOT SPEAK! Wait for the customer to respond.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ BOOK IT ($49)"): go_to('BOOKING')
    with col2:
        if st.button("🤔 PRICE OBJECTION"): go_to('OBJ_PRICE')

# 7. OBJECTION HANDLING
elif st.session_state.step == 'OBJ_PRICE':
    st.title("🛡️ Objection Handling")
    
    st.markdown('<div class="big-script">“Totally understand. The fee covers the trip and a full diagnosis by a certified expert. Plus, if you join our Membership, you get a discount.”</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🤝 SAVED -> BOOK"): go_to('BOOKING')
    with col2:
        if st.button("❌ LOST -> EXIT"): restart()

# 8. FINAL SCREENS
elif st.session_state.step == 'BOOKING':
    st.balloons()
    st.success("🎉 Great Job! Booking Confirmed.")
    st.markdown("### Final Steps:")
    st.checkbox("1. Get Full Address")
    st.checkbox("2. Get Email Address")
    st.checkbox("3. Confirm they will receive a text when tech is on the way")
    
    if st.button("🔄 Finish & Home"): restart()

elif st.session_state.step == 'EMERGENCY':
    st.error("🚨 EMERGENCY MODE")
    st.markdown('<div class="big-script">“This sounds critical. I’m going to see what I can move around to get someone there ASAP.”</div>', unsafe_allow_html=True)
    st.info("⚠️ ACTION: Consult Manager or Dispatcher immediately.")
    if st.button("🔄 Back"): restart()

elif st.session_state.step == 'REFER_OUT':
    st.markdown('<div class="big-script">“I’m really sorry—we don’t service that area, but I’d be happy to point you in the right direction.”</div>', unsafe_allow_html=True)
    if st.button("🏠 Home"): restart()

# 9. CANCELLATION FLOW
elif st.session_state.step == 'CANCEL_FLOW':
    st.title("💔 Cancellation")
    st.markdown('<div class="big-script">“I’m sorry to hear that. I understand things change. What day works best to come out instead?”</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗓️ RESCHEDULE"): go_to('BOOKING')
    with col2:
        if st.button("🛑 CANCEL"): go_to('CX_REASON')

elif st.session_state.step == 'CX_REASON':
    st.markdown('<div class="big-script">“If you don\'t mind me asking, is there a specific reason for the cancellation?”</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💸 FOUND CHEAPER"): go_to('CX_COMPETITOR')
    with col2:
        if st.button("🔧 FIXED ITSELF"): restart()

elif st.session_state.step == 'CX_COMPETITOR':
    st.warning("⚡ OFFER FREE SECOND OPINION")
    st.markdown('<div class="big-script">“We can provide a FREE Second Opinion to confirm their diagnosis. Does that work?”</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ YES, SAVED"): go_to('BOOKING')
    with col2:
        if st.button("❌ NO, CANCEL"): restart()

elif st.session_state.step == 'OUTBOUND_START':
    st.title("📞 Outbound Lead")
    st.markdown('<div class="big-script">“Hi [Name], this is SwiftPro... I see you reached out about your [Issue]. Wanted to get you taken care of.”</div>', unsafe_allow_html=True)
    if st.button("➡️ Continue"): go_to('LOCATION_CHECK')