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
# Background Function
# -------------------------------
def set_bg(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .block-container {{
            background-color: rgba(125, 190, 195, 0.95);
            padding: 2rem;
            border-radius: 12px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

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
# Background Images
# -------------------------------
bg_images = {
    "🏠 Home": "https://share.google/al1XbbYhBm6ToXPc0",
    "👤 Check Eligibility": "https://kommodo.ai/i/dvKkstX4XFQKJhlOQWse",
    "📝 Register to Vote": "https://share.google/kBr9ydOHaP9OaFPd1",
    "🗳️ Voting Guide": "https://kommodo.ai/i/vwqfbPgHEkZ4W0CKLSRS",
    "📍 Find Polling Info": "https://share.google/I7PUPgrIR6uUFYwr2",
    "💬 AI Assistant": "https://share.google/fJf6Uxw1dW6vIY1su"
}

set_bg(bg_images.get(menu, ""))

# -------------------------------
# HOME
# -------------------------------
if menu == "🏠 Home":
    st.header("Welcome 👋")
    st.markdown("""
- 🧾 Check eligibility  
- 📝 Voter registration  
- 🗳️ Voting guide  
- 📍 Polling booth finder  
- 💬 AI assistant  
""")

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
        else:
            st.error("Not eligible")

# -------------------------------
# REGISTER
# -------------------------------
elif menu == "📝 Register to Vote":
    st.header("Voter Registration")

    st.markdown("""
1. Visit NVSP portal  
2. Fill Form 6  
3. Upload documents  
4. Submit  
5. Get EPIC
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
        "Find booth",
        "Vote using EVM"
    ]

    for i, s in enumerate(steps, 1):
        st.write(f"{i}. {s}")

# -------------------------------
# POLLING INFO (FIXED)
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

    st.success(f"Nearest: {booths[0]['name']}")

    m = folium.Map(location=user_location, zoom_start=14)

    folium.Marker(user_location, popup="You").add_to(m)

    for b in booths:
        folium.Marker(b["location"], popup=b["name"]).add_to(m)

    st_folium(m, width=700)

# -------------------------------
# AI CHAT (SAFE VERSION)
# -------------------------------
elif menu == "💬 AI Assistant":
    st.header("Election AI")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    q = st.chat_input("Ask something...")

    def reply(x):
        return model.generate_content(x).text

    if q:
        ans = reply(q)
        st.session_state.chat.append(("You", q))
        st.session_state.chat.append(("AI", ans))

    for s, m in st.session_state.chat:
        st.markdown(f"**{s}:** {m}")
