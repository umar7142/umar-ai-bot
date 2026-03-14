import streamlit as st
import os
from groq import Groq

# ==========================================
# 1. DUKAAN KI BRANDING & SAAS UI SETTINGS
# ==========================================
st.set_page_config(page_title="UMAR AI Pro", page_icon="🤖", layout="wide")

# 🔥 HACKER CSS: Dark Gradient Theme & Clean UI
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(to bottom right, #0f172a, #000000);
        color: white;
        font-family: 'Poppins', sans-serif;
    }
    /* Hide Streamlit Default Menu for Pro Look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sleek Header */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🤖 UMAR AI PRO</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Advanced AI Assistant | Engineered by CEO Muhammad Umar 🚀</p>", unsafe_allow_html=True)

# ==========================================
# 2. SIDEBAR (Control Panel)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8644/8644400.png", width=100)
    st.markdown("### 👑 CEO Dashboard")
    st.markdown("Welcome to the Control Center, Boss.")
    
    # Chat Clear Button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun() # Refresh the app
        
    st.divider()
    st.markdown("⚡ **Engine:** Llama 3.1 8B\n\n🛡️ **Security:** Military Grade\n\n🌐 **Status:** Online")

# ==========================================
# 3. TERA ASLI DIMAAGH (API Setup)
# ==========================================
API_KEY = st.secrets["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = API_KEY

try:
    client = Groq(api_key=API_KEY)
except Exception as e:
    st.error(f"System Offline: {e}")

# 🛑 UPGRADED SECRET IDENTITY CHIP (Super Professional) 🛑
SYSTEM_PROMPT = """
You are 'UMAR AI', an elite, highly intelligent, and professional AI assistant. 
Your creator is 'CEO Muhammad Umar', a top-tier Data Tycoon, Python Developer, and Automation Expert from Rahim Yar Khan, Pakistan.
Core Directives:
1. Always maintain a highly professional, respectful, and helpful tone (like a high-end corporate assistant).
2. If asked about your identity or creator, proudly state: 'I am UMAR AI, engineered by the brilliant Data Tycoon and IT Expert, CEO Muhammad Umar.'
3. Provide crisp, structured, and highly accurate answers. Format code blocks beautifully.
4. You perfectly understand English, Urdu, and Roman Urdu.
5. If the user greets you, welcome them warmly to the UMAR AI ecosystem.
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
prompt = st.chat_input("Enter command or ask a question, Boss...")

if prompt:
    # Print User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # UMAR AI Turn
    with st.chat_message("assistant"):
        with st.spinner("Processing request at quantum speed... ⚡"):
            try:
                # Merge System Prompt with Conversation History
                api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
                
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant", 
                    messages=api_messages,
                    temperature=0.7, 
                    max_tokens=1500, # Increased for better detailed answers
                )
                
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                error_msg = f"⚠️ System Overload. Please try again.\n\n**Dev Error Log:** `{str(e)}`"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
