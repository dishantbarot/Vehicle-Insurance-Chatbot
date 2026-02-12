import streamlit as st

# --- KNOWLEDGE BASE ---
INSURANCE_KNOWLEDGE = {
    "ncb": {
        "answer": "No Claim Bonus (NCB) is a discount on your renewal premium for not making a claim.",
        "details": "In India, it starts at 20% for the 1st year and goes up to 50% for the 5th year. It belongs to the owner, not the car!"
    },
    "idv": {
        "answer": "IDV (Insured Declared Value) is the maximum sum insured by the company.",
        "details": "It is basically the market value of your vehicle. If your car is stolen or totaled, this is the amount you get."
    }
}

def get_contextual_response(user_input, history):
    user_input = user_input.lower()
    
    # 1. Check if user is asking a follow-up like "Tell me more" or "How much?"
    if any(word in user_input for word in ["more", "detail", "how much", "elaborate"]):
        if history:
            last_topic = history[-2]["content"].lower() # Check the last bot response
            for key in INSURANCE_KNOWLEDGE:
                if key in last_topic:
                    return INSURANCE_KNOWLEDGE[key]["details"]
        return "Could you specify what you'd like more details on? (e.g., NCB or IDV)"

    # 2. Standard Keyword Search
    for key, data in INSURANCE_KNOWLEDGE.items():
        if key in user_input:
            return data["answer"]
            
    return "I'm not sure about that. Try asking about NCB, IDV, or Third-party insurance."

# --- STREAMLIT UI ---
st.title("🚗 VahanBima Smart Bot")

# Initialize Session State for Memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display entire conversation from session_state
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask me something..."):
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response using history for context
    response = get_contextual_response(prompt, st.session_state.chat_history)

    # Add assistant response to history
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
