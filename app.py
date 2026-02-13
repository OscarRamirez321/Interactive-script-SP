import streamlit as st
import base64

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="SwiftPro Navigator", page_icon="🔧", layout="centered")

# --- VISUAL STYLES (COLOR PRO + FUNCTIONAL FIX) ---
st.markdown("""
    <style>
    /* 1. FONDO GENERAL CON UN TOQUE AZULADO */
    .stApp {
        background-color: #0f172a; /* Azul noche profundo, menos "negro muerto" */
    }
    section[data-testid="stSidebar"] {
        background-color: #1e293b; /* Azul grisáceo elegante */
        border-right: 1px solid #334155;
    }

    /* 2. TEXTOS Y TÍTULOS (AQUÍ ESTÁ EL COLOR) */
    h1 {
        color: #ff6b35 !important; /* NARANJA SWIFTPRO */
        font-weight: 800 !important;
        text-shadow: 0px 0px 10px rgba(255, 107, 53, 0.3);
    }
    h2, h3 {
        color: #38bdf8 !important; /* CELESTE BRILLANTE */
    }
    h4, p, li, span, label, .stMarkdown {
        color: #e2e8f0 !important; /* Blanco hueso (más suave a la vista) */
    }

    /* ============================================================
       CORRECCIÓN TÉCNICA (NO TOCAR - MANTIENE TODO VISIBLE)
       ============================================================ */
    
    /* Dropdowns oscuros */
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"] {
        background-color: #1e293b !important;
        border: 1px solid #38bdf8 !important; /* Borde Celeste */
    }
    li[data-baseweb="option"] {
        background-color: #1e293b !important;
        color: white !important;
    }
    li[data-baseweb="option"] * {
        color: white !important;
    }
    li[data-baseweb="option"]:hover, li[data-baseweb="option"][aria-selected="true"] {
        background-color: #ff6b35 !important; /* Naranja al seleccionar */
        color: white !important;
    }

    /* Bloque de código (Notas ServiceTitan) */
    div[data-testid="stCodeBlock"] {
        background-color: #020617 !important;
        border: 1px solid #ff6b35; /* Borde Naranja Fino */
        border-radius: 8px;
    }
    div[data-testid="stCodeBlock"] pre, div[data-testid="stCodeBlock"] code {
        background-color: #020617 !important;
        color: #4ade80 !important; /* Texto Verde Matrix */
    }

    /* ============================================================
       DISEÑO VISUAL (CAJAS Y BOTONES)
       ============================================================ */
    
    /* Inputs y Selectboxes */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: #1e293b !important;
        border: 1px solid #475569 !important;
        color: white !important;
    }
    .stTextInput input { color: white !important; }
    
    /* Expanders (Acordeones) */
    div[data-testid="stExpander"] {
        background-color: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid #38bdf8 !important; /* Borde Celeste */
        border-radius: 10px;
    }
    div[data-testid="stExpander"] > details > summary {
        color: #38bdf8 !important; /* Título celeste */
        font-weight: 600;
    }
    div[data-testid="stExpander"] > details > summary:hover {
        color: #ff6b35 !important;
    }

    /* Botones */
    .stButton button {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: #ffffff !important;
        border: 1px solid #38bdf8;
        border-radius: 12px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stButton button:hover {
        border-color: #ff6b35;
        color: #ff6b35 !important;
        transform: translateY(-2px);
        box-shadow: 0 0 15px rgba(255, 107, 53, 0.4); /* Resplandor Naranja */
    }

    /* CAJAS PERSONALIZADAS (EL TOQUE PRO) */
    .big-script {
        background: linear-gradient(90deg, rgba(15,23,42,0.9) 0%, rgba(30,41,59,0.9) 100%);
        border: 1px solid #475569;
        border-left: 6px solid #ff6b35; /* Borde Naranja */
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 25px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }
    
    .dialogue-box {
        background-color: rgba(30, 41, 59, 0.6);
        border: 1px solid #4ade80; /* Verde éxito */
        border-left: 6px solid #4ade80;
        border-radius: 12px;
        padding: 20px;
        color: #f1f5f9 !important;
    }

    .contact-box {
        background-color: #1e293b;
        border: 1px solid #38bdf8;
        border-radius: 12px;
        padding: 15px;
        color: white !important;
    }

    /* Scratchpad */
    .stTextArea textarea {
        background-color: #f8fafc !important; /* Blanco casi puro */
        color: #0f172a !important; /* Texto oscuro */
        border: 2px solid #cbd5e1;
    }
    .stTextArea label { color: #38bdf8 !important; }

    /* Contactos */
    .contact-name { color: #e2e8f0 !important; font-weight: 700; }
    .contact-phone { color: #38bdf8 !important; font-family: monospace; font-size: 16px; }

    /* Ocultar Header */
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if 'step' not in st.session_state: st.session_state.step = 'HOME'
if 'history' not in st.session_state: st.session_state.history = []
if 'customer_concern' not in st.session_state: st.session_state.customer_concern = ''
if 'job_type' not in st.session_state: st.session_state.job_type = ''
if 'triage_notes' not in st.session_state: st.session_state.triage_notes = ''

def go_to(step_name):
    st.session_state.history.append(st.session_state.step)
    st.session_state.step = step_name
    st.rerun()

def go_back():
    if st.session_state.history:
        st.session_state.step = st.session_state.history.pop()
        st.rerun()

def restart():
    st.session_state.step = 'HOME'
    st.session_state.history = []
    st.session_state.customer_concern = ''
    st.session_state.job_type = ''
    st.session_state.triage_notes = '' 
    st.rerun()

def mostrar_disponibilidad_central():
    st.markdown("""
    <div class="contact-box">
        <h4 style="margin-top:0; color:#cbd5e1;">📅 Service Availability</h4>
        <p><b>🔥 HVAC:</b> Feb 11 (Wed) - After 12 PM | Feb 12 (Thu) - Open</p>
        <p><b>🚿 Plumbing:</b> Feb 11 (Wed) - Emergency Only | Feb 12 (Thu) - Open</p>
        <p><b>🧹 Duct/Dryer:</b> Feb 12 (Thu) - Open</p>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR INFO (UPDATED) ---
with st.sidebar:
    # Use logo here or not, but centered logic is in HOME
   # st.image("image_7.png", width=150) 
    
    if st.session_state.history:
        if st.button("⬅️ BACK"):
            go_back()
        st.divider()
    
    st.title("🧠 CSR Command Center")
    
    # --- UPDATED KEY CONTACTS SECTION (Uses new .contact-box CSS) ---
    with st.expander("📞 Key Contacts (Click to View)", expanded=False):
        st.markdown("""
        <div class="contact-box" style="margin-bottom: 0;">
            <div class="contact-item">
                <div class="contact-name">👩‍💼 Hannah (Cell)</div>
                <div class="contact-phone">571-726-9008</div>
            </div>
            <div class="contact-item">
                <div class="contact-name">👨‍🔧 Jevon (Dialpad)</div>
                <div class="contact-phone">703-214-9783</div>
            </div>
            <div class="contact-item">
                <div class="contact-name">👨‍🔧 Raul</div>
                <div class="contact-phone">571-301-3134</div>
            </div>
            <div class="contact-item">
                <div class="contact-name">👨‍🔧 Gio</div>
                <div class="contact-phone">(703) 661-9006</div>
            </div>
            <div class="contact-item">
                <div class="contact-name">📞 Araksan (Dialpad)</div>
                <div class="contact-phone">(703) 239-7626</div>
            </div>
            <div class="contact-item">
                <div class="contact-name">📱 Araksan (Cell)</div>
                <div class="contact-phone">703-928-0937</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Scratchpad
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
    # --- LOGO CENTERING LOGIC ---
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("image_7.png", use_container_width=True)
    # -----------------------------

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

# 3. LOCATION CHECK
elif st.session_state.step == 'LOCATION_CHECK':
    st.title("📍 Service Area")
    st.markdown('<div class="big-script">“Just to make sure you’re in our service area, what city are you calling from?”</div>', unsafe_allow_html=True)
    
    # WRAP REFERENCE IN GLASS BOX
    with st.expander("🗺️ Reference: Covered Locations (NoVA)", expanded=True):
        st.markdown("""
        <div class="contact-box">
            <div style="display:flex; gap:20px;">
                <div style="flex:1;">
                    <b>Fairfax County:</b> Springfield, Burke, Lorton, Fairfax, Vienna, McLean, Reston, Herndon, Chantilly, Centreville, Annandale.<br><br>
                    <b>Arlington & Alexandria:</b> (Inside the beltway).
                </div>
                <div style="flex:1;">
                    <b>Prince William County:</b> Woodbridge, Manassas, Dumfries, Dale City.<br><br>
                    <b>Loudoun County:</b> Ashburn, Leesburg, Sterling.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ IN AREA (NoVA)"): go_to('CLIENT_STATUS')
    with col2:
        if st.button("🚫 OUT OF AREA"): go_to('REFER_OUT')

# 3.5 STEP: OUT OF AREA (REFER OUT)
elif st.session_state.step == 'REFER_OUT':
    st.title("🚫 Out of Service Area")
    st.markdown('<div class="big-script">“I’m really sorry—we don’t service that area, but I’d be happy to point you in the right direction.”</div>', unsafe_allow_html=True)
    
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Go Back"): go_back()
    with col2:
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

# 5. ACKNOWLEDGE & LOG ISSUE
elif st.session_state.step == 'ACKNOWLEDGE_ISSUE':
    st.title("📝 Understanding the Issue")
    
    st.markdown("#### ✅ **If they already explained the issue:**")
    st.markdown('<div class="dialogue-box">“Okay, absolutely. Let me ask you a couple quick questions so we can get this scheduled properly.”</div>', unsafe_allow_html=True)

    st.markdown("#### ✅ **If they have not explained the reason yet:**")
    st.markdown('<div class="dialogue-box" style="border-left: 6px solid #f59e0b; border-color: rgba(245, 158, 11, 0.3);">“Are you needing help with your heating and cooling system or something plumbing-related?”</div>', unsafe_allow_html=True)
    
    st.markdown("### ✍️ Notes")
    st.session_state.customer_concern = st.text_area("Write down the customer's concern here:", height=150, placeholder="e.g. leaking faucet, no heat upstairs...", label_visibility="collapsed")
    
    if st.session_state.customer_concern:
        if st.button("✅ Saved. Continue to Category"):
            go_to('CATEGORY_SELECT')
    else:
        st.caption("*Please enter a note to continue*")

# 6. CATEGORY & JOB SELECTION
elif st.session_state.step == 'CATEGORY_SELECT':
    st.title("🔧 Select Job Type")
    st.markdown('<div class="big-script">“What kind of issue are you experiencing today?”</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    # HVAC COLUMN
    with col1:
        st.info("🔥 HVAC")
        hvac_options = [
            "Select job...",
            "No Heat Repair", 
            "No AC Repair", 
            "Maintenance (Inspections, Cleanings)", 
            "Service/Repair"
        ]
        hvac_choice = st.selectbox("HVAC List:", hvac_options, label_visibility="collapsed")
        
        if hvac_choice != "Select job...":
            if st.button("➡️ GO: HVAC"):
                st.session_state.job_type = hvac_choice.strip()
                go_to('HVAC_TRIAGE')

    # PLUMBING COLUMN
    with col2:
        st.info("🚿 PLUMBING")
        plumb_options = [
            "Select job...",
            "Water Heater / Tank ", "Repipe", "Drain / Sewer ", "Pumps",
            "Toilet / Faucet ", "Underground", "Faucet repair"
        ]
        plumb_choice = st.selectbox("Plumbing List:", plumb_options, label_visibility="collapsed")
        
        if plumb_choice != "Select job...":
            if st.button("➡️ GO: PLUMBING"):
                st.session_state.job_type = plumb_choice
                go_to('PLUMB_TRIAGE')

    # SALES/ESTIMATE COLUMN
    with col3:
        st.info("🆕 ESTIMATES")
        sales_options = [
            "Select job...",
            "HVAC Replacement", "Water Heater Replacement (Tank/Tankless)",
            "Humidifier Replacement", "Boiler Replacement","Mini- Split Installation"
        ]
        sales_choice = st.selectbox("Sales List:", sales_options, label_visibility="collapsed")
        
        if sales_choice != "Select job...":
            if st.button("➡️ GO: ESTIMATE"):
                st.session_state.job_type = sales_choice
                go_to('SALES_TRIAGE')

# 8. HVAC TRIAGE (CUSTOMIZED PER JOB)
elif st.session_state.step == 'HVAC_TRIAGE':
    st.title(f"🔥 Discovery: {st.session_state.job_type}")
    
    # ---------------- NO HEAT REPAIR ----------------
    if st.session_state.job_type == "No Heat Repair":
        st.markdown('<div class="dialogue-box">“I’m sorry to hear about the heat. Let’s get some details so we can help.”</div>', unsafe_allow_html=True)
        
        with st.form("hvac_no_heat_form"):
            st.markdown("### 🗣️ Ask the Customer:")
            q1 = st.text_input("1. 🕒 How long has the heat not been working?")
            q2 = st.selectbox("2. 📉 Is it completely not turning on, or just blowing cold air?", ["Completely Off", "Blowing Cold Air", "Cycling Weirdly"])
            
            # Special Handling for Gas/Electric question
            col_a, col_b = st.columns([2, 1])
            with col_a:
                q3 = st.selectbox("3. ⚡ Is your system gas or electric?", ["Gas", "Electric", "Oil", "Propane", "Unsure"])
            with col_b:
                 st.info("💡 **If unsure:** say “That’s okay, we’ll take a look.”")

            q4 = st.text_input("4. 🏚️ About how old is the system?")
            q5 = st.text_input("5. 🔊 Any unusual smells, loud noises, or error codes?")
            q6 = st.selectbox("6. 🔥 Are you using space heaters right now?", ["No", "Yes"])

            # URGENCY TRIGGERS
            st.error("""
            **⚠ EMERGENCY IF:**
            * Gas smell
            * No heat & outdoor temp below freezing
            * Elderly, infants, medical conditions in home
            """)
            
            submitted = st.form_submit_button("✅ Save Notes & Continue")
            if submitted:
                st.session_state.triage_notes = f"NO HEAT:\n- Duration: {q1}\n- Behavior: {q2}\n- Fuel: {q3}\n- Age: {q4}\n- Symptoms: {q5}\n- Space Heaters: {q6}"
                go_to('HVAC_PRICE')

    # ---------------- NO AC REPAIR ----------------
    elif st.session_state.job_type == "No AC Repair":
        st.markdown('<div class="dialogue-box">“It’s tough without AC. Let’s see what’s going on.”</div>', unsafe_allow_html=True)
        
        with st.form("hvac_no_ac_form"):
            st.markdown("### 🗣️ Ask the Customer:")
            q1 = st.text_input("1. 🕒 How long has the AC not been working?")
            q2 = st.selectbox("2. 📉 Is it completely not turning on, or running but not cooling?", ["Not Turning On", "Running No Cool", "Cycling"])
            q3 = st.selectbox("3. 🌬️ Is warm air coming out of the vents?", ["Yes", "No", "Unsure"])
            q4 = st.selectbox("4. 🏡 Is the outdoor unit running?", ["Yes", "No", "Unsure"])
            q5 = st.selectbox("5. 💧 Any water leaking inside near the air handler?", ["No", "Yes"])
            q6 = st.text_input("6. 🔊 Any unusual noises or smells?")
            q7 = st.text_input("7. 🏚️ About how old is the system?")

            # URGENCY TRIGGERS
            st.error("""
            **⚠ EMERGENCY IF:**
            * Home over 85–90° inside
            * Elderly, babies, medical needs
            * Water leaking through ceiling
            * Burning smell
            """)
            
            submitted = st.form_submit_button("✅ Save Notes & Continue")
            if submitted:
                st.session_state.triage_notes = f"NO AC:\n- Duration: {q1}\n- Behavior: {q2}\n- Warm Air: {q3}\n- Outdoor Unit: {q4}\n- Leaks: {q5}\n- Symptoms: {q6}\n- Age: {q7}"
                go_to('HVAC_PRICE')

    # ---------------- MAINTENANCE ----------------
    elif "Maintenance" in st.session_state.job_type:
        st.markdown('<div class="dialogue-box">“Maintenance is a great idea to keep things running smoothly.”</div>', unsafe_allow_html=True)
        
        with st.form("hvac_maint_form"):
            st.markdown("### 🗣️ Ask the Customer:")
            q1 = st.selectbox("1. 🌡️ Is this for heating, cooling, or both?", ["Heating", "Cooling", "Both"])
            q2 = st.text_input("2. 📅 When was the last maintenance performed?")
            q3 = st.text_input("3. 🤔 Have you noticed anything unusual recently?")
            q4 = st.selectbox("4. ✅ Is the system working normally right now?", ["Yes", "No", "Not really"])
            q5 = st.text_input("5. 🏚️ How old is the equipment?")
            q6 = st.selectbox("6. 📋 Are you currently on a maintenance plan?", ["No", "Yes", "Unsure"])

            # OPPORTUNITY TRIGGERS
            st.success("""
            **🎯 OPPORTUNITY TRIGGERS:**
            * System 10+ years old
            * Hasn’t been serviced in 2+ years
            * Minor complaints mentioned casually
            """)
            
            submitted = st.form_submit_button("✅ Save Notes & Continue")
            if submitted:
                st.session_state.triage_notes = f"MAINTENANCE:\n- Type: {q1}\n- Last Service: {q2}\n- Unusual: {q3}\n- Status: {q4}\n- Age: {q5}\n- Plan: {q6}"
                go_to('HVAC_PRICE')

    # ---------------- SERVICE / GENERAL REPAIR ----------------
    elif "Service" in st.session_state.job_type:
        st.markdown('<div class="dialogue-box">“Let’s figure out exactly what’s going on with the system.”</div>', unsafe_allow_html=True)
        
        with st.form("hvac_service_form"):
            st.markdown("### 🗣️ Ask the Customer:")
            q1 = st.text_area("1. 📝 What exactly is the system doing that concerns you?")
            q2 = st.text_input("2. 🕒 When did you first notice this?")
            q3 = st.selectbox("3. ⚙️ Is the system still running?", ["Yes", "No", "Intermittently"])
            q4 = st.selectbox("4. 📉 Is it heating/cooling properly, just making noise or acting inconsistent?", ["Not Heating/Cooling", "Just Noise", "Inconsistent", "Other"])
            q5 = st.text_input("5. 🛠️ Any recent repairs or work done?")
            q6 = st.text_input("6. 🏚️ About how old is the system?")

            # ESCALATION TRIGGERS
            st.warning("""
            **⚠ ESCALATE IF:**
            * Electrical burning smell
            * Loud banging/grinding
            * Water actively leaking
            * Breaker repeatedly tripping
            """)
            
            submitted = st.form_submit_button("✅ Save Notes & Continue")
            if submitted:
                st.session_state.triage_notes = f"SERVICE/REPAIR:\n- Concern: {q1}\n- Onset: {q2}\n- Running: {q3}\n- Nature: {q4}\n- History: {q5}\n- Age: {q6}"
                go_to('HVAC_PRICE')

    # ---------------- FALLBACK ----------------
    else:
        st.warning("⚠️ Generic HVAC Logic (Category not specifically matched)")
        with st.form("generic_hvac"):
            notes = st.text_area("Enter triage notes:")
            if st.form_submit_button("✅ Continue"):
                st.session_state.triage_notes = notes
                go_to('HVAC_PRICE')
            
    if st.button("🚨 EMERGENCY / ESCALATION"): go_to('EMERGENCY')

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
    mostrar_disponibilidad_central() 
    
    st.markdown('<div class="big-script">“For the diagnostic, it is only <b>$99</b> Our soonest availability is [Day] between 8am-12pm or 12pm-5pm. Which of those works best for you?”</div>', unsafe_allow_html=True)
    st.warning("🛑 DO NOT PAUSE after the price!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ BOOK ($99)"): go_to('CUSTOMER_INFO')
    with col2:
        if st.button("🛑 OBJECTION"): go_to('OBJECTION')

elif st.session_state.step == 'PLUMB_PRICE':
    st.title("💰 The Pivot (Plumbing)")
    mostrar_disponibilidad_central()
    st.markdown('<div class="big-script">“For the diagnostic, it is only<b>$49</b> Our soonest availability is [Day] between 8am-12pm or 12pm 5pm. Which of those works best for you?”</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ BOOK ($49)"): go_to('CUSTOMER_INFO')
    with col2:
        if st.button("🛑 OBJECTION"): go_to('OBJECTION')

elif st.session_state.step == 'SALES_PRICE':
    st.title("🆓 The Pivot (Sales)")
    mostrar_disponibilidad_central()
    st.markdown('<div class="big-script">“For replacements, we provide <b>FREE in-home estimates</b> so we can give you accurate options. Our soonest availability is...”</div>', unsafe_allow_html=True)
    if st.button("✅ BOOK ESTIMATE"): go_to('CUSTOMER_INFO')

# 9.5 OBJECTION HANDLING
elif st.session_state.step == 'OBJECTION':
    st.title("🛡️ Handling Objections")
    st.info("💡 Goal: Calm delivery + Immediate scheduling.")
    
    with st.expander("⏳ Objection: “That’s a big window” (8-12 or 12-5)", expanded=True):
        st.markdown('<div class="big-script">“Totally understand. You’ll receive a text as soon as the technician is on the way to help narrow the timeframe.”</div>', unsafe_allow_html=True)

    with st.expander("📅 Objection: “That day doesn’t work for me”"):
        st.markdown('<div class="big-script">“No problem at all. We schedule in 8–12 or 12–5 windows. What day works best for you within one of those?”</div>', unsafe_allow_html=True)

    with st.expander("🚨 Objection: “I need it sooner”"):
        st.markdown('<div class="big-script">“I completely understand. Let’s get you scheduled now to hold your spot, and I’ll check with my manager to see if there’s any way to get you in sooner. If something opens up, I’ll reach out immediately.”</div>', unsafe_allow_html=True)

    with st.expander("💸 Objection: “The dispatch fee is too high”"):
        st.markdown('<div class="big-script">“Totally understand. The fee covers the trip and a full diagnosis by a certified expert. Plus, if you join our Membership ($20/mo), you get 15% off repairs.”</div>', unsafe_allow_html=True)

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🤝 SAVED -> BOOK"): go_to('CUSTOMER_INFO')
    with col2:
        if st.button("❌ LOST"): restart()

# 10. CUSTOMER INFO & CLOSE
elif st.session_state.step == 'CUSTOMER_INFO':
    st.title("💻 ServiceTitan Entry")
    
    job = st.session_state.get('job_type', '')
    notes = st.session_state.get('triage_notes', '').lower()
    concern = st.session_state.get('customer_concern', '').lower()
    
    rec_tags = ["Booked"]
    
    # 1. Tags by Service
    if any(x in job for x in ["Replacement", "Estimate", "Install", "Sales"]):
        rec_tags.extend(["Sales Lead", "Upgrade Potential"])
    elif "Maintenance" in job:
        rec_tags.extend(["Maintenance Lead", "Membership"])
    else:
        rec_tags.append("Repair Inquiry")

    # 2. Tags by Lead Temp
    if any(x in notes or x in concern for x in ["leak", "no heat", "emergency", "flood", "gas", "spark", "burning"]):
        rec_tags.append("Hot Lead")
    else:
        rec_tags.append("Warm Lead")
        
    # 3. Opportunity Tags
    if "second opinion" in concern or "2nd" in concern:
        rec_tags.append("2nd Opinion")

    st.markdown("### 🏷️ Recommended ServiceTitan Tags")
    st.info(f"**Add these tags:** {', '.join(rec_tags)}")

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
        restart()

elif st.session_state.step == 'EMERGENCY':
    st.title("🚨 Emergency Protocol")
    st.error("STOP. Do not schedule standard service.")
    st.markdown("""
    ### ⚠️ Immediate Actions:
    
    **For Gas Smells:**
    1. Tell them: *"Please evacuate the home immediately and call your gas utility provider or 911 from a safe distance."*
    2. Do NOT book a standard tech until the utility company declares it safe.

    **For Major Water Damage:**
    1. Tell them: *"If it's safe to do so, please shut off your main water valve immediately."*
    
    **For Medical Emergencies (No Heat/Cool):**
    1. Check for **Space Heaters** (temporary fix).
    2. Consult Manager (Hannah/Jevon) for **Priority Dispatch**.
    """)
    
    if st.button("🔙 Back to Triage"): go_back()