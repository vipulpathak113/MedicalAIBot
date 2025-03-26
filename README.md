# MedicalAIBot

This is a bot designed to answer any medical query. Below is a step-by-step explanation of the process implemented in the `memory_llm.py` file:

## Steps Implemented in `memory_llm.py`

1. **Load PDF Documents**:
   - The script uses the `PyPDFDirectoryLoader` to load all PDF files from the `data/` directory. It recursively searches for PDF files while ignoring hidden files.
   - This ensures that all relevant documents are loaded into the system for further processing.

2. **Split Text into Chunks**:
   - The `RecursiveCharacterTextSplitter` is used to split the text from the loaded documents into smaller chunks.
   - Each chunk is limited to 500 characters, with a 50-character overlap between consecutive chunks. This overlap helps preserve context between chunks.

3. **Generate Vector Embeddings**:
   - The `HuggingFaceEmbeddings` model (`sentence-transformers/all-MiniLM-L6-v2`) is used to convert the text chunks into vector embeddings.
   - These embeddings represent the semantic meaning of the text and are essential for efficient querying and similarity searches.

4. **Store Embeddings in FAISS**:
   - The vector embeddings are stored in a FAISS (Facebook AI Similarity Search) index, which is a high-performance library for similarity search.
   - The FAISS index is saved locally at the path `vectorstore/db_faiss` for later use.

This pipeline ensures that the bot can efficiently process and query medical documents to provide accurate answers to user queries.


