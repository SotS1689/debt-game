import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────
#  CONFIGURATION  ← Only thing you need to edit
# ─────────────────────────────────────────────
# Use the exact URL of your workbook (the one with ONLY the Events sheet)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1HfbVFmwGjGGqAfqQ2adXbpZYPJ4pNe1Miel8_u3PCao/edit?usp=sharing"

# gid=0 is your Events sheet
SHEET_GID = 0

US_DEBT = 39_000_000_000_000  # Update this number whenever you like

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="US Debt Challenge",
    page_icon="💸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: #F0EDE6; }
.stApp {
    background: #0A0A0F;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(220,38,38,0.15) 0%, transparent 70%),
        repeating-linear-gradient(0deg, transparent, transparent 60px, rgba(255,255,255,0.015) 60px, rgba(255,255,255,0.015) 61px),
        repeating-linear-gradient(90deg, transparent, transparent 60px, rgba(255,255,255,0.015) 60px, rgba(255,255,255,0.015) 61px);
}
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 2rem; padding-bottom: 4rem; max-width: 760px;}

.hero { text-align: center; padding: 2.5rem 1rem 1.5rem; margin-bottom: 0.5rem; }
.hero-eyebrow { font-family: 'DM Mono', monospace; font-size: 0.7rem; letter-spacing: 0.25em; color: #DC2626; text-transform: uppercase; margin-bottom: 0.75rem; }
.hero-title { font-family: 'Bebas Neue', sans-serif; font-size: clamp(3rem, 10vw, 5.5rem); line-height: 0.95; color: #F0EDE6; letter-spacing: 0.02em; margin: 0 0 0.5rem; }
.hero-title span { color: #DC2626; }
.hero-subtitle { font-size: 1rem; color: #8A8580; font-weight: 300; max-width: 480px; width: 100%; margin: 20px auto 0; line-height: 1.6; text-align: center; display: block; }

.debt-ticker {
    background: linear-gradient(135deg, #1A0A0A 0%, #150505 100%);
    border: 1px solid rgba(220,38,38,0.3);
    border-radius: 12px;
    padding: 1.25rem 1.75rem;
    margin: 1.5rem 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}
.ticker-label { font-family: 'DM Mono', monospace; font-size: 0.65rem; letter-spacing: 0.2em; color: #DC2626; text-transform: uppercase; }
.ticker-value { font-family: 'Bebas Neue', sans-serif; font-size: 2rem; color: #FF4444; letter-spacing: 0.05em; text-shadow: 0 0 30px rgba(220,38,38,0.4); }

.event-card {
    background: linear-gradient(135deg, #111118 0%, #0D0D14 100%);
    border: 1px solid rgba(240,237,230,0.08);
    border-radius: 16px;
    padding: 1.75rem;
    margin: 1rem 0;
}
.event-label { font-family: 'DM Mono', monospace; font-size: 0.65rem; letter-spacing: 0.2em; color: #5A5750; text-transform: uppercase; margin-bottom: 0.5rem; }
.event-name { font-family: 'Bebas Neue', sans-serif; font-size: 2.2rem; color: #F0EDE6; letter-spacing: 0.03em; line-height: 1; margin-bottom: 0.75rem; }
.event-meta { display: flex; gap: 1.5rem; flex-wrap: wrap; }
.meta-chip {
    background: rgba(240,237,230,0.05);
    border: 1px solid rgba(240,237,230,0.08);
    border-radius: 6px;
    padding: 0.3rem 0.75rem;
    font-size: 0.8rem;
    color: #8A8580;
    font-family: 'DM Mono', monospace;
}
.meta-chip strong { color: #C8C4BC; }

.stSelectbox label, .stNumberInput label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.2em !important;
    color: #5A5750 !important;
    text-transform: uppercase !important;
}
.stSelectbox > div > div, .stNumberInput > div > div > input {
    background: #111118 !important;
    border: 1px solid rgba(240,237,230,0.1) !important;
    border-radius: 10px !important;
    color: #F0EDE6 !important;
    font-family: 'DM Mono', monospace !important;
}
.stNumberInput > div > div > input { font-size: 1.1rem !important; padding: 0.6rem 1rem !important; }

.stButton > button {
    background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%) !important;
    color: #F0EDE6 !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.3rem !important;
    letter-spacing: 0.1em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 2.5rem !important;
    width: 100% !important;
    box-shadow: 0 4px 24px rgba(220,38,38,0.25) !important;
}
.stButton > button:hover { transform: translateY(-1px); box-shadow: 0 8px 32px rgba(220,38,38,0.4) !important; }

.result-panel {
    background: linear-gradient(135deg, #0D1117 0%, #0A0F1A 100%);
    border: 1px solid rgba(240,237,230,0.08);
    border-radius: 16px;
    padding: 1.75rem;
    margin-top: 1.5rem;
}
.result-title { font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem; color: #8A8580; letter-spacing: 0.1em; margin-bottom: 1.25rem; text-transform: uppercase; }
.bar-row { margin-bottom: 1.1rem; }
.bar-meta { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.35rem; }
.bar-name { font-size: 0.8rem; font-family: 'DM Mono', monospace; color: #8A8580; letter-spacing: 0.05em; }
.bar-amount { font-size: 0.85rem; font-family: 'DM Mono', monospace; font-weight: 500; }
.bar-track { background: rgba(240,237,230,0.05); border-radius: 4px; height: 28px; overflow: hidden; position: relative; }
.bar-fill { height: 100%; border-radius: 4px; transition: width 0.8s cubic-bezier(0.16,1,0.3,1); display: flex; align-items: center; padding-left: 10px; min-width: 4px; }
.bar-fill-guess { background: linear-gradient(90deg, #2563EB, #3B82F6); box-shadow: 0 0 20px rgba(59,130,246,0.3); }
.bar-fill-debt { background: linear-gradient(90deg, #DC2626, #EF4444); box-shadow: 0 0 20px rgba(220,38,38,0.3); }
.verdict { margin-top: 1.5rem; padding: 1.25rem 1.5rem; border-radius: 12px; border-left: 4px solid; }
.verdict-low { background: rgba(220,38,38,0.06); border-color: #DC2626; }
.verdict-close { background: rgba(34,197,94,0.06); border-color: #22C55E; }
.verdict-high { background: rgba(234,179,8,0.06); border-color: #EAB308; }
.verdict-emoji { font-size: 1.75rem; margin-bottom: 0.4rem; }
.verdict-headline { font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem; letter-spacing: 0.05em; margin-bottom: 0.25rem; }
.verdict-body { font-size: 0.875rem; color: #8A8580; line-height: 1.6; }
.verdict-body strong { color: #C8C4BC; }
.stat-row { display: flex; gap: 0.75rem; margin-top: 1.25rem; flex-wrap: wrap; }
.stat-pill { flex: 1; min-width: 140px; background: rgba(240,237,230,0.04); border: 1px solid rgba(240,237,230,0.07); border-radius: 10px; padding: 0.9rem 1rem; text-align: center; }
.stat-pill-label { font-family: 'DM Mono', monospace; font-size: 0.6rem; letter-spacing: 0.2em; color: #5A5750; text-transform: uppercase; margin-bottom: 0.3rem; }
.stat-pill-value { font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem; letter-spacing: 0.05em; }
.styled-divider { border: none; border-top: 1px solid rgba(240,237,230,0.06); margin: 1.5rem 0; }
.reset-hint { text-align: center; font-size: 0.75rem; color: #3A3730; font-family: 'DM Mono', monospace; margin-top: 1rem; letter-spacing: 0.05em; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DATA LOADING – FINAL FIX for 400 error
# ─────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_data(url: str, gid: int) -> pd.DataFrame:
    """Reliable CSV export using the gviz method (this is the version that fixes the 400 error on new/single-sheet workbooks)."""
    # Extract spreadsheet ID cleanly
    if "/d/" in url:
        spreadsheet_id = url.split("/d/")[1].split("/")[0].split("?")[0]
    else:
        spreadsheet_id = url.split("/")[5] if len(url.split("/")) > 5 else url.split("?")[0]

    # This gviz URL is the most reliable public CSV export method in 2026
    csv_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/gviz/tq?tqx=out:csv&gid={gid}"

    df = pd.read_csv(csv_url)
    df.columns = [col.strip() for col in df.columns]

    # Exact mapping for your column headers
    rename_map = {}
    for col in df.columns:
        low = col.lower()
        if "event" in low:
            rename_map[col] = "Event"
        elif "date" in low:
            rename_map[col] = "Date"
        elif "years past" in low or "years" in low:
            rename_map[col] = "Years Ago"
        elif "dollars per day" in low or "daily" in low:
            rename_map[col] = "Daily Cost"
        elif "total" in low:
            rename_map[col] = "Total"
        elif "us federal debt" in low or "debt" in low:
            rename_map[col] = "US Debt"
    df.rename(columns=rename_map, inplace=True)

    for col in ["Years Ago", "Daily Cost", "Total", "US Debt"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df.dropna(subset=["Event"])

def fmt_dollars(n: float) -> str:
    if pd.isna(n) or n <= 0:
        return "$0"
    if n >= 1_000_000_000_000:
        return f"${n/1_000_000_000_000:.2f}T"
    elif n >= 1_000_000_000:
        return f"${n/1_000_000_000:.2f}B"
    elif n >= 1_000_000:
        return f"${n/1_000_000:.2f}M"
    return f"${n:,.0f}"

def fmt_dollars_full(n: float) -> str:
    if pd.isna(n):
        return "$0"
    return f"${int(n):,}"

# ─────────────────────────────────────────────
#  UI
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Interactive Challenge</div>
    <div class="hero-title">US DEBT<br><span>THROUGH TIME</span></div>
    <p class="hero-subtitle" style="text-align: center; margin: 20px auto 0; max-width: 480px; display: block;">
        Pick a moment in history. Guess how many dollars per day would be needed<br>
        since that date to equal today's national debt. See how your total stacks up.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="debt-ticker">
    <div><div class="ticker-label">Current US National Debt</div>
    <div class="ticker-value">{fmt_dollars_full(US_DEBT)}</div></div>
    <div style="font-size:2.5rem; opacity:0.2;">💸</div>
</div>
""", unsafe_allow_html=True)

try:
    df = load_data(SHEET_URL, SHEET_GID)
except Exception as e:
    st.error(f"⚠️ Couldn't load Google Sheet.\n\nError: {e}\n\nMake sure the sheet is shared as 'Anyone with the link can view'.")
    st.stop()

if df.empty:
    st.error("Sheet loaded but has no data rows.")
    st.stop()

# Live event selector
st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)

event_options = df["Event"].tolist()
selected_event = st.selectbox(
    "CHOOSE A HISTORICAL EVENT",
    options=event_options,
    index=0,
    key="event_select"
)

row = df[df["Event"] == selected_event].iloc[0]
years_ago = int(row.get("Years Ago", 0)) if pd.notna(row.get("Years Ago")) else 0
date_val = int(row.get("Date", 0)) if pd.notna(row.get("Date")) else "Unknown"
actual_daily = float(row.get("Daily Cost", 0)) if pd.notna(row.get("Daily Cost")) else 0

st.markdown(f"""
<div class="event-card">
    <div class="event-label">Selected Event</div>
    <div class="event-name">{selected_event}</div>
    <div class="event-meta">
        <div class="meta-chip">📅 Year <strong>{date_val}</strong></div>
        <div class="meta-chip">⏳ <strong>{years_ago:,}</strong> years ago</div>
        <div class="meta-chip">📐 <strong>{years_ago * 365:,}</strong> days of spending</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)

guess = st.number_input(
    "YOUR GUESS — DAILY DOLLARS NEEDED TO EQUAL DEBT ($)",
    min_value=0,
    value=0,
    step=1_000_000,
    format="%d",
    key="guess_input",
    help="Enter what you think the daily amount would need to be since that event to equal today's debt"
)

calculate = st.button("REVEAL THE TRUTH 🔍", type="primary", key="calc_btn")

# Results
if calculate and guess > 0:
    guess_total = guess * years_ago * 365
    max_val = max(guess_total, US_DEBT, 1)
    guess_pct = min((guess_total / max_val) * 100, 100)
    debt_pct = min((US_DEBT / max_val) * 100, 100)
    ratio = guess / actual_daily if actual_daily > 0 else 0

    if ratio < 0.1:
        verdict_class = "verdict-low"; verdict_emoji = "😱"
        verdict_headline = "Way Under — Reality Is Staggering"
        verdict_body = f"Your guess of <strong>{fmt_dollars(guess)}/day</strong> is less than 10% of the amount needed. The break-even daily amount is <strong>{fmt_dollars(actual_daily)}/day</strong>."
    elif ratio < 0.5:
        verdict_class = "verdict-low"; verdict_emoji = "📉"
        verdict_headline = "Under By A Wide Margin"
        verdict_body = f"The required daily amount of <strong>{fmt_dollars(actual_daily)}/day</strong> is roughly <strong>{1/ratio:.1f}x</strong> higher than your guess."
    elif ratio <= 2.0:
        verdict_class = "verdict-close"; verdict_emoji = "🎯"
        verdict_headline = "Remarkably Close!"
        verdict_body = f"You guessed <strong>{fmt_dollars(guess)}/day</strong> vs the required <strong>{fmt_dollars(actual_daily)}/day</strong>."
    elif ratio <= 10:
        verdict_class = "verdict-high"; verdict_emoji = "📈"
        verdict_headline = "You Overshot"
        verdict_body = f"Your guess was about <strong>{ratio:.1f}x</strong> higher than required."
    else:
        verdict_class = "verdict-high"; verdict_emoji = "🚀"
        verdict_headline = "Way Over The Top"
        verdict_body = f"That's <strong>{ratio:.0f}x</strong> the required daily figure."

    st.markdown('<div class="result-panel"><div class="result-title">THE BREAKDOWN</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="bar-row">
        <div class="bar-meta"><span class="bar-name">🔵 YOUR GUESS TOTAL</span><span class="bar-amount" style="color:#3B82F6">{fmt_dollars_full(guess_total)}</span></div>
        <div class="bar-track"><div class="bar-fill bar-fill-guess" style="width:{guess_pct:.1f}%"></div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="bar-row">
        <div class="bar-meta"><span class="bar-name">🔴 US NATIONAL DEBT</span><span class="bar-amount" style="color:#EF4444">{fmt_dollars_full(US_DEBT)}</span></div>
        <div class="bar-track"><div class="bar-fill bar-fill-debt" style="width:{debt_pct:.1f}%"></div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-pill"><div class="stat-pill-label">Your Daily Guess</div><div class="stat-pill-value" style="color:#3B82F6">{fmt_dollars(guess)}</div></div>
        <div class="stat-pill"><div class="stat-pill-label">Break-Even Daily Amount</div><div class="stat-pill-value" style="color:#EF4444">{fmt_dollars(actual_daily)}</div></div>
        <div class="stat-pill"><div class="stat-pill-label">Your Total</div><div class="stat-pill-value" style="color:#3B82F6">{fmt_dollars(guess_total)}</div></div>
        <div class="stat-pill"><div class="stat-pill-label">Debt vs Your Total</div><div class="stat-pill-value" style="color:#8A8580">{US_DEBT / max(guess_total, 1):.1f}x</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="verdict {verdict_class}">
        <div class="verdict-emoji">{verdict_emoji}</div>
        <div class="verdict-headline">{verdict_headline}</div>
        <div class="verdict-body">{verdict_body}</div>
    </div>
    </div>
    <div class="reset-hint">↑ Change the event or your guess above to play again</div>
    """, unsafe_allow_html=True)

elif calculate and guess == 0:
    st.warning("Please enter a guess greater than 0.")
