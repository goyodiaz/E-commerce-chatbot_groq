from openai import OpenAI
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input('OpenAI API Key', key='chatbot_api_key', type='password')

st.title('간단한 챗봇')
st.caption('OpenAI API를 이용한 챗봇')

# 세션 상태 초기화
if 'messages' not in st.session_state:
    st.session_state['messages'] = [{'role': 'assistant', 'content': '메시지를 입력하세요'}]

# 대화 기록을 화면에 출력
for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

# 사용자 입력 처리 및 GPT 응답 생성
if prompt := st.chat_input():
    if not openai_api_key.startswith('sk-'):
        st.warning('OpenAI API Key를 입력하세요!', icon='⚠')
        st.stop()

    # 사용자 입력을 대화 기록에 추가
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    st.chat_message('user').write(prompt)

    # GPT 모델을 사용하여 응답 생성
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(model='gpt-3.5-turbo', messages=st.session_state.messages)
    
    # 응답 메시지를 대화 기록에 추가
    msg = response.choices[0].message.content
    st.session_state.messages.append({'role': 'assistant', 'content': msg})
    st.chat_message('assistant').write(msg)
