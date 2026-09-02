# ============================================================
# SKIP - Smart Knowledge-based Intelligent Planner
# Phase 6 Final Demonstration App 
# ============================================================

import streamlit as st
import pandas as pd
from datetime import datetime
from html import escape
from pathlib import Path

# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="SKIP Journey Planner",
    page_icon="none",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------
# Project Paths
# ------------------------------------------------------------

BASE_DIR = Path(__file__).parent
LOGO_PATH = BASE_DIR / "logo.png"
# ------------------------------------------------------------
# Brand Colours (Original Python constants, not directly used for styling)
# ------------------------------------------------------------

NAVY = "#081C3A"
TEAL = "#56B4E9"
GREEN = "#009E73"
BLUE = "#0072B2"
WHITE = "#FFFFFF"
LIGHT = "#F6F8FC"
GREY = "#6B7280"
RED = "#D9534F"

# ------------------------------------------------------------
# Temporary Station Registry
# Replace with registry from notebook
# ------------------------------------------------------------

STATIONS = [
    "King's Cross St. Pancras",
    "Canary Wharf",
    "Oxford Circus",
    "Victoria",
    "Waterloo",
    "London Bridge",
    "Liverpool Street",
    "Green Park",
    "Baker Street",
    "Paddington",
]

# ------------------------------------------------------------
# Colour-Blind Mode Toggle
# ------------------------------------------------------------


if "colour_blind_mode" not in st.session_state:
    st.session_state.colour_blind_mode = False

# Place the toggle at the top of the interface
st.session_state.colour_blind_mode = st.toggle(
    "Colour-Blind Mode",
    value=st.session_state.colour_blind_mode,
    help="Toggle to switch to a colour-blind friendly palette.",
)

# Determine the accent color based on the toggle
ACCENT_COLOR = "#0072B2" if st.session_state.colour_blind_mode else "#17BEBB"
ACCENT_HOVER_COLOR = "#005B90" if st.session_state.colour_blind_mode else "#11A7A4" # Slightly darker for hover
ACCENT_LIGHT_COLOR = "#DDEBF6" if st.session_state.colour_blind_mode else "#DDF5F3" # Lighter for primary button background
ACCENT_LIGHTER_COLOR = "#BADCEF" if st.session_state.colour_blind_mode else "#BFE8E6" # Lighter for chip borders

# Function to convert hex to rgba for dynamic shadows
def hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip('#')
    lv = len(hex_color)
    rgb = tuple(int(hex_color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {alpha})"

ACCENT_SHADOW_RGBA = hex_to_rgba(ACCENT_COLOR, 0.16)


# ------------------------------------------------------------
# CSS
# ------------------------------------------------------------

st.markdown(
f"""
<style>

:root {{
    /* Dynamic Accent Colors */
    --accent-color: {ACCENT_COLOR};
    --accent-hover-color: {ACCENT_HOVER_COLOR};
    --accent-light-color: {ACCENT_LIGHT_COLOR};
    --accent-lighter-color: {ACCENT_LIGHTER_COLOR};
    --accent-shadow-rgba: {ACCENT_SHADOW_RGBA};

    /* Fixed Palette Colors */
    --background-color: #F8F5F1;
    --card-background-color: #FFFFFF;
    --primary-text-color: #11284D;
    --secondary-text-color: #6E7891;
    --border-color: #D9E2EC;
    --punctuality-border-color: #3B82F6;
    --accessibility-border-color: #49D17D;
    --compromise-route-card-border: #FF6B2C;
    --warning-chip-background: #FFF0EC;
    --warning-chip-border: #FFB6A6;
    --banner-background: #FDECEC;
    --banner-text-color: #8A1F17;
    --brand-mark-after-color: #FF6B2C; /* Specific for brand mark glow */
    --dark-text-color: #0B2346; /* Used for pac-card h3, rank background */
}}

#MainMenu {{visibility:hidden;}}
footer {{visibility:hidden;}}
header {{visibility:hidden;}}

.block-container{{
    max-width:1180px;
    padding-top:1rem;
    padding-left:2rem;
    padding-right:2rem;
    padding-bottom:4rem;
}}

.stApp{{
    background:var(--background-color);
}}
/* ------------------------------------------------ */
/* Streamlit Inputs */
/* ------------------------------------------------ */


label,
.stSelectbox label,
.stDateInput label,
.stTimeInput label,
.stCheckbox label {{
    color: var(--primary-text-color) !important;
    font-weight: 600 !important;
    opacity: 1 !important;
}}

/* Specific styling for the Streamlit Toggle text */
.stToggle label span {{
    color: var(--primary-text-color) !important;
    font-weight: 600 !important;
    opacity: 1 !important;

}}

/* Select boxes */

.stSelectbox > div > div{{
    background:var(--card-background-color) !important;
    border:1px solid var(--border-color) !important;
    border-radius:16px !important;
    min-height:56px;
}}

/* Date */

.stDateInput > div > div{{
    background:var(--card-background-color) !important;
    border:1px solid var(--border-color) !important;
    border-radius:16px !important;
}}

/* Time */

.stTimeInput > div > div{{
    background:var(--card-background-color) !important;
    border:1px solid var(--border-color) !important;
    border-radius:16px !important;
}}

/* Text inside widgets */

.stSelectbox div,
.stDateInput input,
.stTimeInput input{{
    color:var(--primary-text-color) !important;
    opacity:1 !important;
}}

/* Checkbox text */

.stCheckbox{{
    color:var(--primary-text-color) !important;
}}

/* Planner spacing */

.stSelectbox,
.stDateInput,
.stTimeInput,
.stCheckbox{{
    margin-bottom:12px;
}}
/* ---------- Hero ---------- */

.hero{{
    background:transparent;
    box-shadow:none;
    border-radius:0;
    padding:38px 0 34px 0;
    margin-bottom:0;
    max-width:640px;
}}

.hero h1{{
    font-size:5.7rem;
    font-weight:800;
    line-height:1.0;
    color:var(--primary-text-color);
    margin-bottom:34px;
}}

.hero p{{
    color:var(--secondary-text-color);
    font-size:1.1rem;
    line-height:1.6;
    max-width:620px;
}}

.site-header{{
    align-items:center;
    display:flex;
    justify-content:space-between;
    padding:12px 0 34px 0;
}}

.brand{{
    align-items:center;
    display:flex;
    gap:14px;
}}


/* New CSS for the image logo */
.brand-logo{{
    width:64px;
    height:64px;
    object-fit:contain;
    border:none;
    border-radius:0;
    display:block;
}}

.brand-name{{
    color:var(--primary-text-color);
    font-size:1.2rem;
    font-weight:850;
}}

.brand-subtitle{{
    color:#7B8799;
    font-size:.72rem;
    font-weight:700;
    letter-spacing:4px;
    text-transform:uppercase;
}}

.nav-links{{
    color:var(--primary-text-color);
    display:flex;
    font-size:.95rem;
    font-weight:750;
    gap:42px;
}}

.planner-title{{
    color:var(--primary-text-color) !important;
    font-size:2rem;
    font-weight:850;
    margin:0 0 18px 0;
}}

/* ---------- Cards ---------- */

.card{{
    background:var(--card-background-color);
    border-radius:20px;
    padding:22px;
    box-shadow:0 10px 25px rgba(0,0,0,.08);
}}

.metric-card{{
    background:var(--card-background-color);
    border-radius:18px;
    padding:16px;
    text-align:center;
    box-shadow:0 6px 18px rgba(0,0,0,.08);
}}

/* ---------- PAC ---------- */

.section-kicker{{
    color:#7B8799;
    font-size:.78rem;
    font-weight:800;
    letter-spacing:4px;
    text-transform:uppercase;
    margin-bottom:10px;
}}

h2.priority-heading{{
    color:var(--primary-text-color) !important;
    font-size:2rem;
    line-height:1.08;
    font-weight:850;
    margin:20px 0 28px 0;
}}

h2.priority-heading span{{
    color:var(--accent-color) !important;
    font-style:italic;
}}

.pac-card{{
    background:var(--card-background-color);
    border-radius:18px;
    padding:20px;
    border:2px solid transparent;
    transition:0.25s;
    box-shadow:0 8px 20px rgba(0,0,0,.08);
    min-height:170px;
}}

.pac-selected{{
    background:var(--accent-light-color);
    border:2px solid var(--accent-color);
}}

.pac-card h3{{
    color:var(--dark-text-color);
    margin-bottom:10px;
}}

.pac-card p{{
    color:#5E6C84;
}}

.pac-card:hover{{
    transform:translateY(-3px);
}}

div[class*="st-key-select_"] .stButton button{{
    align-items:flex-start;
    background:var(--card-background-color) !important;
    border:2px solid var(--border-color) !important;
    border-radius:18px !important;
    box-shadow:0 8px 18px rgba(8,28,58,.06) !important;
    color:var(--primary-text-color) !important;
    display:flex;
    font-size:1.05rem !important;
    font-weight:700 !important; /* Semi-bold for button text */
    height:166px;
    justify-content:flex-start;
    line-height:1.35;
    padding:30px 28px !important;
    text-align:left;
    white-space:pre-line;
    width:100%;
}}

div[class*="st-key-select_"] .stButton button p{{
    color:var(--primary-text-color) !important;
    font-size:1.02rem;
    line-height:1.35;
    margin:0;
    font-weight: 700; /* Explicitly ensure label text is semi-bold */
}}

div[class*="st-key-select_"] .stButton button span[data-testid^="stIcon"]{{
    font-size: 28px; /* Increased icon size */
    margin-right: 12px;
}}

div[class*="st-key-select_"] .stButton button:hover{{
    border-color:var(--accent-color) !important;
    transform:translateY(-2px);
}}

div[class*="st-key-select_"] .stButton button[kind="primary"],
div[class*="st-key-select_"] .stButton button[data-testid="stBaseButton-primary"]{{
    background:var(--accent-light-color) !important;
    border-color:var(--accent-color) !important;
    box-shadow:0 14px 28px var(--accent-shadow-rgba) !important; /* Dynamic shadow */
}}

.punctuality{{
    border-top-color:var(--punctuality-border-color);
}}

.accessibility{{
    border-top-color:var(--accessibility-border-color);
}}

.comfort{{
    border-top-color:var(--accent-color);
}}

.small{{
    color:var(--secondary-text-color);
    font-size: 16px; /* Increased explanation text size */
    line-height: 1.6; /* Increased explanation text line height */
}}

.small b {{
    color: var(--accent-color);
}}

.route-card{{
    background:var(--card-background-color);
    border:1px solid var(--border-color);
    border-left:7px solid var(--accent-color);
    border-radius:18px;
    padding:28px 30px;
    margin-top:20px;
    box-shadow:0 8px 18px rgba(8,28,58,.06);
}}

.route-card.compromise{{
    border-left-color:var(--compromise-route-card-border);
}}

.route-eyebrow{{
    color:#7B8799;
    font-size:.82rem;
    font-weight:850;
    letter-spacing:4px;
    text-transform:uppercase;
}}

.route-eyebrow span{{
    color:var(--accent-color);
}}

.route-card.compromise .route-eyebrow span{{
    color:var(--compromise-route-card-border);
}}

.route-title{{
    color:var(--primary-text-color);
    font-size:1.35rem;
    font-weight:800;
    margin:10px 0 8px 0;
}}

.route-subtitle{{
    color:var(--secondary-text-color);
    font-size:1rem;
    font-weight:600;
    margin:0 0 22px 0;
}}

.route-divider{{
    border-top:1px solid var(--border-color);
    margin:22px 0;
}}

.metric-grid{{
    display:grid;
    grid-template-columns:repeat(3, minmax(0, 1fr));
    gap:22px;
}}

.metric-label{{
    color:#7B8799;
    font-size:.8rem;
    font-weight:850;
    letter-spacing:4px;
    text-transform:uppercase;
}}

.metric-value{{
    color:var(--primary-text-color);
    font-size:2rem;
    font-weight:850;
    margin-top:6px;
}}

.chip-row{{
    display:flex;
    flex-wrap:wrap;
    gap:10px;
    margin-top:24px;
}}

.chip{{
    background:var(--accent-light-color);
    border:1px solid var(--accent-lighter-color);
    border-radius:999px;
    color:var(--primary-text-color);
    display:inline-flex;
    font-size:.92rem;
    font-weight:750;
    padding:8px 14px;
}}

.chip.warning-chip{{
    background:var(--warning-chip-background);
    border-color:var(--warning-chip-border);
}}

.rank{{
    background:var(--dark-text-color);
    color:var(--card-background-color);
    border-radius:999px;
    display:inline-block;
    padding:4px 12px;
    font-size:.8rem;
    font-weight:600;
}}

.warning{{
    background:var(--warning-chip-background);
    border:1px solid var(--warning-chip-border);
    color:var(--primary-text-color);
    padding:18px 20px; /* Increased padding */
    border-radius:12px;
    margin-top:18px;
    font-weight:700;
    font-size: 1.1rem; /* Increased text size */
}}

/* ------------------------------------------------ */
/* Button */
/* ------------------------------------------------ */

.stButton button{{

    background:var(--accent-color) !important;

    color:var(--card-background-color) !important;

    border:none !important;

    border-radius:20px !important;

    font-size:1rem !important;

    font-weight:700 !important;

    height:64px;

    transition:.2s;

}}

.stButton button:hover{{

    background:var(--accent-hover-color) !important;

}}
.banner{{
    background:var(--banner-background);
    color:var(--banner-text-color);
    padding:20px; /* Increased padding */
    border-radius:16px;
    font-weight:600;
    margin-bottom:18px;
    font-size: 1.1rem; /* Increased text size */
}}

.cta-row{{
    align-items:center;
    display:grid;
    gap:22px;
    grid-template-columns:minmax(260px, 340px) 1fr;
    margin-top:6px;
}}

.live-note{{
    color:var(--secondary-text-color);
    font-size:.96rem;
    font-weight:700;
}}

.live-note span{{
    color:var(--accent-color);
}}

.results-heading{{
    margin-top:72px;
}}

.results-heading .kicker{{
    color:var(--accent-color);
    font-size:.78rem;
    font-weight:850;
    letter-spacing:4px;
    text-transform:uppercase;
}}

.results-heading h2{{
    color:var(--primary-text-color);
    font-size:4rem;
    line-height:1.02;
    margin:18px 0 10px 0;
}}

.results-heading h2 span{{
    color:var(--accent-color);
    font-style:italic;
}}

.results-context{{
    color:var(--secondary-text-color);
    font-size:1.05rem;
    font-weight:650;
}}

@media (max-width: 760px){{
    .hero h1{{
        font-size:3.6rem;
    }}

    h2.priority-heading,
    .results-heading h2{{
        font-size:2.4rem;
    }}

    .metric-grid{{
        grid-template-columns:1fr;
    }}

    div[class*="st-key-select_"] .stButton button{{
        height:auto;
        min-height:132px;
    }}
}}

</style>
""",
unsafe_allow_html=True,
)


# ------------------------------------------------------------
# Header
# ------------------------------------------------------------

logo_col, title_col, nav_col = st.columns([0.9, 5, 4])

with logo_col:
    st.image(str(LOGO_PATH), width=70)

with title_col:
    st.markdown(
        """
        <div class="brand-name">SKIP</div>
        <div class="brand-subtitle">
        Predictive Accessible Journey Planner
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav_col:
    st.markdown(
        """
        <div class="nav-links">
            <span>Plan a journey</span>
            <span>How SKIP works</span>
            <span>Accessibility</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
f"""
<div class="hero">

<p style="
letter-spacing:3px;
font-size:.78rem;
color:var(--accent-color);
font-weight:700;
text-transform:uppercase;
margin-bottom:26px;
">
Predictive Routing • London Underground
</p>

<h1>
Know <span style="color:var(--accent-color);">before</span><br>
you go.
</h1>

<p>
SKIP predicts and ranks Underground routes around what matters most to you —
punctuality, accessibility, or comfort.
</p>

</div>
""",
unsafe_allow_html=True,
)
# ------------------------------------------------------------
# Journey Planner
# ------------------------------------------------------------

st.markdown(
    '<h2 class="planner-title">Plan your journey</h2>',
    unsafe_allow_html=True,
)
left, right = st.columns(2)

with left:
    from_station = st.selectbox(
        "From",
        STATIONS,
        index=0,
    )

with right:
    to_station = st.selectbox(
        "To",
        STATIONS,
        index=1,
    )

col1, col2 = st.columns(2)

with col1:
    travel_date = st.date_input(
        "Travel Date",
        datetime.today(),
    )

with col2:
    travel_time = st.time_input(
        "Departure Time",
        datetime.now().time(),
    )

# ------------------------------------------------------------
# Journey Goal
# ------------------------------------------------------------

st.markdown(
    f"""
    <h2 class="priority-heading">What matters most on <span style="color:var(--accent-color);">this</span> journey?</h2>
    """,
    unsafe_allow_html=True,
)
if "goal" not in st.session_state:
    st.session_state.goal = "accessibility"

goal_options = [
    {
        "key": "punctuality",
        "label": "Punctuality",
        "icon": ":material/schedule:",
        "copy": "Fewer surprises.",
    },
    {
        "key": "accessibility",
        "label": "Accessibility",
        "icon": ":material/accessible_forward:",
        "copy": "Fewer barriers.",
    },
    {
        "key": "comfort",
        "label": "Comfort",
        "icon": ":material/chair:",
        "copy": "Easier journeys.",
    },
]

goal_cols = st.columns(3)
for col, option in zip(goal_cols, goal_options):
    selected = st.session_state.goal == option["key"]
    button_label = (
        f"**{option['label']}**\n\n"
        f"{option['copy']}"
    )

    with col:
        if st.button(
            button_label,
            key=f"select_{option['key']}",
            use_container_width=True,
            type="primary" if selected else "secondary",
            icon=option["icon"],
        ):
            st.session_state.goal = option["key"]
            st.rerun()

selected_goal = st.session_state.goal

# ------------------------------------------------------------
# Plan Button
# ------------------------------------------------------------

cta_col, note_col = st.columns([1.2, 2.4], vertical_alignment="center")

with cta_col:
    plan = st.button(
        "Find My Routes ->",
        use_container_width=True,
        type="primary",
    )

with note_col:
    st.markdown(
        '<div class="live-note"><span>✣</span> Predictions updated moments ago · TfL live data</div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------------------
# Placeholder
# (This will be replaced with serve())
# ------------------------------------------------------------


# ------------------------------------------------------------
# Recommendation Engine
# ------------------------------------------------------------

if plan:

    #
    # Phase 6 Integration
    #
    # Replace this block with:
    #
    # results = serve(
    #     from_station,
    #     to_station,
    #     goal
    # )
    #
    # Everything below simply renders the
    # output returned by serve().
    #

    goal_label = selected_goal.title()

    results = [
        {
            "rank": 1,
            "label": "Best Match",
            "route": [
                from_station,
                "Westminster",
                to_station,
            ],
            "pac_score": 0.78,
            "probability": 0.86,
            "stops": 8,
            "interchanges": 1,
            "flag": "ok",
            "summary": "Strong accessibility match with fewer interchanges and favourable lift conditions.",
            "good": [
                "Step-free priority",
                "Lift conditions favourable",
                "Fewer interchanges",
            ],
            "warning": "Moderate crowding",
            "why": (
                "SKIP weighs live lift status, predicted crowding at each interchange "
                "and historical disruption for this corridor. Given your priority, "
                "this option balances a strong step-free profile with a low predicted "
                "delay risk over the next 45 minutes."
            ),
            "banner": None,
        },
        {
            "rank": 2,
            "label": "Option 2",
            "route": [
                from_station,
                f"{from_station} Jubilee",
                "Canada Water",
                to_station,
            ],
            "pac_score": 0.71,
            "probability": 0.74,
            "stops": 9,
            "interchanges": 1,
            "flag": "ok",
            "summary": "Reliable Jubilee line routing with slightly longer walking transfer at interchange.",
            "good": [
                "Step-free at boarding",
                "Predicted low disruption",
            ],
            "warning": "Longer platform walk",
            "why": (
                "A steady alternative with good reliability signals, though the transfer "
                "walk is less ideal for this selected priority."
            ),
            "banner": None,
        },
        {
            "rank": 3,
            "label": "Compromise",
            "route": [
                from_station,
                "Bond Street",
                "Bank",
                to_station,
            ],
            "pac_score": 0.52,
            "probability": 0.48,
            "stops": 10,
            "interchanges": 2,
            "flag": "compromise",
            "summary": "Fastest predicted routing but weaker match against your selected priority.",
            "good": [
                "Frequent service",
            ],
            "warning": "Partial step-free access",
            "why": (
                "This route is shown as a closest match but may not fully meet your "
                "selected priority."  # Corrected string concatenation
            ),
            "banner": None,
        },
    ]

    # --------------------------------------------------------
    # Global Banner
    # --------------------------------------------------------

    if results and results[0].get("banner"):

        st.markdown(
            f"""
            <div class="banner">
                ⚠️ {results[0]["banner"]}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # Recommendations
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="results-heading">
            <div class="kicker">Recommended by SKIP</div>
            <h2>SKIP found<br><span>three</span> ways forward.</h2>
            <div class="results-context">
                {from_station} -> {to_station} · {travel_date.strftime("%d %b %Y")} ·
                {travel_time.strftime("%H:%M")} · Planning for {goal_label}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for route in results:

        probability = int(route["probability"] * 100)
        card_class = "route-card compromise" if route["flag"] == "compromise" else "route-card"
        route_path = " -> ".join(escape(stop) for stop in route["route"])
        chip_html = "".join(
            f'<span class="chip">✓ {escape(chip)}</span>' for chip in route["good"]
        )
        if route.get("warning"):
            chip_html += f'<span class="chip warning-chip">△ {escape(route["warning"])}</span>'
        compromise_html = ""
        if route["flag"] == "compromise":
            compromise_html = (
                '<div class="warning">△ This route is shown as a closest match '
                'but may not fully meet your selected priority.</div>'
            )

        st.html(
            (
                f'<div class="{card_class}">'
                f'<div class="route-eyebrow">{escape(route["label"])} · '
                f'<span>{probability}% Model Confidence</span></div>'
                f'<div class="route-title">{route_path}</div>'
                f'<p class="route-subtitle">{escape(route["summary"])}</p>'
                f'{compromise_html}'
                '<div class="route-divider"></div>'
                '<div class="metric-grid">'
                '<div><div class="metric-label">SKIP Score</div>'
                f'<div class="metric-value">{route["pac_score"]:.2f}</div></div>'
                '<div><div class="metric-label">Stops</div>'
                f'<div class="metric-value">{route["stops"]}</div></div>'
                '<div><div class="metric-label">Interchanges</div>'
                f'<div class="metric-value">{route["interchanges"]}</div></div>'
                '</div>'
                f'<div class="chip-row">{chip_html}</div>'
                '<p class="small">'
                '<b>Why SKIP recommends this route</b><br>'
                f'{escape(route["why"])}</p>'
                '</div>'
            )
        )