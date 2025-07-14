
# 두 개의 서버 동시 실행 (자동화)
import subprocess
import time

# Flask 서버 실행
def run_flask():
    print("Flask 서버 실행 중...")
    subprocess.Popen(["python", "server.py"])  # Flask 서버 실행

# Streamlit 애플리케이션 실행
def run_streamlit():
    print("Streamlit 애플리케이션 실행 중...")
    subprocess.Popen(["streamlit", "run", "app.py"])  # Streamlit 실행

if __name__ == "__main__":
    # Flask 서버 먼저 실행
    run_flask()

    # Flask 서버가 준비될 때까지 대기 (필요에 따라 조정)
    time.sleep(3)

    # Streamlit 애플리케이션 실행
    run_streamlit()
