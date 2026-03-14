import streamlit as st
import os
from groq import Groq

# ==========================================
# 1. VIP BRANDING & .PK 🇵🇰
# ==========================================
st.set_page_config(page_title="UMAR AI .pk", page_icon="🇵🇰", layout="centered")

# 🔥 HACKER CSS: 100% PITCH BLACK THEME (No White Spots!)
st.markdown("""
<style>
    /* 1. Main Background */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    
    /* 2. Sidebar Full Black */
    [data-testid="stSidebar"] {
        background-color: #09090b !important;
    }
    
    /* Sidebar Text Color */
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* 3. Top Header (Hide white line) */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* 4. Chat Input Box (Neeche wala dabba) */
    .stChatInputContainer, [data-testid="stChatInput"] {
        background-color: #09090b !important;
        border: 1px solid #27272a !important;
        color: white !important;
    }
    
    /* Title Styling */
    .grok-title {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 3.8rem;
        font-weight: 800;
        text-align: center;
        color: #ffffff;
        margin-bottom: 0px;
        letter-spacing: -2px;
    }
    
    /* .pk styling (Green color for Pakistan) */
    .pk-text {
        color: #10b981; 
        font-size: 2.5rem;
    }

    .grok-subtitle {
        text-align: center;
        color: #a1a1aa;
        font-size: 1.1rem;
        margin-bottom: 40px;
        font-weight: 500;
    }
    
    /* Hide Default Menus */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# THE NEW TITLE WITH .pk
st.markdown("<h1 class='grok-title'>UMAR AI <span class='pk-text'>.pk</span></h1>", unsafe_allow_html=True)
st.markdown("<p class='grok-subtitle'>Engineered by UMAR ASIF | Python Developer, RYK</p>", unsafe_allow_html=True)

# ==========================================
# 2. VIP SIDEBAR (Control Panel)
# ==========================================
with st.sidebar:
    st.markdown("## ⚙️ Control Center")
    
    # ➕ NEW CHAT BUTTON
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.divider()
    
    # 👨‍💻 ABOUT ME SECTION
    st.markdown("### 👨‍💻 Creator")
    st.info("**UMAR ASIF**\n\nExpert Python Developer\nRahim Yar Khan, Pakistan 🇵🇰")
    
    # 🌐 PORTFOLIO LINK
    st.markdown("🔗 **Portfolio:** [umar7142.github.io](https://umar7142.github.io)")
    
    st.divider()
    st.caption("Engine: Groq Llama 3.1\nStatus: Online 🟢")

# ==========================================
# 3. TERA ASLI DIMAAGH (API Setup)
# ==========================================
API_KEY = st.secrets["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = API_KEY

try:
    client = Groq(api_key=API_KEY)
except Exception as e:
    st.error(f"System Offline: {e}")

# 🛑 UPGRADED SECRET IDENTITY CHIP (Umar Asif - Grok Vibe) 🛑
SYSTEM_PROMPT = """
You are 'UMAR AI', an elite, highly intelligent, and professional AI assistant. 
Your creator is 'UMAR ASIF', a brilliant Python Developer from Rahim Yar Khan, Pakistan.
Always maintain a highly professional, concise, and helpful tone.
If asked about your creator, proudly state: 'I am UMAR AI, engineered by UMAR ASIF from Rahim Yar Khan.'
NEVER mention OpenAI, Meta, or Google as your creator.
"""

# ==========================================
# 4. CHAT HISTORY MEMORY
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================================
# 5. USER INPUT & AI THINKING
# ==========================================
prompt = st.chat_input("Ask UMAR AI anything...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing... ⚡"):
            try:
                api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
                
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant", 
                    messages=api_messages,
                    temperature=0.7, 
                    max_tokens=1500,
                )
                
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")
