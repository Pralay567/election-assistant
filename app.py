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
# Page Config
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
# Sidebar Navigation
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
# BACKGROUND IMAGES (6 PAGES)
# -------------------------------
bg_images = {
    "🏠 Home": "https://share.google/al1XbbYhBm6ToXPc0",
    "👤 Check Eligibility": "https://share.google/bLdgCpWS3bWXl5f5k",
    "📝 Register to Vote": "https://share.google/kBr9ydOHaP9OaFPd1",
    "🗳️ Voting Guide": "https://share.google/uQBBcnUDYflVxVcee",
    "📍 Find Polling Info": "https://share.google/I7PUPgrIR6uUFYwr2",
    "💬 AI Assistant": "https://share.google/fJf6Uxw1dW6vIY1su"
}

set_bg(bg_images[menu])

# -------------------------------
# HOME
# -------------------------------
if menu == "🏠 Home":

    st.header("Welcome 👋")

    st.markdown("""
This assistant helps you:

- 🧾 Check voting eligibility  
- 📝 Learn voter registration  
- 🗳️ Understand voting process  
- 📍 Find polling information  
- 💬 Ask AI questions instantly  
""")

    st.info("Use sidebar to navigate features")

    st.subheader("🧠 Quick Quiz")
    q1 = st.radio("Voting age in India?", ["16", "18", "21"])

    if st.button("Submit"):
        if q1 == "18":
            st.success("Correct 🎉")
        else:
            st.error("Incorrect ❌ Correct answer is 18")

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

    if st.button("Check Eligibility"):

        if age >= 18 and citizen == "Indian":
            st.success("You are eligible to vote 🎉")
            st.balloons()
        else:
            st.error("Not eligible ❌")

# -------------------------------
# REGISTRATION
# -------------------------------
elif menu == "📝 Register to Vote":

    st.header("Voter Registration")

    with st.expander("Steps to Register"):
        st.markdown("""
1. Visit NVSP portal  
2. Fill Form 6  
3. Upload documents  
4. Submit application  
5. Receive EPIC (Voter ID)
""")

    st.success("Managed by Election Commission of India 🇮🇳")

# -------------------------------
# VOTING GUIDE
# -------------------------------
elif menu == "🗳️ Voting Guide":

    st.header("How Voting Works")

    steps = [
        "Check eligibility",
        "Register as voter",
        "Get Voter ID",
        "Find polling booth",
        "Go vote",
        "Use EVM machine"
    ]

    for i, step in enumerate(steps, 1):
        st.write(f"{i}. {step}")

# -------------------------------
# POLLING INFO
# -------------------------------
elif menu == "📍 Find Polling Info":

    st.header("🗺️ Find Your Nearest Polling Booth")

    st.info("Enter your location to see nearby polling booths on map")

    # ---------------- USER INPUT ----------------
    col1, col2 = st.columns(2)

    with col1:
        lat = st.number_input("Enter Latitude", value=23.6850, format="%.4f")

    with col2:
        lon = st.number_input("Enter Longitude", value=86.9869, format="%.4f")

    # ✅ FIX: ADD THIS LINE
    user_location = (lat, lon)

    # ---------------- FAKE POLLING BOOTHS DATA ----------------
    booths = [
        {"name": "Govt School Booth A", "location": (23.6845, 86.9900)},
        {"name": "Panchayat Office Booth", "location": (23.6900, 86.9800)},
        {"name": "High School Booth B", "location": (23.6800, 86.9950)},
        {"name": "Community Hall Booth", "location": (23.6880, 86.9700)},
    ]

    # ---------------- FIND NEAREST ----------------
    for b in booths:
        b["distance"] = geodesic(user_location, b["location"]).km

    booths = sorted(booths, key=lambda x: x["distance"])

    nearest = booths[0]

    st.success(f"Nearest Booth: {nearest['name']} ({nearest['distance']:.2f} km)")

    # ---------------- MAP CREATION ----------------
    m = folium.Map(location=user_location, zoom_start=14)

    # User marker
    folium.Marker(
        location=user_location,
        popup="You are here",
        icon=folium.Icon(color="blue")
    ).add_to(m)

    # Booth markers
    for b in booths:
        folium.Marker(
            location=b["location"],
            popup=f"{b['name']} ({b['distance']:.2f} km)",
            icon=folium.Icon(color="red")
        ).add_to(m)

    # ---------------- SHOW MAP ----------------
    st_folium(m, width=800, height=500)

    # ---------------- LIST VIEW ----------------
    st.subheader("📍 Nearby Booths")

    for b in booths:
        st.write(f"🗳️ {b['name']} — {b['distance']:.2f} km")

# -------------------------------
# AI ASSISTANT
# -------------------------------
elif menu == "💬 AI Assistant":

    st.header("Ask Election AI 🤖")

    language = st.selectbox("Language", ["English", "Hindi", "Bengali"])

    if "chat" not in st.session_state:
        st.session_state.chat = []

    # ---------------- QUICK ACTIONS ----------------
    st.subheader("⚡ Quick Actions")

    col1, col2, col3 = st.columns(3)

    quick_question = None

    if col1.button("📄 Apply for Voter ID"):
        quick_question = "How do I apply for voter ID in India?"

    if col2.button("🧾 Documents Required"):
        quick_question = "What documents are required for voter registration?"

    if col3.button("🗳️ Voting Process"):
        quick_question = "Explain voting process in India"

    # ---------------- AI FUNCTION ----------------
    def smart_reply(question):

        try:
            history = ""

            for msg in st.session_state.chat[-6:]:
                history += f"{msg[0]}: {msg[1]}\n"

            prompt = f"""
You are a Smart Indian Election Assistant AI.

Answer in {language}.

Rules:
- Be clear and simple
- Use bullet points if needed
- Do NOT hallucinate
- If unsure say: "Please verify with Election Commission of India"

Conversation History:
{history}

User Question:
{question}
"""

            response = model.generate_content(prompt)
            return response.text

        except Exception as e:
            return f"Error: {str(e)}"

    # ---------------- INPUT ----------------
    user_input = st.chat_input("Ask about voting, registration, EVM...")

    if quick_question:
        user_input = quick_question

    if user_input:

        st.session_state.chat.append(("You", user_input))

        with st.spinner("Thinking..."):
            response = smart_reply(user_input)

        st.session_state.chat.append(("Assistant", response))

    # ---------------- CHAT DISPLAY ----------------
    for sender, msg in st.session_state.chat:

        with st.chat_message(
            "user" if sender == "You" else "assistant"
        ):
            st.markdown(msg)