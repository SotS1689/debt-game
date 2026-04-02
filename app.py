import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────
#  CONFIGURATION  ← Only thing you need to edit
# ─────────────────────────────────────────────
# Paste your Google Sheet URL below.
# The sheet must be shared as "Anyone with the link can VIEW"
SHEET_URL = https://docs.google.com/spreadsheets/d/e/2PACX-1vSsJxcjAYcpqz4xAgR9oNG3d31Eq3y4Z_pk4QqLWOQQvWMYLG36jftwahCV1mHt5aQ-oQ1Pep7PK6iG/pubhtml?gid=2120968951&single=true

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

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #F0EDE6;
}
.stApp {
    background: #0A0A0F;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(220,38,38,0.15) 0%, transparent 70%),
        repeating-linear-gradient(0deg, transparent, transparent 60px, rgba(255,255,255,0.015) 60px, rgba(255,255,255,0.015) 61px),
        repeating-linear-gradient(90deg, transparent, transparent 60px, rgba(255,255,255,0.015) 60px, rgba(255,255,255,0.015) 61px);
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 2rem; padding-bottom: 4rem; max-width: 760px;}

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    margin-bottom: 0.5rem;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    color: #DC2626;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3rem, 10vw, 5.5rem);
    line-height: 0.95;
    color: #F0EDE6;
    letter-spacing: 0.02em;
    margin: 0 0 0.5rem;
}
.hero-title span {
    color: #DC2626;
}
.hero-subtitle {
    font-size: 1rem;
    color: #8A8580;
    font-weight: 300;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Debt Ticker ── */
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
.ticker-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: #DC2626;
    text-transform: uppercase;
}
.ticker-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    color: #FF4444;
    letter-spacing: 0.05em;
    text-shadow: 0 0 30px rgba(220,38,38,0.4);
}

/* ── Event Card ── */
.event-card {
    background: linear-gradient(135deg, #111118 0%, #0D0D14 100%);
    border: 1px solid rgba(240,237,230,0.08);
    border-radius: 16px;
    padding: 1.75rem;
    margin: 1rem 0;
}
.event-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: #5A5750;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.event-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    color: #F0EDE6;
    letter-spacing: 0.03em;
    line-height: 1;
    margin-bottom: 0.75rem;
}
.event-meta {
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
}
.meta-chip {
    background: rgba(240,237,230,0.05);
    border: 1px solid rgba(240,237,230,0.08);
    border-radius: 6px;
    padding: 0.3rem 0.75rem;
    font-size: 0.8rem;
    color: #8A8580;
    font-family: 'DM Mono', monospace;
}
.meta-chip strong {
    color: #C8C4BC;
}

/* ── Selectbox & Number Input ── */
.stSelectbox label, .stNumberInput label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.2em !important;
    color: #5A5750 !important;
    text-transform: uppercase !important;
}
.stSelectbox > div > div {
    background: #111118 !important;
    border: 1px solid rgba(240,237,230,0.1) !important;
    border-radius: 10px !important;
    color: #F0EDE6 !important;
}
.stSelectbox > div > div:focus-within {
    border-color: rgba(220,38,38,0.5) !important;
    box-shadow: 0 0 0 2px rgba(220,38,38,0.1) !important;
}
.stNumberInput > div > div > input {
    background: #111118 !important;
    border: 1px solid rgba(240,237,230,0.1) !important;
    border-radius: 10px !important;
    color: #F0EDE6 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 1.1rem !important;
    padding: 0.6rem 1rem !important;
}
.stNumberInput > div > div > input:focus {
    border-color: rgba(220,38,38,0.5) !important;
    box-shadow: 0 0 0 2px rgba(220,38,38,0.1) !important;
}

/* ── Button ── */
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
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 24px rgba(220,38,38,0.25) !important;
    margin-top: 0.5rem !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 32px rgba(220,38,38,0.4) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Results Panel ── */
.result-panel {
    background: linear-gradient(135deg, #0D1117 0%, #0A0F1A 100%);
    border: 1px solid rgba(240,237,230,0.08);
    border-radius: 16px;
    padding: 1.75rem;
    margin-top: 1.5rem;
}
.result-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    color: #8A8580;
    letter-spacing: 0.1em;
    margin-bottom: 1.25rem;
    text-transform: uppercase;
}

/* ── Bar Chart ── */
.bar-row {
    margin-bottom: 1.1rem;
}
.bar-meta {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.35rem;
}
.bar-name {
    font-size: 0.8rem;
    font-family: 'DM Mono', monospace;
    color: #8A8580;
    letter-spacing: 0.05em;
}
.bar-amount {
    font-size: 0.85rem;
    font-family: 'DM Mono', monospace;
    font-weight: 500;
}
.bar-track {
    background: rgba(240,237,230,0.05);
    border-radius: 4px;
    height: 28px;
    overflow: hidden;
    position: relative;
}
.bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.8s cubic-bezier(0.16,1,0.3,1);
    display: flex;
    align-items: center;
    padding-left: 10px;
    min-width: 4px;
}
.bar-fill-guess {
    background: linear-gradient(90deg, #2563EB, #3B82F6);
    box-shadow: 0 0 20px rgba(59,130,246,0.3);
}
.bar-fill-debt {
    background: linear-gradient(90deg, #DC2626, #EF4444);
    box-shadow: 0 0 20px rgba(220,38,38,0.3);
}

/* ── Verdict ── */
.verdict {
    margin-top: 1.5rem;
    padding: 1.25rem 1.5rem;
    border-radius: 12px;
    border-left: 4px solid;
}
.verdict-low {
    background: rgba(220,38,38,0.06);
    border-color: #DC2626;
}
.verdict-close {
    background: rgba(34,197,94,0.06);
    border-color: #22C55E;
}
.verdict-high {
    background: rgba(234,179,8,0.06);
    border-color: #EAB308;
}
.verdict-emoji {
    font-size: 1.75rem;
    margin-bottom: 0.4rem;
}
.verdict-headline {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    letter-spacing: 0.05em;
    margin-bottom: 0.25rem;
}
.verdict-body {
    font-size: 0.875rem;
    color: #8A8580;
    line-height: 1.6;
}
.verdict-body strong {
    color: #C8C4BC;
}

/* ── Stat Pills ── */
.stat-row {
    display: flex;
    gap: 0.75rem;
    margin-top: 1.25rem;
    flex-wrap: wrap;
}
.stat-pill {
    flex: 1;
    min-width: 140px;
    background: rgba(240,237,230,0.04);
    border: 1px solid rgba(240,237,230,0.07);
    border-radius: 10px;
    padding: 0.9rem 1rem;
    text-align: center;
}
.stat-pill-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    color: #5A5750;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.stat-pill-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    letter-spacing: 0.05em;
}

/* ── Divider ── */
.styled-divider {
    border: none;
    border-top: 1px solid rgba(240,237,230,0.06);
    margin: 1.5rem 0;
}

/* ── Reset button ── */
.reset-hint {
    text-align: center;
    font-size: 0.75rem;
    color: #3A3730;
    font-family: 'DM Mono', monospace;
    margin-top: 1rem;
    letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data(url: str) -> pd.DataFrame:
    """Convert any Google Sheets URL to a CSV export URL and load it."""
    if "/edit" in url:
        csv_url = url.split("/edit")[0] + "/export?format=csv&gid=0"
    elif "/pub" in url:
        csv_url = url.split("/pub")[0] + "/export?format=csv&gid=0"
    else:
        csv_url = url + "/export?format=csv&gid=0"

    df = pd.read_csv(csv_url)
    df.columns = df.columns.str.strip()

    # Normalize column names to be robust to minor variations
    rename_map = {}
    for col in df.columns:
        low = col.lower().strip()
        if "event" in low:
            rename_map[col] = "Event"
        elif "date" in low:
            rename_map[col] = "Date"
        elif "year" in low:
            rename_map[col] = "Years Ago"
        elif "dollar" in low or "per day" in low or "daily" in low:
            rename_map[col] = "Daily Cost"
        elif "total" in low:
            rename_map[col] = "Total"
        elif "debt" in low or "federal" in low:
            rename_map[col] = "US Debt"
    df.rename(columns=rename_map, inplace=True)

    # Ensure numeric columns are actually numeric
    for col in ["Years Ago", "Daily Cost", "Total", "US Debt"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df.dropna(subset=["Event"])


def fmt_dollars(n: float) -> str:
    """Format a large number as a readable dollar string."""
    if n >= 1_000_000_000_000:
        return f"${n/1_000_000_000_000:.2f}T"
    elif n >= 1_000_000_000:
        return f"${n/1_000_000_000:.2f}B"
    elif n >= 1_000_000:
        return f"${n/1_000_000:.2f}M"
    else:
        return f"${n:,.0f}"


def fmt_dollars_full(n: float) -> str:
    """Format with full comma notation."""
    return f"${n:,.0f}"


# ─────────────────────────────────────────────
#  HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Interactive Challenge</div>
    <div class="hero-title">US DEBT<br><span>THROUGH TIME</span></div>
    <p class="hero-subtitle">
        Pick a moment in history. Guess how much the US spends per day.<br>
        See how it stacks up against <strong style="color:#F0EDE6">$39 trillion</strong> in national debt.
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DEBT TICKER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="debt-ticker">
    <div>
        <div class="ticker-label">Current US National Debt</div>
        <div class="ticker-value">{fmt_dollars_full(US_DEBT)}</div>
    </div>
    <div style="font-size:2.5rem; opacity:0.2;">💸</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────
try:
    df = load_data(SHEET_URL)
except Exception as e:
    st.error(f"⚠️ Couldn't load your Google Sheet. Make sure it's shared as 'Anyone with the link can view' and the URL in app.py is correct.\n\nError: {e}")
    st.stop()

if df.empty:
    st.error("Your sheet loaded but appears to have no data rows.")
    st.stop()

# ─────────────────────────────────────────────
#  EVENT SELECTOR
# ─────────────────────────────────────────────
st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)

event_options = df["Event"].tolist()
selected_event = st.selectbox(
    "CHOOSE A HISTORICAL EVENT",
    options=event_options,
    index=0,
    key="event_select"
)

row = df[df["Event"] == selected_event].iloc[0]
years_ago = int(row["Years Ago"]) if pd.notna(row.get("Years Ago")) else 0
date_val = int(row["Date"]) if pd.notna(row.get("Date")) else "Unknown"
actual_daily = float(row["Daily Cost"]) if pd.notna(row.get("Daily Cost")) else 0
actual_total = float(row["Total"]) if pd.notna(row.get("Total")) else (actual_daily * years_ago * 365)

# ─────────────────────────────────────────────
#  EVENT CARD
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
#  GUESS INPUT
# ─────────────────────────────────────────────
st.markdown('<hr class="styled-divider">', unsafe_allow_html=True)

guess = st.number_input(
    "YOUR GUESS — US GOVERNMENT SPENDING PER DAY ($)",
    min_value=0,
    value=None,
    placeholder="Type a number, e.g. 5000000",
    step=1_000_000,
    format="%d",
    key="guess_input",
    help="Enter what you think the US spends per day in today's dollars"
)

calculate = st.button("REVEAL THE TRUTH 🔍", key="calc_btn")

# ─────────────────────────────────────────────
#  RESULTS
# ─────────────────────────────────────────────
if calculate and guess is not None and guess > 0:

    guess_total = guess * years_ago * 365
    max_val = max(guess_total, US_DEBT, 1)

    guess_pct = min((guess_total / max_val) * 100, 100)
    debt_pct = min((US_DEBT / max_val) * 100, 100)

    # Accuracy ratio
    if actual_daily > 0:
        ratio = guess / actual_daily
        accuracy_pct = min(ratio, 1 / ratio) * 100 if ratio != 0 else 0
    else:
        ratio = 0
        accuracy_pct = 0

    # Verdict logic
    if ratio < 0.1:
        verdict_class = "verdict-low"
        verdict_emoji = "😱"
        verdict_headline = "Way Under — Reality Is Staggering"
        verdict_body = f"Your guess of <strong>{fmt_dollars(guess)}/day</strong> is less than 10% of the actual figure. The real daily spend has been <strong>{fmt_dollars(actual_daily)}/day</strong> — most people vastly underestimate this."
    elif ratio < 0.5:
        verdict_class = "verdict-low"
        verdict_emoji = "📉"
        verdict_headline = "Under By A Wide Margin"
        verdict_body = f"Close-ish, but the actual daily cost of <strong>{fmt_dollars(actual_daily)}/day</strong> is roughly <strong>{1/ratio:.1f}x</strong> higher than your guess. The cumulative effect over {years_ago:,} years is enormous."
    elif ratio <= 2.0:
        verdict_class = "verdict-close"
        verdict_emoji = "🎯"
        verdict_headline = "Remarkably Close!"
        verdict_body = f"You guessed <strong>{fmt_dollars(guess)}/day</strong> vs the actual <strong>{fmt_dollars(actual_daily)}/day</strong>. You have a strong grasp of the scale of US government spending."
    elif ratio <= 10:
        verdict_class = "verdict-high"
        verdict_emoji = "📈"
        verdict_headline = "You Overshot"
        verdict_body = f"Your guess was about <strong>{ratio:.1f}x</strong> higher than the actual <strong>{fmt_dollars(actual_daily)}/day</strong>. Even so, compared to the full $39T debt, every number looks small."
    else:
        verdict_class = "verdict-high"
        verdict_emoji = "🚀"
        verdict_headline = "Way Over The Top"
        verdict_body = f"That's <strong>{ratio:.0f}x</strong> the actual figure of <strong>{fmt_dollars(actual_daily)}/day</strong>. Either way, the $39T debt dwarfs almost any guess."

    st.markdown(f"""
    <div class="result-panel">
        <div class="result-title">The Breakdown</div>

        <div class="bar-row">
            <div class="bar-meta">
                <span class="bar-name">🔵 YOUR GUESS TOTAL</span>
                <span class="bar-amount" style="color:#3B82F6">{fmt_dollars_full(guess_total)}</span>
            </div>
            <div class="bar-track">
                <div class="bar-fill bar-fill-guess" style="width:{guess_pct:.1f}%"></div>
            </div>
        </div>

        <div class="bar-row">
            <div class="bar-meta">
                <span class="bar-name">🔴 US NATIONAL DEBT</span>
                <span class="bar-amount" style="color:#EF4444">{fmt_dollars_full(US_DEBT)}</span>
            </div>
            <div class="bar-track">
                <div class="bar-fill bar-fill-debt" style="width:{debt_pct:.1f}%"></div>
            </div>
        </div>

        <div class="stat-row">
            <div class="stat-pill">
                <div class="stat-pill-label">Your Daily Guess</div>
                <div class="stat-pill-value" style="color:#3B82F6">{fmt_dollars(guess)}</div>
            </div>
            <div class="stat-pill">
                <div class="stat-pill-label">Actual Daily Cost</div>
                <div class="stat-pill-value" style="color:#EF4444">{fmt_dollars(actual_daily)}</div>
            </div>
            <div class="stat-pill">
                <div class="stat-pill-label">Your Total</div>
                <div class="stat-pill-value" style="color:#3B82F6">{fmt_dollars(guess_total)}</div>
            </div>
            <div class="stat-pill">
                <div class="stat-pill-label">Debt vs Your Total</div>
                <div class="stat-pill-value" style="color:#8A8580">{US_DEBT/max(guess_total,1):.1f}x</div>
            </div>
        </div>

        <div class="verdict {verdict_class}">
            <div class="verdict-emoji">{verdict_emoji}</div>
            <div class="verdict-headline">{verdict_headline}</div>
            <div class="verdict-body">{verdict_body}</div>
        </div>
    </div>
    <div class="reset-hint">↑ Change the event or your guess above to play again</div>
    """, unsafe_allow_html=True)

elif calculate and (guess is None or guess == 0):
    st.warning("Enter a number greater than 0 to see the results.")
