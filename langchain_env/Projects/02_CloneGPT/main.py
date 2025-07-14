
import streamlit as st 
from utils import print_messages, get_session_history, StreamHandler
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import ChatMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

# 환경 변수 설정
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.environ["OPENAI_API_KEY"]

st.set_page_config(page_title="clone ChatGPT", page_icon="🦜")
st.title("🦜 clone ChatGPT")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 채팅 대화 기록을 저장하는 store 세션 상태 변수
if "store" not in st.session_state:
    st.session_state["store"] = dict()

# 세션 ID 지정하는 사이드바 만들기
with st.sidebar:
    session_id = st.text_input("Session ID", value = "abc123")
    # 대화기록 초기화 하는 기능 추가하기
    clear_btn = st.button("대화기록 초기화")
    if clear_btn:
        st.session_state["messages"] = []
        # st.session_state["store"] = dict() # 대화 기록 저장한 것 까지 초기화 하려면 추가하면 됨
        st.rerun()

print_messages()  # 이전 메시지 출력

user_input = st.chat_input("메세지를 입력해주세요.")
if user_input:
    # 사용자의 입력 저장
    st.chat_message("user").write(f"{user_input}")
    st.session_state["messages"].append(ChatMessage(role="user", content=user_input))

    # 5) AI의 답변 출력
    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())

        # LLM을 사용하여 AI의 답변을 생성
        # 1) 모델 생성
        llm = ChatOpenAI(
            temperature=0, 
            model_name='gpt-4-turbo', 
            api_key=api_key, 
            streaming=True, 
            callbacks=[stream_handler]
        )

        # 2) 프롬프트 생성
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "질문에 짧고 간결하게 답변해 주세요."),
                MessagesPlaceholder(variable_name="history"),  # 대화 기록 사용
                ("human", "{question}")  # 사용자 질문 입력
            ]
        )

        chain = prompt | llm 

        # 3) 메모리 적용한 체인 생성
        chain_with_memory = RunnableWithMessageHistory(
            chain,  # 실행할 Runnable 객체
            get_session_history,  # 세션 기록을 가져오는 함수
            input_messages_key="question",  # 사용자 질문의 키
            history_messages_key="history",  # 기록 메시지의 키
        )

        # 4) AI 응답 생성
        response = chain_with_memory.invoke(
            {"question": user_input},
            config={"configurable": {"session_id": session_id}}
        )

        # 6) 토큰 하나하나 당 스트리밍으로 결과 출력
        st.session_state["messages"].append(ChatMessage(role="assistant", content=response.content))
