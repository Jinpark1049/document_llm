import streamlit as st
from tools import load_embeddings, load_parser, main_page, first_page

st.set_page_config(
    page_title="BTT Report Extractor",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    embeddings_model = load_embeddings()
    
    page_options = ["Pdf Upload", "LLM Run"]
    selected_page = st.sidebar.selectbox("Select Page", page_options)
    
    parser = load_parser()
    
    if parser:
        if selected_page == "Pdf Upload":
            main_page(embeddings_model, parser)
        elif selected_page == "LLM Run":
            first_page()  
    else:
        st.error("Parser 로드에 실패했습니다. 모델 이름을 확인하세요.")

if __name__ == "__main__":
    main()
