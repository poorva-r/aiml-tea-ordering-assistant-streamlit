"""
Streamlit web chat for the AIML Tea Ordering Assistant.
"""
import os
import aiml
import streamlit as st

BRAIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tea.aiml")

st.set_page_config(page_title="Tea Ordering Assistant", page_icon="🍵")
st.title("Tea Ordering Assistant")
st.caption("Say 'hello' to start. Type 'cancel' to stop at any time.")

# one bot per browser session
if "kernel" not in st.session_state:
    kernel = aiml.Kernel()
    kernel.verbose(False)
    # load the chatbot's rules and response templates from the AIML file
    kernel.learn(BRAIN)
    st.session_state.kernel = kernel
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Type your message, e.g. hello")
if prompt:
    reply = st.session_state.kernel.respond(prompt, "user").strip()
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()