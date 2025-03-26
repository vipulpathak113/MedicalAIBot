from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load all PDF files in the data directory
loader = PyPDFDirectoryLoader(
    path="data/",
    glob="**/[!.]*.pdf",
)

documents = loader.load()

# Split the text into characters
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splitted_chunks = splitter.split_documents(documents)

# Create Vector Embeddings
embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

