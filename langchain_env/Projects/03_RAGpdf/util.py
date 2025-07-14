
from PyPDF2 import PdfReader
import requests
import json

# PDF 문서에서 텍스트를 추출
def get_pdf_text(pdf):
    try:
        text = ""
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text.encode('utf-8').decode('utf-8')  # UTF-8로 인코딩 후 디코딩
        return text
    except Exception as e:
        print(f"PDF 처리 중 오류 발생: {e}")
        return None

# Flask API 통신
def send_api(data, path):
    API_HOST = "http://127.0.0.1:5001"  # Flask 서버의 주소
    url = API_HOST + "/" + path
    headers = {
        'Content-Type': 'application/json; charset=utf-8',  # UTF-8 인코딩 명시
        'Accept': '*/*'
    }
    body = {
        "data": data
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        if response and response.status_code == 200:
            return response.json()  # JSON 파싱 시도 전에 상태 코드 확인
        else:
            print("Failed to get a valid response:", response.status_code)
            return None
    except Exception as ex:
        print("An exception occurred:", ex)
        return None
