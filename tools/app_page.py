import streamlit as st
import fitz  # PyMuPDF
import os
import re
from io import BytesIO
from streamlit_pdf_viewer import pdf_viewer
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import pandas as pd
from .llm_parser import *

@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-large-zh-v1.5",  # 다국어 지원 (한국어 포함) 또는 "BAAI/bge-large-en-v1.5" (더 작은 모델)
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True},
    )

@st.cache_resource
def load_parser(model_name = 'gemma3:12b'):
    return Biollm(model = model_name)

def main_page(embeddings_model, parser):
    
    if "run_chat_assistant" not in st.session_state:
        st.session_state.run_chat_assistant = False
    if "run_llm_parser" not in st.session_state:
        st.session_state.run_llm_parser = False
    
    st.session_state["embeddings_model"] = embeddings_model
    st.session_state["parser"] = parser

    col1, col2 = st.columns((1, 1), gap='medium')

    with st.sidebar:
        st.title('📁 BTT Report Extractor')
        
        # Year selection dropdown
        years = list(range(2000, 2031))
        selected_year = st.selectbox('Select a Year', years, index=years.index(2025))
        
        # File uploader
        st.sidebar.header("Upload PDF")
        uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type=["pdf"])
        
        pdf_text = ""  # Initialize empty string to avoid errors

        if uploaded_file is not None:
            st.sidebar.success("File uploaded successfully!")

            # Save directory based on selected year
            save_dir = os.path.join("temp", str(selected_year))
            os.makedirs(save_dir, exist_ok=True)

            # Ensure filename is safe
            safe_file_name = re.sub(r'[<>:"/\\|?*]', '_', uploaded_file.name)
            save_path = os.path.join(save_dir, safe_file_name)
            new_file_uploaded = st.session_state.get("pdf_file_name") != safe_file_name
            if new_file_uploaded:
                st.session_state["messages"] = []  # Reset messages
                st.session_state['run_chat_assistant'] = False
                st.session_state['run_llm_parser'] = False

            # Save the file
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Extract text from PDF
            with fitz.open(save_path) as doc:
                pdf_text = "\n".join([page.get_text("text") for page in doc])

            # Store in session_state
            st.session_state["pdf_path"] = save_path
            st.session_state["pdf_text"] = pdf_text
            st.session_state['binary_data'] = uploaded_file.getvalue()
            st.session_state['new_file_uploaded'] = new_file_uploaded
                        
            if new_file_uploaded or "documents" not in st.session_state:
                doc_text_formatted = st.session_state["pdf_text"].replace('.', '')
                doc_text_formatted = "".join("".join(doc_text_formatted.split("\n")).split("        "))
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=500,
                    chunk_overlap=100,
                    length_function=len,
                )
                texts = text_splitter.split_text(doc_text_formatted)
                documents = [Document(page_content=text) for text in texts]
                st.session_state['documents'] = documents

    with col1:
        if st.session_state.get("pdf_text"):
            st.markdown('<h4 style="text-align: center;">Extracted Text</h4>', unsafe_allow_html=True)
            st.text_area("Extracted PDF Content", st.session_state["pdf_text"], height=800)
        
    with col2:
        if st.session_state.get("binary_data"):
            st.markdown('<h4 style="text-align: center;">PDF Viewer</h4>', unsafe_allow_html=True)
            pdf_viewer(input=st.session_state['binary_data'], height=800)

def first_page():
    
    if "pdf_path" not in st.session_state:
        st.session_state.pdf_path = None
    if "retriever" not in st.session_state:
        st.session_state.retriever = None
    if "documents" not in st.session_state:
        st.session_state.documents = None
    if "df_result" not in st.session_state:
        st.session_state.df_result = None
    if "run_chat_assistant" not in st.session_state:
        st.session_state.run_chat_assistant = False
    if "run_llm_parser" not in st.session_state:
        st.session_state.run_llm_parser = False
    embeddings_model = st.session_state["embeddings_model"]
    parser =  st.session_state["parser"]
    
    with st.sidebar:
        st.title('📁 BTT Report Extractor')    
        if st.session_state.pdf_path is not None:
            pdf_path = st.session_state.pdf_path
            st.sidebar.write(f"📄 **{os.path.basename(pdf_path)}** is ready.")
        else:
            st.sidebar.write("⚠️ No PDF file uploaded.")

        if st.button("🚀 Run LLM Parser"):
            if st.session_state.pdf_path is not None and not st.session_state.run_llm_parser:
                with st.spinner("🔄 Running LLM Parser... Please wait..."):
                    parser.run(st.session_state.pdf_path)
                    new_df = pd.DataFrame([parser.parsed_data])
                    st.session_state.run_llm_parser = True
                    if st.session_state.get('new_file_uploaded'):
                        if st.session_state.df_result is not None:
                            st.session_state.df_result = pd.concat([st.session_state.df_result, new_df], ignore_index=True)
                        else:
                            st.session_state.df_result = new_df
                    else:
                        st.session_state.df_result = new_df
                    parser.refresh()
                st.sidebar.success("✅ LLM Parser finished!")
            elif st.session_state.run_llm_parser:
                st.warning("⚠️ Please upload a new PDF file first.")
            else:
                st.sidebar.warning("⚠️ Please upload a PDF first.")

        if st.button("Run Chat Assistant"):
            if st.session_state.documents is not None and not st.session_state.run_chat_assistant:
                with st.spinner("🔄 Running Chat Assistant... Please wait..."):
                    db = FAISS.from_documents(st.session_state['documents'], embeddings_model)
                    retriever = db.as_retriever(
                        search_type='mmr',
                        search_kwargs={'k': 10, 'fetch_k': 50, 'lambda_mult': 0.5}
                    )
                    st.session_state.retriever = retriever
                    st.session_state.run_chat_assistant = True
            elif st.session_state.run_chat_assistant:
                st.warning("⚠️ Please upload a new PDF file first.")
            else:
                st.warning("⚠️ Please upload a PDF first.")

    if st.session_state.df_result is not None:
        st.subheader("📊 Extracted Data")
        edited_df = st.data_editor(st.session_state.df_result, num_rows="dynamic")
        st.session_state.df_result = edited_df
        st.success("✅ Changes saved!")
        csv = edited_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, "extracted_data.csv", "text/csv")

    if st.session_state.run_chat_assistant:
        st.subheader("🤖 Chat Assistant")
        if "messages" not in st.session_state:
            st.session_state["messages"] = []
        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        if prompt := st.chat_input("Enter your question for the Chat Assistant"):
            st.session_state["messages"].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                response = parser.rag(st.session_state.retriever, prompt)
                st.markdown(response)
            st.session_state["messages"].append({"role": "assistant", "content": response})
