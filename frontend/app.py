import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

from hmpi_engine import calculate_hmpi, classify_hmpi

st.set_page_config(page_title="HMPI System", layout="wide")

st.title("Heavy Metal Pollution Index (HMPI) System")

st.markdown("Upload a CSV file containing heavy metal concentrations.")

# File Upload
uploaded_file = st.file_uploader(
    "Upload Water Quality CSV",
    type=["csv"]
)

if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file)

        required_columns = [
            "Location", "Date", "Lat", "Lon",
            "Pb", "Cd", "Hg", "Cr", "As", "Ni", "Cu", "Zn"
        ]

        # Validate columns
        missing_cols = [col for col in required_columns if col not in df.columns]

        if missing_cols:
            st.error(f"Missing columns in CSV: {missing_cols}")
            st.stop()

        # Calculate HMPI
        df["HMPI"] = df.apply(calculate_hmpi, axis=1)
        df["Classification"] = df["HMPI"].apply(classify_hmpi)

        st.subheader("Processed Data")
        st.dataframe(df)

        # =============================
        # BAR CHART
        # =============================
        st.subheader("HMPI by Location")

        bar_fig = px.bar(
            df,
            x="Location",
            y="HMPI",
            color="Classification",
            title="HMPI Comparison"
        )

        st.plotly_chart(bar_fig, use_container_width=True)

        # =============================
        # PIE CHART
        # =============================
        st.subheader("Pollution Classification Distribution")

        pie_fig = px.pie(
            df,
            names="Classification",
            title="Pollution Distribution"
        )

        st.plotly_chart(pie_fig, use_container_width=True)

        # =============================
        # MAP VISUALIZATION
        # =============================
        st.subheader("Pollution Map")

        center_lat = df["Lat"].mean()
        center_lon = df["Lon"].mean()

        m = folium.Map(location=[center_lat, center_lon], zoom_start=6)

        for _, row in df.iterrows():
            folium.CircleMarker(
                location=[row["Lat"], row["Lon"]],
                radius=8,
                popup=f"{row['Location']} - HMPI: {row['HMPI']}",
                color="red" if row["HMPI"] > 100 else "green",
                fill=True,
                fill_opacity=0.7
            ).add_to(m)

        st_folium(m, width=900, height=500)

        # =============================
        # DOWNLOAD BUTTON
        # =============================
        st.subheader("Download Results")

        csv_data = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Processed CSV",
            data=csv_data,
            file_name="HMPI_results.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    st.info("Please upload a CSV file to begin.")