import requests
import json
import streamlit as st
from typing import List, Dict, Generator

def send_to_ollama(messages: List[Dict[str, str]]) -> Generator[str, None, None]:
    data = {
        "model": st.session_state.model,
        "messages": messages 
    }
    headers = {'Content-Type': 'application/json'}
    
    with requests.post(st.session_state.ollama_api_url, json=data, headers=headers, stream=True) as res:
        for chunk in res.iter_content(chunk_size=None):
            chunk_str = chunk.decode('utf-8')
            if chunk_str.strip():
                try:
                    json_obj = json.loads(chunk_str)
                    if 'message' in json_obj and 'content' in json_obj['message']:
                        yield json_obj['message']['content']
                    if 'done' in json_obj and json_obj['done'] == True:
                        break
                except json.JSONDecodeError:
                    continue