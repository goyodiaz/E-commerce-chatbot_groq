import streamlit as st
import comet_llm
from groq import Groq

# Comet API 키를 설정한다. st.secrets를 통해 안전하게 API 키를 불러온다.
COMET_API_KEY = st.secrets['COMET_API_KEY'] # 또는 st.secrets['COMET_API_KEY'] 대신 직접 입력
## st.secrets 관련 내용은 https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management 참조
## streamlit 및 streamlit community cloud 정리 파일의 마지막 두 페이지 참조

# Groq API 키를 설정한다. st.secrets를 통해 안전하게 API 키를 불러온다.
GROQ_API_KEY = st.secrets['GROQ_API_KEY'] # 또는 st.secrets['GROQ_API_KEY'] 대신 직접 입력
## st.secrets 관련 내용은 https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management 참조
## streamlit 및 streamlit community cloud 정리 파일의 마지막 두 페이지 참조

# Groq Client 설정
client = Groq(api_key=GROQ_API_KEY)

# Comet LLM 초기화 및 프로젝트 이름을 설정
comet_llm.init(project='E-commerce_Chatbot', api_key=COMET_API_KEY)

# 제품 목록을 정의한다. 이 목록은 챗봇의 컨텍스트로 사용하며, 사용자가 대화 중에 요청할 수 있는 제품 정보를 포함한다.
product_list = '''
# 패션샵 제품 목록

## 남성 의류:
- 티셔츠
  - 가격: 20달러
  - 사이즈: Small, Medium, Large, XL
  - 가능한 색상: 그린, 화이트, 블랙, 그레이, 네이비

- 청바지
  - 가격: 50달러
  - 사이즈: Small, Medium, Large, XL
  - 가능한 색상: 블루, 블랙, 그레이, 네이비

## 여성 의류:
- 티셔츠
  - 가격: 20달러
  - 사이즈: Small, Medium, Large, XL
  - 가능한 색상: 레드, 화이트, 블랙, 그레이, 네이비

- 드레스
  - 가격: 50달러
  - 사이즈: Small, Medium, Large, XL
  - 가능한 색상: 레드, 화이트, 블랙, 그레이, 네이비
'''

# --- 챗봇의 System Message 설정 --------------------------------------------------
SYSTEM_MESSAGE = f'''
당신은 저희 온라인 패션 상점 'Trendy Fahsion' 의 AI 어시스턴트, Shopbot 입니다.

당신의 역할은 고객이 원하는 제품을 찾도록 정보를 제공하며, 결제 과정을 안내하는 것입니다.

**반드시** 고객이 사용하는 언어에 맞춰서 응답해야 합니다. 만약 고객이 한국어로 메시지를 보냈다면, 반드시 한국어로 응답해야 합니다. 특별히 요청하지 않는 한, 한국어와 영어 이외 다른 언어로는 응답하지 마십시오.

저희 상점에서는 티셔츠와 청바지 같은 남성 의류와 티셔츠와 드레스 같은 여성 의류를 판매합니다.

현재 재고 목록은 다음과 같습니다:

```{product_list}```

**환영 인사는 처음 한번만 하세요.**

고객이 궁금한 점이 있거나 도움이 필요할 때 친근한 스타일로 도와줘야합니다.
'''

GREETINGS = ''' 안녕하세요, 고객님!

Trendy Fashion에 오신 것을 환영합니다. 

저는 이 상점의 AI 어시스턴트인 Shoptbot입니다. 

어떤 상품을 찾고 계신가요? 

궁금한 점이 있거나 도움이 필요하면 언제든지 저에게 물어보세요. 

'''

# 시스템 메시지와 인사말을 설정한다.
context = [
    {'role': 'system', 'content': SYSTEM_MESSAGE},
    {'role': 'assistant', 'content': GREETINGS}
]

# --- Streamlit 구성 -----------------------------------------------------------
# 메인 화면에 타이틀과 캡션을 설정한다.
st.title('Trendy Fashion')    # 웹 애플리케이션의 제목을 설정한다.
st.caption('AI 쇼핑 어시스턴트입니다.')       # 설명 문구(부제목)를 추가한다.

# AI 챗봇이 먼저 인사말을 한다.
st.chat_message(name='ai').write(GREETINGS)

# 세션 상태에 'messages' 키가 없으면 빈 리스트로 초기화한다.
if 'messages' not in st.session_state:  
    st.session_state['messages'] = []

# 대화 기록을 화면에 출력
for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

# 사용자 입력 처리 및 GPT 응답 생성
if prompt := st.chat_input():
    # 사용자 입력을 대화 기록에 추가
    st.session_state['messages'].append({'role': 'user', 'content': prompt})
    st.chat_message('user').write(prompt)

    # GPT 모델을 사용하여 응답 생성 (context를 메시지에 추가하여 사용)
    response = client.chat.completions.create(
        model='gemma2-9b-it',
        messages=context + st.session_state['messages']
    )
    
    # 응답 메시지를 대화 기록에 추가
    msg = response.choices[0].message.content
    st.session_state['messages'].append({'role': 'assistant', 'content': msg})
    st.chat_message('assistant').write(msg)

    # Comet LLM 로그 저장
    comet_llm.log_prompt(
        prompt=prompt,
        output=msg,
        metadata={
            'role': st.session_state['messages'][-1]['role'],
            'content': st.session_state['messages'][-1]['content'],
            'context': st.session_state['messages'],
            'product_list': product_list
        }
    )
