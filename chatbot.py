import streamlit as st
import time

# --- DATA: FAQ Knowledge Base (Indian Market Context) ---
FAQ_DATA = {
    "mandatory": "Yes, as per the Motor Vehicles Act, 1988, Third-Party (TP) insurance is mandatory for all vehicles plying on Indian roads.",
    "third party": "Third-Party insurance covers legal liability for damage/injury caused by your vehicle to others. It does NOT cover damage to your own vehicle.",
    "comprehensive": "A Comprehensive policy covers both Third-Party liability and 'Own Damage' (OD), protecting your vehicle against accidents, theft, and natural disasters.",
    "idv": "IDV stands for Insured Declared Value. It is the current market value of your vehicle (Sale Price - Depreciation). This is the maximum amount you get if your car is stolen or totaled.",
    "ncb": "No Claim Bonus (NCB) is a reward for not making a claim in the previous year. It’s a discount on your renewal premium, ranging from 20% up to 50% after 5 claim-free years.",
    "zero dep": "Zero Depreciation (Nil Depreciation) is an add-on where the insurer pays the full cost of replaced parts without deducting for wear and tear. Highly recommended for cars under 5 years old.",
    "claim process": "To file a claim in India: 1. Inform the insurer immediately. 2. File an FIR (for theft/major accidents). 3. Take the vehicle to a 'Network Garage' for a cashless experience.",
    "renewal": "You can renew online via the insurer's app or website using your RC and previous policy details. If your policy has lapsed for >90 days, you will lose your NCB."
}

# --- CHAT LOGIC ---
def get_response(user_input):
    user_input = user_input.lower()
    for key, response in FAQ_DATA.items():
        if key in user_input:
            return response
    return "I'm sorry, I don't have information on that specifically. Would you like to know about IDV, NCB, or Zero-Depreciation?"

# --- STREAMLIT UI ---
st.set_page_config(page_title="VahanBima Bot", page_icon="🚗")

st.title("🚗 VahanBima FAQ Bot")
st.markdown("Your assistant for Indian Vehicle Insurance queries.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me about NCB, IDV, or Mandatory insurance..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response
    response = get_response(prompt)

    # Display assistant response with a "typing" effect
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
