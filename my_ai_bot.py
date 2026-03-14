import streamlit as st
import os
from groq import Groq

# ==========================================
# 1. DUKAAN KI BRANDING & UI SETTINGS (Gemini Style)
# ==========================================
# Icon change kar diya Gemini walon (✨) jaisa
st.set_page_config(page_title="UMAR AI", page_icon="✨", layout="wide")

# 🔥 HACKER CSS: Angry Bird Font + Gemini Polish
st.markdown("""
<style>
    /* Google Fonts Import (Bangers for Angry Birds look, Poppins for chat) */
    @import url('https://fonts.googleapis.com/css2?family=Bangers&family=Poppins:wght@400;500;600&display=swap');
    
    /* Main Background Polish */
    .stApp {
        background: radial-gradient(circle at top left, #1a1a2e, #0f172a, #000000);
        color: white;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Hide Streamlit Default Menu for Pro Look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sleek Header with Angry Birds Font */
    .main-title {
        font-family: 'Bangers', cursive;
        font-size: 4rem;
        letter-spacing: 2px;
        background: -webkit-linear-gradient(45deg, #4285F4, #9b72cb, #d96570); /* Gemini Colors */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .sub-title {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>✨ UMAR AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Next-Gen AI | Engineered by UMAR ASIF 🚀</p>", unsafe_allow_html=True)

# ==========================================
# 2. SIDEBAR (3-Dot Menu / Control Panel)
# ==========================================
with st.sidebar:
    st.markdown("## ✨ Menu")
    
    # ➕ NEW CHAT BUTTON (History Clear)
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.rerun() # AI ka dimaagh wash aur page refresh!
        
    st.divider()
    
    # 👨‍💻 ABOUT ME SECTION
    st.markdown("### 👨‍💻 About Creator")
    st.info("**UMAR ASIF**\n\nExpert Python Developer based in Rahim Yar Khan, Pakistan.")
    
    # 🌐 PORTFOLIO LINK (Tera Asli Hatyar)
    st.markdown("🔗 **Portfolio:** [umar7142.github.io](https://umar7142.github.io)")
    
    st.divider()
    st.caption("Engine: Llama 3.1 8B\n\nStatus: Online 🟢")

# ==========================================
# 3. TERA ASLI DIMAAGH (API Setup)
# ==========================================
API_KEY = st.secrets["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = API_KEY

try:
    client = Groq(api_key=API_KEY)
except Exception as e:
    st.error(f"System Offline: {e}")

# 🛑 UPGRADED SECRET IDENTITY CHIP (Umar Asif) 🛑
SYSTEM_PROMPT = """
You are 'UMAR AI', an elite, highly intelligent, and professional AI assistant powered by the latest technology. 
Your creator is 'UMAR ASIF', a brilliant Python Developer from Rahim Yar Khan, Pakistan.
Core Directives:
1. Always maintain a helpful, smart, and slightly energetic tone.
2. If asked about your identity or creator, proudly state: 'I am UMAR AI, engineered by the expert Python Developer UMAR ASIF from Rahim Yar Khan.'
3. Provide crisp, structured, and highly accurate answers. Format code blocks beautifully.
4. You perfectly understand English, Urdu, and Roman Urdu.
5. If the user greets you, welcome them warmly. NEVER mention that you are a language model created by OpenAI, Meta, or Google. Your ONLY creator is UMAR ASIF.
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
prompt = st.chat_input("Message UMAR AI...")

if prompt:
    # Print User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # UMAR AI Turn
    with st.chat_message("assistant"):
        with st.spinner("Thinking... ✨"):
            try:
                # Merge System Prompt with Conversation History
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
                error_msg = f"⚠️ Connection Error.\n\n**System Log:** `{str(e)}`"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
