import os
import time
import json
import streamlit as st
from groq import Groq
from pypdf import PdfReader
from openai import OpenAI

import firebase_admin
from firebase_admin import credentials, auth, firestore

# =========================
# FIREBASE INIT
# =========================
if not firebase_admin._apps:
    cred = credentials.Certificate(json.loads(st.secrets["FIREBASE_KEY"]))
    firebase_admin.initialize_app(cred)

db = firestore.client()

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="UMAR AI", page_icon="🤖", layout="centered")

SYSTEM_PROMPT = """
You are UMAR AI — a fast, intelligent, respectful, and professional AI assistant.
You were created by CEO Muhammad Umar, a Data Tycoon, Python Developer, and Automation Expert from Rahim Yar Khan, Pakistan.
"""

# =========================
# HELPERS
# =========================
def typing_markdown(text: str, speed: float = 0.008):
    placeholder = st.empty()
    out = ""
    for ch in text:
        out += ch
        placeholder.markdown(out)
        time.sleep(speed)

def extract_pdf_text(file) -> str:
    reader = PdfReader(file)
    return "\n".join([p.extract_text() or "" for p in reader.pages[:30]])

def stt_audio_to_text(audio_bytes: bytes) -> str:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    import io
    audio = io.BytesIO(audio_bytes)
    audio.name = "voice.wav"
    return client.audio.transcriptions.create(
        model="whisper-1",
        file=audio
    ).text

# =========================
# FIREBASE LOGIN
# =========================
def require_login():
    st.title("🤖 UMAR AI")
    st.caption("Powered by CEO Muhammad Umar | Llama 3.1 Engine 🚀")

    with st.form("login"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login = st.form_submit_button("Login")
        signup = st.form_submit_button("Signup")

    if login:
        try:
            user = auth.get_user_by_email(email)
            st.session_state.user = user.email
            st.rerun()
        except:
            st.error("User not found")

    if signup:
        try:
            user = auth.create_user(email=email, password=password)
            db.collection("users").document(user.uid).set({
                "email": email,
                "premium": False
            })
            st.success("Account created. Login now.")
        except Exception as e:
            st.error(str(e))

# =========================
# AUTH CHECK
# =========================
if "user" not in st.session_state:
    require_login()
    st.stop()

username = st.session_state.user

# =========================
# HEADER
# =========================
st.title("🤖 UMAR AI")
st.caption(f"Logged in as **{username}**")

if st.button("🚪 Logout"):
    st.session_state.clear()
    st.rerun()

# =========================
# GROQ CLIENT
# =========================
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# =========================
# STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Main UMAR AI hoon! Aaj kya madad kar sakta hoon? 🤖"}
    ]

if "pdf_context" not in st.session_state:
    st.session_state.pdf_context = ""

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.subheader("Tools")
    pdf = st.file_uploader("📄 Upload PDF", type=["pdf"])
    if pdf and st.button("Load PDF"):
        st.session_state.pdf_context = extract_pdf_text(pdf)[:6000]
        st.success("PDF loaded")

# =========================
# CHAT
# =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Umar AI se kuch bhi poocho...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Soch raha hoon..."):
            context = st.session_state.pdf_context
            messages = [{"role": "system", "content": SYSTEM_PROMPT + context}] + st.session_state.messages

            res = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                temperature=0.7,
                max_tokens=1024
            )

            reply = res.choices[0].message.content
            typing_markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
