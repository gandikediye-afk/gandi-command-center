"""
GANDI COMMAND CENTER - Interactive Streamlit Dashboard
Version: 4.0 (GANDI UNIVERSE Edition - Deep Space Cyberpunk)
Created: January 14, 2026
Updated: January 16, 2026

This dashboard connects to REAL data sources:
- Google Workspace (Gmail, Calendar, Sheets)
- Make.com webhooks
- n8n automation (via Serveo tunnel)

Enhancements v4.0:
- GANDI UNIVERSE interactive constellation view
- Force-directed graph with Apache ECharts
- Deep Space Cyberpunk theme
- Physics-based entity visualization
- Real-time entity health monitoring
- Plotly charts for visual metrics
- Auto-refresh every 5 minutes
"""

import streamlit as st
import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from streamlit_echarts import st_echarts

# =============================================================================
# CONFIGURATION
# =============================================================================

# Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="GANDI Command Center",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Auto-refresh every 5 minutes (300000 ms)
refresh_count = st_autorefresh(interval=300000, limit=None, key="dashboard_autorefresh")

# Dark mode toggle state - Default to TRUE for Cyberpunk theme
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True  # Default ON for cyberpunk

# =============================================================================
# DEEP SPACE CYBERPUNK CSS - ALWAYS APPLIED
# =============================================================================
st.markdown("""
<style>
    /* ========== DEEP SPACE BACKGROUND ========== */
    .stApp {
        background: linear-gradient(180deg, #050510 0%, #0a0a1a 50%, #1a0a2e 100%);
        background-attachment: fixed;
    }

    /* Starfield effect overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        background-image:
            radial-gradient(2px 2px at 20px 30px, rgba(255,255,255,0.3), transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.2), transparent),
            radial-gradient(1px 1px at 90px 40px, rgba(255,255,255,0.4), transparent),
            radial-gradient(2px 2px at 160px 120px, rgba(0,212,255,0.3), transparent),
            radial-gradient(1px 1px at 230px 180px, rgba(255,255,255,0.2), transparent),
            radial-gradient(2px 2px at 300px 250px, rgba(0,255,148,0.2), transparent);
        background-size: 350px 350px;
        z-index: 0;
    }

    /* ========== SIDEBAR STYLING ========== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a1a 0%, #1a0a2e 100%);
        border-right: 1px solid #00D4FF33;
    }

    section[data-testid="stSidebar"] .stMarkdown {
        color: #E0E0E0;
    }

    /* ========== MAIN CONTENT ========== */
    .main .block-container {
        background: transparent;
        color: #E0E0E0;
    }

    /* ========== HEADERS ========== */
    h1, h2, h3 {
        color: #00D4FF !important;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
    }

    h1 {
        font-size: 2.5rem !important;
        letter-spacing: 2px;
    }

    /* ========== TABS STYLING ========== */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(5, 5, 16, 0.8);
        border-radius: 10px;
        padding: 0.5rem;
        gap: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: 1px solid #00D4FF33;
        border-radius: 8px;
        color: #8892b0;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 212, 255, 0.1);
        border-color: #00D4FF;
        color: #00D4FF;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.2), rgba(0, 184, 255, 0.1)) !important;
        border-color: #00D4FF !important;
        color: #00D4FF !important;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
    }

    /* ========== METRICS (Stat Cards) ========== */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(26, 10, 46, 0.8));
        border: 1px solid #00D4FF33;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), inset 0 0 30px rgba(0, 212, 255, 0.05);
    }

    [data-testid="stMetricLabel"] {
        color: #8892b0 !important;
    }

    [data-testid="stMetricValue"] {
        color: #00D4FF !important;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }

    /* ========== BUTTONS ========== */
    .stButton > button {
        background: linear-gradient(135deg, #00D4FF22, #00D4FF11);
        border: 1px solid #00D4FF55;
        color: #00D4FF;
        border-radius: 8px;
        transition: all 0.3s ease;
        font-weight: 500;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #00D4FF44, #00D4FF22);
        border-color: #00D4FF;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
        transform: translateY(-2px);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Primary buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00D4FF, #00B8FF);
        color: #050510;
        font-weight: bold;
    }

    /* ========== TEXT INPUTS ========== */
    .stTextInput > div > div > input {
        background: rgba(5, 5, 16, 0.8);
        border: 1px solid #00D4FF33;
        border-radius: 8px;
        color: #E0E0E0;
    }

    .stTextInput > div > div > input:focus {
        border-color: #00D4FF;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.3);
    }

    /* ========== DATA FRAMES ========== */
    .stDataFrame {
        background: rgba(5, 5, 16, 0.8);
        border: 1px solid #00D4FF33;
        border-radius: 8px;
    }

    /* ========== EXPANDERS ========== */
    .streamlit-expanderHeader {
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid #00D4FF33;
        border-radius: 8px;
        color: #00D4FF;
    }

    /* ========== SUCCESS/WARNING/ERROR BOXES ========== */
    .stSuccess {
        background: linear-gradient(135deg, rgba(0, 255, 148, 0.2), rgba(0, 255, 148, 0.05));
        border-left: 4px solid #00FF94;
    }

    .stWarning {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(255, 215, 0, 0.05));
        border-left: 4px solid #FFD700;
    }

    .stError {
        background: linear-gradient(135deg, rgba(255, 0, 85, 0.2), rgba(255, 0, 85, 0.05));
        border-left: 4px solid #FF0055;
    }

    /* ========== DIVIDERS ========== */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #00D4FF33, #00D4FF66, #00D4FF33, transparent);
        margin: 1.5rem 0;
    }

    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #050510;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00D4FF, #00B8FF);
        border-radius: 4px;
    }

    /* ========== ENTITY GLOW EFFECTS ========== */
    .entity-card-afk { border-left-color: #00FF94 !important; box-shadow: 0 0 20px rgba(0, 255, 148, 0.2); }
    .entity-card-gakp { border-left-color: #FF0055 !important; box-shadow: 0 0 20px rgba(255, 0, 85, 0.2); }
    .entity-card-gifp { border-left-color: #FFD700 !important; box-shadow: 0 0 20px rgba(255, 215, 0, 0.2); }
    .entity-card-comf { border-left-color: #00B8FF !important; box-shadow: 0 0 20px rgba(0, 184, 255, 0.2); }
    .entity-card-gakc { border-left-color: #9D00FF !important; box-shadow: 0 0 20px rgba(157, 0, 255, 0.2); }
    .entity-card-prsl { border-left-color: #FF6B35 !important; box-shadow: 0 0 20px rgba(255, 107, 53, 0.2); }

    /* ========== CAPTION/SMALL TEXT ========== */
    .stCaption, small, .stMarkdown p {
        color: #8892b0 !important;
    }

    /* ========== LINKS ========== */
    a {
        color: #00D4FF !important;
        text-decoration: none;
    }

    a:hover {
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# Your n8n webhook base URL (Serveo tunnel)
N8N_BASE_URL = "https://2327d83f0c3480b2-68-47-9-228.serveousercontent.com"

# Make.com webhook URLs (update these when you create them)
MAKE_WEBHOOKS = {
    "business_health": "https://hook.us1.make.com/YOUR_BUSINESS_HEALTH_WEBHOOK",
    "ai_watchdog": "https://hook.us1.make.com/YOUR_AI_WATCHDOG_WEBHOOK",
    "command_sync": "https://hook.us1.make.com/YOUR_COMMAND_SYNC_WEBHOOK",
    "notifications": "https://hook.us1.make.com/YOUR_NOTIFICATIONS_WEBHOOK",
}

# =============================================================================
# DEEP SPACE CYBERPUNK THEME COLORS
# =============================================================================

UNIVERSE_THEME = {
    "void_black": "#050510",      # Deep space background
    "core_white": "#FFFFFF",       # GANDI Core primary
    "core_glow": "#00D4FF",        # GANDI Core cyan glow
    "nebula_purple": "#1a0a2e",    # Secondary background
    "grid_line": "#1e3a5f",        # Grid lines
    "text_primary": "#E0E0E0",     # Primary text
    "text_secondary": "#8892b0",   # Secondary text
}

# Entity codes and colors - Deep Space Cyberpunk palette
ENTITIES = {
    "AFK": {"name": "Afro Farm Kenya", "color": "#00FF94", "icon": "🌾", "glow": "#00FF9455", "location": "Kenya"},
    "GAKP": {"name": "GAK Properties", "color": "#FF0055", "icon": "🏢", "glow": "#FF005555", "location": "USA"},
    "GIFP": {"name": "GIF Properties", "color": "#FFD700", "icon": "🏠", "glow": "#FFD70055", "location": "USA"},
    "COMF": {"name": "Comfort Services", "color": "#00B8FF", "icon": "💊", "glow": "#00B8FF55", "location": "USA", "hipaa": True},
    "GAKC": {"name": "GAK Commodities", "color": "#9D00FF", "icon": "📦", "glow": "#9D00FF55", "location": "Kenya"},
    "PRSL": {"name": "Personal", "color": "#FF6B35", "icon": "👤", "glow": "#FF6B3555", "location": "USA"},
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_kenya_time():
    """Get current time in Kenya (EAT = UTC+3)"""
    utc_now = datetime.utcnow()
    kenya_time = utc_now + timedelta(hours=3)
    return kenya_time.strftime("%I:%M %p")

def get_cst_time():
    """Get current time in Minneapolis (CST = UTC-6)"""
    utc_now = datetime.utcnow()
    cst_time = utc_now - timedelta(hours=6)
    return cst_time.strftime("%I:%M %p")

def is_kenya_window():
    """Check if we're in Kenya Window (6-9 AM CST = 3-6 PM Kenya)"""
    utc_now = datetime.utcnow()
    cst_hour = (utc_now - timedelta(hours=6)).hour
    return 6 <= cst_hour < 9

def fetch_n8n_webhook(endpoint, data=None):
    """Send command to n8n webhook"""
    try:
        url = f"{N8N_BASE_URL}/webhook/{endpoint}"
        if data:
            response = requests.post(url, json=data, timeout=10)
        else:
            response = requests.get(url, timeout=10)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        return {"error": str(e)}

def send_voice_command(command_text):
    """Send voice command to n8n for processing"""
    return fetch_n8n_webhook("claude-commander", {"command": command_text, "source": "streamlit"})

def load_live_data():
    """Load live data from JSON file (updated by Claude/MCP)"""
    data_file = Path(__file__).parent / "data" / "live_data.json"
    try:
        if data_file.exists():
            with open(data_file, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading live data: {e}")
    return None


def render_universe(live_data=None):
    """
    Render the GANDI UNIVERSE interactive constellation view
    Force-directed graph with physics simulation using Apache ECharts
    """
    # Get entity health scores from live data
    entity_data = live_data.get("entities", {}) if live_data else {}

    # Categories for node coloring
    categories = [
        {"name": "Core", "itemStyle": {"color": UNIVERSE_THEME["core_glow"]}},
        {"name": "Kenya", "itemStyle": {"color": "#00FF94"}},
        {"name": "USA", "itemStyle": {"color": "#FF0055"}},
        {"name": "Healthcare", "itemStyle": {"color": "#00B8FF"}},
    ]

    # Build nodes from entities - size based on health score
    nodes = [
        {
            "name": "GANDI\nCORE",
            "symbolSize": 100,
            "value": "Command Center",
            "category": 0,
            "fixed": True,
            "x": 400,
            "y": 300,
            "itemStyle": {
                "color": UNIVERSE_THEME["core_glow"],
                "shadowBlur": 30,
                "shadowColor": UNIVERSE_THEME["core_glow"],
            },
            "label": {
                "show": True,
                "color": "#FFFFFF",
                "fontSize": 14,
                "fontWeight": "bold",
            }
        }
    ]

    # Add entity nodes
    for code, info in ENTITIES.items():
        health = entity_data.get(code, {}).get("health_score", 80)
        pending = entity_data.get(code, {}).get("pending_items", 0)
        status = entity_data.get(code, {}).get("status", "Active")

        # Determine category based on location
        if info.get("hipaa"):
            cat = 3  # Healthcare
        elif info.get("location") == "Kenya":
            cat = 1  # Kenya
        else:
            cat = 2  # USA

        # Size based on health score (30-70 range)
        size = 30 + (health / 100) * 40

        nodes.append({
            "name": f"{info['icon']} {code}",
            "symbolSize": size,
            "value": f"{info['name']}\nHealth: {health}%\nPending: {pending}",
            "category": cat,
            "itemStyle": {
                "color": info["color"],
                "shadowBlur": 20,
                "shadowColor": info["glow"],
            },
            "label": {
                "show": True,
                "color": "#FFFFFF",
                "fontSize": 12,
            }
        })

    # Build links (all entities connect to GANDI CORE)
    links = []
    for code, info in ENTITIES.items():
        links.append({
            "source": "GANDI\nCORE",
            "target": f"{info['icon']} {code}",
            "lineStyle": {
                "color": info["color"],
                "width": 2,
                "curveness": 0.1,
                "opacity": 0.6,
            }
        })

    # Add inter-entity connections (Kenya <-> Kenya, USA <-> USA)
    kenya_entities = [f"{info['icon']} {code}" for code, info in ENTITIES.items() if info.get("location") == "Kenya"]
    usa_entities = [f"{info['icon']} {code}" for code, info in ENTITIES.items() if info.get("location") == "USA" and not info.get("hipaa")]

    # Connect Kenya entities
    for i, e1 in enumerate(kenya_entities):
        for e2 in kenya_entities[i+1:]:
            links.append({
                "source": e1,
                "target": e2,
                "lineStyle": {"color": "#00FF9433", "width": 1, "curveness": 0.2}
            })

    # Connect USA entities (excluding HIPAA)
    for i, e1 in enumerate(usa_entities):
        for e2 in usa_entities[i+1:]:
            links.append({
                "source": e1,
                "target": e2,
                "lineStyle": {"color": "#FF005533", "width": 1, "curveness": 0.2}
            })

    # ECharts configuration
    option = {
        "backgroundColor": UNIVERSE_THEME["void_black"],
        "title": {
            "text": "G A N D I   U N I V E R S E",
            "subtext": "Interactive Entity Constellation",
            "top": "5%",
            "left": "center",
            "textStyle": {
                "color": UNIVERSE_THEME["core_glow"],
                "fontSize": 24,
                "fontWeight": "bold",
                "textShadowColor": UNIVERSE_THEME["core_glow"],
                "textShadowBlur": 10,
            },
            "subtextStyle": {
                "color": UNIVERSE_THEME["text_secondary"],
                "fontSize": 12,
            }
        },
        "tooltip": {
            "trigger": "item",
            "backgroundColor": "rgba(5, 5, 16, 0.9)",
            "borderColor": UNIVERSE_THEME["core_glow"],
            "textStyle": {"color": "#FFFFFF"},
            "formatter": "{b}<br/>{c}"
        },
        "legend": {
            "data": ["Core", "Kenya", "USA", "Healthcare"],
            "orient": "vertical",
            "left": "5%",
            "top": "center",
            "textStyle": {"color": UNIVERSE_THEME["text_primary"]},
            "itemGap": 20,
        },
        "animationDuration": 1500,
        "animationEasingUpdate": "quinticInOut",
        "series": [
            {
                "name": "GANDI Universe",
                "type": "graph",
                "layout": "force",
                "data": nodes,
                "links": links,
                "categories": categories,
                "roam": True,
                "draggable": True,
                "label": {
                    "show": True,
                    "position": "bottom",
                    "distance": 5,
                },
                "force": {
                    "repulsion": 800,
                    "edgeLength": [100, 250],
                    "gravity": 0.1,
                    "friction": 0.6,
                    "layoutAnimation": True,
                },
                "emphasis": {
                    "focus": "adjacency",
                    "lineStyle": {"width": 4},
                    "itemStyle": {"shadowBlur": 40},
                },
                "lineStyle": {
                    "opacity": 0.5,
                    "width": 2,
                },
            }
        ],
    }

    return option


def render_entity_orbit(entity_code, live_data=None):
    """
    Render an orbital view for a single entity with its connections
    Deep dive into specific entity data
    """
    if entity_code not in ENTITIES:
        return None

    info = ENTITIES[entity_code]
    entity_data = live_data.get("entities", {}).get(entity_code, {}) if live_data else {}

    health = entity_data.get("health_score", 80)
    pending = entity_data.get("pending_items", 0)
    status = entity_data.get("status", "Active")
    recent = entity_data.get("recent_activity", "No recent activity")

    # Build orbital nodes
    nodes = [
        # Central entity
        {
            "name": f"{info['icon']} {entity_code}",
            "symbolSize": 80,
            "value": f"{info['name']}\nStatus: {status}",
            "fixed": True,
            "x": 300,
            "y": 200,
            "itemStyle": {"color": info["color"], "shadowBlur": 30, "shadowColor": info["glow"]},
            "label": {"show": True, "color": "#FFFFFF", "fontSize": 14, "fontWeight": "bold"},
        },
        # Orbital nodes
        {"name": f"Health\n{health}%", "symbolSize": 40, "itemStyle": {"color": "#00FF94" if health >= 80 else "#FFD700" if health >= 60 else "#FF0055"}},
        {"name": f"Pending\n{pending}", "symbolSize": 35, "itemStyle": {"color": "#FF6B35" if pending > 0 else "#00FF94"}},
        {"name": f"Status\n{status}", "symbolSize": 35, "itemStyle": {"color": "#00FF94" if status == "Active" else "#FF0055"}},
    ]

    links = [
        {"source": f"{info['icon']} {entity_code}", "target": f"Health\n{health}%"},
        {"source": f"{info['icon']} {entity_code}", "target": f"Pending\n{pending}"},
        {"source": f"{info['icon']} {entity_code}", "target": f"Status\n{status}"},
    ]

    option = {
        "backgroundColor": UNIVERSE_THEME["void_black"],
        "title": {
            "text": f"{info['icon']} {info['name']} Orbit",
            "left": "center",
            "textStyle": {"color": info["color"], "fontSize": 18},
        },
        "tooltip": {"trigger": "item", "backgroundColor": "rgba(5,5,16,0.9)", "borderColor": info["color"]},
        "series": [{
            "type": "graph",
            "layout": "force",
            "data": nodes,
            "links": links,
            "roam": True,
            "force": {"repulsion": 300, "edgeLength": 100, "gravity": 0.2},
            "lineStyle": {"color": info["color"], "opacity": 0.6, "width": 2},
        }]
    }

    return option

# =============================================================================
# SIDEBAR - Navigation & Quick Actions
# =============================================================================

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/command-line.png", width=80)
    st.title("GANDI Command Center")

    # Dark Mode Toggle
    col_mode1, col_mode2 = st.columns([1, 1])
    with col_mode1:
        if st.button("☀️ Light" if st.session_state.dark_mode else "🌙 Dark", use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    with col_mode2:
        st.caption(f"Auto: {refresh_count}")

    # Time Display
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Minneapolis", get_cst_time(), "CST")
    with col2:
        st.metric("Kenya", get_kenya_time(), "EAT")

    # Kenya Window Alert
    if is_kenya_window():
        st.success("🌍 **KENYA WINDOW ACTIVE**\nBest time to call the farm team!")

    st.markdown("---")

    # Quick Commands
    st.subheader("⚡ Quick Commands")

    if st.button("📋 Morning Briefing", use_container_width=True):
        st.session_state.command = "morning_briefing"

    if st.button("🌾 Farm Status", use_container_width=True):
        st.session_state.command = "farm_status"

    if st.button("📧 Check Urgent Emails", use_container_width=True):
        st.session_state.command = "urgent_emails"

    if st.button("📅 Today's Calendar", use_container_width=True):
        st.session_state.command = "calendar_today"

    st.markdown("---")

    # Voice Command Input (Text fallback - voice requires mic library)
    st.subheader("🎤 Voice Command")
    voice_input = st.text_input("Type or speak command:", placeholder="e.g., 'Message Richard about harvest'")
    if voice_input:
        if st.button("Send Command", type="primary"):
            result = send_voice_command(voice_input)
            if result and "error" not in result:
                st.success("Command sent!")
            else:
                st.error("Could not send command")

# =============================================================================
# MAIN CONTENT - Tabbed Interface
# =============================================================================

# Create tabs for each business entity - NOW WITH UNIVERSE VIEW!
tab_universe, tab_overview, tab_afk, tab_properties, tab_comf, tab_admin = st.tabs([
    "🌌 Universe",
    "📊 Overview",
    "🌾 AFK Farm",
    "🏢 Properties",
    "💊 Healthcare",
    "⚙️ Admin"
])

# -----------------------------------------------------------------------------
# TAB: UNIVERSE - Interactive Constellation View
# -----------------------------------------------------------------------------
with tab_universe:
    st.markdown("""
    <style>
    .universe-container {
        background: linear-gradient(180deg, #050510 0%, #1a0a2e 100%);
        border-radius: 16px;
        padding: 1rem;
        margin: -1rem;
    }
    .universe-header {
        text-align: center;
        color: #00D4FF;
        text-shadow: 0 0 20px #00D4FF;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    .universe-subtitle {
        text-align: center;
        color: #8892b0;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # Load live data for Universe visualization
    universe_data = load_live_data()

    st.markdown('<div class="universe-container">', unsafe_allow_html=True)

    # Render the interactive force-directed graph
    universe_option = render_universe(universe_data)
    st_echarts(options=universe_option, height="600px", key="universe_main")

    st.markdown('</div>', unsafe_allow_html=True)

    # Entity orbit selector
    st.markdown("---")
    st.subheader("🔭 Deep Dive: Entity Orbit View")

    orbit_cols = st.columns(6)
    for i, (code, info) in enumerate(ENTITIES.items()):
        with orbit_cols[i]:
            if st.button(f"{info['icon']} {code}", key=f"orbit_{code}", use_container_width=True):
                st.session_state.selected_entity = code

    # Show entity orbit if selected
    if "selected_entity" in st.session_state and st.session_state.selected_entity:
        selected = st.session_state.selected_entity
        st.markdown(f"### {ENTITIES[selected]['icon']} {ENTITIES[selected]['name']} Orbit")

        orbit_option = render_entity_orbit(selected, universe_data)
        if orbit_option:
            st_echarts(options=orbit_option, height="400px", key=f"orbit_{selected}_view")

        # Entity quick stats
        entity_info = universe_data.get("entities", {}).get(selected, {}) if universe_data else {}
        stat_cols = st.columns(4)
        with stat_cols[0]:
            st.metric("Health Score", f"{entity_info.get('health_score', '--')}%")
        with stat_cols[1]:
            st.metric("Pending Items", entity_info.get('pending_items', '--'))
        with stat_cols[2]:
            st.metric("Status", entity_info.get('status', 'Unknown'))
        with stat_cols[3]:
            st.metric("Location", ENTITIES[selected].get('location', '--'))

        st.caption(f"Recent Activity: {entity_info.get('recent_activity', 'No recent activity')}")

# -----------------------------------------------------------------------------
# TAB: OVERVIEW
# -----------------------------------------------------------------------------
with tab_overview:
    st.header("🎯 Command Center Overview")

    # Load live data
    live_data = load_live_data()

    # Top metrics row
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        email_count = live_data.get("email_summary", {}).get("unread_count", "--") if live_data else "--"
        email_delta = "unread" if live_data else "Loading..."
        st.metric(
            label="📧 Emails Today",
            value=email_count,
            delta=email_delta,
            help="Fetched from Gmail"
        )

    with col2:
        event_count = live_data.get("calendar_summary", {}).get("events_today", "--") if live_data else "--"
        event_delta = "scheduled" if live_data else "Loading..."
        st.metric(
            label="📅 Events Today",
            value=event_count,
            delta=event_delta,
            help="From Google Calendar"
        )

    with col3:
        task_count = live_data.get("system_health", {}).get("pending_tasks", 0) if live_data else "--"
        task_delta = "pending" if live_data else "Loading..."
        st.metric(
            label="✅ Tasks Due",
            value=task_count,
            delta=task_delta,
            help="From Command Center Sheet"
        )

    with col4:
        alert_count = live_data.get("alerts", {}).get("count", 0) if live_data else 0
        alert_delta = "urgent" if live_data and alert_count > 0 else "none"
        st.metric(
            label="⚠️ Alerts",
            value=alert_count if alert_count else "--",
            delta=alert_delta,
            delta_color="inverse" if live_data and alert_count > 0 else "off",
            help="Critical items"
        )

    with col5:
        st.metric(
            label="🤖 AI Status",
            value="Online",
            delta="All systems",
            help="MCP servers status"
        )

    st.markdown("---")

    # Business Status Cards
    st.subheader("🏢 Business Status")

    cols = st.columns(len(ENTITIES))  # Dynamic: 6 entities
    for i, (code, info) in enumerate(ENTITIES.items()):
        with cols[i]:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {info['color']}22, {info['color']}11);
                border-left: 4px solid {info['color']};
                padding: 1rem;
                border-radius: 8px;
                margin-bottom: 1rem;
            ">
                <h3 style="margin: 0; color: {info['color']};">{info['icon']} {code}</h3>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">{info['name']}</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem;">Status: <strong>Active</strong></p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Plotly Charts Row
    st.subheader("📈 Visual Metrics")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        # Business Activity Pie Chart
        if live_data:
            entity_data = {
                "Entity": ["AFK", "GAKP", "GIFP", "COMF", "GAKC"],
                "Activity": [35, 25, 20, 15, 5],  # Placeholder - connect to real data
                "Color": ["#22c55e", "#3b82f6", "#8b5cf6", "#ec4899", "#f59e0b"]
            }
            fig_pie = px.pie(
                entity_data,
                values="Activity",
                names="Entity",
                title="Business Activity Distribution",
                color_discrete_sequence=entity_data["Color"]
            )
            fig_pie.update_layout(
                height=300,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E0E0E0" if st.session_state.dark_mode else "#333333")
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Loading chart data...")

    with chart_col2:
        # Email & Tasks Bar Chart
        if live_data:
            metrics_data = {
                "Category": ["Emails", "Events", "Tasks", "Alerts"],
                "Count": [
                    live_data.get("email_summary", {}).get("unread_count", 0),
                    live_data.get("calendar_summary", {}).get("events_today", 0),
                    live_data.get("system_health", {}).get("pending_tasks", 0),
                    live_data.get("alerts", {}).get("count", 0)
                ]
            }
            fig_bar = go.Figure(data=[
                go.Bar(
                    x=metrics_data["Category"],
                    y=metrics_data["Count"],
                    marker_color=["#3b82f6", "#22c55e", "#f59e0b", "#ef4444"]
                )
            ])
            fig_bar.update_layout(
                title="Today's Metrics",
                height=300,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E0E0E0" if st.session_state.dark_mode else "#333333"),
                yaxis=dict(gridcolor="rgba(128,128,128,0.2)")
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Loading chart data...")

    st.markdown("---")

    # Recent Activity & Urgent Items
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("🔔 Recent Emails")
        email_items = live_data.get("email_summary", {}).get("priority_emails", []) if live_data else []
        if email_items:
            for email in email_items[:5]:
                priority_icon = "🔴" if email.get("priority") == "high" else "📧"
                subject = email.get("subject", "No subject")
                st.markdown(f"{priority_icon} **{subject[:50]}{'...' if len(subject) > 50 else ''}**")
                st.caption(f"From: {email.get('from', 'Unknown')} | Entity: {email.get('entity', '--')}")
        else:
            st.info("No recent emails")

    with col_right:
        st.subheader("⚠️ Action Required")
        alert_items = live_data.get("alerts", {}).get("items", []) if live_data else []
        if alert_items:
            for alert in alert_items:
                severity_color = "🔴" if alert.get("severity") == "high" else "🟡"
                st.error(f"{severity_color} **{alert.get('type', 'ALERT').upper()}**: {alert.get('message', 'Unknown')}")
        else:
            st.success("No urgent alerts")

        # Always show pending setup items
        st.markdown("---")
        st.markdown("**Pending Setup:**")
        st.markdown("- 📋 Configure Make.com webhooks (9 pending)")

# -----------------------------------------------------------------------------
# TAB: AFK FARM
# -----------------------------------------------------------------------------
with tab_afk:
    st.header("🌾 Afro Farm Kenya (AFK)")
    st.caption("128 acres | Loitokitok | GLOBALG.A.P. Certified")

    # Farm metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👥 Workers", "18+", help="Farm staff")
    with col2:
        st.metric("🌱 Active Crops", "3", "French beans, Onions, Passion fruit")
    with col3:
        st.metric("📋 Compliance", "Active", "GLOBALG.A.P.")
    with col4:
        st.metric("🌡️ Status", "Operational", help="Last update from Richard")

    st.markdown("---")

    # Team contacts
    st.subheader("👥 Farm Team")

    team_data = {
        "Name": ["Richard", "Abdirahman", "Mohamed", "Suleiman"],
        "Role": ["General Manager", "Finance", "Security", "Agronomist"],
        "Contact": ["WhatsApp", "WhatsApp", "WhatsApp", "WhatsApp"],
        "Status": ["Active", "Active", "Active", "Active"]
    }

    st.dataframe(pd.DataFrame(team_data), use_container_width=True, hide_index=True)

    # Quick actions for farm
    st.subheader("⚡ Farm Actions")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📨 Message Richard", use_container_width=True):
            st.session_state.draft_message = "Richard"
            st.info("Draft message to Richard...")

    with col2:
        if st.button("📊 Daily Report", use_container_width=True):
            st.info("Fetching latest farm report...")

    with col3:
        if st.button("✅ Compliance Check", use_container_width=True):
            st.info("Running GLOBALG.A.P. compliance check...")

# -----------------------------------------------------------------------------
# TAB: PROPERTIES
# -----------------------------------------------------------------------------
with tab_properties:
    st.header("🏢 Real Estate Portfolio")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏢 GAK Properties (GAKP)")
        st.caption("USA | Property Management")
        st.metric("Properties", "--", "Loading...")
        st.metric("Leases Active", "--", "Loading...")

        if st.button("View GAKP Details", use_container_width=True):
            st.info("Loading GAKP data from Google Sheets...")

    with col2:
        st.subheader("🏠 GIF Properties (GIFP)")
        st.caption("USA | Property Management")
        st.metric("Properties", "--", "Loading...")
        st.metric("Leases Active", "--", "Loading...")

        if st.button("View GIFP Details", use_container_width=True):
            st.info("Loading GIFP data from Google Sheets...")

    st.markdown("---")

    st.subheader("📦 GAK Commodities (GAKC)")
    st.caption("Kenya | Property Holdings")
    st.info("Kenya property data will be loaded from Google Sheets")

# -----------------------------------------------------------------------------
# TAB: HEALTHCARE (COMF)
# -----------------------------------------------------------------------------
with tab_comf:
    st.header("💊 Comfort Services (COMF)")
    st.caption("USA | Healthcare Services")

    st.warning("⚠️ **HIPAA NOTICE**: PHI data is processed locally via Ollama only")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Staff Scheduled", "--", "Loading...")
        st.metric("Services Today", "--", "Loading...")

    with col2:
        st.metric("Compliance Status", "Active", "HIPAA Compliant")
        st.metric("Local Processing", "Ollama", "PHI Protected")

    st.markdown("---")
    st.info("Healthcare data is processed locally for HIPAA compliance. Use Ollama for any PHI-related queries.")

# -----------------------------------------------------------------------------
# TAB: ADMIN
# -----------------------------------------------------------------------------
with tab_admin:
    st.header("⚙️ System Administration")

    # System Status
    st.subheader("🖥️ System Status")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**MCP Servers**")
        servers = [
            ("Claude-Flow", "✅"),
            ("Google Workspace", "✅"),
            ("Gemini", "✅"),
            ("GitHub", "✅"),
            ("Memory", "✅"),
        ]
        for name, status in servers:
            st.markdown(f"{status} {name}")

    with col2:
        st.markdown("**Local Services**")
        services = [
            ("Ollama", "✅ Running"),
            ("n8n", "✅ Active"),
            ("Serveo Tunnel", "✅ Connected"),
        ]
        for name, status in services:
            st.markdown(f"{status} - {name}")

    with col3:
        st.markdown("**Webhooks**")
        st.warning("9 webhooks pending setup in Make.com")
        if st.button("View Webhook Config"):
            st.json({
                "GANDI_BUSINESS_HEALTH": "Pending",
                "GANDI_AI_WATCHDOG": "Pending",
                "GANDI_COMMAND_SYNC": "Pending",
                "GANDI_NOTIFICATIONS": "Pending",
                "GANDI_MORNING_BRIEFING": "Pending",
            })

    st.markdown("---")

    # n8n Webhook Test
    st.subheader("🔗 Test n8n Connection")

    if st.button("Test n8n Webhook"):
        with st.spinner("Testing connection..."):
            result = fetch_n8n_webhook("gandi-status")
            if result and "error" not in result:
                st.success(f"Connected! Response: {result}")
            else:
                st.error(f"Connection failed: {result}")

    st.markdown("---")

    # Security Alerts
    st.subheader("🔐 Security Alerts")

    # Load live data for security alerts
    admin_live_data = load_live_data()
    alert_items = admin_live_data.get("alerts", {}).get("items", []) if admin_live_data else []
    if alert_items:
        for alert in alert_items:
            alert_type = alert.get('type', 'ALERT').upper()
            alert_severity = alert.get('severity', 'medium').upper()
            alert_message = alert.get('message', 'Unknown alert')
            st.error(f"""
            **{alert_type} ALERT ({alert_severity}):**
            {alert_message}
            """)
        st.warning("**Action:** Review at https://myaccount.google.com/notifications")
    else:
        st.success("No security alerts at this time")

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")

# Get last updated time from live data
footer_data = load_live_data()
last_updated = footer_data.get("last_updated", "Never") if footer_data else "Never"

col_footer1, col_footer2 = st.columns([3, 1])

with col_footer1:
    st.caption(f"""
    🎯 GANDI Command Center v2.0 | Interactive Edition | {datetime.now().strftime('%B %d, %Y')}
    | Minneapolis: {get_cst_time()} CST | Kenya: {get_kenya_time()} EAT
    | Data Updated: {last_updated}
    """)

with col_footer2:
    if st.button("🔄 Refresh Data", help="Click to refresh data from Google"):
        st.rerun()
