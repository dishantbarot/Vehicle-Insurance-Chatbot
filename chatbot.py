import streamlit as st
import google.generativeai as genai
import os

# --- 1. SETUP & AUTHENTICATION ---
# Securely fetch the API key from st.secrets or environment variables
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Missing Google API Key. Please add it to your Streamlit Secrets or environment.")
    st.stop()

genai.configure(api_key=api_key)

# --- 2. THE VAHANBIMA BRAIN (System Instruction) ---
# This prompt forces the "real-life" continuous questioning behavior.
SYSTEM_INSTRUCTION = """
You are 'VahanBima AI', a specialized assistant for Indian vehicle insurance.
CONTEXT:
- Use terms like 'IDV', 'NCB (No Claim Bonus)', 'Zero-Dep', 'Third-Party Mandatory', 'RC', 'Challan', and 'PUC'.
- Reference the 'Motor Vehicles Act 1988' and 'IRDAI' guidelines.
- Be professional but empathetic, as insurance often involves accidents or claims.

BEHAVIOR:
1. Short & Clear: Keep answers concise (2-3 paragraphs max).
2. Continuous Flow: After answering a user's question, ALWAYS suggest a logical follow-up question or ask a clarifying question about their vehicle (e.g., 'Is your car more than 5 years old?').
3. No Hallucination: If unsure about a specific premium amount, explain that it depends on the make, model, and RTO.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

# --- 3. STREAMLIT UI ---
st.set_page_config(page_title="VahanBima AI", page_icon="🛡️")
st.title("🛡️ VahanBima AI Assistant")
st.markdown("Expert guidance on Indian Car & Bike Insurance.")

# Initialize chat history for the session
if "chat_session" not in st.session_state:
    # Start a fresh chat object from Gemini
    st.session_state.chat_session = model.start_chat(history=[])

# Display history
for message in st.session_state.chat_session.history:
    with st.chat_message("user" if message.role == "user" else "assistant"):
        st.markdown(message.parts[0].text)

# --- 4. THE CHAT LOOP ---
if prompt := st.chat_input("Ask about NCB, Zero-Dep, or Claim process..."):
    # Display user input
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""
        
        # Send message to Gemini chat session (persists history automatically)
        response = st.session_state.chat_session.send_message(prompt, stream=True)
        
        for chunk in response:
            full_response += chunk.text
            response_container.markdown(full_response + "▌")
        response_container.markdown(full_response)
