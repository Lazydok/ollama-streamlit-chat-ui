import streamlit as st
import requests
import json
from typing import List, Dict
from streamlit_option_menu import option_menu

st.set_page_config(page_title="SS-ChatAI 0.0.1 ver", layout="wide")


models = ['qwen2.5-coder:7b', 'qwen2.5-coder:1.5b']

with st.sidebar:
    st.title('SS-ChatAI')
    st.write('Version: 0.0.1')
    st.session_state.model = st.sidebar.selectbox("Select a model:", models)
    
    # 채팅창 선택을 option_menu로 변경
    chat_windows = ['chat 1', 'chat 2', 'chat 3', 'chat 4', 'chat 5']
    
    selected_chat = option_menu(
        menu_title="Chat List",
        options=chat_windows,
        icons=['None'] * len(chat_windows),  # 각 채팅창에 동일한 아이콘 적용
        menu_icon="None",
        default_index=0,
        orientation="vertical",
    )

if 'model' not in st.session_state:
    st.session_state.model = models[0]


def send_to_ollama(messages:List[Dict[str,str]]):
    # API parameters
    api_path = 'http://127.0.0.1:11434/api/chat'
    data = {
        "model": st.session_state.model,
        "messages": messages 
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
                    # print(json_obj)
                    
                    # Append content if 'message' and 'content' exist
                    if 'message' in json_obj and 'content' in json_obj['message']:
                        yield json_obj['message']['content']
                    if 'done' in json_obj and json_obj['done'] == True:
                        break
                except json.JSONDecodeError:
                    # Skip chunks that are not complete JSON
                    continue
    

def chat_page(chat_name):    
    # 각 채팅창별 메시지 세션 초기화
    # st.markdown(f'## {chat_name}')
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {window: [] for window in chat_windows}

    # 선택된 채팅창의 메시지 표시
    for message in st.session_state.chat_sessions[chat_name]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력에 대한 반응
    if prompt := st.chat_input("무엇을 도와드릴까요?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.chat_sessions[chat_name].append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            st.empty()
            
            full_content = st.write_stream(send_to_ollama(st.session_state.chat_sessions[chat_name]))
        
        st.session_state.chat_sessions[chat_name].append({"role": "assistant", "content": full_content})


# 선택된 채팅창 표시
chat_page(selected_chat)

# st.write(st.session_state)