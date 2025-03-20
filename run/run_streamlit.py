import subprocess
import sys
import os
import time
import requests
from tools import ensure_model, get_ollama_models, get_ngrok_url

def main():  # run-btt-llm
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    ensure_model()
    try:
        print("Streamlit 앱이 실행 중입니다!")
        print("종료 방법: ctrl + c")
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path, "--server.headless", "true", "--server.fileWatcherType", "none"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run Streamlit: {e}")
        sys.exit(1)

def main_background():  # run-btt-llm-bg
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    log_file = os.path.join(os.getcwd(), "btt_llm.log")
    port = "8501"
    ensure_model()
    command = f"nohup streamlit run {app_path} --server.fileWatcherType none --server.port {port} > {log_file} 2>&1 &"
    try:
        subprocess.Popen(command, shell=True)  # Popen으로 백그라운드 실행
        time.sleep(2)  # 프로세스가 시작될 시간 확보
        print("앱이 백그라운드에서 실행 중입니다!")
        print(f"로컬 접속 주소: http://localhost:{port}")
        print(f"앱 로그 파일: {log_file}")
        print("실행 중인 프로세스 확인: ps aux | grep streamlit")
        print("종료 방법: sudo kill -9 <PID>")
    except Exception as e:
        print(f"백그라운드 실행 실패: {e}")
        sys.exit(1)

def main_background_ngrok():  # run-btt-llm-open
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    log_file = os.path.join(os.getcwd(), "btt_llm.log")
    ngrok_log = os.path.join(os.getcwd(), "ngrok.log")
    port = "8501"
    
    ensure_model()
    command = f"nohup streamlit run {app_path} --server.fileWatcherType none > {log_file} --server.port {port} 2>&1 &"
    ngrok_cmd = f"nohup ngrok http {port} > {ngrok_log} 2>&1 &"
    try:
        subprocess.run(command, shell=True, check=True)
        subprocess.run(ngrok_cmd, shell=True, check=True)
        time.sleep(2)
        ngrok_url = get_ngrok_url()
        print("앱이 백그라운드에서 실행 중입니다!")
        print(f"로컬 접속 주소: http://localhost:{port}")
        print(f"공용 접속 주소 (ngrok): {ngrok_url}")
        print(f"앱 로그 파일: {log_file}")
        print(f"ngrok 로그 파일: {ngrok_log}")
        print("실행 중인 프로세스 확인 (Streamlit): ps aux | grep streamlit")
        print("실행 중인 프로세스 확인 (ngrok): ps aux | grep ngrok")
        print("종료 방법: sudo kill -9 <PID>")
    except subprocess.CalledProcessError as e:
        print(f"백그라운드 실행 실패: {e}")
        sys.exit(1)

def model_list():  # run-btt-llm-list
    print("사용가능한 모델 리스트를 불러옵니다.")
    result = get_ollama_models()
    print(result)

if __name__ == "__main__":
    main()
