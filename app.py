import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import math

# Page config
st.set_page_config(
    page_title="CampusTrail AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inject custom CSS for premium styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }
    
    .main {
        background: 
            radial-gradient(circle at top left, rgba(18, 114, 217, 0.12), transparent 45%),
            radial-gradient(circle at 85% 15%, rgba(240, 165, 58, 0.12), transparent 35%),
            linear-gradient(140deg, #dff2ff 0%, #edf8ff 40%, #fdf7e9 100%) !important;
        background-attachment: fixed;
    }
    
    /* Hero Banner Card */
    .hero-section {
        background: rgba(248, 251, 255, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 30px;
        padding: 38px;
        margin-bottom: 24px;
        backdrop-filter: blur(14px);
        box-shadow: 0 25px 60px rgba(17, 44, 80, 0.08);
    }
    
    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        border-radius: 999px;
        padding: 6px 14px;
        background: rgba(18, 114, 217, 0.1);
        color: #1272d9;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    
    .hero-title {
        font-size: clamp(2.2rem, 3.8vw, 3.8rem);
        font-weight: 800;
        line-height: 0.95;
        letter-spacing: -0.04em;
        margin: 0 0 12px 0;
        color: #172033;
    }
    
    .hero-desc {
        color: #61708a;
        font-size: 1.06rem;
        line-height: 1.65;
        margin: 0;
        max-width: 800px;
    }
    
    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #172033;
        margin-bottom: 16px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-bottom: 2px solid rgba(18, 114, 217, 0.15);
        padding-bottom: 6px;
    }
    
    /* Premium Glassmorphic Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.72) !important;
        border: 1px solid rgba(23, 32, 51, 0.12) !important;
        border-radius: 24px !important;
        padding: 22px !important;
        margin-bottom: 20px !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: 0 15px 35px rgba(17, 44, 80, 0.03) !important;
        color: #172033 !important;
    }
    
    /* Metric styling */
    .metric-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-top: 12px;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.92);
        border: 1px solid rgba(23, 32, 51, 0.08);
        border-radius: 16px;
        padding: 12px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.01);
    }
    
    .metric-label {
        font-size: 0.78rem;
        color: #61708a;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        display: block;
        margin-bottom: 4px;
    }
    
    .metric-value {
        font-size: 1.15rem;
        font-weight: 700;
        color: #172033;
    }
    
    /* Itinerary Timeline */
    .timeline-container {
        position: relative;
        border-left: 2px solid rgba(18, 114, 217, 0.15);
        margin-left: 28px;
        margin-top: 14px;
        padding-bottom: 1px;
    }
    
    .timeline-item {
        position: relative;
        margin-bottom: 24px;
        padding-left: 24px;
    }
    
    .timeline-node {
        position: absolute;
        left: -34px;
        top: 3px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #1272d9;
        border: 4px solid #ffffff;
        box-shadow: 0 0 0 3px rgba(18, 114, 217, 0.15);
    }
    
    .timeline-day {
        font-size: 1rem;
        font-weight: 700;
        color: #1272d9;
        display: block;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    
    .timeline-text {
        font-size: 0.94rem;
        color: #3b485e;
        line-height: 1.6;
    }
    
    /* Checklist */
    .check-item {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        margin-bottom: 10px;
    }
    
    .check-icon {
        color: #0d8b80;
        font-weight: bold;
        font-size: 1.1rem;
        line-height: 1;
    }
    
    .check-text {
        font-size: 0.94rem;
        color: #3b485e;
        line-height: 1.5;
    }
    
    /* Badge tag */
    .badge {
        background: rgba(13, 139, 128, 0.12);
        color: #0d8b80;
        font-weight: 700;
        font-size: 0.82rem;
        padding: 6px 14px;
        border-radius: 999px;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    
    .badge-inactive {
        background: rgba(97, 112, 138, 0.12);
        color: #61708a;
        font-weight: 700;
        font-size: 0.82rem;
        padding: 6px 14px;
        border-radius: 999px;
    }
</style>
""", unsafe_allow_html=True)

# Datasets
sample_trips = {
    "Weekend Goa": {
        "destination": "Goa",
        "days": 3,
        "budget": 9000,
        "group": "Friends",
        "style": "Balanced",
        "focus": "Food",
        "notes": "Prefer beaches, affordable cafes, scooter travel, and a relaxed night market."
    },
    "Budget Jaipur": {
        "destination": "Jaipur",
        "days": 2,
        "budget": 5000,
        "group": "Friends",
        "style": "Budget",
        "focus": "Culture",
        "notes": "Want forts, local street food, shared transport, and photo spots."
    },
    "Nature Manali": {
        "destination": "Manali",
        "days": 4,
        "budget": 8500,
        "group": "Solo",
        "style": "Balanced",
        "focus": "Nature",
        "notes": "Prefer mountain views, bus travel, sunrise points, and low-noise stays."
    }
}

destination_data = {
    "Goa": {
        "aliases": ["goa", "north goa", "south goa"],
        "center": [15.4909, 73.8278],
        "zoom": 10,
        "base": "Calangute-Anjuna belt",
        "transport": "Scooters, local cabs, and app taxis",
        "season": "November to February",
        "highlights": [
            {"name": "Calangute Beach", "coords": [15.5439, 73.7553], "blurb": "Popular beach strip with budget stays, cafes, and easy scooter access."},
            {"name": "Fontainhas", "coords": [15.4989, 73.8331], "blurb": "Compact Latin quarter for heritage walks, photography, and cafe breaks."},
            {"name": "Anjuna Flea Market", "coords": [15.578, 73.7436], "blurb": "Good for evening browsing, low-cost shopping, and food stalls."}
        ]
    },
    "Jaipur": {
        "aliases": ["jaipur", "pink city"],
        "center": [26.9124, 75.7873],
        "zoom": 11,
        "base": "MI Road or Bani Park",
        "transport": "Metro, autos, and shared cabs",
        "season": "October to March",
        "highlights": [
            {"name": "Hawa Mahal", "coords": [26.9239, 75.8267], "blurb": "Central landmark that works well for a low-cost old-city walk."},
            {"name": "Amer Fort", "coords": [26.9855, 75.8513], "blurb": "Major heritage stop best visited early to avoid heat and crowds."},
            {"name": "Bapu Bazaar", "coords": [26.9163, 75.8206], "blurb": "Street shopping and snacks in a dense, student-friendly market zone."}
        ]
    },
    "Manali": {
        "aliases": ["manali", "old manali", "new manali"],
        "center": [32.2432, 77.1892],
        "zoom": 12,
        "base": "Old Manali or Mall Road edge",
        "transport": "Walkable core, local cabs, and buses",
        "season": "March to June, September to November",
        "highlights": [
            {"name": "Hadimba Temple", "coords": [32.2474, 77.1873], "blurb": "Forest-backed heritage stop close to the main Manali base area."},
            {"name": "Mall Road", "coords": [32.2396, 77.1887], "blurb": "Good base for food, essentials, and bus pickup coordination."},
            {"name": "Solang Valley", "coords": [32.3169, 77.1569], "blurb": "Adventure zone for a half-day outing with weather-dependent activities."}
        ]
    },
    "Delhi": {
        "aliases": ["delhi", "new delhi", "ncr"],
        "center": [28.6139, 77.209],
        "zoom": 11,
        "base": "Connaught Place or Karol Bagh",
        "transport": "Delhi Metro, buses, and autos",
        "season": "October to March",
        "highlights": [
            {"name": "India Gate", "coords": [28.6129, 77.2295], "blurb": "Easy central landmark around which you can build a low-cost evening loop."},
            {"name": "Humayun's Tomb", "coords": [28.5933, 77.2507], "blurb": "Large heritage site suited for culture-focused morning visits."},
            {"name": "Chandni Chowk", "coords": [28.6506, 77.2303], "blurb": "Dense market area with food trails and old-city atmosphere."}
        ]
    }
}

focus_plans = {
    "Culture": [
        "Visit landmark heritage sites and walk through old city streets.",
        "Add museum time, local market browsing, and a low-cost guided tour.",
        "Reserve evening time for street food and cultural performances."
    ],
    "Adventure": [
        "Start with a light local exploration and book one key activity.",
        "Keep the second half of the day for outdoor sports or a trail.",
        "Finish with a recovery meal and early rest."
    ],
    "Food": [
        "Build the day around famous breakfast, lunch, and dinner stops.",
        "Leave space for one cafe break and one local snack market.",
        "Track food spend closely to avoid budget drift."
    ],
    "Nature": [
        "Prioritize sunrise or sunset viewpoints and slow travel blocks.",
        "Add a park, trail, or riverside stop during the day.",
        "Keep transport simple so more time goes to scenic spots."
    ],
    "Mixed": [
        "Balance one sightseeing stop, one food stop, and one leisure block.",
        "Use public transport or shared cabs to control costs.",
        "End the day with a flexible free-time window."
    ]
}

# Helper calculations
def get_budget_band(amount):
    if amount < 5000: return "Low"
    if amount < 9000: return "Medium"
    return "High"

def build_budget_split(amount, style):
    ratios = {
        "Budget": {"travel": 0.32, "stay": 0.24, "food": 0.24, "buffer": 0.20},
        "Balanced": {"travel": 0.30, "stay": 0.28, "food": 0.24, "buffer": 0.18},
        "Comfort": {"travel": 0.26, "stay": 0.34, "food": 0.24, "buffer": 0.16}
    }
    ratio = ratios[style]
    return {k: amount * v for k, v in ratio.items()}

def distance_km(from_coords, to_coords):
    lat1, lng1 = from_coords
    lat2, lng2 = to_coords
    r = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lng / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c

def find_local_dest(query):
    normalized = query.strip().lower()
    if not normalized: return None
    for name, data in destination_data.items():
        if any(alias in normalized for alias in data["aliases"]):
            return name, data
    return None

def geocode_dest(query):
    try:
        url = f"https://nominatim.openstreetmap.org/search?format=jsonv2&limit=1&q={requests.utils.quote(query)}"
        headers = {"User-Agent": "CampusTrailAI-Streamlit/3.0"}
        res = requests.get(url, headers=headers, timeout=5)
        if res.ok and res.json():
            return res.json()[0]
    except Exception:
        pass
    return None

def resolve_dest(query):
    local = find_local_dest(query)
    if local:
        name, data = local
        return {
            "name": name,
            "source": "dataset",
            "center": data["center"],
            "zoom": data["zoom"],
            "base": data["base"],
            "transport": data["transport"],
            "season": data["season"],
            "highlights": data["highlights"]
        }
    if not query.strip(): return None
    geocoded = geocode_dest(query)
    if geocoded:
        label = ", ".join(geocoded.get("display_name", "").split(",")[:2]).strip()
        return {
            "name": label if label else query,
            "source": "geocoder",
            "center": [float(geocoded["lat"]), float(geocoded["lon"])],
            "zoom": 11,
            "base": "City center or main transit corridor",
            "transport": "Public transport, cabs, and walkable hubs",
            "season": "Check the local weather window",
            "highlights": []
        }
    return None

# App Header Banner
st.markdown("""
<div class="hero-section">
    <div class="eyebrow">Capstone Project • AI Travel Planner</div>
    <h1 class="hero-title">CampusTrail AI</h1>
    <p class="hero-desc">
        A student-focused travel planner that builds a budget-friendly trip outline from destination,
        budget, number of days, travel style, and interests. It creates a day-wise plan, cost split,
        packing checklist, and practical tips in one screen.
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize Session State
if "form_dest" not in st.session_state:
    st.session_state["form_dest"] = ""
if "form_days" not in st.session_state:
    st.session_state["form_days"] = 3
if "form_budget" not in st.session_state:
    st.session_state["form_budget"] = 6000
if "form_group" not in st.session_state:
    st.session_state["form_group"] = "Friends"
if "form_style" not in st.session_state:
    st.session_state["form_style"] = "Balanced"
if "form_focus" not in st.session_state:
    st.session_state["form_focus"] = "Culture"
if "form_notes" not in st.session_state:
    st.session_state["form_notes"] = ""
if "start_coords" not in st.session_state:
    st.session_state["start_coords"] = None
if "start_loc_name" not in st.session_state:
    st.session_state["start_loc_name"] = ""

# Handle Preset Clicks
def apply_preset(name):
    p = sample_trips[name]
    st.session_state["form_dest"] = p["destination"]
    st.session_state["form_days"] = p["days"]
    st.session_state["form_budget"] = p["budget"]
    st.session_state["form_group"] = p["group"]
    st.session_state["form_style"] = p["style"]
    st.session_state["form_focus"] = p["focus"]
    st.session_state["form_notes"] = p["notes"]

def reset_fields():
    st.session_state["form_dest"] = ""
    st.session_state["form_days"] = 3
    st.session_state["form_budget"] = 6000
    st.session_state["form_group"] = "Friends"
    st.session_state["form_style"] = "Balanced"
    st.session_state["form_focus"] = "Culture"
    st.session_state["form_notes"] = ""
    st.session_state["start_coords"] = None
    st.session_state["start_loc_name"] = ""

# Primary Columns
col_left, col_right = st.columns([0.95, 1.05], gap="large")

with col_left:
    st.markdown('<div class="section-title">Plan a Trip</div>', unsafe_allow_html=True)
    st.markdown('<p style="color: #61708a; font-size:0.92rem; margin-bottom: 12px;">Fill the details below or click a preset to auto-fill. Enter starting location to draw the routing line.</p>', unsafe_allow_html=True)
    
    # Presets Row
    preset_cols = st.columns(len(sample_trips) + 1)
    for index, name in enumerate(sample_trips.keys()):
        with preset_cols[index]:
            if st.button(name, key=f"preset_{index}", use_container_width=True):
                apply_preset(name)
                st.rerun()
    with preset_cols[-1]:
        if st.button("Reset Form", key="reset_btn", type="secondary", use_container_width=True):
            reset_fields()
            st.rerun()
            
    # Form fields in a container card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    dest_val = st.text_input("Destination", value=st.session_state["form_dest"], placeholder="Jaipur, Goa, Manali", key="dest_input")
    st.session_state["form_dest"] = dest_val
    
    input_col1, input_col2 = st.columns(2)
    with input_col1:
        days_val = st.selectbox("Trip Duration", [2, 3, 4, 5], index=[2, 3, 4, 5].index(st.session_state["form_days"]), key="days_input")
        st.session_state["form_days"] = days_val
        
        style_val = st.selectbox("Travel Style", ["Budget", "Balanced", "Comfort"], index=["Budget", "Balanced", "Comfort"].index(st.session_state["form_style"]), key="style_input")
        st.session_state["form_style"] = style_val

    with input_col2:
        budget_val = st.number_input("Budget (INR)", min_value=1000, step=500, value=st.session_state["form_budget"], key="budget_input")
        st.session_state["form_budget"] = budget_val
        
        group_val = st.selectbox("Travel Group", ["Solo", "Friends", "Couple", "Family"], index=["Solo", "Friends", "Couple", "Family"].index(st.session_state["form_group"]), key="group_input")
        st.session_state["form_group"] = group_val
        
    focus_val = st.selectbox("Trip Focus", ["Culture", "Adventure", "Food", "Nature", "Mixed"], index=["Culture", "Adventure", "Food", "Nature", "Mixed"].index(st.session_state["form_focus"]), key="focus_input")
    st.session_state["form_focus"] = focus_val

    notes_val = st.text_area("Preferences", value=st.session_state["form_notes"], placeholder="Example: prefer trains, low-cost stays, local food, sunrise spots, and safe evening plans.", key="notes_input")
    st.session_state["form_notes"] = notes_val
    
    # Distance comparison helper (live location)
    st.markdown("<hr style='margin: 15px 0; opacity: 0.15;'/>", unsafe_allow_html=True)
    st.write("**Route Planning (Distance from Your Location)**")
    route_col1, route_col2 = st.columns([1.3, 0.7])
    with route_col1:
        start_loc = st.text_input("Your Starting Location", value=st.session_state["start_loc_name"], placeholder="e.g. Mumbai, Delhi, Bangalore", label_visibility="collapsed")
    with route_col2:
        if st.button("Resolve Route", use_container_width=True, type="secondary"):
            if start_loc.strip():
                with st.spinner("Locating..."):
                    start_resolved = resolve_dest(start_loc)
                    if start_resolved:
                        st.session_state["start_coords"] = start_resolved["center"]
                        st.session_state["start_loc_name"] = start_resolved["name"]
                        st.toast(f"Located start: {start_resolved['name']}", icon="📍")
                        st.rerun()
                    else:
                        st.toast("Could not locate starting location.", icon="⚠️")
            else:
                st.session_state["start_coords"] = None
                st.session_state["start_loc_name"] = ""
                st.rerun()
                
    if st.session_state["start_coords"]:
        st.info(f"📍 Route comparison active from **{st.session_state['start_loc_name']}**")
        
    st.markdown('</div>', unsafe_allow_html=True)

# Generate Itinerary Plan
resolved_dest = None
if st.session_state["form_dest"].strip():
    resolved_dest = resolve_dest(st.session_state["form_dest"])

with col_right:
    st.markdown('<div class="section-title">Generated Plan</div>', unsafe_allow_html=True)
    
    if not resolved_dest:
        # Placeholder snapshot & card
        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <h4 style="margin:0; font-size: 1.1rem; font-weight: 800; color: #172033; text-transform: uppercase; letter-spacing: 0.05em;">Trip Snapshot</h4>
                <span class="badge-inactive">No Plan Loaded</span>
            </div>
            <div style="padding: 12px; background: rgba(255,255,255,0.6); border-radius: 14px; border: 1px solid rgba(23,32,51,0.06);">
                <span style="color: #61708a; display: block; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px;">Planner Summary</span>
                <strong style="color: #172033; font-size: 0.95rem;">Ready to build a student trip. Enter destination to begin.</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.info("👈 Enter a destination in the form on the left to generate the complete student itinerary and load the interactive map.")
    else:
        # 1. Snapshot Card
        badge_style = f"{resolved_dest['name']} • {st.session_state['form_style']}"
        summary_val = f"{resolved_dest['name']} {st.session_state['form_focus'].lower()} trip for {st.session_state['form_group'].lower()} travelers."
        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <h4 style="margin: 0; font-size: 1.1rem; font-weight: 800; color: #172033; text-transform: uppercase; letter-spacing: 0.05em;">Trip Snapshot</h4>
                <span class="badge">{badge_style}</span>
            </div>
            <div style="padding: 12px; background: rgba(255,255,255,0.6); border-radius: 14px; border: 1px solid rgba(23,32,51,0.06); margin-bottom: 14px;">
                <span style="color: #61708a; display: block; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px;">Planner Summary</span>
                <strong style="color: #172033; font-size: 0.95rem;">{summary_val}</strong>
            </div>
            <div class="metric-row">
                <div class="metric-card">
                    <span class="metric-label">Budget Band</span>
                    <span class="metric-value">{get_budget_band(st.session_state["form_budget"])}</span>
                </div>
                <div class="metric-card">
                    <span class="metric-label">Style</span>
                    <span class="metric-value">{st.session_state["form_style"]}</span>
                </div>
                <div class="metric-card">
                    <span class="metric-label">Duration</span>
                    <span class="metric-value">{st.session_state["form_days"]} Days</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Overview Card
        overview_msg = f"CampusTrail suggests a <strong>{st.session_state['form_days']}-day {st.session_state['form_focus'].lower()} trip</strong> to <strong>{resolved_dest['name']}</strong> for a <strong>{st.session_state['form_group'].lower()}</strong> group with a budget of <strong>Rs {st.session_state['form_budget']:,}</strong>. The plan aims to keep travel practical, affordable, and student-friendly."
        st.markdown(f"""
        <div class="glass-card">
            <h4 style="margin: 0 0 12px 0; font-size: 1.1rem; font-weight: 800; color: #172033; text-transform: uppercase; letter-spacing: 0.05em;">Trip Overview</h4>
            <p style="margin: 0; color: #3b485e; font-size: 0.98rem; line-height: 1.7; font-weight: 400;">{overview_msg}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 3. Map & Location Card
        coords_str = f"{resolved_dest['center'][0]:.4f}, {resolved_dest['center'][1]:.4f}"
        source_label = "built-in place data loaded" if resolved_dest["source"] == "dataset" else "OpenStreetMap lookup loaded"
        distance_status = ""
        
        # Initialize Folium Map
        m = folium.Map(location=resolved_dest["center"], zoom_start=resolved_dest["zoom"], tiles="OpenStreetMap")
        
        # Destination Marker
        folium.Marker(
            location=resolved_dest["center"],
            popup=f"<b>{resolved_dest['name']}</b><br>Primary Destination",
            tooltip=resolved_dest["name"],
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)
        
        # Highlight Markers (if available)
        for spot in resolved_dest["highlights"]:
            folium.CircleMarker(
                location=spot["coords"],
                radius=8,
                popup=f"<b>{spot['name']}</b><br>{spot['blurb']}",
                tooltip=spot["name"],
                color="#1272d9",
                fill=True,
                fill_color="#f0a53a",
                fill_opacity=0.85
            ).add_to(m)
            
        # User Location & Route Line
        if st.session_state["start_coords"]:
            user_coords = st.session_state["start_coords"]
            folium.Marker(
                location=user_coords,
                popup=f"<b>{st.session_state['start_loc_name']}</b><br>Your Location",
                tooltip=st.session_state["start_loc_name"],
                icon=folium.Icon(color="green", icon="home")
            ).add_to(m)
            
            # Polyline between User and Destination
            folium.PolyLine(
                locations=[user_coords, resolved_dest["center"]],
                color="#0d8b80",
                weight=3,
                dash_array="5, 10",
                opacity=0.8
            ).add_to(m)
            
            # Distance computation
            dist = distance_km(user_coords, resolved_dest["center"])
            distance_status = f" • <b>{int(dist)} km</b> from starting location ({st.session_state['start_loc_name']})"
            m.fit_bounds([user_coords, resolved_dest["center"]])
            
        map_status_str = f"Showing {resolved_dest['name']} on the map • {source_label}{distance_status}"
        
        highlights_li = ""
        if resolved_dest["highlights"]:
            highlights_li = "<div style='margin-top:14px; font-size:0.92rem;'><b>📍 Local Highlights:</b><ul style='margin: 8px 0 0 0; padding-left: 18px; color: #3b485e;'>"
            for h in resolved_dest["highlights"]:
                highlights_li += f"<li style='margin-bottom: 6px;'><b>{h['name']}</b>: {h['blurb']}</li>"
            highlights_li += "</ul></div>"
            
        st.markdown(f"""
        <div class="glass-card">
            <h4 style="margin: 0 0 14px 0; font-size: 1.1rem; font-weight: 800; color: #172033; text-transform: uppercase; letter-spacing: 0.05em;">Map & Location Insights</h4>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; font-size: 0.88rem; margin-bottom: 14px; padding: 12px; background: rgba(255,255,255,0.5); border-radius: 12px; border: 1px solid rgba(23,32,51,0.04);">
                <div>
                    <span style="color:#61708a; display:block; font-size:0.72rem; text-transform:uppercase; font-weight:600; margin-bottom:2px;">Coordinates</span>
                    <strong style="color:#172033; font-size:0.9rem;">{coords_str}</strong>
                </div>
                <div>
                    <span style="color:#61708a; display:block; font-size:0.72rem; text-transform:uppercase; font-weight:600; margin-bottom:2px;">Best Base</span>
                    <strong style="color:#172033; font-size:0.9rem;">{resolved_dest['base']}</strong>
                </div>
                <div style="margin-top: 8px;">
                    <span style="color:#61708a; display:block; font-size:0.72rem; text-transform:uppercase; font-weight:600; margin-bottom:2px;">Transport</span>
                    <strong style="color:#172033; font-size:0.9rem;">{resolved_dest['transport']}</strong>
                </div>
                <div style="margin-top: 8px;">
                    <span style="color:#61708a; display:block; font-size:0.72rem; text-transform:uppercase; font-weight:600; margin-bottom:2px;">Best Season</span>
                    <strong style="color:#172033; font-size:0.9rem;">{resolved_dest['season']}</strong>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Render map natively in Streamlit-Folium inside the card block
        st_folium(m, width=650, height=350, returned_objects=[])
        
        st.markdown(f"""
            <p style="color: #61708a; font-size: 0.8rem; margin: 10px 0 0 0; font-weight: 500;">{map_status_str}</p>
            {highlights_li}
        </div>
        """, unsafe_allow_html=True)
        
        # 4. Budget Split Card (Premium grid style with progress)
        costs = build_budget_split(st.session_state["form_budget"], st.session_state["form_style"])
        percentages = {
            "Budget": {"travel": 32, "stay": 24, "food": 24, "buffer": 20},
            "Balanced": {"travel": 30, "stay": 28, "food": 24, "buffer": 18},
            "Comfort": {"travel": 26, "stay": 34, "food": 24, "buffer": 16}
        }[st.session_state["form_style"]]
        
        items = [
            ("Travel", costs["travel"], percentages["travel"], "✈️", "rgba(18, 114, 217, 0.1)", "#1272d9"),
            ("Stay", costs["stay"], percentages["stay"], "🏨", "rgba(13, 139, 128, 0.1)", "#0d8b80"),
            ("Food", costs["food"], percentages["food"], "🍔", "rgba(240, 165, 58, 0.1)", "#f0a53a"),
            ("Buffer", costs["buffer"], percentages["buffer"], "🛡️", "rgba(97, 112, 138, 0.1)", "#61708a")
        ]
        
        cost_cards_html = ""
        for name, amount, pct, icon, bg, color in items:
            cost_cards_html += f"""
            <div style="background: #ffffff; border: 1px solid rgba(23,32,51,0.08); border-radius: 16px; padding: 14px; display: flex; align-items: center; gap: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.01);">
                <div style="width: 42px; height: 42px; border-radius: 12px; background: {bg}; display: flex; align-items: center; justify-content: center; font-size: 1.25rem;">{icon}</div>
                <div style="flex-grow: 1;">
                    <div style="display: flex; justify-content: space-between; align-items: baseline;">
                        <span style="font-size: 0.75rem; color: #61708a; text-transform: uppercase; letter-spacing: 0.05em; font-weight:600;">{name}</span>
                        <span style="font-size: 0.7rem; color: {color}; font-weight: 700; background: {bg}; padding: 2px 6px; border-radius: 6px;">{pct}%</span>
                    </div>
                    <strong style="font-size: 1.1rem; color: #172033; display: block; margin-top: 2px;">Rs {int(amount):,}</strong>
                </div>
            </div>
            """
            
        st.markdown(f"""
        <div class="glass-card">
            <h4 style="margin:0 0 14px 0; font-size: 1.1rem; font-weight: 800; color: #172033; text-transform: uppercase; letter-spacing: 0.05em;">Budget Split ({st.session_state['form_style']} Style)</h4>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;">
                {cost_cards_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 5. Day-wise Itinerary Card (Vertical timeline)
        days_plan = []
        base_plans = focus_plans.get(st.session_state["form_focus"], focus_plans["Mixed"])
        for i in range(1, st.session_state["form_days"] + 1):
            if i == 1:
                intro = f"Arrive in {resolved_dest['name']}, settle in, and map nearby transport and food options."
            elif i == st.session_state["form_days"]:
                intro = "Keep the final day lighter, buy essentials, and prepare return travel."
            else:
                intro = "Use the day for focused exploration with a student-budget schedule."
            
            style_line = ""
            if st.session_state["form_style"] == "Budget":
                style_line = "Prefer buses, shared autos, hostels, and fixed daily spending."
            elif st.session_state["form_style"] == "Comfort":
                style_line = "Use direct transport, better stays, and reserved time for rest."
            else:
                style_line = "Mix public transport with one convenience upgrade if needed."
                
            base_action = base_plans[(i - 1) % len(base_plans)]
            days_plan.append({
                "day": i,
                "text": f"{intro} {base_action} {style_line}"
            })
            
        timeline_items_html = ""
        for d in days_plan:
            timeline_items_html += f"""
            <div style="position: relative; margin-bottom: 24px; padding-left: 24px;">
                <!-- Circle Node -->
                <div style="position: absolute; left: -31px; top: 3px; width: 12px; height: 12px; border-radius: 50%; background: #1272d9; border: 4px solid #ffffff; box-shadow: 0 0 0 3px rgba(18, 114, 217, 0.15);"></div>
                <div>
                    <strong style="font-size: 1rem; color: #1272d9; display: block; margin-bottom: 4px; font-weight: 700; text-transform: uppercase; letter-spacing:0.03em;">Day {d['day']}</strong>
                    <p style="margin: 0; font-size: 0.94rem; color: #3b485e; line-height: 1.6;">{d['text']}</p>
                </div>
            </div>
            """
            
        st.markdown(f"""
        <div class="glass-card">
            <h4 style="margin:0 0 14px 0; font-size: 1.1rem; font-weight: 800; color: #172033; text-transform: uppercase; letter-spacing: 0.05em;">Day-wise Timeline</h4>
            <div style="position: relative; border-left: 2px solid rgba(18, 114, 217, 0.15); margin-left: 31px; margin-top: 14px; padding-bottom: 1px;">
                {timeline_items_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 6. Packing & Safety Card (Checklist style)
        tips_list = [
            f"Save offline maps and keep the {resolved_dest['name']} hotel or hostel address pinned.",
            "Carry student ID, one power bank, refillable water bottle, and emergency cash.",
            "Check local transport closing times before planning late evening travel."
        ]
        if st.session_state["form_focus"] in ["Adventure", "Nature"]:
            tips_list.append("Pack walking shoes, weather protection, and basic medicines.")
        elif st.session_state["form_focus"] == "Food":
            tips_list.append("Set a food budget cap for each day and shortlist clean, well-rated places.")
        else:
            tips_list.append("Start early to avoid crowds and reduce transport waiting time.")
            
        if st.session_state["form_group"] == "Solo":
            tips_list.append("Share your live location or daily route summary with a trusted contact.")
        else:
            tips_list.append("Set one common meet-up point in case the group splits during the day.")
            
        if st.session_state["form_notes"].strip():
            truncated_notes = st.session_state["form_notes"].strip()[:90] + ("..." if len(st.session_state["form_notes"].strip()) > 90 else "")
            tips_list.append(f"Planner note used: {truncated_notes}")
            
        checklist_items_html = ""
        for t in tips_list:
            checklist_items_html += f"""
            <div style="display: flex; align-items: flex-start; gap: 10px; margin-bottom: 10px;">
                <div style="color: #0d8b80; font-weight: bold; font-size: 1.1rem; line-height: 1;">✓</div>
                <span style="font-size: 0.94rem; color: #3b485e; line-height: 1.5;">{t}</span>
            </div>
            """
            
        st.markdown(f"""
        <div class="glass-card">
            <h4 style="margin:0 0 14px 0; font-size: 1.1rem; font-weight: 800; color: #172033; text-transform: uppercase; letter-spacing: 0.05em;">Packing & Safety Tips</h4>
            <div style="margin-top: 10px;">
                {checklist_items_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; color: #61708a; font-size: 0.85rem; padding: 20px 0;">
    This prototype is built for demonstration. It uses OpenStreetMap via Nominatim and Folium for mapping visualizations.
</div>
""", unsafe_allow_html=True)
