# Hack_It_Out_2026
# 🌍 PyClimaExplorer
### Interactive Climate Data Visualisation Dashboard

> **Technex '26 — Hack It Out** | IIT (BHU) Varanasi | 13–15 March 2026
> **Team:** Cosmos_Sync | GLA University, Mathura
> video link-: https://youtu.be/Rj10iYAkzIA?feature=shared

---

## 🎯 Problem Statement

Climate scientists generate terabytes of raw NetCDF data daily — but there are **no accessible tools** to explore it without deep Python expertise. Researchers, students, and the public are locked out of critical climate insights.

**PyClimaExplorer solves this** with a zero-code, browser-based interactive dashboard.

---

## ✨ Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Upload Any NetCDF** | Drag-and-drop `.nc` files from ERA5, CESM, or any standard source |
| 2 | **Global Heatmap** | Colour-coded world map for any variable at any time step |
| 3 | **Time-Series Explorer** | Pick any lat/lon — instant time-series graph |
| 4 | **Compare Mode** | Side-by-side two time steps + animated difference map |
| 5 | **Story Mode** | Guided tour of 4 real climate anomalies with explanations |
| 6 | **Zonal Mean Profile** | Variable vs latitude band chart |
| 7 | **Sparklines** | All-variable mini-trends at your selected location |
| 8 | **Built-in Sample Data** | Works immediately — no file download needed for demo |

---

## 🚀 Quick Start (3 Steps)

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Run the app
```bash
py -3.11 -m streamlit run app.py
```

> ✅ `climate_data.nc` is **pre-installed** — no download or generation needed!
Opens at **http://localhost:8501** 🎉

---

## 🌐 Deploy to Streamlit Cloud

```
1. Push this folder to a GitHub repo
2. Go to https://share.streamlit.io
3. Connect repo → select app.py → click Deploy
4. Share the public URL with judges!
```

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-----------|
| Web Framework | Streamlit |
| Data Loading | Xarray + NetCDF4 |
| Data Wrangling | Pandas + NumPy |
| Visualisation | Plotly Express + Graph Objects |
| Deployment | Streamlit Cloud |

---

## 📂 Project Structure

```
PyClimaExplorer/
├── app.py                ← Main Streamlit dashboard (dark theme UI)
├── generate_dataset.py   ← One-time script to create sample NetCDF
├── requirements.txt      ← All Python dependencies
└── README.md             ← This file
```

---

## 📡 Real NetCDF Data Sources

| Source | URL | Dataset |
|--------|-----|---------|
| ERA5 (ECMWF) | https://cds.climate.copernicus.eu | Monthly averaged reanalysis |
| NCAR/UCAR | https://rda.ucar.edu | CESM climate model output |
| NOAA CDR | https://www.ncei.noaa.gov | Climate data records |

> The app runs with built-in sample data — no download needed for the demo.

---

## 👥 Team — Cosmos_Sync

| Name | Registration ID |
|------|----------------|
| Aryan Agarwal | TX261925 |
| Ashish Sindhi | TX262412 |
| Aditya Mishra | TX262422 |
| Sarthak Dubey | TX262429 |

**GLA University, Mathura**

---

## ✅ Hackathon Deliverables Checklist

- [x] Working web dashboard (Streamlit)
- [x] NetCDF file upload support
- [x] Global heatmap visualisation
- [x] Interactive time-series explorer
- [x] Variable & time selector
- [x] **Bonus:** Year comparison + difference map
- [x] **Bonus:** Guided Story Mode (4 climate anomalies)
- [x] One-command deploy via Streamlit Cloud
- [x] Sample dataset generator script
- [x] Full README with setup instructions

---

*Technex '26 — Hack It Out | IIT (BHU) Varanasi | 13–15 March 2026*
