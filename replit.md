# HMPI Pollution Monitoring System

AI-powered heavy metal contamination surveillance dashboard for Tamil Nadu, built with Streamlit.

## Stack
- **Python 3.12** + **Streamlit 1.59**
- **Folium / streamlit-folium** — interactive maps & heatmaps
- **Plotly** — bar and line charts
- **scikit-learn** — linear regression for 2030 AI predictions
- **ReportLab** — PDF report generation
- **pandas** — data processing

## How to run
The app is configured as the **HMPI Dashboard** workflow and starts automatically.

```
cd frontend && echo '' | streamlit run app.py \
  --server.port 5000 --server.address 0.0.0.0 \
  --server.headless true --browser.gatherUsageStats false
```

Config file at `frontend/.streamlit/config.toml` suppresses the Streamlit email prompt.

## Project structure
```
frontend/
  app.py                  # Main Streamlit dashboard
  heavy_metal_data.csv    # Source dataset (locations, metals, years)
  .streamlit/config.toml  # Streamlit server config
```

## Features
- Pollution Overview metrics (Average HMPI, Highest HMPI, district count, high-risk zones)
- Interactive district/year filter in sidebar with risk badge
- Folium map with colour-coded circle markers (Safe → Critical)
- Pollution heatmap with green-to-red gradient
- Animated time-lapse heatmap (2021–2025)
- District HMPI comparison bar chart
- Per-district HMPI trend line chart
- AI 2030 pollution prediction (linear regression)
- Policy recommendation panel
- PDF government report generator
- CSV dataset download

## User preferences
- Green dark theme throughout the UI
