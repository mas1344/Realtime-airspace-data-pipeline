# dashboard_streamlit.py
import streamlit as st
from pathlib import Path
import pandas as pd
import folium
import plotly.express as px
from snowflake_utils import load_from_snowflake
import datetime
import io
import base64
import numpy as np

ROOT = Path(__file__).parent
PUBLIC = ROOT / "public"
PUBLIC.mkdir(exist_ok=True)

ICON_PATH = ROOT / "plane.png"

st.set_page_config(page_title="Live Airspace Dashboard", layout="wide")

@st.cache_data(ttl=30)
def load_data():
    df = load_from_snowflake()
    # Ensure expected columns exist and normalize types
    if "ALTITUDE_BARO" in df.columns:
        df["ALTITUDE_BARO"] = pd.to_numeric(df["ALTITUDE_BARO"], errors="coerce")
    if "VELOCITY" in df.columns:
        df["VELOCITY"] = pd.to_numeric(df["VELOCITY"], errors="coerce")
    if "ON_GROUND" in df.columns:
        df["ON_GROUND"] = df["ON_GROUND"].astype(bool)
    return df

def make_folium_map(df, start_location=[59.3, 18.0], zoom_start=5):
    m = folium.Map(location=start_location, zoom_start=zoom_start)
    if ICON_PATH.exists():
        icon = folium.CustomIcon(str(ICON_PATH), icon_size=(24, 24))
    else:
        icon = None
    for _, row in df.iterrows():
        lat = row.get("LATITUDE")
        lon = row.get("LONGITUDE")
        if pd.isna(lat) or pd.isna(lon):
            continue
        tooltip = (
            f"ICAO24: {row.get('ICAO24')}<br>"
            f"Country: {row.get('ORIGIN_COUNTRY')}<br>"
            f"Altitude: {row.get('ALTITUDE_BARO')} m<br>"
            f"Velocity: {row.get('VELOCITY')} m/s<br>"
            f"Heading: {row.get('HEADING')}°<br>"
            f"Time: {row.get('TIMESTAMP_UTC')}"
        )
        marker_kwargs = {"location": [lat, lon], "tooltip": tooltip}
        if icon:
            marker_kwargs["icon"] = icon
        folium.Marker(**marker_kwargs).add_to(m)
    return m

def folium_static(m, height=600):
    """Render folium map in Streamlit without saving to disk."""
    html = m._repr_html_()
    st.components.v1.html(html, height=height)

def compute_stats(df):
    stats = {}
    stats["total_flights"] = int(len(df))
    stats["on_ground"] = int(df["ON_GROUND"].sum()) if "ON_GROUND" in df.columns else 0
    stats["avg_altitude"] = float(df["ALTITUDE_BARO"].dropna().mean()) if "ALTITUDE_BARO" in df.columns else 0.0
    stats["avg_velocity"] = float(df["VELOCITY"].dropna().mean()) if "VELOCITY" in df.columns else 0.0
    stats["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return stats

# --- Sidebar: filter controls ---
st.sidebar.header("Filter")
st.sidebar.markdown("Justera filtren och klicka Uppdatera")

df = load_data()

countries = sorted(df["ORIGIN_COUNTRY"].dropna().unique().tolist()) if "ORIGIN_COUNTRY" in df.columns else []
countries.insert(0, "Alla")

selected_country = st.sidebar.selectbox("Land", countries, index=0)
on_ground_only = st.sidebar.checkbox("Visa endast flyg på marken", value=False)
min_altitude = st.sidebar.number_input("Minhöjd (m)", min_value=0, value=0, step=100)

if st.sidebar.button("Uppdatera"):
    # clear cache so load_data() will re-run next call
    load_data.clear()

# Apply filters
df_filtered = df.copy()
if selected_country and selected_country != "Alla":
    df_filtered = df_filtered[df_filtered["ORIGIN_COUNTRY"] == selected_country]
if on_ground_only:
    if "ON_GROUND" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["ON_GROUND"] == True]
if min_altitude:
    if "ALTITUDE_BARO" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["ALTITUDE_BARO"].fillna(0) >= float(min_altitude)]

# --- Top row: stats and map ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Översikt")
    stats = compute_stats(df_filtered)
    st.metric("Totalt flyg", stats["total_flights"])
    st.metric("På marken", stats["on_ground"])
    st.metric("Medelhöjd (m)", f"{stats['avg_altitude']:.1f}")
    st.metric("Medelhastighet (m/s)", f"{stats['avg_velocity']:.1f}")
    st.write("Senast uppdaterad:", stats["last_updated"])
    if st.button("Exportera filtrerad CSV"):
        csv = df_filtered.to_csv(index=False).encode("utf-8")
        b64 = base64.b64encode(csv).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="filtered_flights.csv">Ladda ner CSV</a>'
        st.markdown(href, unsafe_allow_html=True)

with col2:
    st.subheader("Karta")
    if len(df_filtered) == 0:
        st.info("Inga datapunkter för valda filter.")
    else:
        m = make_folium_map(df_filtered)
        folium_static(m, height=600)

# --- Lower row: charts ---
st.markdown("---")
st.subheader("Diagram")

# Flights per country (top 10)
if "ORIGIN_COUNTRY" in df_filtered.columns and len(df_filtered) > 0:
    counts = df_filtered["ORIGIN_COUNTRY"].fillna("Unknown").value_counts().nlargest(10)
    df_counts = counts.reset_index()
    df_counts.columns = ["country", "count"]

    fig1 = px.bar(
        df_counts,
        x="country",
        y="count",
        labels={"country": "Land", "count": "Antal"},
        title="Antal flyg per land (topp 10)"
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("Ingen landdata att visa.")


# Altitude distribution
if "ALTITUDE_BARO" in df_filtered.columns and len(df_filtered) > 0:
    fig2 = px.histogram(df_filtered, x="ALTITUDE_BARO", nbins=30, title="Höjdfördelning", labels={"ALTITUDE_BARO":"Altitude (m)"})
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Ingen höjddata att visa.")

# Top velocities
if "VELOCITY" in df_filtered.columns and len(df_filtered) > 0:
    topv = df_filtered[["ICAO24","VELOCITY"]].dropna().sort_values("VELOCITY", ascending=False).head(10)
    fig3 = px.bar(topv, x="VELOCITY", y="ICAO24", orientation="h", title="Topp 10 hastigheter (m/s)", labels={"VELOCITY":"Velocity", "ICAO24":"ICAO24"})
    fig3.update_yaxes(autorange="reversed")
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Ingen hastighetsdata att visa.")

st.markdown("---")
st.caption("Dashboard genererad med data från Snowflake. Klicka Uppdatera i sidopanelen för att hämta ny data.")
