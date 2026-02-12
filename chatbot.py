import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="VahanBima AI", page_icon="🛡️", layout="centered")

# Securely fetch API Key
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Please add your GOOGLE_API_KEY to Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# --- THE SYSTEM PROMPT (The "Continuous Questioning" Engine) ---
SYSTEM_PROMPT = """
You are 'VahanBima AI', a friendly and expert Indian vehicle insurance assistant.
YOUR GOAL: Provide expert advice on motor insurance and keep the conversation going.

STRICT RULES:
1. RESPONSE STYLE: Use a clean, modern tone similar to Google Gemini. Use bold text for emphasis.
2. CONTEXT: Always assume the Indian market (mention NCB, IDV, IRDAI, Zero-Dep, Third-Party liability).
3. CONTINUOUS FLOW: After every answer, you MUST ask exactly one relevant follow-up question. 
   - Example: After explaining NCB, ask "By the way, do you have your previous policy's expiry date handy to check your eligibility?"
   - Example: After explaining IDV, ask "Is your car currently under a loan? That might affect your claim process."
4. NO DEAD ENDS: Never say 'Let me know if you have more questions.' Instead, suggest the next step.
"""

# Initialize Gemini 2.0 Flash
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash", # Updated for Feb 2026
    system_instruction=SYSTEM_PROMPT
)

# --- SESSION STATE (Memory) ---
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- UI DESIGN ---
st.title("🛡️ VahanBima AI")
st.caption("Ask about Indian Vehicle Insurance • Powered by Gemini 2.0")

# Custom Styling to mimic Gemini's clean look
st.markdown("""
    <style>
    .stChatMessage { background-color: #f0f2f6; border-radius: 15px; padding: 10px; margin-bottom: 10px; }
    .stChatInput { border-radius: 20px; }
    </style>
""", unsafe_allow_html=True)

# Display Chat History
for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Chat Input Logic
if prompt := st.chat_input("Ask about Zero-Dep, NCB, or Claims..."):
    # User message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Assistant response (Streaming)
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # We use stream=True for that "Gemini-like" typing feel
        response = st.session_state.chat.send_message(prompt, stream=True)
        
        for chunk in response:
            full_response += chunk.text
            response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
