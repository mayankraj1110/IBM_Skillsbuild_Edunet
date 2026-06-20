import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import math

# Page configuration
st.set_page_config(
    page_title="CampusTrail AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inject custom CSS for premium styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main {
        background: 
            radial-gradient(circle at top left, rgba(18, 114, 217, 0.15), transparent 40%),
            radial-gradient(circle at 85% 15%, rgba(240, 165, 58, 0.15), transparent 30%),
            linear-gradient(140deg, #dff2ff 0%, #edf8ff 40%, #fdf7e9 100%);
        background-attachment: fixed;
    }
    
    /* Premium Glassmorphic Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.72);
        border: 1px solid rgba(23, 32, 51, 0.12);
        border-radius: 24px;
        padding: 24px;
        margin-bottom: 20px;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 30px rgba(17, 44, 80, 0.05);
    }
    
    .hero-section {
        background: rgba(248, 251, 255, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.45);
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
    
    h1 {
        font-size: clamp(2.2rem, 4vw, 3.8rem) !important;
        font-weight: 800 !important;
        line-height: 1.0 !important;
        letter-spacing: -0.04em !important;
        margin: 0 0 16px 0 !important;
        color: #172033 !important;
    }
    
    .hero-desc {
        color: #61708a;
        font-size: 1.08rem;
        line-height: 1.6;
        margin: 0;
        max-width: 800px;
    }
    
    .section-title {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #172033;
        margin-bottom: 16px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Preset Chips */
    .preset-btn {
        border-radius: 999px !important;
        background: white !important;
        border: 1px solid rgba(23, 32, 51, 0.12) !important;
        color: #172033 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 8px 16px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
    }
    
    /* Metric styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(23, 32, 51, 0.1);
        border-radius: 16px;
        padding: 12px 16px;
        text-align: center;
    }
    
    .metric-label {
        font-size: 0.78rem;
        color: #61708a;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
        display: block;
    }
    
    .metric-value {
        font-size: 1.15rem;
        font-weight: 700;
        color: #172033;
    }
    
    /* Itinerary Day Cards */
    .day-card {
        background: linear-gradient(135deg, rgba(18, 114, 217, 0.05), rgba(13, 139, 128, 0.04));
        border: 1px solid rgba(18, 114, 217, 0.1);
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
    }
    
    .day-num {
        font-size: 1rem;
        font-weight: 700;
        color: #1272d9;
        display: block;
        margin-bottom: 4px;
    }
    
    .day-desc {
        font-size: 0.95rem;
        color: #3b485e;
        line-height: 1.6;
    }
    
    /* Tips List */
    .tip-item {
        color: #3b485e;
        margin-bottom: 8px;
        line-height: 1.5;
        font-size: 0.95rem;
    }
    
    .badge {
        display: inline-block;
        border-radius: 999px;
        padding: 6px 12px;
        font-size: 0.82rem;
        font-weight: 700;
        background: rgba(13, 139, 128, 0.12);
        color: #0d8b80;
    }
</style>
""", unsafe_allow_html=True)

# Datasets
sample_trips = {
    "Goa (Weekend)": {
        "destination": "Goa",
        "days": 3,
        "budget": 9000,
        "group": "Friends",
        "style": "Balanced",
        "focus": "Food",
        "notes": "Prefer beaches, affordable cafes, scooter travel, and a relaxed night market."
    },
    "Jaipur (Budget)": {
        "destination": "Jaipur",
        "days": 2,
        "budget": 5000,
        "group": "Friends",
        "style": "Budget",
        "focus": "Culture",
        "notes": "Want forts, local street food, shared transport, and photo spots."
    },
    "Manali (Nature)": {
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

# Helper functions
def get_budget_band(amount):
    if amount < 5000:
        return "Low"
    elif amount < 9000:
        return "Medium"
    return "High"

def build_budget_split(amount, trip_style):
    ratios = {
        "Budget": {"travel": 0.32, "stay": 0.24, "food": 0.24, "buffer": 0.20},
        "Balanced": {"travel": 0.30, "stay": 0.28, "food": 0.24, "buffer": 0.18},
        "Comfort": {"travel": 0.26, "stay": 0.34, "food": 0.24, "buffer": 0.16}
    }
    ratio = ratios[trip_style]
    return {k: amount * v for k, v in ratio.items()}

def build_day_plan(location, total_days, trip_focus, trip_style):
    base_plans = focus_plans.get(trip_focus, focus_plans["Mixed"])
    items = []
    trip_location = location if location else "your destination"
    
    for i in range(1, total_days + 1):
        if i == 1:
            intro = f"Arrive in {trip_location}, settle in, and map nearby transport and food options."
        elif i == total_days:
            intro = f"Keep the final day lighter, buy essentials, and prepare return travel."
        else:
            intro = "Use the day for focused exploration with a student-budget schedule."
            
        style_line = ""
        if trip_style == "Budget":
            style_line = "Prefer buses, shared autos, hostels, and fixed daily spending."
        elif trip_style == "Comfort":
            style_line = "Use direct transport, better stays, and reserved time for rest."
        else:
            style_line = "Mix public transport with one convenience upgrade if needed."
            
        base_action = base_plans[(i - 1) % len(base_plans)]
        items.append({
            "title": f"Day {i}",
            "text": f"{intro} {base_action} {style_line}"
        })
    return items

def build_tips(location, trip_focus, travel_group, user_notes):
    trip_location = location if location else "destination"
    tips = [
        f"Save offline maps and keep the {trip_location} hotel or hostel address pinned.",
        "Carry student ID, one power bank, refillable water bottle, and emergency cash.",
        "Check local transport closing times before planning late evening travel."
    ]
    
    if trip_focus in ["Adventure", "Nature"]:
        tips.append("Pack walking shoes, weather protection, and basic medicines.")
    elif trip_focus == "Food":
        tips.append("Set a food budget cap for each day and shortlist clean, well-rated places.")
    else:
        tips.append("Start early to avoid crowds and reduce transport waiting time.")
        
    if travel_group == "Solo":
        tips.append("Share your live location or daily route summary with a trusted contact.")
    else:
        tips.append("Set one common meet-up point in case the group splits during the day.")
        
    if user_notes.strip():
        truncated_notes = user_notes.strip()[:90] + ("..." if len(user_notes.strip()) > 90 else "")
        tips.append(f"Planner note used: {truncated_notes}")
        
    return tips

def find_destination_data(query):
    normalized = query.strip().lower()
    if not normalized:
        return None
    for name, data in destination_data.items():
        if any(alias in normalized for alias in data["aliases"]):
            return name, data
    return None

def geocode_destination(query):
    try:
        url = f"https://nominatim.openstreetmap.org/search?format=jsonv2&limit=1&q={requests.utils.quote(query)}"
        headers = {"User-Agent": "CampusTrailAI/1.0"}
        response = requests.get(url, headers=headers, timeout=5)
        if response.ok and response.json():
            data = response.json()[0]
            return data
    except Exception:
        pass
    return None

def resolve_destination(query):
    local = find_destination_data(query)
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
    
    if not query.strip():
        return None
        
    geocoded = geocode_destination(query)
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

def distance_km(from_coords, to_coords):
    lat1, lng1 = from_coords
    lat2, lng2 = to_coords
    r = 6371  # Earth radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lng / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c

# App Header
st.markdown("""
<div class="hero-section">
    <div class="eyebrow">Capstone Project • AI Travel Planner</div>
    <h1>CampusTrail AI</h1>
    <p class="hero-desc">
        A student-focused travel planner that builds a budget-friendly trip outline from destination,
        budget, number of days, travel style, and interests. It creates a day-wise plan, cost split,
        packing checklist, and practical tips in one screen.
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize Session State for form values
if "form_destination" not in st.session_state:
    st.session_state["form_destination"] = ""
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
if "start_location_name" not in st.session_state:
    st.session_state["start_location_name"] = ""

# Handle Preset Clicks
def apply_preset(preset_name):
    p = sample_trips[preset_name]
    st.session_state["form_destination"] = p["destination"]
    st.session_state["form_days"] = p["days"]
    st.session_state["form_budget"] = p["budget"]
    st.session_state["form_group"] = p["group"]
    st.session_state["form_style"] = p["style"]
    st.session_state["form_focus"] = p["focus"]
    st.session_state["form_notes"] = p["notes"]

def reset_fields():
    st.session_state["form_destination"] = ""
    st.session_state["form_days"] = 3
    st.session_state["form_budget"] = 6000
    st.session_state["form_group"] = "Friends"
    st.session_state["form_style"] = "Balanced"
    st.session_state["form_focus"] = "Culture"
    st.session_state["form_notes"] = ""
    st.session_state["start_coords"] = None
    st.session_state["start_location_name"] = ""

# Primary layout
col_left, col_right = st.columns([0.95, 1.05], gap="large")

with col_left:
    st.markdown('<div class="section-title">Plan a Trip</div>', unsafe_allow_html=True)
    st.write("Fill the trip details or use one of the sample presets. The planner pairs itinerary output with a live map view and destination metadata.")
    
    # Presets row
    preset_cols = st.columns(len(sample_trips) + 1)
    for index, name in enumerate(sample_trips.keys()):
        with preset_cols[index]:
            if st.button(name, key=f"preset_{index}", use_container_width=True):
                apply_preset(name)
    with preset_cols[-1]:
        if st.button("Reset Form", key="reset_btn", type="secondary", use_container_width=True):
            reset_fields()
            
    # Form fields inside a container card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    input_col1, input_col2 = st.columns(2)
    with input_col1:
        dest_val = st.text_input("Destination", value=st.session_state["form_destination"], placeholder="Jaipur, Goa, Manali", key="dest_input")
        st.session_state["form_destination"] = dest_val
        
        budget_val = st.number_input("Budget (INR)", min_value=1000, step=500, value=st.session_state["form_budget"], key="budget_input")
        st.session_state["form_budget"] = budget_val
        
        style_val = st.selectbox("Travel Style", ["Budget", "Balanced", "Comfort"], index=["Budget", "Balanced", "Comfort"].index(st.session_state["form_style"]), key="style_input")
        st.session_state["form_style"] = style_val

    with input_col2:
        days_val = st.selectbox("Trip Duration", [2, 3, 4, 5], index=[2, 3, 4, 5].index(st.session_state["form_days"]), key="days_input")
        st.session_state["form_days"] = days_val
        
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
        start_loc = st.text_input("Your Starting Location", value=st.session_state["start_location_name"], placeholder="e.g. Mumbai, Delhi, Bangalore", label_visibility="collapsed")
    with route_col2:
        if st.button("Resolve Distance", use_container_width=True, type="secondary"):
            if start_loc.strip():
                with st.spinner("Locating your starting point..."):
                    start_resolved = resolve_destination(start_loc)
                    if start_resolved:
                        st.session_state["start_coords"] = start_resolved["center"]
                        st.session_state["start_location_name"] = start_resolved["name"]
                        st.toast(f"Located start: {start_resolved['name']}", icon="📍")
                    else:
                        st.toast("Could not locate starting location.", icon="⚠️")
            else:
                st.session_state["start_coords"] = None
                st.session_state["start_location_name"] = ""
                
    if st.session_state["start_coords"]:
        st.info(f"📍 Route comparison active from **{st.session_state['start_location_name']}**")
        
    st.markdown('</div>', unsafe_allow_html=True)

# Generate Itinerary Plan
resolved_dest = None
if st.session_state["form_destination"].strip():
    resolved_dest = resolve_destination(st.session_state["form_destination"])

with col_right:
    st.markdown('<div class="section-title">Generated Plan</div>', unsafe_allow_html=True)
    
    # Header card containing summary
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    badge_style = resolved_dest["name"] + " • " + st.session_state["form_style"] if resolved_dest else "Student-friendly plan"
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
            <div>
                <h4 style="margin: 0; font-size: 1.15rem; font-weight: 700;">Trip Snapshot</h4>
            </div>
            <span class="badge">{badge_style}</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Trip snapshot metrics
    snap_col1, snap_col2, snap_col3 = st.columns(3)
    with snap_col1:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-label">Budget Band</span>
            <span class="metric-value">{get_budget_band(st.session_state["form_budget"])}</span>
        </div>
        """, unsafe_allow_html=True)
    with snap_col2:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-label">Travel Style</span>
            <span class="metric-value">{st.session_state["form_style"]}</span>
        </div>
        """, unsafe_allow_html=True)
    with snap_col3:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-label">Duration</span>
            <span class="metric-value">{st.session_state["form_days"]} Days</span>
        </div>
        """, unsafe_allow_html=True)
        
    summary_text = "Ready to build a student trip. Enter destination to begin."
    if resolved_dest:
        summary_text = f"{resolved_dest['name']} {st.session_state['form_focus'].lower()} trip for {st.session_state['form_group'].lower()} travelers."
    st.markdown(f"""
        <div style="margin-top: 14px; padding: 12px; background: rgba(255,255,255,0.5); border-radius: 12px; font-size: 0.9rem; color: #172033; font-weight: 600;">
            <span style="color: #61708a; display: block; font-size: 0.78rem; text-transform: uppercase; margin-bottom: 2px;">Planner Summary</span>
            {summary_text}
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display Plan
    if not resolved_dest:
        st.info("👈 Enter a destination in the form on the left to generate the complete student itinerary and load the interactive map.")
    else:
        # Trip Overview Card
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="margin:0 0 10px 0; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.05em; color: #172033;">Trip Overview</h4>', unsafe_allow_html=True)
        overview_msg = f"CampusTrail suggests a {st.session_state['form_days']}-day {st.session_state['form_focus'].lower()} trip to {resolved_dest['name']} for a {st.session_state['form_group'].lower()} group with a budget of Rs {st.session_state['form_budget']:,}. The plan aims to keep travel practical, affordable, and student-friendly."
        st.write(overview_msg)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Map & Location Card
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="margin:0 0 10px 0; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.05em; color: #172033;">Map & Location Insights</h4>', unsafe_allow_html=True)
        
        # Metadata Columns
        coords_str = f"{resolved_dest['center'][0]:.4f}, {resolved_dest['center'][1]:.4f}"
        meta_col1, meta_col2 = st.columns(2)
        with meta_col1:
            st.markdown(f"**Coordinates:** `{coords_str}`")
            st.markdown(f"**Best Base:** {resolved_dest['base']}")
        with meta_col2:
            st.markdown(f"**Transport:** {resolved_dest['transport']}")
            st.markdown(f"**Best Season:** {resolved_dest['season']}")
            
        # Draw Map
        m = folium.Map(location=resolved_dest["center"], zoom_start=resolved_dest["zoom"], tiles="OpenStreetMap")
        
        # Destination Marker
        folium.Marker(
            location=resolved_dest["center"],
            popup=f"<b>{resolved_dest['name']}</b><br>Primary Destination",
            tooltip=resolved_dest["name"],
            icon=folium.Icon(color="red", icon="info-sign")
        ).addTo(m)
        
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
            ).addTo(m)
            
        # User Location & Route Line
        route_text = ""
        if st.session_state["start_coords"]:
            user_coords = st.session_state["start_coords"]
            folium.Marker(
                location=user_coords,
                popup=f"<b>{st.session_state['start_location_name']}</b><br>Your Location",
                tooltip=st.session_state["start_location_name"],
                icon=folium.Icon(color="green", icon="home")
            ).addTo(m)
            
            # Polyline between User and Destination
            folium.PolyLine(
                locations=[user_coords, resolved_dest["center"]],
                color="#0d8b80",
                weight=3,
                dash_array="5, 10",
                opacity=0.8
            ).addTo(m)
            
            # Distance computation
            dist = distance_km(user_coords, resolved_dest["center"])
            route_text = f" • **{int(dist)} km** from starting location"
            
            # Adjust bounds
            m.fit_bounds([user_coords, resolved_dest["center"]])
            
        # Render map using streamlit-folium
        st_folium(m, width="100%", height=320, returned_objects=[])
        
        source_label = "built-in place data loaded" if resolved_dest["source"] == "dataset" else "OpenStreetMap lookup loaded"
        st.markdown(f"<p style='color: #61708a; font-size: 0.82rem; margin-top: 6px;'>Showing {resolved_dest['name']} on the map • {source_label}{route_text}</p>", unsafe_allow_html=True)
        
        # Highlights detailed text
        if resolved_dest["highlights"]:
            st.markdown("**Local Highlights:**")
            for h in resolved_dest["highlights"]:
                st.markdown(f"- **{h['name']}**: {h['blurb']}")
        else:
            st.markdown("*No pre-defined highlights found in the offline database. Map coordinates resolved via geocoding.*")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Budget Split Card
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="margin:0 0 14px 0; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.05em; color: #172033;">Budget Split</h4>', unsafe_allow_html=True)
        costs = build_budget_split(st.session_state["form_budget"], st.session_state["form_style"])
        
        cost_cols = st.columns(4)
        labels = ["Travel", "Stay", "Food", "Buffer"]
        keys = ["travel", "stay", "food", "buffer"]
        for index, col in enumerate(cost_cols):
            with col:
                st.markdown(f"""
                <div class="metric-card" style="background: rgba(18,114,217,0.04);">
                    <span class="metric-label">{labels[index]}</span>
                    <span class="metric-value" style="color: #0d8b80;">Rs {int(costs[keys[index]]):,}</span>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Day-wise Itinerary Card
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="margin:0 0 14px 0; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.05em; color: #172033;">Day-wise Itinerary</h4>', unsafe_allow_html=True)
        days_plan = build_day_plan(
            resolved_dest["name"],
            st.session_state["form_days"],
            st.session_state["form_focus"],
            st.session_state["form_style"]
        )
        
        for item in days_plan:
            st.markdown(f"""
            <div class="day-card">
                <span class="day-num">{item['title']}</span>
                <span class="day-desc">{item['text']}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Packing & Safety Tips Card
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="margin:0 0 14px 0; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.05em; color: #172033;">Packing & Safety</h4>', unsafe_allow_html=True)
        tips = build_tips(
            resolved_dest["name"],
            st.session_state["form_focus"],
            st.session_state["form_group"],
            st.session_state["form_notes"]
        )
        for tip in tips:
            st.markdown(f"<div class='tip-item'>• {tip}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; color: #61708a; font-size: 0.85rem; padding: 20px 0;">
    This prototype is built for demonstration. It uses OpenStreetMap via Nominatim and Folium for mapping visualizations.
</div>
""", unsafe_allow_html=True)
