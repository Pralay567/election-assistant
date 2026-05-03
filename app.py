import streamlit as st

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Election Assistant", page_icon="🗳️", layout="wide")

# -------------------------------
# Title
# -------------------------------
st.title("🗳️ Smart Election Assistant")
st.caption("Powered with guidance inspired by Election Commission of India 🇮🇳")

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
    st.header("Welcome to Your Election Guide")

    st.markdown("""
This assistant helps you:
- ✅ Check if you're eligible
- 📝 Register as a voter
- 🗳️ Understand voting steps
- 💬 Ask questions interactively
    """)

    st.info("💡 Tip: Use the sidebar to explore different sections.")

# -------------------------------
# ELIGIBILITY
# -------------------------------
elif menu == "👤 Check Eligibility":
    st.header("Check Your Voting Eligibility")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Your Age", 0, 120)

    with col2:
        citizen = st.selectbox("Citizenship", ["Indian", "Other"])

    if st.button("Check Eligibility"):
        if age >= 18 and citizen == "Indian":
            st.success("🎉 You are eligible to vote!")
            st.balloons()
        else:
            st.error("❌ You are not eligible.")

# -------------------------------
# REGISTRATION
# -------------------------------
elif menu == "📝 Register to Vote":
    st.header("Voter Registration Process")

    with st.expander("📌 Step-by-step Guide"):
        st.markdown("""
1. Visit NVSP Portal: https://www.nvsp.in  
2. Fill **Form 6**  
3. Upload documents  
4. Submit application  
5. Receive your Voter ID (EPIC)
        """)

    st.success("💡 Registration is handled by the Election Commission of India")

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
        "Go on election day",
        "Vote using EVM"
    ]

    for i, step in enumerate(steps, 1):
        st.write(f"**Step {i}:** {step}")

# -------------------------------
# POLLING INFO
# -------------------------------
elif menu == "📍 Find Polling Info":
    st.header("Polling Information")

    state = st.text_input("Enter your state")
    district = st.text_input("Enter your district")

    if st.button("Find Info"):
        if state and district:
            st.success(f"Polling info for {district}, {state} will be available on official portals.")
        else:
            st.warning("Please enter both fields.")

# -------------------------------
# CHATBOT
# -------------------------------
elif menu == "💬 AI Assistant":
    st.header("Ask Anything About Elections")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    user_input = st.text_input("Type your question")

    def smart_reply(q):
        q = q.lower()

        if "vote" in q:
            return "To vote: Register → Get Voter ID → Visit polling booth → Cast vote."

        elif "register" in q:
            return "Go to NVSP portal, fill Form 6, upload documents."

        elif "document" in q:
            return "You need Aadhaar, address proof, and a photo."

        elif "eligibility" in q:
            return "You must be 18+ and an Indian citizen."

        elif "evm" in q:
            return "EVM stands for Electronic Voting Machine used in Indian elections."

        else:
            return "I can help with voting, registration, eligibility, EVM, and documents."

    if st.button("Send"):
        if user_input:
            response = smart_reply(user_input)

            st.session_state.chat.append(("You", user_input))
            st.session_state.chat.append(("Assistant", response))

    # Display chat
    for sender, msg in st.session_state.chat:
        if sender == "You":
            st.markdown(f"**🧑 {sender}:** {msg}")
        else:
            st.markdown(f"**🤖 {sender}:** {msg}")