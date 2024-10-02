import streamlit as st
from typing import List, Dict

def initialize_chat_sessions():
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {window: [] for window in st.session_state.chat_windows}

def display_chat_messages(chat_name: str):
    for message in st.session_state.chat_sessions[chat_name]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def add_user_message(chat_name: str, prompt: str):
    st.session_state.chat_sessions[chat_name].append({"role": "user", "content": prompt})

def add_assistant_message(chat_name: str, content: str):
    st.session_state.chat_sessions[chat_name].append({"role": "assistant", "content": content})

def get_chat_messages(chat_name: str) -> List[Dict[str, str]]:
    return st.session_state.chat_sessions[chat_name]