import streamlit as st
import requests
import json

# Streamlit UI settings
st.title("Real-Time Streaming of Model Response")
st.write("Streaming content from model:")

# API parameters
api_path = 'http://127.0.0.1:11434/api/chat'
data = {
    "model": "qwen2.5-coder:1.5b",
    "messages": [
        {
            "role": "user",
            "content": "안녕?"
        }
    ]    
}
headers = {
    'Content-Type': 'application/json'
}

# Placeholder for streaming output
content_placeholder = st.empty()

# Accumulate content in this variable
full_content = ""

# Make the POST request with streaming enabled
with requests.post(api_path, json=data, headers=headers, stream=True) as res:
    # Iterate over the content as it streams in
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
                    full_content += json_obj['message']['content']
                    
                    # Update the Streamlit placeholder with current content
                    content_placeholder.markdown(full_content)
            except json.JSONDecodeError:
                # Skip chunks that are not complete JSON
                continue
