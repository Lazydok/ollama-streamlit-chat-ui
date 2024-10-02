import streamlit as st
from streamlit_option_menu import option_menu
from config import MODELS, CHAT_WINDOWS, APP_TITLE, APP_VERSION, OLLAMA_API_URL
from chat_utils import initialize_chat_sessions, display_chat_messages, add_user_message, add_assistant_message, get_chat_messages
from ollama_api import send_to_ollama

def setup_page():
    st.set_page_config(page_title=f"{APP_TITLE} {APP_VERSION}", layout="wide")

def setup_sidebar():
    with st.sidebar:
        st.title(APP_TITLE)
        st.write(f'Version: {APP_VERSION}')
        st.session_state.model = st.sidebar.selectbox("Select a model:", MODELS)
        
        return option_menu(
            menu_title="Chat List",
            options=CHAT_WINDOWS,
            icons=['None'] * len(CHAT_WINDOWS),
            menu_icon="None",
            default_index=0,
            orientation="vertical",
        )

def chat_page(chat_name: str):
    display_chat_messages(chat_name)

    if prompt := st.chat_input("Input your message here..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        add_user_message(chat_name, prompt)

        with st.chat_message("assistant"):
            st.empty()
            full_content = st.write_stream(send_to_ollama(get_chat_messages(chat_name)))
        
        add_assistant_message(chat_name, full_content)

def main():
    setup_page()
    selected_chat = setup_sidebar()

    if 'model' not in st.session_state:
        st.session_state.model = MODELS[0]
    
    st.session_state.ollama_api_url = OLLAMA_API_URL
    st.session_state.chat_windows = CHAT_WINDOWS

    initialize_chat_sessions()
    chat_page(selected_chat)

if __name__ == "__main__":
    main()