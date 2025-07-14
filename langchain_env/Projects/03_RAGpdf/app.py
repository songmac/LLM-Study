
import streamlit as st
import util

# 파일 업로드 UI
user_upload = st.file_uploader("파일을 업로드해주세요", accept_multiple_files=False)
if user_upload is not None:
    if st.button("Upload"):
        with st.spinner("PDF 처리중.."):
            raw_text = util.get_pdf_text(user_upload)
            if raw_text:
                response = util.send_api(raw_text, "pdf")
                if response:
                    st.success("파일이 성공적으로 업로드되었습니다.")
                    st.write(response)  # 응답 로그 출력
                else:
                    st.error("파일 업로드에 실패했습니다.")
            else:
                st.error("PDF 텍스트를 추출하는 데 실패했습니다.")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요, Bot 입니다. 무엇을 도와드릴까요?"}]

# 대화형 UI 로직
for msg in st.session_state.messages:
    st.write(f"{msg['role']}: {msg['content']}")

# 사용자 질문 입력
user_query = st.text_input("질문을 입력해주세요~")
if st.button("Send"):
    if user_query:
        response = util.send_api(user_query, "handbook")
        if response:
            st.session_state.messages.append({"role": "user", "content": user_query})
            st.session_state.messages.append({"role": "assistant", "content": response.get("message", "No response received")})
        else:
            st.session_state.messages.append({"role": "assistant", "content": "오류가 발생했습니다. 답변을 불러올 수 없습니다."})
        st.rerun()
