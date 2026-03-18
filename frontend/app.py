import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="OilWatch Dashboard", page_icon="🛢️", layout="wide")
st.title("🛢️ OilWatch - SAR Oil Spill Detection")

# Sidebar
st.sidebar.header("Detection Parameters")

# Default bbox for Niger Delta
default_lat1, default_lon1 = 4.1, 5.2
default_lat2, default_lon2 = 5.5, 7.3

lat1 = st.sidebar.number_input("Lat Min", value=default_lat1)
lon1 = st.sidebar.number_input("Lon Min", value=default_lon1)
lat2 = st.sidebar.number_input("Lat Max", value=default_lat2)
lon2 = st.sidebar.number_input("Lon Max", value=default_lon2)

start_date = st.sidebar.date_input("Start Date", value=datetime(2023, 1, 1))
end_date = st.sidebar.date_input("End Date", value=datetime.today())

run_detection = st.sidebar.button("Run Detection")

st.markdown("### Region Map")
# Initialize map
m = folium.Map(location=[(lat1 + lat2) / 2, (lon1 + lon2) / 2], zoom_start=7)

# Draw bbox
folium.Rectangle(
    bounds=[[lat1, lon1], [lat2, lon2]],
    color='#ff7800',
    fill=True,
    fill_color='#ffff00',
    fill_opacity=0.2
).add_to(m)

# Columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    # We will update this map if an overlay mask URL is returned
    map_placeholder = st.empty()
    with map_placeholder:
        st_folium(m, width=700, height=500)

with col2:
    st.markdown("### Detection Results")
    results_placeholder = st.empty()
    results_placeholder.info("Click 'Run Detection' to scan the selected area.")

if run_detection:
    with st.spinner("Fetching SAR imagery and running U-Net model..."):
        try:
            payload = {
                "bbox": [lat1, lon1, lat2, lon2],
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }
            response = requests.post(f"{BACKEND_URL}/detect", json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                
                with results_placeholder.container():
                    if result["spill_detected"]:
                        st.error("🚨 Oil Spill Detected!")
                        st.metric("Estimated Area", f"{result['area_km2']} km²")
                        st.metric("Confidence", f"{result['confidence'] * 100:.1f}%")
                        
                        # Add image overlay to map
                        if result["mask_path"]:
                            mask_url = f"{BACKEND_URL}{result['mask_path']}"
                            # We simulate placing it over the bounding box
                            folium.raster_layers.ImageOverlay(
                                image=mask_url,
                                bounds=[[lat1, lon1], [lat2, lon2]],
                                opacity=0.6,
                            ).add_to(m)
                            
                            with map_placeholder:
                                st_folium(m, width=700, height=500, key=f"map_{result['id']}")
                    else:
                        st.success("✅ No Oil Spill Detected")
                        st.metric("Confidence", f"{result['confidence'] * 100:.1f}%")
            else:
                st.error(f"Backend error: {response.text}")
        except requests.exceptions.RequestException as e:
            st.warning("⚠️ Backend is unreachable. Running in standalone mode.")
            st.error(f"Connection failed: {e}")

st.markdown("---")
st.markdown("### Detection History")

history_placeholder = st.empty()

try:
    history_resp = requests.get(f"{BACKEND_URL}/history", timeout=5)
    if history_resp.status_code == 200:
        history_data = history_resp.json()
        if history_data:
            df = pd.DataFrame(history_data)
            df = df.rename(columns={'created_at': 'timestamp'})
            df = df[['timestamp', 'spill_detected', 'area_km2', 'confidence']]
            df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
            history_placeholder.dataframe(df, use_container_width=True)
        else:
            history_placeholder.info("No past detections found.")
    else:
        history_placeholder.error("Failed to fetch history.")
except requests.exceptions.RequestException:
    history_placeholder.warning("Backend unreachable. Cannot fetch history.")
