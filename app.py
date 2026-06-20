import gradio as gr
import folium
import requests
import math

# Custom CSS for glassmorphic styling, fonts, and grid layout in Gradio
css = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

body, .gradio-container {
    font-family: 'Outfit', sans-serif !important;
    background: 
        radial-gradient(circle at top left, rgba(18, 114, 217, 0.08), transparent 40%),
        radial-gradient(circle at 85% 15%, rgba(240, 165, 58, 0.08), transparent 30%),
        linear-gradient(140deg, #dff2ff 0%, #edf8ff 40%, #fdf7e9 100%) !important;
    background-attachment: fixed !important;
}

.hero-banner {
    background: rgba(248, 251, 255, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.45);
    border-radius: 30px;
    padding: 30px;
    margin-bottom: 20px;
    backdrop-filter: blur(14px);
    box-shadow: 0 20px 50px rgba(17, 44, 80, 0.06);
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
    margin-bottom: 10px;
}

.hero-title {
    font-size: clamp(2rem, 3.5vw, 3.5rem);
    font-weight: 800;
    line-height: 0.95;
    letter-spacing: -0.04em;
    margin: 0 0 10px 0;
    color: #172033;
}

.hero-desc {
    color: #61708a;
    font-size: 1.02rem;
    line-height: 1.6;
    margin: 0;
    max-width: 800px;
}

/* Glassmorphic output styling */
.glass-panel {
    background: rgba(255, 255, 255, 0.72) !important;
    border: 1px solid rgba(23, 32, 51, 0.12) !important;
    border-radius: 24px !important;
    padding: 20px !important;
    backdrop-filter: blur(12px) !important;
    box-shadow: 0 10px 30px rgba(17, 44, 80, 0.04) !important;
    margin-bottom: 16px !important;
}

.section-hdr {
    font-size: 1.05rem;
    font-weight: 700;
    color: #172033;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 12px;
    border-bottom: 1px solid rgba(23, 32, 51, 0.08);
    padding-bottom: 6px;
}

/* Metric grids */
.metric-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-top: 10px;
}

.budget-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-top: 10px;
}

.metric-card {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(23, 32, 51, 0.08);
    border-radius: 14px;
    padding: 10px;
    text-align: center;
}

.metric-label {
    font-size: 0.75rem;
    color: #61708a;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    display: block;
    margin-bottom: 2px;
}

.metric-val {
    font-size: 1.1rem;
    font-weight: 700;
    color: #172033;
}

/* Day Cards */
.day-card {
    background: linear-gradient(135deg, rgba(18, 114, 217, 0.05), rgba(13, 139, 128, 0.04));
    border: 1px solid rgba(18, 114, 217, 0.08);
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 10px;
}

.day-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #1272d9;
    margin-bottom: 4px;
    display: block;
}

.day-text {
    font-size: 0.9rem;
    color: #3b485e;
    line-height: 1.5;
}

/* General Layout helpers */
.badge {
    background: rgba(13, 139, 128, 0.12);
    color: #0d8b80;
    font-weight: 700;
    font-size: 0.8rem;
    padding: 4px 10px;
    border-radius: 999px;
}
"""

# Presets and Data
sample_trips = {
    "Goa": {
        "destination": "Goa",
        "days": 3,
        "budget": 9000,
        "group": "Friends",
        "style": "Balanced",
        "focus": "Food",
        "notes": "Prefer beaches, affordable cafes, scooter travel, and a relaxed night market."
    },
    "Jaipur": {
        "destination": "Jaipur",
        "days": 2,
        "budget": 5000,
        "group": "Friends",
        "style": "Budget",
        "focus": "Culture",
        "notes": "Want forts, local street food, shared transport, and photo spots."
    },
    "Manali": {
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
        headers = {"User-Agent": "CampusTrailAI-Gradio/1.0"}
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

# Core logic function returning HTML strings
def generate_itinerary(dest, days, budget, group, style, focus, notes, start_loc):
    if not dest.strip():
        # Default empty page HTML
        empty_snap = f"""
        <div class="glass-panel">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin:0; font-size: 1.05rem; font-weight:700;">Trip Snapshot</h4>
                <span class="badge">No Plan Loaded</span>
            </div>
            <div class="metric-row">
                <div class="metric-card"><span class="metric-label">Budget Band</span><span class="metric-val">-</span></div>
                <div class="metric-card"><span class="metric-label">Travel Style</span><span class="metric-val">-</span></div>
                <div class="metric-card"><span class="metric-label">Duration</span><span class="metric-val">-</span></div>
            </div>
        </div>
        """
        empty_overview = """
        <div class="glass-panel">
            <div class="section-hdr">Trip Overview</div>
            <p style="color: #61708a; margin: 0;">Enter details on the left and submit to generate your student-friendly itinerary.</p>
        </div>
        """
        # Create empty map
        m = folium.Map(location=[22.9734, 78.6569], zoom_start=5, tiles="OpenStreetMap")
        map_html = m._repr_html_()
        return empty_snap, empty_overview, map_html, "", "", ""

    resolved = resolve_dest(dest)
    if not resolved:
        error_snap = f"""
        <div class="glass-panel">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin:0; font-size: 1.05rem; font-weight:700;">Trip Snapshot</h4>
                <span class="badge" style="background: rgba(220,53,69,0.1); color: #dc3545;">Lookup Failed</span>
            </div>
        </div>
        """
        error_overview = f"""
        <div class="glass-panel">
            <div class="section-hdr">Trip Overview</div>
            <p style="color: #dc3545; margin: 0;">Could not locate destination <b>"{dest}"</b> on the map. Please check your spelling or connection.</p>
        </div>
        """
        m = folium.Map(location=[22.9734, 78.6569], zoom_start=5)
        return error_snap, error_overview, m._repr_html_(), "", "", ""

    # Geocode starting location if provided
    start_coords = None
    resolved_start_name = ""
    if start_loc.strip():
        start_resolved = resolve_dest(start_loc)
        if start_resolved:
            start_coords = start_resolved["center"]
            resolved_start_name = start_resolved["name"]

    # 1. Snapshot HTML
    badge = f"{resolved['name']} • {style}"
    snap_html = f"""
    <div class="glass-panel">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <h4 style="margin:0; font-size:1.05rem; font-weight:700;">Trip Snapshot</h4>
            <span class="badge">{badge}</span>
        </div>
        <div class="metric-row">
            <div class="metric-card">
                <span class="metric-label">Budget Band</span>
                <span class="metric-val">{get_budget_band(budget)}</span>
            </div>
            <div class="metric-card">
                <span class="metric-label">Travel Style</span>
                <span class="metric-val">{style}</span>
            </div>
            <div class="metric-card">
                <span class="metric-label">Duration</span>
                <span class="metric-val">{days} Days</span>
            </div>
        </div>
        <div style="margin-top: 12px; padding: 10px; background: rgba(255,255,255,0.6); border-radius: 10px; font-size: 0.88rem; font-weight: 600;">
            <span style="color: #61708a; display: block; font-size: 0.72rem; text-transform: uppercase; margin-bottom: 2px;">Planner Summary</span>
            {resolved['name']} {focus.lower()} trip for {group.lower()} travelers.
        </div>
    </div>
    """

    # 2. Overview HTML
    overview_text = f"CampusTrail suggests a {days}-day {focus.lower()} trip to {resolved['name']} for a {group.lower()} group with a budget of Rs {int(budget):,}. The plan aims to keep travel practical, affordable, and student-friendly."
    overview_html = f"""
    <div class="glass-panel">
        <div class="section-hdr">Trip Overview</div>
        <p style="margin: 0; color: #3b485e; line-height:1.6;">{overview_text}</p>
    </div>
    """

    # 3. Folium Map HTML
    m = folium.Map(location=resolved["center"], zoom_start=resolved["zoom"], tiles="OpenStreetMap")
    folium.Marker(
        location=resolved["center"],
        popup=f"<b>{resolved['name']}</b><br>Primary Destination",
        tooltip=resolved["name"],
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

    for spot in resolved["highlights"]:
        folium.CircleMarker(
            location=spot["coords"],
            radius=7,
            popup=f"<b>{spot['name']}</b><br>{spot['blurb']}",
            tooltip=spot["name"],
            color="#1272d9",
            fill=True,
            fill_color="#f0a53a",
            fill_opacity=0.85
        ).add_to(m)

    distance_status = ""
    if start_coords:
        folium.Marker(
            location=start_coords,
            popup=f"<b>{resolved_start_name}</b><br>Your Location",
            tooltip=resolved_start_name,
            icon=folium.Icon(color="green", icon="home")
        ).add_to(m)
        
        folium.PolyLine(
            locations=[start_coords, resolved["center"]],
            color="#0d8b80",
            weight=3,
            dash_array="5, 10",
            opacity=0.8
        ).add_to(m)
        
        dist = distance_km(start_coords, resolved["center"])
        distance_status = f" • <b>{int(dist)} km</b> from your starting location ({resolved_start_name})"
        m.fit_bounds([start_coords, resolved["center"]])

    source_label = "built-in place data loaded" if resolved["source"] == "dataset" else "OpenStreetMap lookup loaded"
    map_status = f"Showing {resolved['name']} on the map • {source_label}{distance_status}"
    
    highlights_html = ""
    if resolved["highlights"]:
        highlights_html = "<div style='margin-top:10px; font-size:0.88rem;'><b>Local Highlights:</b><ul>"
        for h in resolved["highlights"]:
            highlights_html += f"<li><b>{h['name']}</b>: {h['blurb']}</li>"
        highlights_html += "</ul></div>"
    
    map_box_html = f"""
    <div class="glass-panel">
        <div class="section-hdr">Map & Location Insights</div>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 0.88rem; margin-bottom:10px;">
            <div><b>Coordinates:</b> {resolved['center'][0]:.4f}, {resolved['center'][1]:.4f}<br><b>Best Base:</b> {resolved['base']}</div>
            <div><b>Transport:</b> {resolved['transport']}<br><b>Best Season:</b> {resolved['season']}</div>
        </div>
        <div style="border-radius:14px; overflow:hidden; border: 1px solid rgba(23,32,51,0.1);">{m._repr_html_()}</div>
        <p style="color: #61708a; font-size: 0.8rem; margin: 8px 0 0 0;">{map_status}</p>
        {highlights_html}
    </div>
    """

    # 4. Budget Split HTML
    costs = build_budget_split(budget, style)
    budget_html = f"""
    <div class="glass-panel">
        <div class="section-hdr">Budget Split</div>
        <div class="budget-row">
            <div class="metric-card" style="background: rgba(18,114,217,0.04);">
                <span class="metric-label">Travel</span>
                <span class="metric-val" style="color: #0d8b80;">Rs {int(costs['travel']):,}</span>
            </div>
            <div class="metric-card" style="background: rgba(18,114,217,0.04);">
                <span class="metric-label">Stay</span>
                <span class="metric-val" style="color: #0d8b80;">Rs {int(costs['stay']):,}</span>
            </div>
            <div class="metric-card" style="background: rgba(18,114,217,0.04);">
                <span class="metric-label">Food</span>
                <span class="metric-val" style="color: #0d8b80;">Rs {int(costs['food']):,}</span>
            </div>
            <div class="metric-card" style="background: rgba(18,114,217,0.04);">
                <span class="metric-label">Buffer</span>
                <span class="metric-val" style="color: #0d8b80;">Rs {int(costs['buffer']):,}</span>
            </div>
        </div>
    </div>
    """

    # 5. Day-wise Itinerary HTML
    days_plan = []
    base_plans = focus_plans.get(focus, focus_plans["Mixed"])
    for i in range(1, days + 1):
        if i == 1:
            intro = f"Arrive in {resolved['name']}, settle in, and map nearby transport and food options."
        elif i == days:
            intro = "Keep the final day lighter, buy essentials, and prepare return travel."
        else:
            intro = "Use the day for focused exploration with a student-budget schedule."
        
        style_line = ""
        if style == "Budget":
            style_line = "Prefer buses, shared autos, hostels, and fixed daily spending."
        elif style == "Comfort":
            style_line = "Use direct transport, better stays, and reserved time for rest."
        else:
            style_line = "Mix public transport with one convenience upgrade if needed."
            
        base_action = base_plans[(i - 1) % len(base_plans)]
        days_plan.append({
            "title": f"Day {i}",
            "text": f"{intro} {base_action} {style_line}"
        })

    day_cards_html = ""
    for d in days_plan:
        day_cards_html += f"""
        <div class="day-card">
            <span class="day-title">{d['title']}</span>
            <span class="day-text">{d['text']}</span>
        </div>
        """
    itinerary_html = f"""
    <div class="glass-panel">
        <div class="section-hdr">Day-wise Itinerary</div>
        {day_cards_html}
    </div>
    """

    # 6. Packing & Tips HTML
    tips = [
        f"Save offline maps and keep the {resolved['name']} hotel or hostel address pinned.",
        "Carry student ID, one power bank, refillable water bottle, and emergency cash.",
        "Check local transport closing times before planning late evening travel."
    ]
    if focus in ["Adventure", "Nature"]:
        tips.append("Pack walking shoes, weather protection, and basic medicines.")
    elif focus == "Food":
        tips.append("Set a food budget cap for each day and shortlist clean, well-rated places.")
    else:
        tips.append("Start early to avoid crowds and reduce transport waiting time.")
        
    if group == "Solo":
        tips.append("Share your live location or daily route summary with a trusted contact.")
    else:
        tips.append("Set one common meet-up point in case the group splits during the day.")
        
    if notes.strip():
        truncated_notes = notes.strip()[:90] + ("..." if len(notes.strip()) > 90 else "")
        tips.append(f"Planner note used: {truncated_notes}")

    tips_li = "".join([f"<li style='margin-bottom: 6px;'>{t}</li>" for t in tips])
    tips_html = f"""
    <div class="glass-panel">
        <div class="section-hdr">Packing & Safety</div>
        <ul style="margin: 0; padding-left: 18px; color: #3b485e; font-size:0.92rem; line-height: 1.5;">
            {tips_li}
        </ul>
    </div>
    """

    return snap_html, overview_html, map_box_html, budget_html, itinerary_html, tips_html


# Building Gradio Interface
with gr.Blocks(css=css, title="CampusTrail AI") as demo:
    # Banner
    gr.HTML("""
    <div class="hero-banner">
        <div class="eyebrow">Capstone Project • AI Travel Planner</div>
        <h1 class="hero-title">CampusTrail AI</h1>
        <p class="hero-desc">
            A student-focused travel planner that builds a budget-friendly trip outline from destination,
            budget, number of days, travel style, and interests. It creates a day-wise plan, cost split,
            packing checklist, and practical tips in one screen.
        </p>
    </div>
    """)

    with gr.Row(equal_height=False):
        # Left Panel (Inputs)
        with gr.Column(scale=45):
            gr.HTML('<div class="section-hdr">Plan a Trip</div>')
            gr.Markdown("Fill the details or click a preset below. Enter starting location to draw the routing line.")
            
            # Preset Row
            with gr.Row():
                goa_btn = gr.Button("Weekend Goa", size="sm", elem_classes=["preset-btn"])
                jaipur_btn = gr.Button("Budget Jaipur", size="sm", elem_classes=["preset-btn"])
                manali_btn = gr.Button("Nature Manali", size="sm", elem_classes=["preset-btn"])

            # Inputs Group
            with gr.Group():
                dest = gr.Textbox(label="Destination", placeholder="Jaipur, Goa, Manali", value="")
                
                with gr.Row():
                    days = gr.Dropdown(label="Trip Duration", choices=[2, 3, 4, 5], value=3)
                    budget = gr.Number(label="Budget (INR)", value=6000, minimum=1000, step=500)
                
                with gr.Row():
                    group = gr.Dropdown(label="Travel Group", choices=["Solo", "Friends", "Couple", "Family"], value="Friends")
                    style = gr.Dropdown(label="Travel Style", choices=["Budget", "Balanced", "Comfort"], value="Balanced")
                    focus = gr.Dropdown(label="Trip Focus", choices=["Culture", "Adventure", "Food", "Nature", "Mixed"], value="Culture")
                
                notes = gr.Textbox(label="Preferences / Notes", placeholder="e.g. prefer trains, low-cost stays, local food...", lines=3)
                
                gr.HTML("<hr style='margin: 10px 0; opacity: 0.15;'/>")
                start_loc = gr.Textbox(label="Your Starting Location (for Route planning)", placeholder="e.g. Mumbai, Delhi, Bangalore", value="")
            
            with gr.Row():
                submit_btn = gr.Button("Generate Itinerary", variant="primary")
                reset_btn = gr.Button("Reset Form")

        # Right Panel (Outputs)
        with gr.Column(scale=55):
            gr.HTML('<div class="section-hdr">Generated Plan</div>')
            
            # Interactive HTML outputs
            out_snap = gr.HTML()
            out_overview = gr.HTML()
            out_map = gr.HTML()
            out_budget = gr.HTML()
            out_itinerary = gr.HTML()
            out_tips = gr.HTML()

    # Preset Event Handler Bindings
    def load_preset(name):
        p = sample_trips[name]
        return p["destination"], p["days"], p["budget"], p["group"], p["style"], p["focus"], p["notes"]

    goa_btn.click(fn=lambda: load_preset("Goa"), outputs=[dest, days, budget, group, style, focus, notes])
    jaipur_btn.click(fn=lambda: load_preset("Jaipur"), outputs=[dest, days, budget, group, style, focus, notes])
    manali_btn.click(fn=lambda: load_preset("Manali"), outputs=[dest, days, budget, group, style, focus, notes])

    # Submit Event Binding
    submit_btn.click(
        fn=generate_itinerary,
        inputs=[dest, days, budget, group, style, focus, notes, start_loc],
        outputs=[out_snap, out_overview, out_map, out_budget, out_itinerary, out_tips]
    )

    # Reset Event Binding
    def clear_form():
        return "", 3, 6000, "Friends", "Balanced", "Culture", "", ""

    reset_btn.click(
        fn=clear_form,
        outputs=[dest, days, budget, group, style, focus, notes, start_loc]
    ).then(
        fn=generate_itinerary,
        inputs=[dest, days, budget, group, style, focus, notes, start_loc],
        outputs=[out_snap, out_overview, out_map, out_budget, out_itinerary, out_tips]
    )

    # Load initial default state on mount
    demo.load(
        fn=generate_itinerary,
        inputs=[dest, days, budget, group, style, focus, notes, start_loc],
        outputs=[out_snap, out_overview, out_map, out_budget, out_itinerary, out_tips]
    )

# Launch with share=True for public deployment link
if __name__ == "__main__":
    demo.launch(share=True)
