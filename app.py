import streamlit as st
import pandas as pd
import re

# ─────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────
# Ensure this is the "Anyone with the link can view" URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1HfbVFmwGjGGqAfqQ2adXbpZYPJ4pNe1Miel8_u3PCao/edit?usp=sharing"
SHEET_GID = 0  # Change if your data is on a different tab
US_DEBT = 34_000_000_000_000  # Updated to current approx; edit as needed

# ─────────────────────────────────────────────
#  PAGE CONFIG (Must be the very first Streamlit command)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="US Debt Challenge",
    page_icon="💸",
    layout="centered",
)

# ─────────────────────────────────────────────
#  STYLING
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;700&family=DM+Mono&display=swap');
    
    .stApp { background-color: #0A0A0F; color: #F0EDE6; }
    .hero-title { font-family: 'Bebas Neue', sans-serif; font-size: 4rem; color: #DC2626; text-align: center; line-height: 1; }
    .hero-sub { font-family: 'DM Sans', sans-serif; text-align: center; color: #8A8580; margin-bottom: 2rem; }
    
    /* Stats Cards */
    .stat-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(220, 38, 38, 0.3);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Result Bars */
    .bar-container { height: 30px; width: 100%; background: #1A1A24; border-radius: 5px; margin: 10px 0; overflow: hidden; }
    .bar-fill { height: 100%; transition: width 1s ease-in-out; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CORE FUNCTIONS
# ─────────────────────────────────────────────

@st.cache_data(ttl=600)
def load_data_safe(url, gid):
    try:
        # Robust Regex to pull Spreadsheet ID even from messy URLs
        pattern = r"/d/([a-zA-Z0-9-_]+)"
        match = re.search(pattern, url)
        if not match:
            st.error("Invalid Google Sheets URL format.")
            return pd.DataFrame()
        
        spreadsheet_id = match.group(1)
        # Construct direct export link
        export_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid}"
        
        df = pd.read_csv(export_url)
        
        # Clean column names (remove whitespace/newlines)
        df.columns = [str(c).strip() for c in df.columns]
        
        # Logic to find columns even if named slightly differently
        mapping = {}
        for col in df.columns:
            c_low = col.lower()
            if "event" in c_low: mapping[col] = "Event"
            elif "date" in c_low or "year" in c_low: mapping[col] = "Year"
            elif "daily" in c_low or "day" in c_low: mapping[col] = "DailyCost"
            elif "years past" in c_low or "years ago" in c_low: mapping[col] = "YearsAgo"
            
        df = df.rename(columns=mapping)
        
        # Numeric clean up
        for c in ["DailyCost", "YearsAgo"]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')
        
        return df.dropna(subset=["Event"])
    except Exception as e:
        st.error(f"Data Connection Error (400): {e}")
        return pd.DataFrame()

def format_money(val):
    if val >= 1e12: return f"${val/1e12:.2f} Trillion"
    if val >= 1e9: return f"${val/1e9:.2f} Billion"
    return f"${val:,.0f}"

# ─────────────────────────────────────────────
#  APP LOGIC
# ─────────────────────────────────────────────

st.markdown('<div class="hero-title">DEBT TIME MACHINE</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">How much money per day since history\'s biggest events equals the US Debt?</div>', unsafe_allow_html=True)

df = load_data_safe(SHEET_URL, SHEET_GID)

if not df.empty:
    # 1. Selector
    selected_event = st.selectbox("Select a historical event:", df["Event"].unique())
    event_data = df[df["Event"] == selected_event].iloc[0]
    
    # 2. Display Context
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Year of Event", int(event_data['Year']))
    with col2:
        st.metric("Years Passed", f"{int(event_data['YearsAgo'])} yrs")

    # 3. User Interaction
    st.divider()
    user_guess = st.number_input("Guess the daily amount needed ($ per day):", 
                                 min_value=0, value=1000000, step=1000000)
    
    if st.button("REVEAL TRUTH", type="primary"):
        actual_daily = event_data["DailyCost"]
        days_passed = event_data["YearsAgo"] * 365.25
        total_from_guess = user_guess * days_passed
        
        # 4. Results Visualization
        st.subheader("The Comparison")
        
        # Bars
        guess_perc = min(100, (total_from_guess / US_DEBT) * 100)
        
        st.write(f"Your Guess Total: {format_money(total_from_guess)}")
        st.markdown(f'<div class="bar-container"><div class="bar-fill" style="width:{guess_perc}%; background:#2563EB;"></div></div>', unsafe_allow_html=True)
        
        st.write(f"Actual US Debt: {format_money(US_DEBT)}")
        st.markdown(f'<div class="bar-container"><div class="bar-fill" style="width:100%; background:#DC2626;"></div></div>', unsafe_allow_html=True)
        
        # Detailed Stats
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""<div class="stat-card">
                <small>YOU GUESSED</small><h3>{format_money(user_guess)}/day</h3>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="stat-card" style="border-color:#22C55E">
                <small>REALITY REQUIRES</small><h3>{format_money(actual_daily)}/day</h3>
            </div>""", unsafe_allow_html=True)

        # Verdict
        diff_factor = actual_daily / user_guess if user_guess > 0 else 0
        if diff_factor > 1.5:
            st.warning(f"You're way off! Reality is actually {diff_factor:.1f}x higher than your guess.")
        elif diff_factor < 0.5:
            st.info(f"You overshot! It only takes {1/diff_factor:.1f}x less than what you thought.")
        else:
            st.success("Impressive! You're in the ballpark.")

else:
    st.info("Awaiting data connection... Ensure your Google Sheet is shared as 'Anyone with the link can view'.")
