import streamlit as st
import os
from groq import Groq

# 1. Dukaan Ki Branding (ChatGPT Style)
st.set_page_config(page_title="UMAR AI", page_icon="🤖", layout="centered")

st.title("🤖 UMAR AI")
st.caption("Powered by CEO Muhammad Umar | Llama 3.1 Engine 🚀")

# 2. Tera Asli Dimaagh (API Key setup)
API_KEY = st.secrets["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = API_KEY # Safe environment variable

try:
    client = Groq(api_key=API_KEY)
except Exception as e:
    st.error(f"Client Initialize Error: {e}")

# 🛑 THE SECRET IDENTITY CHIP (Tera System Prompt) 🛑
SYSTEM_PROMPT = """
You are 'UMAR AI', a highly advanced, super-fast, and respectful AI assistant. 
You were created by the one and only 'CEO Muhammad Umar', a top Data Tycoon, Python Developer, and Automation Expert from Rahim Yar Khan, Pakistan.
If anyone asks who you are, what your name is, or who created you, proudly and enthusiastically say: 'Main UMAR AI hoon! Aur mujhe Pakistan ke sab se behtareen Data Tycoon aur IT Expert, CEO Muhammad Umar ne banaya hai!'
Always be helpful, smart, and energetic. You understand English, Urdu, and Roman Urdu perfectly.
"""

# 3. Chat History Memory (Taake AI purani baatein yaad rakhe)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Purane Messages Screen Par Dikhana
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. User Ka Input Dabba (Neeche chat bar)
prompt = st.chat_input("Umar AI se kuch bhi poocho Boss...")

if prompt:
    # Pehle user ka message screen par dikhao
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 6. UMAR AI Ki Bari (Thinking & Answering)
    with st.chat_message("assistant"):
        # ⏳ Tera Custom Pop-up / Spinner
        with st.spinner("Umar bhai ka ai soch rha ha... 🤔"):
            try:
                # 🧠 SYSTEM CHIP KO API KE SATH JORNA (Asli Hacker Move)
                api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
                
                # Groq Server ko message bhejna (Llama 3.1 Model)
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant", 
                    messages=api_messages,
                    temperature=0.7, 
                    max_tokens=1024,
                )
                
                # Jawab aagaya!
                response = completion.choices[0].message.content
                st.markdown(response)
                
                # Jawab ko memory mein save kar lo
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                # 🛑 Tera Custom Error Message + X-Ray (Asli Bimari)
                error_msg = f"koi or app use kro abhi beta... 🚫\n\n**Hacker X-Ray (Asli Masla):** `{str(e)}`"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
