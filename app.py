import streamlit as st

import base64

st.set_page_config(
    page_title="SwiftPro Navigator",  # El título que sale en la pestaña
    page_icon="image_7.png",          # ¡AQUÍ VA TU LOGO! (Usa el nombre exacto de tu archivo)
    layout="wide"                     # Opcional: usa todo el ancho de la pantalla
)

def mostrar_disponibilidad_central():
    st.markdown("### 📅 Service Availability Update")
    info_araksan = """
    **🔥 HVAC:** Feb 11 (Wed) - After 12 PM | Feb 12 (Thu) - Open (All Day)
    
    **🚿 Plumbing:** Feb 11 (Wed) - Emergency only | Feb 12 (Thu) - Open (All Day)
    
    **🧹 Duct/Dryer:** Feb 12 (Thu) - Open (All Day)
    """
    st.success(info_araksan)
    st.divider()

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="SwiftPro Navigator", page_icon="🔧", layout="centered")

# --- FUNCTION TO ADD BACKGROUND (Robust Version) ---
def add_background(image_file):
    try:
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        
        st.markdown(
            f"""
            <style>
            /* Apply directly to the main app container */
            [data-testid="stAppViewContainer"] {{
                background-image: url("data:image/png;base64,{encoded_string}");
                background-repeat: no-repeat;
                background-position: center 50px; /* 50px from the TOP */
                background-size: 300px; /* Size of the logo */
                background-attachment: scroll; /* Scrolls with the page */
            }}
            
            /* Push the text down so it doesn't cover the logo */
            [data-testid="block-container"] {{
                padding-top: 180px !important; /* Adjust this if you need more space */
            }}
            
            /* Hide the default Streamlit header decoration */
            header {{
                visibility: hidden;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning(f"⚠️ Could not find background image: {image_file}")

# ✅ Call it
add_background("image_7.png")

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
if 'history' not in st.session_state:
    st.session_state.history = []
if 'customer_concern' not in st.session_state:
    st.session_state.customer_concern = ''
if 'job_type' not in st.session_state:
    st.session_state.job_type = ''

def go_to(step_name):
    """Save current step to history, then move to new step."""
    st.session_state.history.append(st.session_state.step)
    st.session_state.step = step_name
    st.rerun()

def go_back():
    """Pop the last step from history and go back to it."""
    if st.session_state.history:
        st.session_state.step = st.session_state.history.pop()
        st.rerun()

def restart():
    st.session_state.step = 'HOME'
    st.session_state.history = [] # Clear history on restart
    st.session_state.customer_concern = ''
    st.session_state.job_type = ''
    st.session_state.triage_notes = '' # Reset triage notes
    st.rerun()

# --- SIDEBAR INFO ---
with st.sidebar:
    # ✅ 1. TU LOGO DE SWIFT PRO (Restaurado)
    st.image("image_7.png") 
    
    if st.session_state.history:
        if st.button("⬅️ BACK"):
            go_back()
        st.divider()
    
    st.title("🧠 CSR Command Center")
    
    # ✅ 2. TELÉFONOS IMPORTANTES
    st.info("""
    ### 📞 Key Contacts
    
    **👩‍💼 Hannah (Cell):** 571-726-9008
    
    **👨‍🔧 Jevon (Dialpad):** 703-214-9783
    
    **👨‍🔧 Raul:** 571-301-3134
    
    **👨‍🔧 Gio:** (703) 661-9006
    
    **📞 Araksan (Dialpad):** (703) 239-7626
    
    **📱 Araksan (Cell):** 703-928-0937
    """)
    
    st.divider()
    
    # 3. El Bloc de Notas (Scratchpad)
    if 'scratchpad' not in st.session_state:
        st.session_state.scratchpad = ""
    
    st.markdown("### 📝 Scratchpad")
    st.session_state.scratchpad = st.text_area(
        "Quick notes (Name, #, Codes):", 
        value=st.session_state.scratchpad,
        height=200,
        placeholder="Type quick details here..."
    )
    
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

elif st.session_state.step == 'LOCATION_CHECK':
    st.title("📍 Service Area")
    st.markdown('<div class="big-script">“Just to make sure you’re in our service area, what city are you calling from?”</div>', unsafe_allow_html=True)
    
    # --- ADDED LOCATION QUICK-REFERENCE ---
    # We use an expander so it doesn't clutter the UI, but keep it open by default for visibility
    with st.expander("🗺️ Reference: Covered Locations (NoVA)", expanded=True):
        loc_col1, loc_col2 = st.columns(2)
        with loc_col1:
            st.markdown("""
            **Fairfax County:** Springfield, Burke, Lorton, Fairfax, Vienna, McLean, Reston, Herndon, Chantilly, Centreville, Annandale.
            
            **Arlington & Alexandria:** (Inside the beltway, closer to DC).
            """)
        with loc_col2:
            st.markdown("""
            **Prince William County:** Woodbridge, Manassas, Dumfries, Dale City.
            
            **Loudoun County:** Ashburn, Leesburg, Sterling.
            """)
    # --------------------------------------

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ IN AREA (NoVA)"): go_to('CLIENT_STATUS')
    with col2:
        if st.button("🚫 OUT OF AREA"): go_to('REFER_OUT')

        # --- STEP: OUT OF AREA (REFER OUT) ---
elif st.session_state.step == 'REFER_OUT':
    st.title("🚫 Out of Service Area")
    
    # El guion exacto que pediste
    st.markdown('<div class="big-script">“I’m really sorry—we don’t service that area, but I’d be happy to point you in the right direction.”</div>', unsafe_allow_html=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        # Botón para regresar por si te equivocaste al hacer clic
        if st.button("⬅️ Go Back"): go_back()
    with col2:
        # Botón para terminar y empezar nueva llamada
        if st.button("🔄 New Call"): restart()

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

# 6. CATEGORY & JOB SELECTION (Combined)
elif st.session_state.step == 'CATEGORY_SELECT':
    st.title("🔧 Select Job Type")
    st.markdown('<div class="big-script">“What kind of issue are you experiencing today?”</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # --- HVAC COLUMN ---
    with col1:
        st.info("🔥 HVAC")
        hvac_options = [
            "Select job...",
            "AC Repair", "Heat Pump Repair", "Natural Gas/Propane Furnace Repair", 
            "Boiler Replacement", "Full HVAC System Replacement", "Mini-Split Repairs",
            "New Mini-Split Installations", "HVAC Maintenance / Tune-ups", "Duct Cleanings",
            "Filter replacement", "Fan Coils Replacements", "Packaged Unit Replacements",
            "Thermostats", "Humidifiers & Dehumidifiers", "Air Scrubbers/UV/Air Purification"
        ]
        hvac_choice = st.selectbox("HVAC List:", hvac_options, label_visibility="collapsed")
        
        if hvac_choice != "Select job...":
            if st.button("➡️ GO: HVAC"):
                st.session_state.job_type = hvac_choice
                go_to('HVAC_TRIAGE')

    # --- PLUMBING COLUMN ---
    with col2:
        st.info("🚿 PLUMBING")
        plumb_options = [
            "Select job...",
            "Leaks", "Clogged drains", "Spigots", "Thermostatic Mixing Valves",
            "Water Softeners & filtration systems", "Toilet repair/replacement", "Faucet repair",
            "Water heater repair or replacement", "Tankless water heaters", "Garbage disposals",
            "Sump pumps", "Sewer line issues", "Water line repair", "Fixture installs",
            "Repipes", "Underground", "Well Pumps", "Customer supplied basic plumbing repairs"
        ]
        plumb_choice = st.selectbox("Plumbing List:", plumb_options, label_visibility="collapsed")
        
        if plumb_choice != "Select job...":
            if st.button("➡️ GO: PLUMBING"):
                st.session_state.job_type = plumb_choice
                go_to('PLUMB_TRIAGE')

    # --- SALES/ESTIMATE COLUMN ---
    with col3:
        st.info("🆕 ESTIMATES")
        sales_options = [
            "Select job...",
            "HVAC Replacement", "Water Heater Replacement (Tank/Tankless)",
            "Humidifier Replacement", "Boiler Replacement"
        ]
        sales_choice = st.selectbox("Sales List:", sales_options, label_visibility="collapsed")
        
        if sales_choice != "Select job...":
            if st.button("➡️ GO: ESTIMATE"):
                st.session_state.job_type = sales_choice
                go_to('SALES_TRIAGE')

# 8. TRIAGE QUESTIONS (Interactive)
elif st.session_state.step == 'HVAC_TRIAGE':
    st.title("🔥 HVAC Discovery")
    st.info(f"Job: {st.session_state.job_type}")
    
    # We use a form so the page doesn't reload on every keystroke
    with st.form("hvac_triage_form"):
        st.markdown("### 🗣️ Ask the Customer:")
        
        # Capture answers
        q1 = st.text_input("1. 🕒 How long has this been going on?", key="hvac_q1")
        q2 = st.selectbox("2. ⚡ Is it Gas or Electric?", ["Unsure", "Gas", "Electric", "Oil", "Propane"], key="hvac_q2")
        q3 = st.text_input("3. 🏚️ About how old is the system?", key="hvac_q3")
        q4 = st.text_input("4. 🔊 Any weird noises or smells?", key="hvac_q4")
        
        st.error("⚠️ EMERGENCY IF: Gas Smell OR No Heat < 32°F")
        
        submitted = st.form_submit_button("✅ Save Notes & Continue")
        if submitted:
            # Save a formatted summary string to session state for later
            st.session_state.triage_notes = f"""
            - Duration: {q1}
            - Type: {q2}
            - Age: {q3}
            - Symptoms: {q4}
            """
            go_to('HVAC_PRICE')
            
    if st.button("🚨 EMERGENCY"): go_to('EMERGENCY')

elif st.session_state.step == 'PLUMB_TRIAGE':
    st.title("🚿 Plumbing Discovery")
    st.info(f"Job: {st.session_state.job_type}")
    
    with st.form("plumb_triage_form"):
        st.markdown("### 🗣️ Ask the Customer:")
        
        q1 = st.selectbox("1. 💧 Is water actively leaking right now?", ["No", "Yes - Major", "Yes - Minor"], key="plumb_q1")
        q2 = st.selectbox("2. 🚫 Can you shut the water off?", ["Yes", "No", "Unsure"], key="plumb_q2")
        q3 = st.text_input("3. 🚽 Are drains backing up? Where?", key="plumb_q3")
        q4 = st.selectbox("4. 🏠 Do you have at least one working toilet?", ["Yes", "No"], key="plumb_q4")
        
        st.error("⚠️ EMERGENCY IF: Major flooding or structural damage.")
        
        submitted = st.form_submit_button("✅ Save Notes & Continue")
        if submitted:
            st.session_state.triage_notes = f"""
            - Active Leak: {q1}
            - Shut off?: {q2}
            - Backups: {q3}
            - Working Toilet: {q4}
            """
            go_to('PLUMB_PRICE')
            
    if st.button("🚨 EMERGENCY"): go_to('EMERGENCY')

elif st.session_state.step == 'SALES_TRIAGE':
    st.title("🆕 Replacement Discovery")
    st.info(f"Job: {st.session_state.job_type}")
    
    with st.form("sales_triage_form"):
        st.markdown("### 🗣️ Ask the Customer:")
        
        q1 = st.selectbox("1. 🏚️ Is the current system working?", ["Working", "Not Working", "Intermittent"], key="sales_q1")
        q2 = st.text_input("2. 📅 How old is the unit?", key="sales_q2")
        q3 = st.text_input("3. 🤔 What is the main reason for replacement?", key="sales_q3")
        
        submitted = st.form_submit_button("✅ Save Notes & Book Estimate")
        if submitted:
            st.session_state.triage_notes = f"""
            - Status: {q1}
            - Age: {q2}
            - Motivation: {q3}
            """
            go_to('SALES_PRICE')

# 9. THE PIVOT (PRICING)
elif st.session_state.step == 'HVAC_PRICE':
    st.title("💰 The Pivot (HVAC)")
    mostrar_disponibilidad_central() # <--- PEGAR AQUÍ
    
    st.markdown('<div class="big-script">“ HVAC, it’s only <b>$99</b> to send a tech out to diagnose the system... Our soonest availability is [Day] between 8-12 or 12-5.”</div>', unsafe_allow_html=True)
    st.warning("🛑 DO NOT PAUSE after the price!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ BOOK ($99)"): go_to('CUSTOMER_INFO')
    with col2:
        if st.button("🛑 OBJECTION"): go_to('OBJECTION')

elif st.session_state.step == 'PLUMB_PRICE':
    st.title("💰 The Pivot (Plumbing)")
    mostrar_disponibilidad_central() # <--- PEGAR AQUÍ
    st.markdown('<div class="big-script">" plumbing, it’s only <b>$49</b> to send a tech out... Our soonest availability is [Day] between 8-12 or 12-5.”</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ BOOK ($49)"): go_to('CUSTOMER_INFO')
    with col2:
        if st.button("🛑 OBJECTION"): go_to('OBJECTION')

elif st.session_state.step == 'SALES_PRICE':
    st.title("🆓 The Pivot (Sales)")
    mostrar_disponibilidad_central() # <--- PEGAR AQUÍ
    st.markdown('<div class="big-script">“For replacements, we provide <b>FREE in-home estimates</b> so we can give you accurate options. Our soonest availability is...”</div>', unsafe_allow_html=True)
    if st.button("✅ BOOK ESTIMATE"): go_to('CUSTOMER_INFO')

# 9.5 OBJECTION HANDLING (Ensure this is here too)
elif st.session_state.step == 'OBJECTION':
    st.title("🛡️ Handling Objections")
    st.info("💡 Goal: Calm delivery + Immediate scheduling.")
    
    # 1. TIME WINDOW OBJECTION
    with st.expander("⏳ Objection: “That’s a big window” (8-12 or 12-5)", expanded=True):
        st.markdown('<div class="big-script">“Totally understand. You’ll receive a text as soon as the technician is on the way to help narrow the timeframe.”</div>', unsafe_allow_html=True)

    # 2. WRONG DAY OBJECTION
    with st.expander("📅 Objection: “That day doesn’t work for me”"):
        st.markdown('<div class="big-script">“No problem at all. We schedule in 8–12 or 12–5 windows. What day works best for you within one of those?”</div>', unsafe_allow_html=True)

    # 3. URGENCY OBJECTION
    with st.expander("🚨 Objection: “I need it sooner”"):
        st.markdown('<div class="big-script">“I completely understand. Let’s get you scheduled now to hold your spot, and I’ll check with my manager to see if there’s any way to get you in sooner. If something opens up, I’ll reach out immediately.”</div>', unsafe_allow_html=True)

    # 4. PRICE OBJECTION
    with st.expander("💸 Objection: “The dispatch fee is too high”"):
        st.markdown('<div class="big-script">“Totally understand. The fee covers the trip and a full diagnosis by a certified expert. Plus, if you join our Membership ($20/mo), you get 15% off repairs.”</div>', unsafe_allow_html=True)

    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🤝 SAVED -> BOOK"): go_to('CUSTOMER_INFO')
    with col2:
        if st.button("❌ LOST"): restart()

# 10. CUSTOMER INFO & CLOSE
# 10. CUSTOMER INFO & CLOSE
elif st.session_state.step == 'CUSTOMER_INFO':
    st.title("💻 ServiceTitan Entry")
    
    # --- LÓGICA DE ETIQUETAS AUTOMÁTICAS ---
    job = st.session_state.get('job_type', '')
    notes = st.session_state.get('triage_notes', '').lower()
    concern = st.session_state.get('customer_concern', '').lower()
    
    rec_tags = ["Booked"] # Etiqueta base
    
    # 1. Etiquetas por tipo de servicio
    if any(x in job for x in ["Replacement", "Estimate", "Install", "Sales"]):
        rec_tags.extend(["Sales Lead", "Upgrade Potential"])
    elif "Maintenance" in job:
        rec_tags.extend(["Maintenance Lead", "Membership"])
    else:
        rec_tags.append("Repair Inquiry")

    # 2. Etiquetas por urgencia (Lead Temperature)
    if any(x in notes or x in concern for x in ["leak", "no heat", "emergency", "flood", "gas", "spark"]):
        rec_tags.append("Hot Lead")
    else:
        rec_tags.append("Warm Lead")
        
    # 3. Etiquetas de oportunidad
    if "second opinion" in concern or "2nd" in concern:
        rec_tags.append("2nd Opinion")
    # ---------------------------------------

    # Mostrar las etiquetas recomendadas visualmente
    st.markdown("### 🏷️ Recommended ServiceTitan Tags")
    st.info(f"**Add these tags:** {', '.join(rec_tags)}")

    # Cuadro consolidado para copiar y pegar
    st.info("👇 Copy these notes into the Job Description in ServiceTitan:")
    
    full_notes = f"""
    JOB TYPE: {job}
    TAGS: {', '.join(rec_tags)}
    
    CUSTOMER CONCERN:
    {st.session_state.get('customer_concern', 'N/A')}
    
    TRIAGE DETAILS:
    {st.session_state.get('triage_notes', 'No notes recorded.')}
    
    SCRATCHPAD NOTES:
    {st.session_state.get('scratchpad', 'N/A')}
    """
    st.code(full_notes, language="text")

    st.markdown("### ➡️ Next Steps:")
    st.markdown("""
    1. **Go to ServiceTitan** and create the job.
    2. **Add the Tags** listed above.
    3. **Paste the Notes** from the box above.
    4. **Book the Appointment.**
    """)
    
    st.divider()
    
    if st.button("✅ I HAVE BOOKED IT IN SERVICETITAN"):
        go_to('CLOSE_CALL')