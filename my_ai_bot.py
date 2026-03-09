import streamlit as st
import os
from google import genai

# 1. VIP ChatGPT Style Setup
st.set_page_config(page_title="CEO AI Bot", page_icon="🤖", layout="centered")

# 2. Khufiya CSS (Streamlit ka watermark aur menu gayab karne ke liye)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. Sidebar (Bilkul ChatGPT ke left panel ki tarah)
with st.sidebar:
    st.title("💼 CEO's Workspace")
    st.markdown("Welcome to the Tycoon AI Engine.")
    
    # New Chat Button
    if st.button("➕ New Chat"):
        st.session_state.chat_history = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("Developed by **Muhammad Umar** 🚀")

# 4. Main Chat Interface
st.title("🤖 TycoonGPT")

# 5. Teri VIP API Key (Khufiya Locker Se)
os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
client = genai.Client()

# Chat History Memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Purani chat dikhana (Custom Avatars ke sath)
for msg in st.session_state.chat_history:
    avatar_icon = "🧑‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["text"])

# 6. Chat Input (Message likhne ki jagah)
tera_sawal = st.chat_input("Message TycoonGPT...")

if tera_sawal:
    # User ka message
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(tera_sawal)
    st.session_state.chat_history.append({"role": "user", "text": tera_sawal})

    # AI ka jawab (Loading animation)
    with st.spinner("Tycoon AI is typing..."):
        vip_command = f"Tum ek asaan zaban bolne wale dost ho. Jawab asaan Roman Urdu mein do. Sawal: {tera_sawal}"
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=vip_command
        )
        
    # AI ka message screen par dikhao
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response.text)
    st.session_state.chat_history.append({"role": "assistant", "text": response.text})
