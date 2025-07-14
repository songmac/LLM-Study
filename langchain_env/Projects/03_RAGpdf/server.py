
import rag
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask("PDF_Test")
CORS(app)  # CORS 활성화

@app.route('/pdf', methods=['POST'])
def uploadPDF():
    try:
        app.logger.info("파일 업로드 요청 수신")

        # 수신된 헤더 및 요청 데이터 로그 출력
        app.logger.info(f"요청 헤더: {request.headers}")
        app.logger.info(f"요청 데이터: {request.get_data()}")

        data = request.get_json()
        if not data or 'data' not in data:
            app.logger.error("잘못된 데이터 형식")
            return jsonify({"error": "No valid data received"}), 400

        pdf_text = data["data"]
        app.logger.info(f"PDF 텍스트: {pdf_text[:100]}")

        # 텍스트에서 청크 검색
        text_chunks = rag.get_text_chunks(pdf_text)

        # PDF 텍스트 저장을 위해 벡터 저장소 만들기
        vectorstore = rag.get_vectorstore(text_chunks)

        # 대화 체인 만들기
        conversation_chain = rag.get_conversation_chain(vectorstore)

        return jsonify({"result": "success", "message": "PDF 처리 성공!"})

    except Exception as e:
        app.logger.error(f"오류 발생: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/handbook', methods=['POST'])
def sendData():
    try:
        # 요청으로부터 JSON 데이터 받기
        data = request.get_json()
        query = data["data"]

        # 대화 체인 처리
        app.logger.info(f"사용자 질문: {query}")
        
        # 대화 체인을 가져와서 쿼리 처리
        conversation_chain = rag.get_conversation_chain(rag.get_vectorstore(rag.get_text_chunks(query)))
        result = conversation_chain({"question": query})

        # 결과 반환
        return jsonify({
            "result": "success",
            "message": result['answer']  # 'answer' 필드에 응답이 포함되어 있을 것임
        })

    except Exception as e:
        app.logger.error(f"오류 발생: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5001)  # 외부에서 접근 가능하게 host를 0.0.0.0으로 설정
