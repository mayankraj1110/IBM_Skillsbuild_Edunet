# ✈️ CampusTrail AI: Student Travel Planner

CampusTrail AI is a modern, student-focused travel planner designed to build budget-friendly, personalized itineraries. By taking a destination, budget limit, duration, travel style, group composition, and personal preferences, it automatically computes a structured budget split, a day-wise itinerary, packing/safety checklists, and interactive map routes.

---

## 🔗 Live Demo Link
https://ibmskillsbuildedunet-lmfjfs4b5whvhgmv4boizh.streamlit.app/

---

## 🌟 Key Features

- **🎓 Student-Oriented Layout**: Optimized for budget constraints and group configurations (solo, friends, couples, families).
- **📊 Automatic Budget Splitting**: Dynamically divides your budget across Travel, Stays, Food, and Buffer based on your travel style (Budget, Balanced, Comfort).
- **🗺️ Interactive Folium Maps**: Integrates Leaflet-based maps displaying the destination, markers for local highlights, and routing lines between your starting location and target.
- **⚡ Preset Configurations**: Quick-start templates for major destinations like **Weekend Goa**, **Budget Jaipur**, and **Nature Manali**.
- **🔍 Geocoding Integration**: Queries OpenStreetMap's Nominatim API to locate destinations worldwide in real-time, loading coordinates, seasons, transport guidelines, and transit hubs.
- **🎨 Glassmorphic Aesthetic**: Designed with custom responsive CSS styling that provides a high-end, premium experience.

---

## 📂 Project Structure

```text
CampusTrailAI/
├── .streamlit/
│   └── config.toml         # Custom theme configuration for Streamlit
├── .gitignore              # Ignores venv, cache, and system files
├── app.py                  # Main Streamlit application file
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

### 4. Run the Streamlit application
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 📓 Try it Instantly (Jupyter Notebook / Google Colab)

For an instant test run without setting up Python environments manually on your system, you can use the included Jupyter notebook:
1. Open the [run_notebook.ipynb](file:///home/babydemonx/Documents/Project/CampusTrailAI/run_notebook.ipynb) locally, or upload it to [Google Colab](https://colab.research.google.com/).
2. Run the cells in order to install requirements, launch the Streamlit server in the background, and expose a secure public URL.

---

## ☁️ Deployment Guide

This project is ready to be deployed to the cloud for free:

### Option A: Streamlit Community Cloud (Recommended)
1. Push this repository to your **GitHub** account.
2. Visit [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3. Click **New app**, select your repository (`CampusTrailAI`), branch (`main`), and set the main file path to `app.py`.
4. Click **Deploy!** Your app will be live with a permanent URL.

### Option B: Hugging Face Spaces
1. Create a new Space on [Hugging Face](https://huggingface.co/spaces).
2. Choose **Streamlit** as the SDK.
3. Clone the space repository locally or upload these project files (`app.py`, `requirements.txt`, `.streamlit/`) directly.
4. Commit and push the files. Hugging Face will automatically build and deploy the app.
