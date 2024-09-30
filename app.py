import streamlit as st
import requests
import json
from typing import List, Dict

def send_to_ollama(messages:List[Dict[str,str]]):

    # API parameters
    api_path = 'http://127.0.0.1:11434/api/chat'
    data = {
        "model": "qwen2.5-coder:1.5b",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]    
    }
    headers = {
        'Content-Type': 'application/json'
    }
        
    # Make the POST request with streaming enabled
    with requests.post(api_path, json=data, headers=headers, stream=True) as res:
        # Iterate over the content as it streams in
        # full_content = ""
        for chunk in res.iter_content(chunk_size=None):
            # Decode the bytes to string
            chunk_str = chunk.decode('utf-8')
            
            # Check for valid JSON lines
            if chunk_str.strip():
                try:
                    # Convert string to JSON object
                    json_obj = json.loads(chunk_str)
                    
                    # Append content if 'message' and 'content' exist
                    if 'message' in json_obj and 'content' in json_obj['message']:
                        # json_obj['message']['content']
                        yield json_obj['message']['content']
                        # Update the Streamlit placeholder with current content
                        # content_placeholder.markdown(full_content)
                except json.JSONDecodeError:
                    # Skip chunks that are not complete JSON
                    continue
    

st.title("Echo Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display placeholder for assistant response in chat
    with st.chat_message("assistant"):
        content_placeholder = st.empty()  # Placeholder for streaming output
        
        # Accumulate content in this variable
        full_content = st.write_stream(send_to_ollama(st.session_state.messages))
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_content})
    
    # st.write(st.session_state)