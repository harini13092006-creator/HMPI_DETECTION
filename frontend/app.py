import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap, HeatMapWithTime
import plotly.express as px
from sklearn.linear_model import LinearRegression
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

st.set_page_config(page_title="HMPI Pollution Monitoring System", layout="wide")

st.title("Heavy Metal Pollution Monitoring Dashboard")
st.write("AI-powered monitoring of heavy metal contamination across Tamil Nadu")

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("heavy_metal_data.csv")
    return df
df = load_data()

# -----------------------------
# WHO Standards
# -----------------------------
WHO_LIMITS = {
    "Ni":0.02,
    "Zn":3.0,
    "Pb":0.01,
    "Cd":0.003,
    "Cr":0.05
}

# -----------------------------
# HMPI Calculation
# -----------------------------
def calculate_hmpi(row):
    hmpi = 0
    for metal in WHO_LIMITS:
        hmpi += (row[metal] / WHO_LIMITS[metal]) * 20
    return hmpi

df["HMPI"] = df.apply(calculate_hmpi, axis=1)

# -----------------------------
# Risk Classification
# -----------------------------
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

# -----------------------------
# Policy Suggestions
# -----------------------------
def policy_advice(risk):

    if risk == "Safe":
        return "Maintain regular monitoring"

    elif risk == "Moderate":
        return "Increase monitoring and regulate pollution"

    elif risk == "High":
        return "Install treatment plants and restrict discharge"

    else:
        return "Immediate government intervention required"

df["Policy"] = df["Risk"].apply(policy_advice)

# -----------------------------
# Dashboard Metrics
# -----------------------------
st.subheader("Pollution Overview")

col1,col2,col3 = st.columns(3)

col1.metric("Average HMPI", round(df["HMPI"].mean(),2))
col2.metric("Highest HMPI", round(df["HMPI"].max(),2))
col3.metric("Total Districts", df["Location"].nunique())

# -----------------------------
# Filters
# -----------------------------
st.sidebar.header("Filters")

district = st.sidebar.selectbox("Select District", df["Location"].unique())
year = st.sidebar.selectbox("Select Year", sorted(df["Date"].unique()))

filtered = df[(df["Location"]==district) & (df["Date"]==year)]

st.subheader("District Pollution Data")
st.dataframe(filtered)

# -----------------------------
# Interactive Map
# -----------------------------
st.subheader("Pollution Map")

m = folium.Map(location=[11.5,78], zoom_start=7)

for _,row in df.iterrows():

    if row["Risk"]=="Safe":
        color="green"
    elif row["Risk"]=="Moderate":
        color="yellow"
    elif row["Risk"]=="High":
        color="orange"
    else:
        color="red"

    folium.CircleMarker(
        location=[row["Lat"],row["Lon"]],
        radius=7,
        popup=f"{row['Location']} | HMPI {round(row['HMPI'],2)} | {row['Risk']}",
        color=color,
        fill=True
    ).add_to(m)

st_folium(m,width=900)

# -----------------------------
# Heatmap
# -----------------------------
st.subheader("Pollution Heatmap")

heat_data = df[["Lat","Lon","HMPI"]].values.tolist()

heatmap = folium.Map(location=[11.5,78], zoom_start=7)
HeatMap(heat_data).add_to(heatmap)

st_folium(heatmap,width=900)

# -----------------------------
# Animated Pollution Map
# -----------------------------
st.subheader("Animated Pollution Map (2021-2025)")

years = sorted(df["Date"].unique())

heat_frames = []

for y in years:

    data = df[df["Date"]==y]
    heat_frames.append(data[["Lat","Lon","HMPI"]].values.tolist())

animated_map = folium.Map(location=[11.5,78], zoom_start=7)

HeatMapWithTime(
    heat_frames,
    index=years,
    radius=25,
    auto_play=True
).add_to(animated_map)

st_folium(animated_map,width=900)

# -----------------------------
# District Comparison Chart
# -----------------------------
st.subheader("District HMPI Comparison")

avg_pollution = df.groupby("Location")["HMPI"].mean().reset_index()

fig = px.bar(
    avg_pollution,
    x="Location",
    y="HMPI",
    title="Average Pollution Level by District"
)

st.plotly_chart(fig)

# -----------------------------
# Pollution Trend
# -----------------------------
st.subheader("Pollution Trend")

trend = df[df["Location"]==district]

fig2 = px.line(
    trend,
    x="Date",
    y="HMPI",
    markers=True,
    title=f"HMPI Trend for {district}"
)

st.plotly_chart(fig2)

# -----------------------------
# AI Prediction for 2030
# -----------------------------
st.subheader("AI Prediction for 2030 Pollution")

predictions=[]

for d in df["Location"].unique():

    data = df[df["Location"]==d]

    X = data[["Date"]]
    y = data["HMPI"]

    model = LinearRegression()
    model.fit(X,y)

    future = pd.DataFrame({"Date":[2030]})
    pred = model.predict(future)[0]

    predictions.append({
        "Location":d,
        "Predicted_HMPI_2030":round(pred,2)
    })

pred_df = pd.DataFrame(predictions)

st.dataframe(pred_df)

fig3 = px.bar(
    pred_df,
    x="Location",
    y="Predicted_HMPI_2030",
    title="Predicted Pollution Level in 2030"
)

st.plotly_chart(fig3)

# -----------------------------
# Policy Recommendation
# -----------------------------
st.subheader("Policy Recommendation")
st.write(filtered["Policy"].values[0])

# -----------------------------
# PDF Report Generator
# -----------------------------
def generate_report(data):

    file="pollution_report.pdf"

    c=canvas.Canvas(file,pagesize=letter)

    c.setFont("Helvetica",14)
    c.drawString(200,750,"Tamil Nadu Heavy Metal Pollution Report")

    y=700

    for i,row in data.iterrows():

        text=f"{row['Location']}  HMPI:{round(row['HMPI'],2)}  Risk:{row['Risk']}"

        c.drawString(50,y,text)

        y-=20

        if y<100:
            c.showPage()
            y=700

    c.save()

    return file

if st.button("Generate Government Report"):

    file=generate_report(df)

    with open(file,"rb") as f:
        st.download_button(
            "Download Report",
            f,
            "pollution_report.pdf"
        )

# -----------------------------
# Download Dataset
# -----------------------------
st.subheader("Download Processed Data")

st.download_button(
    "Download CSV",
    df.to_csv(index=False),
    "processed_pollution_data.csv"
)