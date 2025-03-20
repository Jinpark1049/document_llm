import ollama
import subprocess
import sys
import os, time
import requests
import re

# Check if Ollama is installed
def check_ollama():
    try:
        subprocess.run(["ollama", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Ollama is not installed. Run: `curl -fsSL https://ollama.com/install.sh | sh`")
        sys.exit(1)

# Ensure  model is available
def ensure_model():
    check_ollama()
    try:
        ollama.chat(model="gemma3:12b", messages=[{"role": "user", "content": "test"}])
        print("기본 모델 설치가 되어있습니다.")
    except Exception:
        print("model not found. Pulling it now...")
        ollama.pull("gemma3:12b")
        print("model pulled successfully!")
     
def get_ollama_models():
    """Ollama에 설치된 모델 리스트를 반환"""
    check_ollama()
    try:
        result = subprocess.run("ollama list", shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Ollama 모델 리스트를 가져오는 데 실패했습니다: {e}"
    
def get_ollama_model_names():
    """설치된 Ollama 모델 이름만 리스트로 반환"""
    raw_output = get_ollama_models()
    if "failed" in raw_output.lower():
        return ["gemma3:12b"]  
    lines = raw_output.splitlines()
    if len(lines) <= 1:  
        return ["gemma3:12b"]

    model_names = [line.split()[0] for line in lines[1:] if line.strip()]
    return model_names if model_names else ["gemma3:12b"]

def get_ngrok_url():
    """ngrok의 공용 URL을 가져옴"""
    time.sleep(2)  # ngrok이 시작될 시간을 줌
    try:
        response = requests.get(f"http://localhost:4040/api/tunnels")
        tunnels = response.json()["tunnels"]
        if tunnels:
            return tunnels[0]["public_url"]
        return "ngrok URL을 가져오는 데 실패했습니다."
    except Exception as e:
        return f"ngrok URL을 가져오는 데 실패했습니다: {e}"
    

def get_page(doc, page_num):
    return doc[page_num].get_text('text')

def pages_to_text(doc, index_list):
    text = ""
    for index in index_list:
        text += get_page(doc, index) + '\n'
    return text

def extract_table_of_content(doc):
    
    results = ''

    for page_num, page in enumerate(doc, start=1):
        page_text = page.get_text("text")
        if page_text.count("·") > 200:
            if page_num < 8:
                results += page_text
        if page_num >= 8:
            break
    text_list = [re.sub(r'·+', '', text).strip() for text in results.split("\n") if text.count("·") > 5]
    
    table_info = dict()
    for item in text_list:
        match = re.match(r'(.+?)\s+(\d+)$', item) 
        if match:
            front_word = match.group(1).strip()
            last_number = match.group(2)
            table_info[front_word] = int(last_number)
    return table_info

def year_pdf_files(main_dir, year):
    
    directory_path = os.path.join(main_dir, str(year))
    all_files = [os.path.join(directory_path, files) for files in os.listdir(directory_path) if files.endswith('.pdf')] 
    print(f"number of files in the folder are {len(all_files)}")
    return all_files
