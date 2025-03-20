from tools import *

st.set_page_config(
    page_title="BTT Report Extractor",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded"
)

if __name__ == "__main__":
    embeddings_model = load_embeddings()
    parser = load_parser()
    main_page(embeddings_model, parser)