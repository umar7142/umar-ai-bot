import streamlit as st
import os
from google import genai

# 1. Website Ka Design Aur Title
st.set_page_config(page_title="CEO AI Bot", page_icon="🤖")
st.title("🚀 CEO Muhammad Umar's AI")
st.subheader("Welcome to the Data Tycoon's Personal Chatbot! 💼")

# 2. Teri VIP API Key Setup
os.environ["GEMINI_API_KEY"] = "AIzaSyAp42_GwZrP59YyGPokcGQJucKt1shLkLQ"
client = genai.Client()

# 3. Chat History Save Karne Ka Jugar (Taake AI purani baat yaad rakhay)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Purani chat screen par dikhana
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# 4. Chat Input (Neechay message likhne wali jagah)
tera_sawal = st.chat_input("Apna sawal yahan type kar Boss...")

if tera_sawal:
    # User ka sawal screen par dikhao aur save karo
    with st.chat_message("user"):
        st.markdown(tera_sawal)
    st.session_state.chat_history.append({"role": "user", "text": tera_sawal})

    # 5. AI Ka Jawab Lana (Loading Animation ke sath)
    with st.spinner("⏳ VIP AI Soch Raha Hai..."):
        vip_command = f"Tum ek asaan zaban bolne wale dost ho. Jawab asaan Roman Urdu mein do. Sawal: {tera_sawal}"
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=vip_command
        )
        
    # AI ka jawab screen par dikhao aur save karo
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.chat_history.append({"role": "assistant", "text": response.text})