# ============================================================
# SKIP - Smart Knowledge-based Intelligent Planner
# Phase 6 Final Demonstration App 
# ============================================================

import base64

import streamlit as st
import pandas as pd
from datetime import datetime, time
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
LOGO_DATA_URI = "data:image/png;base64," + base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
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
# Accessible colour modes
# ------------------------------------------------------------

if "colour_blind_mode" not in st.session_state:
    st.session_state.colour_blind_mode = False

# Determine the accent color based on the toggle
ACCENT_COLOR = "#0072B2" if st.session_state.colour_blind_mode else "#17BEBB"
ACCENT_HOVER_COLOR = "#005B90" if st.session_state.colour_blind_mode else "#11A7A4" # Slightly darker for hover
ACCENT_LIGHT_COLOR = "#DDEBF6" if st.session_state.colour_blind_mode else "#DDF5F3" # Lighter for primary button background
ACCENT_LIGHTER_COLOR = "#BADCEF" if st.session_state.colour_blind_mode else "#BFE8E6" # Lighter for chip borders
BACKGROUND_COLOR = "#FFFFFF" if st.session_state.colour_blind_mode else "#FBFAF6"
BACKGROUND_TOP_COLOR = "#FFFFFF" if st.session_state.colour_blind_mode else "#EAF8FD"
BACKGROUND_MID_COLOR = "#FFFFFF" if st.session_state.colour_blind_mode else "#F5FAF8"
PRIMARY_TEXT_COLOR = "#001A35" if st.session_state.colour_blind_mode else "#11284D"
SECONDARY_TEXT_COLOR = "#334155" if st.session_state.colour_blind_mode else "#6E7891"
FIELD_BORDER_COLOR = "#475569" if st.session_state.colour_blind_mode else "#CBD5E1"

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
    --background-color: {BACKGROUND_COLOR};
    --card-background-color: #FFFFFF;
    --primary-text-color: {PRIMARY_TEXT_COLOR};
    --secondary-text-color: {SECONDARY_TEXT_COLOR};
    --border-color: #D9E2EC;
    --field-border-color: {FIELD_BORDER_COLOR};
    --field-text-color: #102A43;
    --field-placeholder-color: #66788A;
    --field-focus-ring: {hex_to_rgba(ACCENT_COLOR, 0.24)};
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
header[data-testid="stHeader"] {{visibility:hidden;}}

.block-container{{
    max-width:1100px;
    padding-top:1rem;
    padding-left:2rem;
    padding-right:2rem;
    padding-bottom:4rem;
}}

.stApp{{
    background:
        linear-gradient(180deg, {BACKGROUND_TOP_COLOR} 0, {BACKGROUND_MID_COLOR} 25rem, var(--background-color) 43rem) !important;
    color:var(--primary-text-color) !important;
    color-scheme:light !important;
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
    font-size:.94rem !important;
    font-weight: 750 !important;
    letter-spacing:.01em;
    margin-bottom:.42rem !important;
    opacity: 1 !important;
}}

/* Specific styling for the Streamlit Toggle text */
.stToggle label span {{
    color: var(--primary-text-color) !important;
    font-size:1rem !important;
    font-weight:750 !important;
    opacity: 1 !important;

}}

/* Make the toggle visible even when it is switched off. */
.stToggle [role="switch"],
.stToggle [data-baseweb="checkbox"] > div {{
    background:#CBD5E1 !important;
    border:2px solid #64748B !important;
    opacity:1 !important;
}}

.stToggle [role="switch"][aria-checked="true"],
.stToggle input:checked + div {{
    background:var(--accent-color) !important;
    border-color:var(--accent-color) !important;
}}

.stToggle [role="switch"] > div,
.stToggle [data-baseweb="checkbox"] > div > div {{
    background:#FFFFFF !important;
    box-shadow:0 1px 4px rgba(17,40,77,.35) !important;
}}

/* Current Streamlit renders st.toggle through its checkbox component. */
label:has(input[role="switch"]) > div:first-of-type {{
    align-items:center !important;
    background:#CBD5E1 !important;
    border:2px solid #64748B !important;
    border-radius:999px !important;
    box-sizing:border-box !important;
    display:flex !important;
    flex:0 0 auto !important;
    height:1.55rem !important;
    padding:2px !important;
    transition:background .18s ease, border-color .18s ease, box-shadow .18s ease !important;
    width:2.8rem !important;
}}

label:has(input[role="switch"]) > div:first-of-type > div {{
    background:#FFFFFF !important;
    border-radius:50% !important;
    box-shadow:0 1px 4px rgba(17,40,77,.35) !important;
    height:1rem !important;
    transform:translateX(0) !important;
    transition:transform .18s ease !important;
    width:1rem !important;
}}

label > span:has(input[role="switch"]:checked) + div {{
    background:var(--accent-color) !important;
    border-color:var(--accent-color) !important;
}}

label > span:has(input[role="switch"]:checked) + div > div {{
    transform:translateX(1.2rem) !important;
}}

label:has(input[role="switch"]:focus-visible) > div:first-of-type {{
    box-shadow:0 0 0 4px var(--field-focus-ring) !important;
}}

/* Select boxes */

.stSelectbox > div > div{{
    background:var(--card-background-color) !important;
    border:2px solid var(--field-border-color) !important;
    border-radius:16px !important;
    min-height:56px;
}}

/* Keep selected values and dropdown options readable. Streamlit renders the
   open menu in a BaseWeb portal outside the selectbox container, so it needs
   explicit colours as well as the widget itself. */
.stSelectbox [data-baseweb="select"],
.stSelectbox [data-baseweb="select"] > div {{
    background:#FFFFFF !important;
    border-radius:16px !important;
}}

.stSelectbox [data-baseweb="select"] *,
.stSelectbox [data-baseweb="select"] input {{
    color:var(--field-text-color) !important;
    -webkit-text-fill-color:var(--field-text-color) !important;
    font-weight:650 !important;
    opacity:1 !important;
}}

/* Selected value displayed in the closed selectbox */
.stSelectbox [data-baseweb="select"] > div > div,
.stSelectbox [data-baseweb="select"] > div > div * {{
    color:#000000 !important;
    -webkit-text-fill-color:#000000 !important;
    opacity:1 !important;
}}

.stSelectbox [data-baseweb="select"] svg {{
    color:#11284D !important;
    fill:#11284D !important;
}}

div[data-baseweb="popover"] > div,
ul[data-baseweb="menu"],
div[data-baseweb="menu"],
[role="listbox"] {{
    background:#FFFFFF !important;
    color:#11284D !important;
}}

[role="option"],
[role="option"] * {{
    background:#FFFFFF !important;
    color:#11284D !important;
    -webkit-text-fill-color:#11284D !important;
    opacity:1 !important;
}}

[role="option"]:hover,
[role="option"]:hover *,
[role="option"][aria-selected="true"],
[role="option"][aria-selected="true"] * {{
    background:#DDF8F6 !important;
    color:#11284D !important;
    -webkit-text-fill-color:#11284D !important;
}}

.stSelectbox [data-baseweb="select"] > div:focus-within,
.stDateInput [data-baseweb="input"] > div:focus-within,
.stTimeInput [data-baseweb="input"] > div:focus-within {{
    border-color:var(--accent-color) !important;
    box-shadow:0 0 0 2px var(--accent-light-color) !important;
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
    color:#000000 !important;
    -webkit-text-fill-color:#000000 !important;
    opacity:1 !important;
}}

/* Streamlit may generate different wrapper classes between releases. Target
   its stable widget IDs so every entered or selected value stays black. */
html body .stApp [data-testid="stSelectbox"] [data-baseweb="select"],
html body .stApp [data-testid="stSelectbox"] [data-baseweb="select"] div,
html body .stApp [data-testid="stSelectbox"] [data-baseweb="select"] span,
html body .stApp [data-testid="stSelectbox"] [data-baseweb="select"] p,
html body .stApp [data-testid="stSelectbox"] [data-baseweb="select"] input,
html body .stApp [data-testid="stDateInput"] input,
html body .stApp [data-testid="stTimeInput"] input {{
    color:#000000 !important;
    -webkit-text-fill-color:#000000 !important;
    opacity:1 !important;
    text-shadow:none !important;
}}

html body .stApp [data-testid="stSelectbox"] [data-baseweb="select"] input:disabled,
html body .stApp [data-testid="stDateInput"] input:disabled,
html body .stApp [data-testid="stTimeInput"] input:disabled {{
    color:#000000 !important;
    -webkit-text-fill-color:#000000 !important;
    opacity:1 !important;
}}

.stDateInput input::placeholder,
.stTimeInput input::placeholder,
.stSelectbox input::placeholder {{
    color:var(--secondary-text-color) !important;
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
    margin-bottom:18px;
}}

/* Durable field styling across Streamlit/BaseWeb releases. These selectors use
   widget test IDs and semantic input roles rather than generated class names. */
[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stDateInput"] [data-baseweb="input"] > div,
[data-testid="stTimeInput"] [data-baseweb="input"] > div {{
    background:#FFFFFF !important;
    border:2px solid var(--field-border-color) !important;
    border-radius:14px !important;
    box-shadow:0 2px 6px rgba(11,31,58,.06) !important;
    min-height:54px !important;
    transition:border-color .16s ease, box-shadow .16s ease, background .16s ease;
}}

[data-testid="stSelectbox"] [data-baseweb="select"] > div:hover,
[data-testid="stDateInput"] [data-baseweb="input"] > div:hover,
[data-testid="stTimeInput"] [data-baseweb="input"] > div:hover {{
    border-color:#607891 !important;
}}

[data-testid="stSelectbox"] [data-baseweb="select"] > div:focus-within,
[data-testid="stDateInput"] [data-baseweb="input"] > div:focus-within,
[data-testid="stTimeInput"] [data-baseweb="input"] > div:focus-within {{
    border-color:var(--accent-color) !important;
    box-shadow:0 0 0 4px var(--field-focus-ring), 0 3px 9px rgba(11,31,58,.08) !important;
    outline:none !important;
}}

[data-testid="stSelectbox"] [data-baseweb="select"] span,
[data-testid="stSelectbox"] [data-baseweb="select"] input,
[data-testid="stDateInput"] input,
[data-testid="stTimeInput"] input {{
    background:transparent !important;
    color:var(--field-text-color) !important;
    -webkit-text-fill-color:var(--field-text-color) !important;
    caret-color:var(--accent-color) !important;
    font-size:1rem !important;
    font-weight:650 !important;
    opacity:1 !important;
}}

[data-testid="stDateInput"] input::placeholder,
[data-testid="stTimeInput"] input::placeholder,
[data-testid="stSelectbox"] input::placeholder {{
    color:var(--field-placeholder-color) !important;
    -webkit-text-fill-color:var(--field-placeholder-color) !important;
    opacity:1 !important;
}}

[data-testid="stSelectbox"] svg,
[data-testid="stDateInput"] svg,
[data-testid="stTimeInput"] svg {{
    color:var(--primary-text-color) !important;
    fill:currentColor !important;
}}

/* The select menu and date picker render in a portal outside the widget. */
[data-baseweb="popover"] [role="listbox"],
[data-baseweb="popover"] [role="dialog"],
[data-baseweb="calendar"] {{
    background:#FFFFFF !important;
    border:1px solid var(--field-border-color) !important;
    border-radius:12px !important;
    box-shadow:0 14px 35px rgba(11,31,58,.18) !important;
    color:var(--field-text-color) !important;
}}

/* React Aria calendar used by current Streamlit releases. The direct-parent
   selector also colours the popover shell without affecting app containers. */
div:has(> [role="application"][aria-label^="Choose date"]) {{
    background:#FFFFFF !important;
    border:1px solid var(--field-border-color) !important;
    border-radius:16px !important;
    box-shadow:0 16px 36px rgba(16,42,67,.18) !important;
    color:var(--field-text-color) !important;
}}

[role="application"][aria-label^="Choose date"] {{
    background:#FFFFFF !important;
    color:var(--field-text-color) !important;
}}

[role="application"][aria-label^="Choose date"] > header,
[role="application"][aria-label^="Choose date"] > header * {{
    color:var(--field-text-color) !important;
    visibility:visible !important;
}}

[role="application"][aria-label^="Choose date"] th,
[role="application"][aria-label^="Choose date"] [role="gridcell"] [role="button"] {{
    color:var(--field-text-color) !important;
}}

[role="application"][aria-label^="Choose date"] [role="gridcell"][aria-disabled="true"] [role="button"] {{
    color:#94A3B8 !important;
}}

[role="application"][aria-label^="Choose date"] [role="gridcell"][aria-selected="true"] [role="button"] {{
    background:var(--accent-color) !important;
    color:#FFFFFF !important;
}}

[role="option"] {{
    color:var(--field-text-color) !important;
    font-weight:600 !important;
}}

[role="option"]:focus-visible {{
    outline:3px solid var(--accent-color) !important;
    outline-offset:-3px;
}}

/* ------------------------------------------------ */
/* Lovable-inspired journey form                    */
/* ------------------------------------------------ */

.stApp,
.stApp input,
.stApp button {{
    font-family:Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}

div.st-key-journey_form {{
    background:#FFFFFF;
    border:1px solid #DDE5EC;
    border-radius:24px;
    box-shadow:0 14px 38px rgba(16,42,67,.08);
    margin:10px 0 46px;
    padding:30px 34px 16px;
}}

.journey-form-heading {{
    margin-bottom:14px;
}}

.journey-form-heading h2 {{
    color:var(--primary-text-color) !important;
    font-size:2rem;
    font-weight:800;
    letter-spacing:-.025em;
    line-height:1.2;
    margin:0 0 8px;
}}

.journey-form-heading p,
.field-help {{
    color:#66788A !important;
    font-size:.94rem;
    line-height:1.5;
    margin:0;
}}

.field-copy {{
    margin:4px 0 8px;
}}

.field-label {{
    color:var(--primary-text-color) !important;
    font-size:.94rem;
    font-weight:750;
    line-height:1.35;
    margin-bottom:3px;
}}

/* Streamlit 1.5x uses React Aria rather than BaseWeb for these controls. */
.stApp [data-testid="stSelectbox"] input[role="combobox"] {{
    background:transparent !important;
    color:var(--field-text-color) !important;
    -webkit-text-fill-color:var(--field-text-color) !important;
    caret-color:var(--accent-color) !important;
    font-size:1rem !important;
    font-weight:600 !important;
    opacity:1 !important;
}}

.stApp [data-testid="stDateInput"] [contenteditable="true"],
.stApp [data-testid="stTimeInput"] [contenteditable="true"],
.stApp [data-testid="stDateInput"] [role="group"] span,
.stApp [data-testid="stTimeInput"] [role="group"] span {{
    color:var(--field-text-color) !important;
    -webkit-text-fill-color:var(--field-text-color) !important;
    font-size:1rem !important;
    font-weight:600 !important;
    opacity:1 !important;
}}

.stApp [data-testid="stSelectbox"] input[role="combobox"]::placeholder {{
    color:var(--field-placeholder-color) !important;
    -webkit-text-fill-color:var(--field-placeholder-color) !important;
    opacity:1 !important;
}}

.stApp [data-testid="stSelectbox"] [role="group"],
.stApp [data-testid="stDateInputField"],
.stApp [data-testid="stTimeInputTimeDisplay"] {{
    background:#FFFFFF !important;
    border:1.5px solid var(--field-border-color) !important;
    border-radius:14px !important;
    box-shadow:0 1px 3px rgba(16,42,67,.04) !important;
    min-height:52px !important;
    transition:border-color .16s ease, box-shadow .16s ease !important;
}}

.stApp [data-testid="stSelectbox"] [role="group"]:hover,
.stApp [data-testid="stDateInputField"]:hover,
.stApp [data-testid="stTimeInputTimeDisplay"]:hover {{
    border-color:#91A3B8 !important;
}}

.stApp [data-testid="stSelectbox"] [role="group"]:focus-within,
.stApp [data-testid="stDateInputField"]:focus-within,
.stApp [data-testid="stTimeInputTimeDisplay"]:focus-within {{
    border-color:var(--accent-color) !important;
    box-shadow:0 0 0 4px var(--field-focus-ring) !important;
    outline:none !important;
}}

.stApp [data-testid="stSelectbox"] button,
.stApp [data-testid="stDateInput"] svg,
.stApp [data-testid="stTimeInput"] svg {{
    color:var(--primary-text-color) !important;
}}

.stApp [data-testid="stSelectbox"],
.stApp [data-testid="stDateInput"],
.stApp [data-testid="stTimeInput"] {{
    margin-bottom:16px;
}}

@media (max-width:700px) {{
    div.st-key-journey_form {{
        border-radius:20px;
        padding:24px 20px 10px;
    }}
}}

@media (max-width: 700px) {{
    .block-container {{
        padding-left:1rem;
        padding-right:1rem;
    }}

    .brand-bar {{
        gap:10px;
    }}

    .brand-logo {{
        height:44px;
        width:44px;
    }}

    .brand-subtitle {{
        font-size:.54rem;
        letter-spacing:.12em;
        white-space:normal;
    }}

    div.st-key-site_header .stToggle label span {{
        font-size:.82rem !important;
    }}

    .hero h1 {{
        font-size:3.5rem;
    }}
}}
/* ---------- Hero ---------- */

.hero{{
    background:transparent;
    box-shadow:none;
    border-radius:0;
    padding:30px 0 34px;
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

div.st-key-site_header {{
    border-bottom:1px solid rgba(145,163,184,.34);
    margin:4px 0 0;
    padding:8px 0 16px;
}}

div.st-key-site_header [data-testid="stHorizontalBlock"] {{
    align-items:center;
}}

.brand-bar{{
    align-items:center;
    align-self:flex-start;
    display:inline-flex;
    gap:13px;
    margin:0;
    padding:0;
    width:auto;
}}

.brand-logo{{
    width:50px;
    height:50px;
    object-fit:contain;
    border:none;
    border-radius:0;
    display:block;
    filter:drop-shadow(0 3px 6px rgba(16,42,67,.10));
    flex:0 0 auto;
}}

.brand-copy{{
    min-width:0;
}}

.brand-name{{
    color:var(--primary-text-color);
    font-size:1.12rem;
    font-weight:800;
    letter-spacing:-.01em;
    line-height:1.1;
    margin-bottom:6px;
}}

.brand-subtitle{{
    color:#697B8F;
    font-size:.61rem;
    font-weight:750;
    letter-spacing:.19em;
    line-height:1.45;
    text-transform:uppercase;
    white-space:nowrap;
}}

div.st-key-site_header [data-testid="stToggle"] {{
    display:flex;
    justify-content:flex-end;
    margin:0;
}}

div.st-key-site_header .stToggle label {{
    justify-content:flex-end;
    white-space:nowrap;
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
    align-items:center;
    background:var(--card-background-color) !important;
    border:2px solid var(--border-color) !important;
    border-radius:18px !important;
    box-shadow:0 8px 18px rgba(8,28,58,.06) !important;
    color:var(--primary-text-color) !important;
    display:flex;
    font-size:1.2rem !important;
    font-weight:700 !important; /* Semi-bold for button text */
    height:166px;
    justify-content:center;
    line-height:1.35;
    padding:30px 28px !important;
    text-align:center;
    white-space:pre-line;
    width:100%;
}}

div[class*="st-key-select_"] .stButton button p{{
    color:var(--primary-text-color) !important;
    font-size:1.18rem !important;
    line-height:1.35;
    margin:0;
    font-weight: 700; /* Explicitly ensure label text is semi-bold */
    text-align:center !important;
}}

div[class*="st-key-select_"] .stButton button span[data-testid^="stIcon"]{{
    font-size:32px; /* Increased icon size */
    margin-right:14px;
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

with st.container(key="site_header"):
    brand_col, contrast_col = st.columns([5, 2], vertical_alignment="center")

    with brand_col:
        st.markdown(
            f"""
            <div class="brand-bar" aria-label="SKIP — Predictive Accessible Journey Planner">
                <img class="brand-logo" src="{LOGO_DATA_URI}" alt="SKIP logo">
                <div class="brand-copy">
                    <div class="brand-name">SKIP</div>
                    <div class="brand-subtitle">Predictive Accessible Journey Planner</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with contrast_col:
        st.toggle(
            "High contrast",
            key="colour_blind_mode",
            help="Increase text, control, and focus contrast throughout the planner.",
        )

st.markdown(
f"""
<div class="hero">

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

with st.container(key="journey_form"):
    st.markdown(
        """
        <div class="journey-form-heading">
            <h2>Plan your journey</h2>
            <p>Choose your route and when you would like to travel.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)

    with left:
        st.markdown(
            '<div class="field-copy"><div class="field-label">From</div>'
            '<div class="field-help">Choose your starting station.</div></div>',
            unsafe_allow_html=True,
        )
        from_station = st.selectbox(
            "From",
            STATIONS,
            index=0,
            label_visibility="collapsed",
        )

    with right:
        st.markdown(
            '<div class="field-copy"><div class="field-label">To</div>'
            '<div class="field-help">Choose your destination station.</div></div>',
            unsafe_allow_html=True,
        )
        to_station = st.selectbox(
            "To",
            STATIONS,
            index=1,
            label_visibility="collapsed",
        )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="field-copy"><div class="field-label">Travel date</div>'
            '<div class="field-help">Select the day of your journey.</div></div>',
            unsafe_allow_html=True,
        )
        travel_date = st.date_input(
            "Travel Date",
            datetime.today(),
            format="DD/MM/YYYY",
            label_visibility="collapsed",
        )

    with col2:
        st.markdown(
            '<div class="field-copy"><div class="field-label">Departure time</div>'
            '<div class="field-help">Choose when you plan to leave.</div></div>',
            unsafe_allow_html=True,
        )
        time_slots = [time(hour, minute) for hour in range(24) for minute in (0, 15, 30, 45)]
        now = datetime.now()
        default_time_index = min((now.hour * 60 + now.minute) // 15, len(time_slots) - 1)
        travel_time = st.selectbox(
            "Departure Time",
            time_slots,
            index=default_time_index,
            format_func=lambda value: value.strftime("%H:%M"),
            label_visibility="collapsed",
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
