import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic
import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# -------------------------------
# Load API Key
# -------------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------------------
# Page Config (MUST BE FIRST STREAMLIT CALL)
# -------------------------------
st.set_page_config(
    page_title="Election Assistant",
    page_icon="🗳️",
    layout="wide"
)

# -------------------------------
# Professional Styling
# -------------------------------
st.markdown("""
<style>
.main > div {
    padding-top: 2rem;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background-color: #f5f7fa;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Title
# -------------------------------
st.title("🗳️ Smart Election Assistant")
st.caption("AI-powered guide for Indian voters 🇮🇳")

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Go to",
    [
        "🏠 Home",
        "👤 Check Eligibility",
        "📝 Register to Vote",
        "🗳️ Voting Guide",
        "📍 Find Polling Info",
        "💬 AI Assistant"
    ]
)
# -------------------------------
# HOME
# -------------------------------
if menu == "🏠 Home":

    st.image(
        "https://images.unsplash.com/photo-1598091383021-15ddea10925d?w=1400",
        use_container_width=True
    )

    st.title("🇮🇳 Welcome to Smart Election Assistant")

    st.markdown("""
    ### Your Complete Election Guide

    This assistant helps Indian citizens:

    ✅ Check voting eligibility  
    ✅ Register as a voter  
    ✅ Understand voting process  
    ✅ Find nearest polling booth  
    ✅ Ask election-related questions using AI
    """)

    st.info("🗳️ First-time voter? Start with **Eligibility Check** from the sidebar.")

# -------------------------------
# ELIGIBILITY
# -------------------------------
elif menu == "👤 Check Eligibility":
    st.header("Check Eligibility")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Enter Age", 0, 120, 18)

    with col2:
        citizen = st.selectbox("Citizenship", ["Indian", "Other"])

    if st.button("Check"):
        if age >= 18 and citizen == "Indian":
            st.success("You are eligible 🎉")
            st.balloons()
        else:
            st.error("Not eligible")

# -------------------------------
# REGISTER
# -------------------------------
elif menu == "📝 Register to Vote":
    st.header("Voter Registration")

    st.markdown("""
### Steps to Register

1. Visit the NVSP portal  
2. Fill Form 6  
3. Upload required documents  
4. Submit application  
5. Receive EPIC voter ID
""")

# -------------------------------
# VOTING GUIDE
# -------------------------------
elif menu == "🗳️ Voting Guide":
    st.header("Voting Steps")

    steps = [
        "Check eligibility",
        "Register",
        "Get Voter ID",
        "Find polling booth",
        "Vote using EVM"
    ]

    for i, s in enumerate(steps, 1):
        st.write(f"✅ Step {i}: {s}")

# -------------------------------
# POLLING INFO
# -------------------------------
elif menu == "📍 Find Polling Info":
    st.header("Nearest Booth Finder")

    lat = st.number_input("Latitude", value=23.6850)
    lon = st.number_input("Longitude", value=86.9869)

    user_location = (lat, lon)

    booths = [
        {"name": "Govt School Booth", "location": (23.6845, 86.9900)},
        {"name": "Panchayat Office", "location": (23.6900, 86.9800)},
        {"name": "High School Booth", "location": (23.6800, 86.9950)},
    ]

    for b in booths:
        b["distance"] = geodesic(user_location, b["location"]).km

    booths.sort(key=lambda x: x["distance"])

    st.success(f"Nearest Booth: {booths[0]['name']}")

    m = folium.Map(location=user_location, zoom_start=14)

    folium.Marker(user_location, popup="You").add_to(m)

    for b in booths:
        folium.Marker(b["location"], popup=b["name"]).add_to(m)

    st_folium(m, width=700)

# -------------------------------
# AI CHAT
# -------------------------------
elif menu == "💬 AI Assistant":
    st.header("Election AI Assistant")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    q = st.chat_input("Ask something...")

    def reply(x):
        return model.generate_content(x).text

    if q:
        ans = reply(q)
        st.session_state.chat.append(("You", q))
        st.session_state.chat.append(("AI", ans))

    for sender, msg in st.session_state.chat:
        st.markdown(f"**{sender}:** {msg}")
