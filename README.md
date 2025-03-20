# document_llm
Document LLM은 PDF 보고서를 파싱하고 LLM을 활용한 챗봇 기능을 제공하는 Streamlit 기반 애플리케이션입니다.  Ollama와 ngrok을 연동해 로컬 및 외부에서 쉽게 실행할 수 있습니다.
Streamlit BTT LLM은 PDF 보고서를 파싱하고 RAG을 활용한 LLM 챗봇 기능을 제공하는 Streamlit 기반 애플리케이션입니다. Ollama와 ngrok을 연동해 로컬 및 외부에서 쉽게 실행할 수 있습니다.

## Quick Start
- pip install document_llm-0.1.0.tar.gz
  
## Prerequisites

## 1. Conda 환경 설정
- Conda를 사용해 Python 3.10 환경을 생성하세요:
```bash
conda create --name [이름] python=3.10
conda activate [이름]
```

## 2. Ollama 설치
Ollama는 LLM 모델을 로컬에서 실행하기 위한 도구입니다. 설치 방법은 OS에 따라 다릅니다:

Windows / macOS
1. [Ollama 공식 사이트](https://ollama.com/)에서 다운로드:
   - Windows: `.exe` 파일을 다운로드해 실행.
   - macOS: Homebrew 사용 가능:
     brew install ollama
2. 설치 후 터미널에서 확인:

   ollama --version

Linux (설치 시 자동 처리)
- `pip install .` 또는 `pip install -e .` 실행 시 자동으로 설치됩니다:
- 수동 설치 시:
```bash
  curl -fsSL https://ollama.com/install.sh | sh
```

## 3. ngrok 설치 및 토큰 등록 (ngrok 상용 시)
ngrok은 로컬 서버를 외부에 노출하는 터널링 도구입니다.

설치 방법
1. [ngrok 공식 사이트](https://ngrok.com/download)에서 다운로드:
   - Windows/macOS: ZIP 파일을 다운로드해 압축 해제 후 실행 파일을 PATH에 추가.
2. 설치 확인:
```bash
  ngrok --version
```

토큰 등록
1. [ngrok 대시보드](https://dashboard.ngrok.com/)에서 계정을 만들고 "Your Authtoken"을 복사.
2. 터미널에서 토큰 등록:
```bash
ngrok config add-authtoken <YOUR_AUTH_TOKEN>
```

## Installation
## 1. 레포지토리 클론:

```bash
git clone https://github.com/Jinpark1049/document_llm.git
```
```bash
cd document_llm
```

## 2. 패키지 설치:

```bash
pip install .
```
또는 개발자 모드
```bash
pip install -e .
```
- Linux에서는 Ollama와 기본 모델(`gemma3:12b`)이 자동 설치됩니다.

## Command

패키지 설치 후 다음 명령어를 사용할 수 있습니다:
run-btt-llm
- 설명: Streamlit 앱을 로컬에서 실행합니다.
- 사용법:
```bash
  run-btt-llm
```
- 동작: `http://localhost:8501`에서 앱이 실행되며, 터미널이 종료되면 앱도 종료됩니다.

run-btt-llm-bg
- 설명: Streamlit 앱을 백그라운드에서 실행합니다.
- 사용법:
```bash
  run-btt-llm-bg
```
- 출력 예시:
```bash
  Streamlit 앱이 백그라운드에서 실행 중입니다!
  접속 주소: http://localhost:8501
  로그 파일: /path/to/btt_llm/streamlit.log
  실행 중인 프로세스 확인: ps aux | grep streamlit
  종료 방법: kill <PID>
```

run-btt-llm-open
- 설명: Streamlit 앱과 ngrok을 모두 백그라운드에서 실행하며, ngrok의 공용 URL을 제공합니다.
- 사용법:
```bash
  run-btt-llm-open
```
- 출력 예시:
```bash
  Streamlit 앱과 ngrok이 백그라운드에서 실행 중입니다!
  로컬 접속 주소: http://localhost:8501
  공용 접속 주소 (ngrok): https://abcd-123-456-789.ngrok-free.app
  Streamlit 로그 파일: /path/to/btt_llm/streamlit.log
  ngrok 로그 파일: /path/to/btt_llm/ngrok.log
  실행 중인 프로세스 확인: ps aux | grep 'streamlit\|ngrok'
  종료 방법: kill <PID>
```
  
run-btt-llm-list
- 설명: 현재 설치된 모델 목록을 표시합니다.
- 사용법:
```bash
  run-btt-llm-list
```
- 출력 예시:
```bash
  현재 설치된 Ollama 모델 목록:
  NAME            ID              SIZE    MODIFIED
  gemma3:12b      abc123def456    8 GB    1 week ago
  mistral:latest  xyz789abc123    4.1 GB  2 days ago

```
모델 설치
- 설치하고자 하는 모델을 확인하고 설치 [Ollama 공식 사이트](https://ollama.com/search)
```bash
  ollama pull [모델 이름]
```
Features
- Main Page: PDF를 업로드해 텍스트를 추출하고 뷰어로 확인.
- First Page: 업로드된 PDF에 대해 LLM 파싱 및 챗 어시스턴트 실행.


Troubleshooting
- Ollama 실행 안 됨: `ollama serve`를 백그라운드에서 실행하세요:
  nohup ollama serve &
- ngrok 연결 실패: 토큰이 올바른지 확인하고, `ngrok.log`를 체크하세요.
- 포트 충돌: 8501 포트가 사용 중이면, `run_background.py`에서 포트를 변경하세요.

Contact
- Author: Jinpark1049
- GitHub: [Jinpark1049](https://github.com/Jinpark1049)
