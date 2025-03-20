import subprocess
import sys
import os
import pprint
from tools import *
import os, time

def main_background_ngrok():
    # streamlit_app/app.py의 절대 경로를 구함
    ensure_model()
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    # 로그 파일 경로 (프로젝트 루트에 저장)
    log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "btt_llm.log")
    ngrok_log = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ngrok.log")
    
    port = "8501"
    command = f"nohup streamlit run {app_path} --server.port {port} > {log_file} 2>&1 &"
    ngrok_cmd = f"nohup ngrok http {port} > {ngrok_log} 2>&1 &"
    # 예: nohup streamlit run streamlit_app/app.py --server.port > streamlit.log 2>&1 &
    try:
        # 백그라운드에서 실행
        subprocess.run(command, shell=True, check=True)
        
        subprocess.run(ngrok_cmd, shell=True, check=True)
        
        time.sleep(2)
        # 접속 정보 출력
        ngrok_url = get_ngrok_url()
        print("앱이 백그라운드에서 실행 중입니다!")
        print(f"로컬 접속 주소: http://localhost:{port}")        
        print(f"공용 접속 주소 (ngrok): {ngrok_url}")
        print(f"\n")
        print(f"앱 로그 파일: {log_file}")
        print(f"ngrok 로그 파일: {ngrok_log}")
        print(f"\n")
        print("실행 중인 프로세스 확인 (Streamlit): ps aux | grep streamlit")
        print("종료 방법: sudo kill -9 <PID>")
        print("실행 중인 프로세스 확인 (ngork): ps aux | grep ngrok")
        print("종료 방법: sudo kill -9 <PID>")
        
    except subprocess.CalledProcessError as e:
        print(f"백그라운드 실행 실패: {e}")
        sys.exit(1)

def main_background():
    # streamlit_app/app.py의 절대 경로를 구함
    ensure_model()
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    # 로그 파일 경로 (프로젝트 루트에 저장)
    log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "btt_llm.log")
    
    port = "8501"
    command = f"nohup streamlit run {app_path} --server.port {port} > {log_file} 2>&1 &"
    # 예: nohup streamlit run streamlit_app/app.py --server.port > streamlit.log 2>&1 &
    try:
        # 백그라운드에서 실행
        subprocess.run(command, shell=True, check=True)
                
        time.sleep(2)
        # 접속 정보 출력
        ngrok_url = get_ngrok_url()
        print("앱이 백그라운드에서 실행 중입니다!")
        print(f"로컬 접속 주소: http://localhost:{port}")        
        print(f"앱 로그 파일: {log_file}")
        print("실행 중인 프로세스 확인: ps aux | grep streamlit")
        print("종료 방법: sudo kill <PID>")
        
    except subprocess.CalledProcessError as e:
        print(f"백그라운드 실행 실패: {e}")
        sys.exit(1)

        
def main():
    # Get the path to app.py relative to this script
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    ensure_model()
    try:
        print("Streamlit 앱이 실행 중입니다!")
        print("종료 방법: ctrl + c")
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path], check=True)
        time.sleep(2)

    except subprocess.CalledProcessError as e:
        print(f"Failed to run Streamlit: {e}")
        sys.exit(1)
        
def model_list():
    result = get_ollama_models()
    print("사용가능한 모델 리스트를 불러옵니다.")
    pprint.pprint(result)

    
if __name__ == "__main__":
    main()