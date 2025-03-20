from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import sys
import os

class CustomInstallCommand(install):
    def run(self):
        # check linux
        if sys.platform.startswith("linux"):
            print("리눅스 환경이 확인되었습니다. Ollama 설치를 확인합니다...")
            
            ollama_installed = False
            try:
                subprocess.run(["ollama", "--version"], check=True, capture_output=True)
                ollama_installed = True
                print("Ollama가 이미 설치되어 있습니다.")
            
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("Ollama를 설치합니다...")
                
                try:
                    subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, check=True)
                    print("Ollama 설치 완료!")
                    ollama_installed = True
                    
                except subprocess.CalledProcessError:
                    print("Ollama 설치 실패. 수동으로 설치하세요: curl -fsSL https://ollama.com/install.sh | sh")
                    sys.exit(1)
             # 특정 모델 자동 다운로드 (예: mistral)
            if ollama_installed:
                try: 
                    print("기본 모델을 다운로드 중...")
                    subprocess.run(["ollama", "pull", "gemma3:12b"], check=True) # model can be searched from ollama models and changed depends on gpu vram
                    print("기본 모델 다운로드 완료!")
                except subprocess.CalledProcessError:
                    print("모델 다운로드 실패. 수동으로 실행하세요: ollama pull gemma3:12b")
                    sys.exit(1)
        else:
            print("현재 운영 체제는 리눅스가 아닙니다. Ollama를 직접 설치해주세요.")
    
        # 기본 설치 진행
        install.run(self)

setup(
    name="btt_llm",
    version="0.1.0",
    description="Specialized BTT report parser using Ollama",
    author="Jinpark1049",
    url="https://github.com/Jinpark1049/document_llm.git",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.20.0",
        "PyMuPDF>=1.23.0",  # For fitz
        "pandas>=1.5.0",
        "ollama>=0.1.0",
        "langchain>=0.0.300",
        "langchain-huggingface>=0.0.1",
        "langchain-community>=0.0.1",  # For FAISS
        "streamlit-pdf-viewer>=0.0.8",
        "faiss-cpu>=1.7.0",  # FAISS CPU version
        "requests>=2.28.0",  # ngrok URL 요청용
        "langchain-ollama>=0.0.1", 
    ],
    package_data = {
        "tools": ["prompt.json"],}, # tools 패키지에 prompt.json 포함
    entry_points={ # 명령어 설정
        "console_scripts": [
            "run-btt-llm = run.run_streamlit:main",
            "run-btt-llm-bg = run.run_streamlit:main_background",  # 백그라운드 실행 명령어
            "run-btt-llm-open = run.run_streamlit:main_background_ngrok", # 
            "run-btt-llm-list = run.run_streamlit:model_list",

        ]
    },
    cmdclass={
        'install': CustomInstallCommand,  # 커스텀 설치 명령
    },
)
