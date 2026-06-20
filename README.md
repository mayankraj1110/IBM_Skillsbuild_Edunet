# ✈️ CampusTrail AI: Student Travel Planner

CampusTrail AI is a modern, student-focused travel planner designed to build budget-friendly, personalized itineraries. By taking a destination, budget limit, duration, travel style, group composition, and personal preferences, it automatically computes a structured budget split, a day-wise itinerary, packing/safety checklists, and interactive map routes.

---

## 🌟 Key Features

- **🎓 Student-Oriented Layout**: Optimized for budget constraints and group configurations (solo, friends, couples, families).
- **📊 Automatic Budget Splitting**: Dynamically divides your budget across Travel, Stays, Food, and Buffer based on your travel style (Budget, Balanced, Comfort).
- **🗺️ Interactive HTML Maps**: Uses `folium` to display interactive maps inside Gradio, showing the destination, markers for local highlights, and routing lines between your starting location and target.
- **⚡ Preset Configurations**: Quick-start templates for major destinations like **Weekend Goa**, **Budget Jaipur**, and **Nature Manali**.
- **🔍 Geocoding Integration**: Queries OpenStreetMap's Nominatim API to locate destinations worldwide in real-time, loading coordinates, seasons, transport guidelines, and transit hubs.
- **🎨 Glassmorphic Aesthetic**: Designed with custom responsive CSS styling that provides a high-end, premium experience.

---

## 📂 Project Structure

```text
CampusTrailAI/
├── .gitignore              # Ignores venv, cache, and system files
├── app.py                  # Main Gradio application file
├── requirements.txt        # Python package dependencies
└── README.md               # Project documentation (this file)
```

---

## 🚀 Running Locally

Follow these instructions to run the application on your computer:

### 1. Clone the repository
```bash
git clone https://github.com/your-username/CampusTrailAI.git
cd CampusTrailAI
```

### 2. Create and activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Gradio application
```bash
python app.py
```

The app will start locally, opening a browser tab automatically. Additionally, because the application is launched with sharing enabled, it will print a secure, public shareable link (e.g., `https://xxxx.gradio.live`) in the console.

---

## ☁️ Deployment Guide

This project is ready to be deployed to the cloud for free:

### Option A: Hugging Face Spaces (Recommended for Gradio)
1. Visit [huggingface.co/spaces](https://huggingface.co/spaces) and create a new Space.
2. Select **Gradio** as the SDK.
3. Clone the space repository locally or upload these files (`app.py`, `requirements.txt`) directly via the web interface.
4. Commit and push the files. Hugging Face will automatically build and host the Gradio app on a permanent public URL.
