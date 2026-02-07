import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
import math
import time
import threading
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Food Delivery AI Assistant",
    page_icon="🍔",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

body {
    background: linear-gradient(120deg, #0f172a, #1e293b);
    color: white;
}

h1, h2, h3 {
    font-family: "Poppins", sans-serif;
}

.block-container {
    padding-top: 2rem;
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
    margin-bottom: 20px;
}

.stButton button {
    width: 100%;
    background: linear-gradient(90deg, #ff512f, #dd2476);
    color: white;
    border-radius: 12px;
    padding: 12px;
    font-size: 16px;
    border: none;
}

.stButton button:hover {
    transform: scale(1.03);
    transition: 0.2s ease-in-out;
}

.sidebar .sidebar-content {
    background: #111827;
}

input {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("🍔 Food Delivery AI Assistant")
st.caption(" AI-powered Delivery Prediction + Maps + Smart Chatbots")

# ---------------- SIDEBAR MENU ----------------
menu = st.sidebar.radio(
    "📌 Navigation",
    ["ETA Prediction", "Live Route Map", "RAG Chatbot", "Rider AI Assistant"]
)

# ---------------- DISTANCE FUNCTION ----------------
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon/2)**2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c








# ======================================================
# ✅ ETA PREDICTION PAGE
# ======================================================
if menu == "ETA Prediction":
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.header("⏱ ETA Prediction Dashboard")
    st.write("Enter delivery details to predict estimated delivery time.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📍 Restaurant Location")
        restaurant_lat = st.number_input("Latitude", value=40.7128, format="%.4f")
        restaurant_lng = st.number_input("Longitude", value=-74.0060, format="%.4f")

    with col2:
        st.subheader("🏠 Customer Location")
        customer_lat = st.number_input("Latitude ", value=40.7589, format="%.4f")
        customer_lng = st.number_input("Longitude ", value=-73.9851, format="%.4f")

    distance_km = haversine_distance(
        restaurant_lat, restaurant_lng,
        customer_lat, customer_lng
    )

    st.info(f"📏 Distance Calculated: **{distance_km:.2f} km**")

    st.divider()

    col3, col4, col5 = st.columns(3)

    with col3:
        weather = st.selectbox("🌦 Weather", ["sunny", "cloudy", "rainy", "snowy"])
        traffic_level = st.slider("🚦 Traffic Level", 0.0, 1.0, 0.5)

    with col4:
        hour_of_day = st.slider("🕒 Hour", 0, 23, 12)
        multiple_deliveries = st.slider("📦 Multiple Deliveries", 0, 10, 1)

    with col5:
        delivery_person_rating = st.slider("⭐ Rider Rating", 1.0, 5.0, 4.0)
        festival = st.checkbox("🎉 Festival Day")

    prep_time_minutes = st.number_input("🍳 Preparation Time (mins)", value=10.0)

    city_type = st.selectbox("🏙 City Type", ["urban", "rural"])
    delivery_person_age = st.slider("👤 Rider Age", 18, 60, 30)
    vehicle_condition = st.selectbox("🚲 Vehicle Condition", ["good", "average", "poor"])

    if st.button("🚀 Predict Delivery ETA"):
        response = requests.post("http://localhost:8000/predict/eta", json={
            "distance_km": distance_km,
            "weather": weather,
            "hour_of_day": hour_of_day,
            "day_of_week": 1,
            "traffic_level": traffic_level,
            "delivery_person_rating": delivery_person_rating,
            "multiple_deliveries": multiple_deliveries,
            "festival": festival,
            "prep_time_minutes": prep_time_minutes,
            "city_type": city_type,
            "delivery_person_age": delivery_person_age,
            "vehicle_condition": vehicle_condition
        })

        if response.status_code == 200:
            eta = response.json()["eta_minutes"]
            st.success(f"✅ Estimated Delivery Time: **{eta:.2f} minutes**")
        else:
            st.error("❌ Prediction Failed")

    st.markdown("</div>", unsafe_allow_html=True)


# ======================================================
# ✅ LIVE MAP ROUTES PAGE
# ======================================================
elif menu == "Live Route Map":
    st.header("🗺 Live Delivery Route Map")

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    m = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

    folium.Marker(
        [40.7128, -74.0060],
        popup="Restaurant",
        icon=folium.Icon(color="green")
    ).add_to(m)

    folium.Marker(
        [40.7589, -73.9851],
        popup="Customer",
        icon=folium.Icon(color="red")
    ).add_to(m)

    folium_static(m)

    st.markdown("</div>", unsafe_allow_html=True)


# ======================================================
# ✅ RAG CHATBOT PAGE
# ======================================================
elif menu == "RAG Chatbot":
    st.header("🤖 Food Delivery Knowledge Chatbot")

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    user_query = st.text_input("Ask something about food delivery:")

    if st.button("💬 Chat with AI"):
        response = requests.post(
            "http://localhost:8000/rag/chat",
            json={"query": user_query}
        )

        if response.status_code == 200:
            st.success(response.json()["answer"])
        else:
            st.error("Chat failed")

    st.markdown("</div>", unsafe_allow_html=True)


# ======================================================
# ✅ RIDER AI ASSISTANT PAGE
# ======================================================
elif menu == "Rider AI Assistant":
    st.header("🚴 Rider Smart Assistant")

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    rider_query = st.text_input("Ask rider-related query:")

    if st.button("🧠 Ask Rider AI"):
        response = requests.post(
            "http://localhost:8000/ai/rider",
            json={"query": rider_query}
        )

        if response.status_code == 200:
            st.success(response.json()["answer"])
        else:
            st.error("AI failed")

    st.markdown("</div>", unsafe_allow_html=True)