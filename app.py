import streamlit as st
from chatbot_engine import GeminiEngine, GroqEngine

st.set_page_config(page_title="Multi-Model Pro")

# 1. Sidebar for Model Selection
with st.sidebar:
    st.title("Settings")
    model_choice = st.selectbox("Choose AI Provider", ["Gemini", "Groq"])

    # Initialize or Switch the Engine
    if (
        "current_provider" not in st.session_state
        or st.session_state.current_provider != model_choice
    ):
        st.session_state.current_provider = model_choice
        if model_choice == "Gemini":
            st.session_state.bot = GeminiEngine()
        else:
            st.session_state.bot = GroqEngine()
        # Reset history on switch
        st.session_state.chat_history = []

# 2. Display Common History
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Handle Input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Use the unified function!
    response = st.session_state.bot.get_response(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.chat_history.append({"role": "assistant", "content": response})
