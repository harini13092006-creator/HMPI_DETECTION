import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap, HeatMapWithTime
import plotly.express as px
from sklearn.linear_model import LinearRegression
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(
    page_title="HMPI Pollution Monitoring System",
    page_icon="🌿",
    layout="wide"
)

# ─────────────────────────────────────────────
# Green Theme CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Base & Background ── */
    .stApp {
        background: linear-gradient(135deg, #0a1f0e 0%, #0d2b14 40%, #102d18 100%);
        color: #d4f5d4;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d2b14 0%, #1a4d2e 100%);
        border-right: 1px solid #2d6a4f;
    }
    [data-testid="stSidebar"] * {
        color: #a8e6a3 !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #52c96e !important;
        font-weight: 600;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] {
        background-color: #1a4d2e !important;
        border-color: #2d8a4e !important;
    }

    /* ── Headers ── */
    h1, h2, h3 {
        color: #52c96e !important;
    }
    .stSubheader, [data-testid="stHeading"] {
        color: #52c96e !important;
    }

    /* ── Metric cards ── */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a4d2e, #1e5c35);
        border: 1px solid #2d8a4e;
        border-radius: 12px;
        padding: 16px !important;
        box-shadow: 0 4px 15px rgba(45, 138, 78, 0.2);
    }
    [data-testid="stMetricLabel"] {
        color: #a8e6a3 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    [data-testid="stMetricValue"] {
        color: #52c96e !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] {
        border: 1px solid #2d6a4f;
        border-radius: 10px;
        overflow: hidden;
    }

    /* ── Buttons ── */
    .stButton > button, .stDownloadButton > button {
        background: linear-gradient(135deg, #2d8a4e, #1a5c35) !important;
        color: #ffffff !important;
        border: 1px solid #52c96e !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 3px 10px rgba(45, 138, 78, 0.3) !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #3da862, #2d8a4e) !important;
        box-shadow: 0 5px 18px rgba(45, 138, 78, 0.5) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Section dividers ── */
    hr {
        border: none;
        border-top: 1px solid #2d6a4f;
        margin: 1.5rem 0;
    }

    /* ── Plotly chart container ── */
    .js-plotly-plot {
        border: 1px solid #2d6a4f;
        border-radius: 10px;
        overflow: hidden;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0a1f0e; }
    ::-webkit-scrollbar-thumb { background: #2d8a4e; border-radius: 3px; }

    /* ── Section header pill ── */
    .section-pill {
        display: inline-block;
        background: linear-gradient(135deg, #1a4d2e, #2d8a4e);
        border: 1px solid #52c96e;
        border-radius: 20px;
        padding: 4px 16px;
        font-size: 0.75rem;
        font-weight: 600;
        color: #a8e6a3;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Header with Logo
# ─────────────────────────────────────────────
st.markdown("""
<div style="display:flex; align-items:center; gap:18px; padding:10px 0 18px 0; border-bottom:1px solid #2d6a4f; margin-bottom:24px;">
    <svg xmlns="http://www.w3.org/2000/svg" width="68" height="68" viewBox="0 0 68 68">
        <circle cx="34" cy="34" r="34" fill="#1a4d2e"/>
        <circle cx="34" cy="34" r="30" fill="none" stroke="#52c96e" stroke-width="1.5" stroke-dasharray="5 3"/>
        <!-- Globe lines -->
        <ellipse cx="34" cy="34" rx="16" ry="22" fill="none" stroke="#2d8a4e" stroke-width="1.2"/>
        <ellipse cx="34" cy="34" rx="22" ry="22" fill="none" stroke="#2d8a4e" stroke-width="1.2"/>
        <line x1="12" y1="34" x2="56" y2="34" stroke="#2d8a4e" stroke-width="1.2"/>
        <line x1="34" y1="12" x2="34" y2="56" stroke="#2d8a4e" stroke-width="1.2"/>
        <!-- Leaf -->
        <path d="M34 24 Q44 28 40 40 Q34 36 30 30 Q28 24 34 24Z" fill="#52c96e" opacity="0.9"/>
        <path d="M34 24 L37 36" stroke="#1a4d2e" stroke-width="1" fill="none"/>
        <!-- Water drop -->
        <path d="M26 42 Q26 48 30 48 Q34 48 34 42 Q32 38 30 36 Q28 38 26 42Z" fill="#4ecca3" opacity="0.85"/>
        <!-- Alert ring -->
        <circle cx="44" cy="24" r="7" fill="#ff6b6b" opacity="0.9"/>
        <text x="44" y="28" text-anchor="middle" font-size="9" font-weight="bold" fill="white">!</text>
    </svg>
    <div>
        <div style="font-size:1.75rem; font-weight:800; color:#52c96e; line-height:1.1; letter-spacing:-0.5px;">
            HMPI Pollution Monitor
        </div>
        <div style="font-size:0.9rem; color:#a8e6a3; margin-top:4px;">
            🌿 AI-Powered Heavy Metal Contamination Surveillance · Tamil Nadu
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Sidebar branding
# ─────────────────────────────────────────────
st.sidebar.markdown("""
<div style="text-align:center; padding:12px 0 16px 0; border-bottom:1px solid #2d6a4f; margin-bottom:12px;">
    <div style="font-size:1.1rem; font-weight:700; color:#52c96e;">🌿 Control Panel</div>
    <div style="font-size:0.75rem; color:#a8e6a3; margin-top:3px;">Filter & Explore Data</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Load Dataset
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("heavy_metal_data.csv")
    return df
df = load_data()

# ─────────────────────────────────────────────
# WHO Standards
# ─────────────────────────────────────────────
WHO_LIMITS = {
    "Ni": 0.02,
    "Zn": 3.0,
    "Pb": 0.01,
    "Cd": 0.003,
    "Cr": 0.05
}

# ─────────────────────────────────────────────
# HMPI Calculation
# ─────────────────────────────────────────────
def calculate_hmpi(row):
    hmpi = 0
    for metal in WHO_LIMITS:
        hmpi += (row[metal] / WHO_LIMITS[metal]) * 20
    return hmpi

df["HMPI"] = df.apply(calculate_hmpi, axis=1)

# ─────────────────────────────────────────────
# Risk Classification
# ─────────────────────────────────────────────
def classify_risk(hmpi):
    if hmpi < 50:
        return "Safe"
    elif hmpi < 100:
        return "Moderate"
    elif hmpi < 200:
        return "High"
    else:
        return "Critical"

df["Risk"] = df["HMPI"].apply(classify_risk)

# ─────────────────────────────────────────────
# Policy Suggestions
# ─────────────────────────────────────────────
def policy_advice(risk):
    if risk == "Safe":
        return "✅ Maintain regular monitoring"
    elif risk == "Moderate":
        return "⚠️ Increase monitoring and regulate pollution sources"
    elif risk == "High":
        return "🚨 Install treatment plants and restrict industrial discharge"
    else:
        return "🔴 Immediate government intervention required"

df["Policy"] = df["Risk"].apply(policy_advice)

# ─────────────────────────────────────────────
# Dashboard Metrics
# ─────────────────────────────────────────────
st.markdown('<div class="section-pill">📊 Overview</div>', unsafe_allow_html=True)
st.subheader("Pollution Overview")

col1, col2, col3, col4 = st.columns(4)
col1.metric("📈 Average HMPI", round(df["HMPI"].mean(), 2))
col2.metric("🔺 Highest HMPI", round(df["HMPI"].max(), 2))
col3.metric("🏙️ Total Districts", df["Location"].nunique())
risk_counts = df["Risk"].value_counts()
critical_count = risk_counts.get("Critical", 0) + risk_counts.get("High", 0)
col4.metric("⚠️ High-Risk Zones", int(critical_count))

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Filters
# ─────────────────────────────────────────────
district = st.sidebar.selectbox("📍 Select District", df["Location"].unique())
year = st.sidebar.selectbox("📅 Select Year", sorted(df["Date"].unique()))

filtered = df[(df["Location"] == district) & (df["Date"] == year)]

# Risk badge helper
def risk_badge(risk):
    colors = {"Safe": "#52c96e", "Moderate": "#f0c040", "High": "#f08040", "Critical": "#ff4b4b"}
    return colors.get(risk, "#a8e6a3")

# Sidebar risk summary
if not filtered.empty:
    risk_val = filtered["Risk"].values[0]
    hmpi_val = round(filtered["HMPI"].values[0], 2)
    badge_color = risk_badge(risk_val)
    st.sidebar.markdown(f"""
    <div style="margin-top:16px; background:#1a4d2e; border:1px solid #2d6a4f; border-radius:10px; padding:14px; text-align:center;">
        <div style="color:#a8e6a3; font-size:0.8rem; margin-bottom:6px;">Current Selection</div>
        <div style="color:#52c96e; font-weight:700; font-size:1rem;">{district} · {year}</div>
        <div style="color:#d4f5d4; font-size:0.85rem; margin-top:4px;">HMPI: <b>{hmpi_val}</b></div>
        <div style="display:inline-block; background:{badge_color}22; border:1px solid {badge_color}; border-radius:20px; padding:3px 14px; margin-top:8px; color:{badge_color}; font-size:0.8rem; font-weight:700;">{risk_val}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-pill">🗂️ Data</div>', unsafe_allow_html=True)
st.subheader("District Pollution Data")
st.dataframe(filtered, width="stretch")

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Interactive Map
# ─────────────────────────────────────────────
st.markdown('<div class="section-pill">🗺️ Maps</div>', unsafe_allow_html=True)
st.subheader("Pollution Map")

m = folium.Map(location=[11.5, 78], zoom_start=7, tiles="CartoDB dark_matter")

for _, row in df.iterrows():
    if row["Risk"] == "Safe":
        color = "#52c96e"
    elif row["Risk"] == "Moderate":
        color = "#f0c040"
    elif row["Risk"] == "High":
        color = "#f08040"
    else:
        color = "#ff4b4b"

    folium.CircleMarker(
        location=[row["Lat"], row["Lon"]],
        radius=8,
        popup=folium.Popup(
            f"<b>{row['Location']}</b><br>HMPI: {round(row['HMPI'], 2)}<br>Risk: {row['Risk']}",
            max_width=180
        ),
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8,
        weight=2
    ).add_to(m)

st_folium(m, use_container_width=True, height=480)

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Heatmap
# ─────────────────────────────────────────────
st.subheader("Pollution Heatmap")

heat_data = df[["Lat", "Lon", "HMPI"]].values.tolist()
heatmap = folium.Map(location=[11.5, 78], zoom_start=7, tiles="CartoDB dark_matter")
HeatMap(heat_data, radius=25, gradient={0.2: "#52c96e", 0.5: "#f0c040", 0.8: "#f08040", 1.0: "#ff4b4b"}).add_to(heatmap)
st_folium(heatmap, use_container_width=True, height=480)

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Animated Pollution Map
# ─────────────────────────────────────────────
st.subheader("Animated Pollution Map (2021–2025)")

years = sorted(df["Date"].unique())
heat_frames = []
for y in years:
    data = df[df["Date"] == y]
    heat_frames.append(data[["Lat", "Lon", "HMPI"]].values.tolist())

animated_map = folium.Map(location=[11.5, 78], zoom_start=7, tiles="CartoDB dark_matter")
HeatMapWithTime(
    heat_frames,
    index=[str(y) for y in years],
    radius=25,
    auto_play=True,
    gradient={0.2: "#52c96e", 0.5: "#f0c040", 0.8: "#f08040", 1.0: "#ff4b4b"}
).add_to(animated_map)
st_folium(animated_map, use_container_width=True, height=480)

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# District Comparison Chart
# ─────────────────────────────────────────────
st.markdown('<div class="section-pill">📊 Analytics</div>', unsafe_allow_html=True)
st.subheader("District HMPI Comparison")

avg_pollution = df.groupby("Location")["HMPI"].mean().reset_index()

fig = px.bar(
    avg_pollution,
    x="Location",
    y="HMPI",
    title="Average Pollution Level by District",
    color="HMPI",
    color_continuous_scale=["#52c96e", "#f0c040", "#f08040", "#ff4b4b"],
    template="plotly_dark"
)
fig.update_layout(
    paper_bgcolor="#0d2b14",
    plot_bgcolor="#0d2b14",
    font_color="#d4f5d4",
    title_font_color="#52c96e",
    coloraxis_showscale=False
)
fig.update_traces(marker_line_color="#1a4d2e", marker_line_width=1)
st.plotly_chart(fig, width="stretch")

# ─────────────────────────────────────────────
# Pollution Trend
# ─────────────────────────────────────────────
st.subheader("Pollution Trend")

trend = df[df["Location"] == district]

fig2 = px.line(
    trend,
    x="Date",
    y="HMPI",
    markers=True,
    title=f"HMPI Trend for {district}",
    template="plotly_dark"
)
fig2.update_layout(
    paper_bgcolor="#0d2b14",
    plot_bgcolor="#0d2b14",
    font_color="#d4f5d4",
    title_font_color="#52c96e"
)
fig2.update_traces(line_color="#52c96e", marker_color="#4ecca3", marker_size=9)
st.plotly_chart(fig2, width="stretch")

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# AI Prediction for 2030
# ─────────────────────────────────────────────
st.markdown('<div class="section-pill">🤖 AI Forecast</div>', unsafe_allow_html=True)
st.subheader("AI Prediction for 2030 Pollution")

predictions = []
for d in df["Location"].unique():
    data = df[df["Location"] == d]
    X = data[["Date"]]
    y_col = data["HMPI"]
    model = LinearRegression()
    model.fit(X, y_col)
    future = pd.DataFrame({"Date": [2030]})
    pred = model.predict(future)[0]
    predictions.append({"Location": d, "Predicted_HMPI_2030": round(pred, 2)})

pred_df = pd.DataFrame(predictions)
st.dataframe(pred_df, width="stretch")

fig3 = px.bar(
    pred_df,
    x="Location",
    y="Predicted_HMPI_2030",
    title="Predicted Pollution Level in 2030",
    color="Predicted_HMPI_2030",
    color_continuous_scale=["#52c96e", "#f0c040", "#f08040", "#ff4b4b"],
    template="plotly_dark"
)
fig3.update_layout(
    paper_bgcolor="#0d2b14",
    plot_bgcolor="#0d2b14",
    font_color="#d4f5d4",
    title_font_color="#52c96e",
    coloraxis_showscale=False
)
fig3.update_traces(marker_line_color="#1a4d2e", marker_line_width=1)
st.plotly_chart(fig3, width="stretch")

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Policy Recommendation
# ─────────────────────────────────────────────
st.markdown('<div class="section-pill">📋 Policy</div>', unsafe_allow_html=True)
st.subheader("Policy Recommendation")

if not filtered.empty:
    policy_text = filtered["Policy"].values[0]
    risk_val = filtered["Risk"].values[0]
    badge_color = risk_badge(risk_val)
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #1a4d2e, #1e5c35); border:1px solid {badge_color};
                border-left: 4px solid {badge_color}; border-radius:10px; padding:18px 22px; margin-top:8px;">
        <div style="font-size:1rem; color:#d4f5d4; font-weight:500;">{policy_text}</div>
        <div style="margin-top:10px;">
            <span style="background:{badge_color}22; border:1px solid {badge_color}; border-radius:20px;
                         padding:3px 14px; color:{badge_color}; font-size:0.78rem; font-weight:700;">
                Risk Level: {risk_val}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PDF Report Generator
# ─────────────────────────────────────────────
st.markdown('<div class="section-pill">📄 Reports</div>', unsafe_allow_html=True)
st.subheader("Government Report")

def generate_report(data):
    file = "pollution_report.pdf"
    c = canvas.Canvas(file, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(120, 750, "Tamil Nadu Heavy Metal Pollution Report")
    c.setFont("Helvetica", 10)
    c.drawString(120, 730, "Generated by HMPI Pollution Monitoring System")
    c.line(50, 720, 550, 720)
    c.setFont("Helvetica", 12)
    y = 700
    for i, row in data.iterrows():
        text = f"{row['Location']}  |  HMPI: {round(row['HMPI'], 2)}  |  Risk: {row['Risk']}"
        c.drawString(50, y, text)
        y -= 20
        if y < 100:
            c.showPage()
            y = 700
    c.save()
    return file

if st.button("📄 Generate Government Report"):
    file = generate_report(df)
    with open(file, "rb") as f:
        st.download_button(
            "⬇️ Download PDF Report",
            f,
            "pollution_report.pdf",
            mime="application/pdf"
        )

st.markdown("<hr>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Download Dataset
# ─────────────────────────────────────────────
st.markdown('<div class="section-pill">💾 Export</div>', unsafe_allow_html=True)
st.subheader("Download Processed Data")

st.download_button(
    "⬇️ Download CSV",
    df.to_csv(index=False),
    "processed_pollution_data.csv",
    mime="text/csv"
)

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("""
<div style="margin-top:40px; padding:20px; text-align:center; border-top:1px solid #2d6a4f; color:#5a8f6a; font-size:0.8rem;">
    🌿 HMPI Pollution Monitoring System &nbsp;·&nbsp; AI-powered environmental surveillance &nbsp;·&nbsp; Tamil Nadu
</div>
""", unsafe_allow_html=True)
