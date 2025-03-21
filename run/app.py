import streamlit as st
from tools import load_embeddings, load_parser, main_page, first_page, get_ollama_model_names

st.set_page_config(
    page_title="BTT Report Extractor",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    embeddings_model = load_embeddings()
    
    page_options = ["App", "LLM Run"]
    selected_page = st.sidebar.selectbox("Select Page", page_options)
    
    st.sidebar.header("Select LLM Model")
    model_options = get_ollama_model_names()
    model_name = st.sidebar.selectbox(
        "Choose a model",
        options=model_options,
        index=model_options.index("gemma3:12b") if "gemma3:12b" in model_options else 0
    )
    parser = load_parser(model_name)

    if parser:
        if selected_page == "App":
            main_page(embeddings_model, parser)
        elif selected_page == "LLM Run":
            first_page()  
    else:
        st.error("Parser 로드에 실패했습니다. 모델 이름을 확인하세요.")

if __name__ == "__main__":
    main()
