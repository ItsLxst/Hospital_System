import sqlite3
from contextlib import closing

import streamlit as st

DB_NAME = "hospital.db"

# =================================================================
# PAGE CONFIG + THEME (light green everywhere)
# =================================================================

st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500&family=Public+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg:            #F3F8F0;
        --bg-deep:        #E6F1E1;
        --surface:        #FFFFFF;
        --surface-soft:   #F1F8ED;
        --ink:            #1C2B20;
        --ink-soft:       #5C6E60;
        --ink-faint:      #8A9B8E;
        --brand-800:      #16311E;
        --brand-600:      #2C6B3F;
        --brand-500:      #3E8153;
        --brand-300:      #9BC9A4;
        --brand-100:      #DCEFDA;
        --gold:           #C6963A;
        --gold-soft:      #F3E4C2;
        --terracotta:     #BE5236;
        --terracotta-soft:#F6DFD6;
        --sky:            #3E7CA6;
        --sky-soft:       #DCEBF3;
        --radius:         14px;
        --shadow-sm:      0 1px 2px rgba(22, 49, 30, 0.06);
        --shadow-md:      0 6px 20px rgba(22, 49, 30, 0.08);
        --shadow-lg:      0 16px 40px rgba(22, 49, 30, 0.14);
    }

    html, body, [class*="css"] {
        font-family: 'Public Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* ---------- App shell ---------- */
    .stApp {
        background:
            radial-gradient(1100px 500px at 8% -8%, var(--brand-100) 0%, transparent 60%),
            radial-gradient(900px 500px at 105% 10%, var(--gold-soft) 0%, transparent 55%),
            var(--bg);
    }

    .block-container {
        padding-top: 2rem;
        max-width: 1180px;
    }

    /* ---------- Typography ---------- */
    h1, h2, h3 {
        font-family: 'Fraunces', Georgia, serif !important;
        color: var(--brand-800) !important;
        letter-spacing: -0.01em;
    }
    h3 {
        font-weight: 600 !important;
        border-bottom: 1px solid var(--brand-100);
        padding-bottom: 0.5rem;
        margin-bottom: 1rem !important;
    }
    p, span, label, li { color: var(--ink); }
    .stCaption, [data-testid="stCaptionContainer"] { color: var(--ink-faint) !important; }
    code, .stCodeBlock, .hms-mono { font-family: 'JetBrains Mono', monospace !important; }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(190deg, var(--brand-800) 0%, var(--brand-600) 100%);
        border-right: none;
    }
    section[data-testid="stSidebar"] * { color: #EAF4EB !important; }
    section[data-testid="stSidebar"] .stCaption, section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #BFDCC4 !important;
    }
    section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15); }
    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.35);
        color: #FFFFFF !important;
        box-shadow: none;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.22);
        transform: none;
    }

    /* ---------- Cards: forms, expanders, containers ---------- */
    div[data-testid="stForm"], div[data-testid="stExpander"] {
        background: var(--surface);
        border: 1px solid var(--brand-100);
        border-radius: var(--radius);
        padding: 1.3rem 1.4rem;
        box-shadow: var(--shadow-sm);
    }
    div[data-testid="stExpander"] summary {
        font-weight: 600;
        color: var(--brand-800);
    }

    /* ---------- Inputs ---------- */
    .stTextInput input, .stNumberInput input, .stDateInput input,
    .stTextArea textarea, div[data-baseweb="select"] > div {
        background: var(--surface-soft) !important;
        border: 1px solid var(--brand-100) !important;
        border-radius: 9px !important;
        color: var(--ink) !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
        border-color: var(--brand-500) !important;
        box-shadow: 0 0 0 3px var(--brand-100) !important;
    }
    label p { font-weight: 600 !important; color: var(--brand-800) !important; font-size: 0.92rem; }

    /* Radio / segmented look */
    div[role="radiogroup"] {
        gap: 0.4rem;
    }
    div[role="radiogroup"] label {
        background: var(--surface-soft);
        border: 1px solid var(--brand-100);
        border-radius: 999px;
        padding: 0.25rem 0.9rem;
    }

    /* ---------- Buttons ---------- */
    .stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(135deg, var(--brand-500) 0%, var(--brand-600) 100%);
        color: #FFFFFF;
        border-radius: 999px;
        border: none;
        padding: 0.55rem 1.5rem;
        font-weight: 600;
        letter-spacing: 0.01em;
        box-shadow: var(--shadow-sm);
        transition: transform 0.12s ease, box-shadow 0.12s ease;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
        color: #FFFFFF;
    }
    .stButton > button:active, .stFormSubmitButton > button:active { transform: translateY(0); }

    /* ---------- Tabs as pill nav ---------- */
    div[data-testid="stTabs"] div[role="tablist"] {
        gap: 0.4rem;
        border-bottom: none;
        background: var(--surface-soft);
        padding: 0.35rem;
        border-radius: 999px;
        border: 1px solid var(--brand-100);
        width: fit-content;
    }
    div[data-testid="stTabs"] button[role="tab"] {
        border-radius: 999px !important;
        color: var(--ink-soft);
        font-weight: 600;
        padding: 0.4rem 1.1rem;
    }
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        background: var(--brand-600);
        color: #FFFFFF !important;
    }
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] p { color: #FFFFFF !important; }

    /* ---------- Metrics ---------- */
    div[data-testid="stMetric"] {
        background: var(--surface);
        border: 1px solid var(--brand-100);
        border-top: 3px solid var(--brand-500);
        border-radius: var(--radius);
        padding: 0.9rem 1rem;
        box-shadow: var(--shadow-sm);
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Fraunces', serif !important;
        color: var(--brand-800) !important;
    }
    div[data-testid="stMetricLabel"] { color: var(--ink-soft) !important; }

    /* ---------- Banner / hero ---------- */
    .hms-banner {
        position: relative;
        background: linear-gradient(120deg, var(--brand-800) 0%, var(--brand-600) 65%, var(--brand-500) 100%);
        padding: 1.4rem 1.6rem 1.1rem;
        border-radius: 18px;
        color: #FFFFFF;
        margin-bottom: 1.4rem;
        box-shadow: var(--shadow-md);
        overflow: hidden;
    }
    .hms-banner .hms-eyebrow {
        text-transform: uppercase;
        letter-spacing: 0.14em;
        font-size: 0.7rem;
        color: var(--gold-soft);
        font-weight: 600;
    }
    .hms-banner h2 {
        color: #FFFFFF !important;
        margin: 0.15rem 0 0.2rem;
        font-size: 1.7rem;
    }
    .hms-banner p { margin: 0; opacity: 0.85; font-size: 0.95rem; }
    .hms-banner .hms-pulse { margin-top: 0.7rem; opacity: 0.9; }

    /* ---------- Status badges ---------- */
    .hms-badge {
        display: inline-block;
        padding: 0.18rem 0.65rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.01em;
    }
    .hms-badge-green { background: var(--brand-100); color: var(--brand-800); }
    .hms-badge-gold  { background: var(--gold-soft); color: #7A5A16; }
    .hms-badge-red   { background: var(--terracotta-soft); color: var(--terracotta); }
    .hms-badge-blue  { background: var(--sky-soft); color: var(--sky); }

    /* ---------- Tables / dataframes ---------- */
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--brand-100);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: var(--shadow-sm);
    }
    thead tr th {
        background-color: var(--brand-600) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* ---------- Alerts ---------- */
    div[data-testid="stAlertContentSuccess"] { color: var(--brand-800); }
    div[data-testid="stNotification"] { border-radius: 12px; }

    /* ---------- Divider ---------- */
    hr { border-color: var(--brand-100); }

    /* ---------- Login hero card ---------- */
    .hms-login-hero {
        background: linear-gradient(165deg, var(--brand-800) 0%, var(--brand-600) 55%, var(--brand-500) 100%);
        border-radius: 22px;
        padding: 2.2rem 2rem;
        color: #FFFFFF;
        height: 100%;
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
    }
    .hms-login-hero .hms-eyebrow {
        text-transform: uppercase;
        letter-spacing: 0.16em;
        font-size: 0.72rem;
        color: var(--gold-soft);
        font-weight: 700;
    }
    .hms-login-hero h1 {
        color: #FFFFFF !important;
        font-size: 2.1rem;
        margin: 0.3rem 0 0.6rem;
        line-height: 1.15;
    }
    .hms-login-hero p { color: #DCEFDA; font-size: 0.98rem; line-height: 1.55; max-width: 34ch; }
    .hms-login-card {
        background: var(--surface);
        border-radius: 22px;
        padding: 2.1rem 2rem;
        box-shadow: var(--shadow-lg);
        border: 1px solid var(--brand-100);
    }
    .hms-role-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 999px;
        padding: 0.3rem 0.75rem;
        font-size: 0.82rem;
        margin: 0.2rem 0.35rem 0.2rem 0;
    }

    /* ---------- Landing page ---------- */
    .hms-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.4rem 0.2rem 1.6rem;
    }
    .hms-nav-brand {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        font-family: 'Fraunces', serif;
        font-weight: 700;
        font-size: 1.35rem;
        color: var(--brand-800);
    }
    .hms-nav-brand span.hms-nav-tag {
        font-family: 'Public Sans', sans-serif;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        background: var(--brand-100);
        color: var(--brand-800);
        padding: 0.2rem 0.55rem;
        border-radius: 999px;
    }
    .hms-hero-wrap {
        position: relative;
        background: linear-gradient(150deg, var(--brand-800) 0%, var(--brand-600) 55%, var(--brand-500) 100%);
        border-radius: 28px;
        padding: 3.4rem 3rem;
        color: #FFFFFF;
        box-shadow: var(--shadow-lg);
        overflow: hidden;
        margin-bottom: 2.2rem;
    }
    .hms-hero-wrap .hms-eyebrow {
        text-transform: uppercase;
        letter-spacing: 0.18em;
        font-size: 0.74rem;
        font-weight: 700;
        color: var(--gold-soft);
    }
    .hms-hero-wrap h1 {
        color: #FFFFFF !important;
        font-size: 3rem;
        line-height: 1.08;
        margin: 0.5rem 0 1rem;
        max-width: 18ch;
    }
    .hms-hero-wrap p.hms-hero-sub {
        color: #DCEFDA;
        font-size: 1.08rem;
        line-height: 1.6;
        max-width: 46ch;
        margin-bottom: 0;
    }
    .hms-stat-row {
        display: flex;
        gap: 2.4rem;
        margin-top: 2rem;
        flex-wrap: wrap;
    }
    .hms-stat-row .hms-stat-num {
        font-family: 'Fraunces', serif;
        font-size: 1.9rem;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1;
    }
    .hms-stat-row .hms-stat-label {
        font-size: 0.78rem;
        color: #BFDCC4;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.25rem;
    }
    .hms-feature-card {
        background: var(--surface);
        border: 1px solid var(--brand-100);
        border-radius: var(--radius);
        padding: 1.4rem 1.3rem 1.5rem;
        box-shadow: var(--shadow-sm);
        height: 100%;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .hms-feature-card:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-md);
    }
    .hms-feature-card .hms-feature-icon {
        font-size: 1.7rem;
        display: inline-block;
        margin-bottom: 0.6rem;
        background: var(--brand-100);
        border-radius: 12px;
        padding: 0.5rem 0.65rem;
    }
    .hms-feature-card h4 {
        font-family: 'Fraunces', serif;
        color: var(--brand-800);
        font-size: 1.08rem;
        margin: 0 0 0.4rem;
        font-weight: 600;
    }
    .hms-feature-card p {
        color: var(--ink-soft);
        font-size: 0.9rem;
        line-height: 1.5;
        margin: 0;
    }
    .hms-role-strip {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin-top: 1.6rem;
    }
    .hms-role-card {
        flex: 1 1 150px;
        background: var(--surface);
        border: 1px solid var(--brand-100);
        border-radius: var(--radius);
        padding: 1.1rem 1rem;
        text-align: center;
        box-shadow: var(--shadow-sm);
    }
    .hms-role-card .hms-role-icon { font-size: 1.6rem; }
    .hms-role-card .hms-role-name {
        font-weight: 700;
        color: var(--brand-800);
        margin-top: 0.4rem;
        font-size: 0.92rem;
    }
    .hms-role-card .hms-role-desc {
        color: var(--ink-faint);
        font-size: 0.78rem;
        margin-top: 0.15rem;
    }
    .hms-cta-wrap {
        background: linear-gradient(120deg, var(--brand-100) 0%, var(--gold-soft) 100%);
        border-radius: 24px;
        padding: 2.4rem 2.4rem;
        text-align: center;
        margin-top: 2.4rem;
        border: 1px solid var(--brand-100);
    }
    .hms-cta-wrap h2 { margin-bottom: 0.4rem; }
    .hms-cta-wrap p { color: var(--ink-soft); margin-bottom: 0; }
    .hms-footer {
        text-align: center;
        color: var(--ink-faint);
        font-size: 0.82rem;
        padding: 2rem 0 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def pulse_svg(width="100%", height=26, color1="#9BC9A4", color2="#F3E4C2"):
    """A small ECG / vital-sign trace used as the app's signature motif."""
    gid = "pulseGrad"
    return f"""
    <svg width="{width}" height="{height}" viewBox="0 0 400 40" preserveAspectRatio="none"
         xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" style="stop-color:{color1}"/>
                <stop offset="55%" style="stop-color:#FFFFFF"/>
                <stop offset="100%" style="stop-color:{color2}"/>
            </linearGradient>
        </defs>
        <path d="M0 20 H150 L162 20 L172 4 L182 36 L192 20 L204 20 H400"
              fill="none" stroke="url(#{gid})" stroke-width="2.5"
              stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """


def badge(text, tone="green"):
    return f'<span class="hms-badge hms-badge-{tone}">{text}</span>'


# =================================================================
# AI ASSISTANT (Groq API) — drafts suggestions, humans stay in control
# =================================================================

def get_ai_client():
    try:
        from groq import Groq
    except ImportError:
        return None, "The `groq` package isn't installed. Add it to requirements.txt."
    api_key = st.secrets.get("GROQ_API_KEY", None) if hasattr(st, "secrets") else None
    if not api_key:
        return None, "No GROQ_API_KEY found in Streamlit secrets."
    return Groq(api_key=api_key), None


def ask_ai(system_prompt, user_prompt, max_tokens=500):
    client, err = get_ai_client()
    if client is None:
        return None, err
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return response.choices[0].message.content.strip(), None
    except Exception as e:
        return None, f"AI request failed: {e}"


def ai_triage_widget():
    """Reception-facing: suggests urgency + department from a symptom description."""
    with st.expander("🤖 AI Triage Helper — draft an urgency check (not a diagnosis)"):
        symptoms = st.text_area(
            "Describe symptoms in plain language", key="triage_symptoms",
            placeholder="e.g. sudden chest pain, shortness of breath, started 20 minutes ago",
        )
        if st.button("Check urgency", key="triage_btn"):
            if not symptoms.strip():
                st.warning("Describe the symptoms first.")
            else:
                with st.spinner("Thinking..."):
                    result, err = ask_ai(
                        system_prompt=(
                            "You are a hospital reception triage helper. Given a plain-language "
                            "symptom description, respond in 3 short lines: "
                            "1) Urgency: Routine / Urgent / Emergency. "
                            "2) Suggested department. "
                            "3) One line of reasoning. "
                            "You are NOT diagnosing — always add a final line telling staff to "
                            "confirm with a doctor. Be concise."
                        ),
                        user_prompt=symptoms,
                        max_tokens=200,
                    )
                if err:
                    st.error(err)
                else:
                    st.info(result)


def ai_clinical_assistant(patient_name, illness, observation_text):
    """Doctor-facing: drafts test/medicine suggestions from notes. Doctor must review & edit."""
    st.markdown("##### 🤖 AI Assistant — draft suggestions for review")
    st.caption("This drafts ideas only. Always review and edit before saving — never auto-applied.")
    if st.button("Suggest tests & medicines", key=f"ai_suggest_{patient_name}"):
        if not observation_text.strip():
            st.warning("Write at least a brief observation first.")
        else:
            with st.spinner("Drafting suggestions..."):
                result, err = ask_ai(
                    system_prompt=(
                        "You are a clinical documentation assistant helping a doctor draft "
                        "notes. Given the patient's illness and the doctor's observation, "
                        "suggest: 1) possible tests to consider, 2) possible medicine "
                        "categories to consider. Keep it to 4 short bullet points total. "
                        "This is a DRAFT for a licensed doctor to review, edit, and confirm — "
                        "never state this as a final decision."
                    ),
                    user_prompt=f"Illness: {illness}\nDoctor's observation: {observation_text}",
                    max_tokens=250,
                )
            if err:
                st.error(err)
            else:
                st.info(result)


def ai_discharge_summary(patient_name, illness, observation_text, medicines):
    """Generates a patient-friendly discharge summary draft from clinical notes."""
    if st.button("Generate discharge summary draft", key=f"ai_discharge_{patient_name}"):
        with st.spinner("Writing summary..."):
            result, err = ask_ai(
                system_prompt=(
                    "Turn the clinical notes into a short, warm, plain-language discharge "
                    "summary a patient can understand. 4-6 sentences. No medical jargon. "
                    "End with a line reminding them to follow up with their doctor if symptoms "
                    "return."
                ),
                user_prompt=(
                    f"Patient: {patient_name}\nIllness: {illness}\n"
                    f"Doctor's notes: {observation_text}\nMedicines given: {medicines}"
                ),
                max_tokens=300,
            )
        if err:
            st.error(err)
        else:
            st.success(result)


# =================================================================
# DATABASE SETUP (same schema/logic as the original console app)
# =================================================================

def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():
    with closing(get_connection()) as conn:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                name TEXT NOT NULL,
                on_leave INTEGER DEFAULT 0,
                specialty TEXT
            )
        """)
        # Migration: add specialty column if this is an existing DB from before
        cur.execute("PRAGMA table_info(users)")
        existing_cols = {row[1] for row in cur.fetchall()}
        if "specialty" not in existing_cols:
            cur.execute("ALTER TABLE users ADD COLUMN specialty TEXT")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS visits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                illness TEXT NOT NULL,
                doctor_id INTEGER,
                status TEXT DEFAULT 'waiting'
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS billing (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                status TEXT DEFAULT 'pending'
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                visit_id INTEGER NOT NULL,
                observation TEXT,
                tests TEXT,
                medicines TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS admissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                floor_no INTEGER NOT NULL,
                room_no INTEGER,
                bed_no INTEGER,
                nurse_id INTEGER,
                status TEXT DEFAULT 'pending'
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS medications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                admission_id INTEGER NOT NULL,
                medicine_name TEXT NOT NULL,
                times_to_give INTEGER NOT NULL,
                times_given INTEGER DEFAULT 0
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS beds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                floor_no INTEGER NOT NULL,
                room_no INTEGER NOT NULL,
                bed_no INTEGER NOT NULL,
                occupied INTEGER DEFAULT 0,
                admission_id INTEGER
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS leaves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                from_date TEXT NOT NULL,
                to_date TEXT NOT NULL,
                reason TEXT,
                status TEXT DEFAULT 'pending'
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS medicines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category TEXT,
                stock INTEGER DEFAULT 0
            )
        """)
        conn.commit()

def seed_data():
    with closing(get_connection()) as conn:
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM beds")
        if cur.fetchone()[0] == 0:
            for floor in range(1, 6):
                for room in range(1, 11):
                    for bed in range(1, 3):
                        cur.execute(
                            "INSERT INTO beds (floor_no, room_no, bed_no) VALUES (?,?,?)",
                            (floor, room, bed),
                        )

        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            default_users = [
                ("admin", "admin123", "admin", "System Admin", None),
                ("reception", "reception123", "reception", "Front Desk", None),
                ("floor", "floor123", "floor", "Floor Manager", None),
                ("nurse1", "nurse123", "nurse", "Nurse Priya Rao", None),
            ]
            cur.executemany(
                "INSERT INTO users (username, password, role, name, specialty) VALUES (?,?,?,?,?)",
                default_users,
            )

            default_doctors = [
                ("doctor1", "doctor123", "Dr. Asha Mehta", "Cardiology"),
                ("doctor2", "doctor123", "Dr. Ravi Kapoor", "Orthopedics"),
                ("doctor3", "doctor123", "Dr. Neha Sharma", "Pediatrics"),
                ("doctor4", "doctor123", "Dr. Vikram Singh", "Neurology"),
                ("doctor5", "doctor123", "Dr. Priya Nair", "Dermatology"),
                ("doctor6", "doctor123", "Dr. Arjun Rao", "General Medicine"),
                ("doctor7", "doctor123", "Dr. Kavita Iyer", "Gynecology"),
                ("doctor8", "doctor123", "Dr. Sameer Khan", "ENT"),
                ("doctor9", "doctor123", "Dr. Anjali Gupta", "Psychiatry"),
                ("doctor10", "doctor123", "Dr. Rohan Desai", "Ophthalmology"),
            ]
            cur.executemany(
                "INSERT INTO users (username, password, role, name, specialty) VALUES (?,?, 'doctor', ?, ?)",
                default_doctors,
            )

        cur.execute("SELECT COUNT(*) FROM medicines")
        if cur.fetchone()[0] == 0:
            default_medicines = [
                ("Paracetamol", "Painkiller / Fever", 500),
                ("Ibuprofen", "Painkiller / Anti-inflammatory", 300),
                ("Amoxicillin",, "Antibiotic", 200),
                ("Azithromycin", "Antibiotic", 150),
                ("Cetirizine", "Antihistamine / Allergy", 250),
                ("Omeprazole", "Antacid", 300),
                ("Metformin", "Diabetes", 400),
                ("Amlodipine", "Blood Pressure", 350),
                ("Salbutamol Inhaler", "Respiratory", 100),
                ("Insulin", "Diabetes", 80),
            ]
            cur.executemany(
                "INSERT INTO medicines (name, category, stock) VALUES (?,?,?)",
                default_medicines,
            )

        cur.execute("SELECT COUNT(*) FROM patients")
        if cur.fetchone()[0] == 0:
            cur.execute("SELECT id FROM users WHERE role = 'doctor' ORDER BY id")
            doctor_ids = [r[0] for r in cur.fetchall()]
            sample_patients = [
                ("Rohit Verma", "9876543210", "Chest pain"),
                ("Sneha Joshi", "9876543211", "Fracture in left arm"),
                ("Aarav Malhotra", "9876543212", "High fever"),
                ("Meera Pillai", "9876543213", "Skin rash"),
                ("Karan Chawla", "9876543214", "Migraine"),
                ("Ishita Bose", "9876543215", "Pregnancy checkup"),
                ("Devansh Rathi", "9876543216", "Ear infection"),
                ("Ananya Reddy", "9876543217", "Anxiety and stress"),
            ]
            for i, (name, phone, illness) in enumerate(sample_patients):
                cur.execute("INSERT INTO patients (name, phone) VALUES (?,?)", (name, phone))
                patient_id = cur.lastrowid
                doctor_id = doctor_ids[i % len(doctor_ids)] if doctor_ids else None
                cur.execute(
                    "INSERT INTO visits (patient_id, illness, doctor_id, status) VALUES (?,?,?, 'waiting')",
                    (patient_id, illness, doctor_id),
                )

            cur.execute("SELECT id FROM users WHERE role = 'nurse'")
            nurse_ids = [r[0] for r in cur.fetchall()]

            admit_indices = [0, 2]
            for idx in admit_indices:
                patient_id = idx + 1
                doctor_id = doctor_ids[idx % len(doctor_ids)] if doctor_ids else None
                floor_no = (idx % 5) + 1
                cur.execute(
                    "SELECT room_no, bed_no, id FROM beds WHERE floor_no = ? AND occupied = 0 LIMIT 1",
                    (floor_no,),
                )
                bed = cur.fetchone()
                if bed and doctor_id:
                    room_no, bed_no, bed_id = bed
                    nurse_id = nurse_ids[0] if nurse_ids else None
                    cur.execute(
                        "INSERT INTO admissions (patient_id, doctor_id, floor_no, room_no, bed_no, nurse_id, status) "
                        "VALUES (?,?,?,?,?,?, 'admitted')",
                        (patient_id, doctor_id, floor_no, room_no, bed_no, nurse_id),
                    )
                    admission_id = cur.lastrowid
                    cur.execute(
                        "UPDATE beds SET occupied = 1, admission_id = ? WHERE id = ?",
                        (admission_id, bed_id),
                    )
                    cur.execute(
                        "INSERT INTO medications (admission_id, medicine_name, times_to_give) VALUES (?,?,?)",
                        (admission_id, "Paracetamol", 3),
                    )

        conn.commit()




create_tables()
seed_data()


# =================================================================
# SESSION STATE HELPERS
# =================================================================

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "landing"  # "landing" -> "login" -> app


def do_login(username, password):
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        row = cur.fetchone()
    if row is None:
        return None
    return {
        "id": row[0],
        "username": row[1],
        "role": row[3],
        "name": row[4],
        "on_leave": row[5],
        "specialty": row[6] if len(row) > 6 else None,
    }


def logout():
    st.session_state.user = None
    st.session_state.page = "landing"
    st.rerun()


def banner(title, subtitle, eyebrow="Hospital Management System"):
    st.markdown(
        f"""<div class="hms-banner">
            <div class="hms-eyebrow">{eyebrow}</div>
            <h2>{title}</h2>
            <p>{subtitle}</p>
            <div class="hms-pulse">{pulse_svg(height=20)}</div>
        </div>""",
        unsafe_allow_html=True,
    )


# =================================================================
# LANDING PAGE
# =================================================================

def landing_page():
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users WHERE role = 'doctor'")
        n_doctors = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM beds")
        n_beds = cur.fetchone()[0]
        cur.execute("SELECT COUNT(DISTINCT specialty) FROM users WHERE role='doctor' AND specialty IS NOT NULL")
        n_specialties = cur.fetchone()[0]

    # ---- top nav ----
    nav_l, nav_r = st.columns([3, 1])
    with nav_l:
        st.markdown(
            """
            <div class="hms-nav-brand">
                🏥 MediFlow <span class="hms-nav-tag">Hospital OS</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with nav_r:
        if st.button("Sign in →", key="nav_login_btn", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

    # ---- hero ----
    st.markdown(
        f"""
        <div class="hms-hero-wrap">
            <div class="hms-eyebrow">Est. for calmer wards</div>
            <h1>One calm dashboard for every ward, every role.</h1>
            <p class="hms-hero-sub">
                Registration, doctor queues, bed assignments, medication rounds,
                billing and staff leave — all connected in a single, easy-to-read
                hospital operating system. Built for reception, doctors, floor
                managers, nurses and admins alike.
            </p>
            <div style="margin-top:1.4rem;">{pulse_svg(height=28, color1="#9BC9A4", color2="#F3E4C2")}</div>
            <div class="hms-stat-row">
                <div>
                    <div class="hms-stat-num">{n_beds}</div>
                    <div class="hms-stat-label">Beds tracked</div>
                </div>
                <div>
                    <div class="hms-stat-num">{n_doctors}</div>
                    <div class="hms-stat-label">Doctors on roster</div>
                </div>
                <div>
                    <div class="hms-stat-num">{n_specialties}</div>
                    <div class="hms-stat-label">Specialties covered</div>
                </div>
                <div>
                    <div class="hms-stat-num">5</div>
                    <div class="hms-stat-label">Role-based views</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cta_l, cta_r, _ = st.columns([1, 1, 2])
    with cta_l:
        if st.button("Get started →", key="hero_cta_btn", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()
    with cta_r:
        with st.expander("Demo logins"):
            st.markdown(
                """
| Role | User ID | Password |
|---|---|---|
| Admin | `admin` | `admin123` |
| Reception | `reception` | `reception123` |
| Floor manager | `floor` | `floor123` |
| Doctor | `doctor1` | `doctor123` |
| Nurse | `nurse1` | `nurse123` |
                """
            )

    st.write("")
    st.markdown("### Everything one hospital floor needs")
    st.caption("A single system, tuned to what each role actually does day to day.")

    features = [
        ("🛎️", "Reception", "Register new patients, route them to the right doctor, and manage billing in a few clicks."),
        ("🩺", "Doctor queues", "See assigned patients, log observations, prescribe medicines, and admit patients when needed."),
        ("🏢", "Bed & floor control", "Live view of bed occupancy across every floor, with nurse assignment and discharge in one place."),
        ("💉", "Medication rounds", "Nurses track exactly which doses have been given and what's still due for each patient."),
        ("🧾", "Billing, built in", "Simple, transparent billing records tied directly to each patient's visit history."),
        ("🤖", "AI drafting assist", "Optional AI-drafted triage notes, clinical suggestions and discharge summaries — staff always review and confirm."),
    ]
    for row_start in range(0, len(features), 3):
        cols = st.columns(3)
        for col, (icon, title, desc) in zip(cols, features[row_start:row_start + 3]):
            with col:
                feature_html = (
                    f'<div class="hms-feature-card">'
                    f'<div class="hms-feature-icon">{icon}</div>'
                    f'<h4>{title}</h4>'
                    f'<p>{desc}</p>'
                    f'</div>'
                )
                st.markdown(feature_html, unsafe_allow_html=True)

    st.write("")
    st.markdown("### Built around five roles")
    roles = [
        ("🛡️", "Admin", "Staff, medicines & leave"),
        ("🛎️", "Reception", "Patients & billing"),
        ("🩺", "Doctor", "Diagnosis & admission"),
        ("🏢", "Floor manager", "Beds & nurses"),
        ("💉", "Nurse", "Medication rounds"),
    ]
    role_cards = "".join(
        f'<div class="hms-role-card">'
        f'<div class="hms-role-icon">{icon}</div>'
        f'<div class="hms-role-name">{name}</div>'
        f'<div class="hms-role-desc">{desc}</div>'
        f'</div>'
        for icon, name, desc in roles
    )
    role_html = f'<div class="hms-role-strip">{role_cards}</div>'
    st.markdown(role_html, unsafe_allow_html=True)

    # ---- final CTA ----
    st.markdown(
        """
        <div class="hms-cta-wrap">
            <h2>Ready to see it in action?</h2>
            <p>Sign in with any demo account below and explore your role's dashboard.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    _, mid, _ = st.columns([1.3, 1, 1.3])
    with mid:
        st.write("")
        if st.button("Sign in now →", key="bottom_cta_btn", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

    st.markdown(
        '<div class="hms-footer">🏥 MediFlow — Hospital Management System</div>',
        unsafe_allow_html=True,
    )


# =================================================================
# LOGIN SCREEN
# =================================================================

def login_screen():
    top_l, top_r = st.columns([4, 1])
    with top_r:
        if st.button("← Back", key="back_to_landing_btn", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()

    st.write("")
    left, right = st.columns([1.05, 1], gap="large")

    with left:
        st.markdown(
            f"""
            <div class="hms-login-hero">
                <div class="hms-eyebrow">Est. for calmer wards</div>
                <h1>One dashboard for<br>every ward, every role.</h1>
                <p>Registration, doctor queues, bed assignments, medication
                rounds and staff leave — all in one calm, connected place.</p>
                <div style="margin: 1.3rem 0 1.5rem;">{pulse_svg(height=30, color1="#9BC9A4", color2="#F3E4C2")}</div>
                <div>
                    <span class="hms-role-chip">🛎️ Reception</span>
                    <span class="hms-role-chip">🩺 Doctor</span>
                    <span class="hms-role-chip">🏢 Floor</span>
                    <span class="hms-role-chip">💉 Nurse</span>
                    <span class="hms-role-chip">🛡️ Admin</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            '<div style="text-transform:uppercase;letter-spacing:0.14em;font-size:0.72rem;'
            'font-weight:700;color:var(--gold);margin-bottom:0.1rem;">Welcome back</div>',
            unsafe_allow_html=True,
        )
        st.markdown("### Sign in to your account")

        with st.form("login_form"):
            username = st.text_input("User ID", placeholder="e.g. doctor1")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Log in", use_container_width=True)

        if submitted:
            user = do_login(username.strip(), password.strip())
            if user is None:
                st.error("Invalid user ID or password. Please try again.")
            else:
                st.session_state.user = user
                st.session_state.page = "app"
                st.rerun()

        with st.expander("Need a demo login?"):
            st.markdown(
                """
| Role | User ID | Password |
|---|---|---|
| Admin | `admin` | `admin123` |
| Reception | `reception` | `reception123` |
| Floor manager | `floor` | `floor123` |
| Doctor | `doctor1` | `doctor123` |
| Nurse | `nurse1` | `nurse123` |
                """
            )


# =================================================================
# SHARED HELPERS
# =================================================================

def list_available_doctors(cur):
    cur.execute(
        "SELECT id, name, specialty FROM users WHERE role = 'doctor' AND on_leave = 0 ORDER BY specialty, name"
    )
    return cur.fetchall()


def doctor_picker(cur, key):
    doctors = list_available_doctors(cur)
    if not doctors:
        st.warning("No doctors are available right now.")
        return None

    specialties = sorted({spec for _, _, spec in doctors if spec})
    specialty_choice = st.selectbox(
        "Filter by specialty", ["All specialties"] + specialties, key=f"{key}_spec"
    )
    filtered = doctors if specialty_choice == "All specialties" else [
        d for d in doctors if d[2] == specialty_choice
    ]
    if not filtered:
        st.warning("No doctors available in that specialty.")
        return None

    options = {
        f"{name} — {spec or 'General'} (ID {doc_id})": doc_id
        for doc_id, name, spec in filtered
    }
    choice = st.selectbox("Assign to doctor", list(options.keys()), key=key)
    return options[choice]


# =================================================================
# RECEPTION FEATURES
# =================================================================

def reception_register_patient():
    st.subheader("Register a New Patient")
    ai_triage_widget()
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        with st.form("register_patient_form"):
            name = st.text_input("Patient name")
            phone = st.text_input("Phone number")
            illness = st.text_input("Illness")
            doctor_id = doctor_picker(cur, key="reg_doc")
            submitted = st.form_submit_button("Register patient")

        if submitted:
            if not name or not phone or not illness:
                st.error("Please fill in all fields.")
            elif doctor_id is None:
                st.error("No doctor available to assign.")
            else:
                cur.execute("INSERT INTO patients (name, phone) VALUES (?,?)", (name, phone))
                patient_id = cur.lastrowid
                cur.execute(
                    "INSERT INTO visits (patient_id, illness, doctor_id, status) VALUES (?,?,?, 'waiting')",
                    (patient_id, illness, doctor_id),
                )
                conn.commit()
                st.success(f"Patient '{name}' registered and sent to the doctor's queue.")


def reception_update_billing():
    st.subheader("Update Billing")
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, phone FROM patients")
        patients = cur.fetchall()

        if not patients:
            st.info("No patients found.")
            return

        options = {f"{name} ({phone}) — ID {pid}": pid for pid, name, phone in patients}
        with st.form("billing_form"):
            choice = st.selectbox("Patient", list(options.keys()))
            amount = st.number_input("Bill amount", min_value=0.0, step=100.0)
            status = st.radio("Status", ["pending", "paid"], horizontal=True)
            submitted = st.form_submit_button("Save billing")

        if submitted:
            patient_id = options[choice]
            cur.execute(
                "INSERT INTO billing (patient_id, amount, status) VALUES (?,?,?)",
                (patient_id, amount, status),
            )
            conn.commit()
            st.success("Billing updated.")

        cur.execute("""
            SELECT b.id, p.name, b.amount, b.status FROM billing b
            JOIN patients p ON p.id = b.patient_id ORDER BY b.id DESC
        """)
        rows = cur.fetchall()
        if rows:
            st.markdown("**Recent billing records**")
            st.dataframe(
                [{"Bill ID": r[0], "Patient": r[1], "Amount": r[2], "Status": r[3]} for r in rows],
                use_container_width=True, hide_index=True,
            )


def reception_access_old_patient():
    st.subheader("Access Old Patient")
    search_term = st.text_input("Search by name or phone")

    with closing(get_connection()) as conn:
        cur = conn.cursor()
        if not search_term:
            st.info("Type a name or phone number to search.")
            return

        cur.execute(
            "SELECT id, name, phone FROM patients WHERE name LIKE ? OR phone LIKE ?",
            (f"%{search_term}%", f"%{search_term}%"),
        )
        matches = cur.fetchall()

        if not matches:
            st.warning("No matching patients found.")
            return

        options = {f"{name} ({phone}) — ID {pid}": pid for pid, name, phone in matches}
        choice = st.selectbox("Matching patients", list(options.keys()))
        patient_id = options[choice]

        cur.execute("SELECT illness, status FROM visits WHERE patient_id = ?", (patient_id,))
        history = cur.fetchall()
        st.markdown("**Previous visits**")
        if history:
            st.dataframe(
                [{"Illness": h[0], "Status": h[1]} for h in history],
                use_container_width=True, hide_index=True,
            )
        else:
            st.caption("(no previous visits)")

        with st.expander("Add a new illness / book a new appointment"):
            with st.form("new_visit_form"):
                illness = st.text_input("New illness")
                doctor_id = doctor_picker(cur, key="old_pt_doc")
                submitted = st.form_submit_button("Book appointment")
            if submitted:
                if not illness:
                    st.error("Please enter the illness.")
                elif doctor_id is None:
                    st.error("No doctor available to assign.")
                else:
                    cur.execute(
                        "INSERT INTO visits (patient_id, illness, doctor_id, status) VALUES (?,?,?, 'waiting')",
                        (patient_id, illness, doctor_id),
                    )
                    conn.commit()
                    st.success("New appointment booked and sent to the doctor.")


def reception_menu(user):
    banner("Reception Desk", f"Signed in as {user['name']}")
    tab1, tab2, tab3 = st.tabs(["Register patient", "Update billing", "Access old patient"])
    with tab1:
        reception_register_patient()
    with tab2:
        reception_update_billing()
    with tab3:
        reception_access_old_patient()


# =================================================================
# DOCTOR FEATURES
# =================================================================

def doctor_view_patients(user):
    st.subheader("Your Patients")
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT v.id, p.id, p.name, v.illness, v.status
            FROM visits v JOIN patients p ON p.id = v.patient_id
            WHERE v.doctor_id = ?
        """, (user["id"],))
        rows = cur.fetchall()

        if not rows:
            st.info("No patients assigned to you yet.")
            return

        st.dataframe(
            [{"Visit ID": r[0], "Patient": r[2], "Illness": r[3], "Status": r[4]} for r in rows],
            use_container_width=True, hide_index=True,
        )

        options = {f"Visit {v}: {name} - {illness} ({status})": v for v, pid, name, illness, status in rows}
        choice = st.selectbox("Select a visit to add observations", list(options.keys()))
        visit_id = options[choice]
        visit_illness = next(illness for v, pid, name, illness, status in rows if v == visit_id)
        visit_patient = next(name for v, pid, name, illness, status in rows if v == visit_id)

        obs_key = f"obs_text_{visit_id}"
        observation = st.text_area("Observations", key=obs_key)

        ai_clinical_assistant(visit_patient, visit_illness, st.session_state.get(obs_key, ""))

        cur.execute("SELECT name FROM medicines ORDER BY category, name")
        medicine_names = [r[0] for r in cur.fetchall()]

        with st.form("observation_form"):
            tests = st.text_input("Tests to be performed")
            medicines_selected = st.multiselect("Medicine(s) to be given", medicine_names)
            submitted = st.form_submit_button("Save observation")

        if submitted:
            medicines = ", ".join(medicines_selected)
            cur.execute(
                "INSERT INTO observations (visit_id, observation, tests, medicines) VALUES (?,?,?,?)",
                (visit_id, st.session_state.get(obs_key, ""), tests, medicines),
            )
            cur.execute("UPDATE visits SET status = 'seen' WHERE id = ?", (visit_id,))
            conn.commit()
            st.success("Observation saved.")


def doctor_admit_patient(user):
    st.subheader("Admit a Patient")
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT v.id, p.id, p.name
            FROM visits v JOIN patients p ON p.id = v.patient_id
            WHERE v.doctor_id = ?
        """, (user["id"],))
        rows = cur.fetchall()

        if not rows:
            st.info("You have no patients to admit.")
            return

        options = {f"{name} (visit {v})": (v, pid) for v, pid, name in rows}
        choice = st.selectbox("Patient to admit", list(options.keys()))
        visit_id, patient_id = options[choice]
        floor_no = st.selectbox("Floor number", [1, 2, 3, 4, 5])

        cur.execute("SELECT name FROM medicines ORDER BY category, name")
        medicine_names = [r[0] for r in cur.fetchall()]

        st.markdown("**Medications** (add as many rows as needed)")
        if not medicine_names:
            st.warning("No medicines in the catalog yet. Ask an admin to add some first.")
        med_count = st.number_input("How many medicines to prescribe?", min_value=0, max_value=10, value=1, step=1)
        meds = []
        for i in range(int(med_count)):
            c1, c2 = st.columns([2, 1])
            with c1:
                mname = st.selectbox(
                    f"Medicine {i + 1} name",
                    medicine_names if medicine_names else ["-- no medicines available --"],
                    key=f"med_name_{i}",
                )
            with c2:
                mtimes = st.number_input(f"Times/day {i + 1}", min_value=1, value=1, step=1, key=f"med_times_{i}")
            if mname and medicine_names:
                meds.append((mname, mtimes))

        if st.button("Admit patient"):
            cur.execute(
                "INSERT INTO admissions (patient_id, doctor_id, floor_no, status) VALUES (?,?,?, 'pending')",
                (patient_id, user["id"], floor_no),
            )
            admission_id = cur.lastrowid
            for mname, mtimes in meds:
                cur.execute(
                    "INSERT INTO medications (admission_id, medicine_name, times_to_give) VALUES (?,?,?)",
                    (admission_id, mname, mtimes),
                )
            conn.commit()
            st.success(f"Admission request sent to Floor {floor_no}.")


def apply_leave(user):
    st.subheader("Apply for Leave / Holiday")
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        with st.form("leave_form"):
            from_date = st.date_input("From date")
            to_date = st.date_input("To date")
            reason = st.text_input("Reason")
            submitted = st.form_submit_button("Submit request")

        if submitted:
            cur.execute(
                "INSERT INTO leaves (user_id, from_date, to_date, reason) VALUES (?,?,?,?)",
                (user["id"], str(from_date), str(to_date), reason),
            )
            conn.commit()
            st.success("Leave request submitted.")

        cur.execute(
            "SELECT from_date, to_date, status FROM leaves WHERE user_id = ?", (user["id"],)
        )
        rows = cur.fetchall()
        if rows:
            st.markdown("**Your leave requests**")
            st.dataframe(
                [{"From": r[0], "To": r[1], "Status": r[2]} for r in rows],
                use_container_width=True, hide_index=True,
            )


def doctor_menu(user):
    subtitle = f"Signed in as {user['name']}"
    if user.get("specialty"):
        subtitle += f" · {user['specialty']}"
    banner("Doctor Dashboard", subtitle)
    tab1, tab2, tab3, tab4 = st.tabs(["My patients", "Admit a patient", "Apply for leave", "Medicine inventory"])
    with tab1:
        doctor_view_patients(user)
    with tab2:
        doctor_admit_patient(user)
    with tab3:
        apply_leave(user)
    with tab4:
        admin_medicine_list()


# =================================================================
# FLOOR MANAGER FEATURES
# =================================================================

def floor_assign_room_and_bed():
    st.subheader("Pending Admissions — Assign Room / Bed")
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT a.id, p.name, a.floor_no
            FROM admissions a JOIN patients p ON p.id = a.patient_id
            WHERE a.status = 'pending'
        """)
        pending = cur.fetchall()

        if not pending:
            st.info("No pending admissions.")
            return

        options = {f"{name} -> Floor {floor_no} (admission {aid})": (aid, floor_no) for aid, name, floor_no in pending}
        choice = st.selectbox("Admission", list(options.keys()))
        admission_id, floor_no = options[choice]

        cur.execute(
            "SELECT room_no, bed_no FROM beds WHERE floor_no = ? AND occupied = 0", (floor_no,)
        )
        free_beds = cur.fetchall()
        if not free_beds:
            st.warning(f"No free beds on Floor {floor_no}.")
            return

        bed_options = {f"Room {r}, Bed {b}": (r, b) for r, b in free_beds}
        bed_choice = st.selectbox("Free bed", list(bed_options.keys()))
        room_no, bed_no = bed_options[bed_choice]

        if st.button("Assign bed"):
            cur.execute(
                "UPDATE admissions SET room_no = ?, bed_no = ?, status = 'admitted' WHERE id = ?",
                (room_no, bed_no, admission_id),
            )
            cur.execute(
                "UPDATE beds SET occupied = 1, admission_id = ? WHERE floor_no = ? AND room_no = ? AND bed_no = ?",
                (admission_id, floor_no, room_no, bed_no),
            )
            conn.commit()
            st.success(f"Patient admitted to Floor {floor_no}, Room {room_no}, Bed {bed_no}.")


def floor_assign_nurse():
    st.subheader("Assign Nurse")
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT a.id, p.name
            FROM admissions a JOIN patients p ON p.id = a.patient_id
            WHERE a.status = 'admitted' AND a.nurse_id IS NULL
        """)
        waiting = cur.fetchall()

        if not waiting:
            st.info("Every admitted patient already has a nurse.")
            return

        options = {f"{name} (admission {aid})": aid for aid, name in waiting}
        choice = st.selectbox("Patient waiting for a nurse", list(options.keys()))
        admission_id = options[choice]

        cur.execute("SELECT id, name, on_leave FROM users WHERE role = 'nurse'")
        nurses = cur.fetchall()

        rows = []
        nurse_options = {}
        for nurse_id, name, on_leave in nurses:
            cur.execute(
                "SELECT COUNT(*) FROM admissions WHERE nurse_id = ? AND status = 'admitted'",
                (nurse_id,),
            )
            count = cur.fetchone()[0]
            leave_note = "ON LEAVE" if on_leave else "Available"
            rows.append({"Nurse": name, "Patients": f"{count}/4", "Status": leave_note})
            if not on_leave and count < 4:
                nurse_options[f"{name} ({count}/4 patients)"] = nurse_id

        st.dataframe(rows, use_container_width=True, hide_index=True)

        if not nurse_options:
            st.warning("No nurse is currently available (all on leave or full).")
            return

        nurse_choice = st.selectbox("Assign nurse", list(nurse_options.keys()))
        if st.button("Assign nurse"):
            nurse_id = nurse_options[nurse_choice]
            cur.execute("UPDATE admissions SET nurse_id = ? WHERE id = ?", (nurse_id, admission_id))
            conn.commit()
            st.success("Nurse assigned.")


def floor_discharge_patient():
    st.subheader("Discharge a Patient")
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT a.id, p.name, a.floor_no, a.room_no, a.bed_no
            FROM admissions a JOIN patients p ON p.id = a.patient_id
            WHERE a.status = 'admitted'
        """)
        admitted = cur.fetchall()

        if not admitted:
            st.info("No admitted patients.")
            return

        options = {
            f"{name} - Floor {f}, Room {r}, Bed {b} (admission {aid})": aid
            for aid, name, f, r, b in admitted
        }
        choice = st.selectbox("Patient to discharge", list(options.keys()))
        admission_id = options[choice]
        patient_name = next(name for aid, name, f, r, b in admitted if aid == admission_id)

        cur.execute("SELECT patient_id FROM admissions WHERE id = ?", (admission_id,))
        patient_id = cur.fetchone()[0]
        cur.execute(
            "SELECT o.observation, v.illness FROM observations o "
            "JOIN visits v ON v.id = o.visit_id WHERE v.patient_id = ? ORDER BY o.id DESC LIMIT 1",
            (patient_id,),
        )
        note_row = cur.fetchone()
        cur.execute(
            "SELECT medicine_name FROM medications WHERE admission_id = ?", (admission_id,)
        )
        meds = ", ".join(m[0] for m in cur.fetchall()) or "none recorded"

        if note_row:
            ai_discharge_summary(patient_name, note_row[1], note_row[0], meds)

        if st.button("Discharge patient"):
            cur.execute("UPDATE admissions SET status = 'discharged' WHERE id = ?", (admission_id,))
            cur.execute("UPDATE beds SET occupied = 0, admission_id = NULL WHERE admission_id = ?", (admission_id,))
            conn.commit()
            st.success("Patient discharged and bed freed up.")


def floor_overview():
    st.subheader("Floor Overview")
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cols = st.columns(5)
        for i, floor_no in enumerate(range(1, 6)):
            cur.execute("SELECT COUNT(*) FROM beds WHERE floor_no = ?", (floor_no,))
            total = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM beds WHERE floor_no = ? AND occupied = 1", (floor_no,))
            occupied = cur.fetchone()[0]
            with cols[i]:
                st.metric(f"Floor {floor_no}", f"{occupied}/{total} beds")


def floor_menu(user):
    banner("Reception Floor", f"Signed in as {user['name']}")
    floor_overview()
    st.divider()
    tab1, tab2, tab3 = st.tabs(["Assign room/bed", "Assign nurse", "Discharge patient"])
    with tab1:
        floor_assign_room_and_bed()
    with tab2:
        floor_assign_nurse()
    with tab3:
        floor_discharge_patient()


# =================================================================
# NURSE FEATURES
# =================================================================

def nurse_view_patients(user):
    st.subheader("Patients Assigned to Me")
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT a.id, p.name, a.floor_no, a.room_no, a.bed_no
            FROM admissions a JOIN patients p ON p.id = a.patient_id
            WHERE a.nurse_id = ? AND a.status = 'admitted'
        """, (user["id"],))
        patients = cur.fetchall()

        if not patients:
            st.info("No patients assigned to you yet.")
            return

        st.dataframe(
            [{"Admission": a, "Patient": name, "Floor": f, "Room": r, "Bed": b} for a, name, f, r, b in patients],
            use_container_width=True, hide_index=True,
        )

        options = {f"{name} (admission {aid})": aid for aid, name, f, r, b in patients}
        choice = st.selectbox("View medications for", list(options.keys()))
        admission_id = options[choice]

        cur.execute(
            "SELECT id, medicine_name, times_to_give, times_given FROM medications WHERE admission_id = ?",
            (admission_id,),
        )
        meds = cur.fetchall()

        if not meds:
            st.caption("No medications ordered for this patient.")
            return

        st.dataframe(
            [{"Medicine": m[1], "Given": f"{m[3]}/{m[2]}"} for m in meds],
            use_container_width=True, hide_index=True,
        )

        med_options = {f"{m[1]} ({m[3]}/{m[2]})": m[0] for m in meds}
        med_choice = st.selectbox("Mark a dose given", list(med_options.keys()))
        if st.button("Record dose"):
            med_id = med_options[med_choice]
            match = next((m for m in meds if m[0] == med_id), None)
            new_given = match[3] + 1
            if new_given > match[2]:
                st.warning("This medicine has already been given the full number of times today.")
            else:
                cur.execute("UPDATE medications SET times_given = ? WHERE id = ?", (new_given, med_id))
                conn.commit()
                st.success(f"Marked one more dose given ({new_given}/{match[2]}).")


def nurse_menu(user):
    banner("Nurse Dashboard", f"Signed in as {user['name']}")
    tab1, tab2 = st.tabs(["My patients", "Apply for leave"])
    with tab1:
        nurse_view_patients(user)
    with tab2:
        apply_leave(user)


# =================================================================
# ADMIN FEATURES
# =================================================================

def admin_add_staff():
    st.subheader("Add Doctor / Nurse")
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        specialty_options = [
            "Cardiology", "Orthopedics", "Pediatrics", "Neurology",
            "Dermatology", "General Medicine", "Gynecology", "ENT",
            "Psychiatry", "Ophthalmology", "Oncology", "Urology", "Other",
        ]

        role = st.radio("Role", ["doctor", "nurse"], horizontal=True, key="add_staff_role")
        specialty = None
        specialty_custom = ""
        if role == "doctor":
            specialty = st.selectbox("Specialty", specialty_options, key="add_staff_specialty")
            if specialty == "Other":
                specialty_custom = st.text_input("Enter specialty", key="add_staff_specialty_custom")

        with st.form("add_staff_form"):
            name = st.text_input("Full name")
            username = st.text_input("User ID")
            password = st.text_input("Password")
            submitted = st.form_submit_button("Create account")

        if submitted:
            final_specialty = (specialty_custom.strip() if specialty == "Other" else specialty) if role == "doctor" else None
            if not name or not username or not password:
                st.error("Please fill in all fields.")
            elif role == "doctor" and not final_specialty:
                st.error("Please enter the doctor's specialty.")
            else:
                cur.execute("SELECT id FROM users WHERE username = ?", (username,))
                if cur.fetchone() is not None:
                    st.error("That user ID is already taken.")
                else:
                    cur.execute(
                        "INSERT INTO users (username, password, role, name, specialty) VALUES (?,?,?,?,?)",
                        (username, password, role, name, final_specialty),
                    )
                    conn.commit()
                    if role == "doctor":
                        st.success(f"Doctor account created for {name} ({final_specialty}, user ID: {username}).")
                    else:
                        st.success(f"{role.title()} account created for {name} (user ID: {username}).")


def admin_approve_leaves():
    st.subheader("Approve Leave / Holiday Requests")
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT l.id, u.name, u.role, l.from_date, l.to_date, l.reason
            FROM leaves l JOIN users u ON u.id = l.user_id
            WHERE l.status = 'pending'
        """)
        pending = cur.fetchall()

        if not pending:
            st.info("No pending leave requests.")
            return

        st.dataframe(
            [{"ID": p[0], "Name": p[1], "Role": p[2], "From": p[3], "To": p[4], "Reason": p[5]} for p in pending],
            use_container_width=True, hide_index=True,
        )

        options = {f"{name} ({role}): {f} -> {t}": (lid, name) for lid, name, role, f, t, reason in pending}
        choice = st.selectbox("Select request", list(options.keys()))
        leave_id, _ = options[choice]
        decision = st.radio("Decision", ["Approve", "Reject"], horizontal=True)

        if st.button("Submit decision"):
            cur.execute("SELECT user_id FROM leaves WHERE id = ?", (leave_id,))
            user_id = cur.fetchone()[0]
            if decision == "Approve":
                cur.execute("UPDATE leaves SET status = 'approved' WHERE id = ?", (leave_id,))
                cur.execute("UPDATE users SET on_leave = 1 WHERE id = ?", (user_id,))
                st.success("Leave approved. That staff member is now marked as on leave.")
            else:
                cur.execute("UPDATE leaves SET status = 'rejected' WHERE id = ?", (leave_id,))
                st.success("Leave rejected.")
            conn.commit()


def admin_doctor_roster():
    st.subheader("Doctor Roster")
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT name, specialty, username, on_leave FROM users WHERE role = 'doctor' ORDER BY specialty, name"
        )
        doctors = cur.fetchall()

    if not doctors:
        st.info("No doctors on file yet.")
        return

    st.dataframe(
        [
            {
                "Name": name,
                "Specialty": specialty or "General",
                "User ID": username,
                "Status": "On leave" if on_leave else "Available",
            }
            for name, specialty, username, on_leave in doctors
        ],
        use_container_width=True, hide_index=True,
    )


def admin_add_medicine():
    st.subheader("Add Medicine")
    category_options = [
        "Painkiller / Fever", "Antibiotic", "Antihistamine / Allergy",
        "Antacid", "Diabetes", "Blood Pressure", "Respiratory",
        "Vitamin / Supplement", "Cardiac", "Other",
    ]

    category = st.selectbox("Category", category_options, key="add_med_category")
    category_custom = ""
    if category == "Other":
        category_custom = st.text_input("Enter category", key="add_med_category_custom")

    with st.form("add_medicine_form"):
        med_name = st.text_input("Medicine name")
        stock = st.number_input("Stock quantity", min_value=0, value=0, step=1)
        submitted = st.form_submit_button("Add medicine")

    if submitted:
        final_category = category_custom.strip() if category == "Other" else category
        if not med_name:
            st.error("Please enter the medicine name.")
        elif category == "Other" and not final_category:
            st.error("Please enter a category.")
        else:
            with closing(get_connection()) as conn:
                cur = conn.cursor()
                cur.execute("SELECT id FROM medicines WHERE name = ?", (med_name.strip(),))
                if cur.fetchone() is not None:
                    st.error("That medicine is already in the catalog.")
                else:
                    cur.execute(
                        "INSERT INTO medicines (name, category, stock) VALUES (?,?,?)",
                        (med_name.strip(), final_category, stock),
                    )
                    conn.commit()
                    st.success(f"Medicine added: {med_name.strip()} ({final_category}, stock: {stock}).")


def admin_medicine_list():
    st.subheader("Medicine Inventory")
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT name, category, stock FROM medicines ORDER BY category, name")
        medicines = cur.fetchall()

    if not medicines:
        st.info("No medicines on file yet.")
        return

    st.dataframe(
        [
            {
                "Name": name,
                "Category": category or "Uncategorized",
                "Stock": stock,
                "Status": "Low stock" if stock < 50 else "In stock",
            }
            for name, category, stock in medicines
        ],
        use_container_width=True, hide_index=True,
    )


def admin_menu(user):
    banner("Admin Dashboard", f"Signed in as {user['name']}")

    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM patients")
        n_patients = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM users WHERE role = 'doctor'")
        n_doctors = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM users WHERE role = 'nurse'")
        n_nurses = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM beds WHERE occupied = 1")
        n_occupied = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM beds")
        n_beds = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM medicines")
        n_medicines = cur.fetchone()[0]

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Patients", n_patients)
    c2.metric("Doctors", n_doctors)
    c3.metric("Nurses", n_nurses)
    c4.metric("Beds occupied", f"{n_occupied}/{n_beds}")
    c5.metric("Medicines", n_medicines)

    st.divider()
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Add staff", "Approve leaves", "Doctor roster", "Add medicine", "Medicine inventory"]
    )
    with tab1:
        admin_add_staff()
    with tab2:
        admin_approve_leaves()
    with tab3:
        admin_doctor_roster()
    with tab4:
        admin_add_medicine()
    with tab5:
        admin_medicine_list()


# =================================================================
# MAIN APP
# =================================================================

def main():
    # Landing page comes first, then login, then the role-based app.
    if st.session_state.user is None:
        if st.session_state.page == "landing":
            landing_page()
        else:
            login_screen()
        return

    st.session_state.page = "app"
    user = st.session_state.user
    role = user["role"]
    role_icons = {
        "admin": "🛡️",
        "reception": "🛎️",
        "floor": "🏢",
        "doctor": "🩺",
        "nurse": "💉",
    }

    with st.sidebar:
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.2rem;">
                <span style="font-size:1.5rem;">🏥</span>
                <span style="font-family:'Fraunces',serif;font-size:1.15rem;font-weight:600;color:#FFFFFF;">
                    MediFlow
                </span>
            </div>
            <div style="font-size:0.72rem;letter-spacing:0.12em;text-transform:uppercase;color:#BFDCC4;margin-bottom:1.1rem;">
                Hospital Management
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);
                        border-radius:14px;padding:0.9rem 1rem;margin-bottom:1rem;">
                <div style="font-size:1.6rem;line-height:1;">{role_icons.get(role, "👤")}</div>
                <div style="font-weight:700;margin-top:0.4rem;">{user['name']}</div>
                <div style="font-size:0.78rem;color:#BFDCC4;text-transform:uppercase;letter-spacing:0.06em;">
                    {role.title()}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()
        if st.button("↩ Logout", use_container_width=True):
            logout()

    if role == "reception":
        reception_menu(user)
    elif role == "doctor":
        doctor_menu(user)
    elif role == "floor":
        floor_menu(user)
    elif role == "nurse":
        nurse_menu(user)
    elif role == "admin":
        admin_menu(user)
    else:
        st.error("Unknown role - contact the system administrator.")


if __name__ == "__main__":
    main()
