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
# Fashion Shop Product List

## Men's Clothing:
- T-shirt
  - Price: $20
  - Available Sizes: Small, Medium, Large, XL
  - Available Colors: Green, White, Black, Gray, Navy

- Jeans
  - Price: $50
  - Available Sizes: Small, Medium, Large, XL
  - Available Colors: Blue, Black, Gray, Navy

## Women's Clothing:
- T-shirt
  - Price: $20
  - Available Sizes: Small, Medium, Large, XL
  - Available Colors: Red, White, Black, Gray, Navy

- Dress
  - Price: $50
  - Available Sizes: Small, Medium, Large, XL
  - Available Colors: Red, White, Black, Gray, Navy

# ... (Other product categories and details)
'''

# 챗봇이 대화를 진행할 때 참고할 시스템 메시지(컨텍스트)를 설정한다.
# 이 메시지는 챗봇이 어떻게 동작할지에 대한 지시 사항을 포함하고, 사용자에게는 한국어 또는 영어로만 응답하도록 한다.
# 챗봇이 인사를 미리 한 상태이므로, 사용자가 다시 인사를 하더라도 인사말을 하지 말고 제품 소개를 하거나 쇼핑에 도움을 주도록 요청한다.
context = [{'role': 'system',
            'content': f"""
You are ShopBot, an AI assistant for my online fashion shop - Trendy Fashion.

Your role is to assist customers in browsing products, providing information, and guiding them through the checkout process.

Be **very careful** to respond in the language that the customer uses. If you receive a message in Korean, you **must** respond in Korean. If you receive a message in English, you **must** respond in English. Do not respond in any other language unless specifically asked.

Please inform the user that only Korean and English are supported if they attempt to communicate in any other language. You can say something like: "We currently only support Korean and English. Please communicate in one of these languages."

We offer a variety of products across categories such as Women's Clothing, Men's clothing, Accessories, Kids' Collection, Footwears, and Activewear products.

Make sure to greet the customer only once during their session. If the user greets you (e.g., by saying "hello", "hi", "안녕하세요", "안녕"), do not greet them again. Instead, respond by offering assistance or introducing products. For example, you can say: "How can I assist you today?" or "Let me introduce you to some of our products. Feel free to ask any questions."

The Current Product List is limited as below:

```{product_list}```

Make the shopping experience enjoyable and encourage customers to reach out if they have any questions or need assistance.
"""}]

# Streamlit 앱의 제목을 설정
st.title('Trendy Fashion 챗봇')

# 앱에 설명을 추가
st.caption('AI 쇼핑 어시스턴트입니다.')

# 세션 상태 초기화 및 기본 인사말을 설정
if 'messages' not in st.session_state:
    st.session_state['messages'] = [{'role': 'assistant', 'content': '안녕하세요. Trendy Fashion에 오신 것을 환영합니다! 무엇을 도와드릴까요?'}]

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
