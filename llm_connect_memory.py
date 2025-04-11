from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
import os

# Load environment variables from .env file
load_dotenv()
hf_token = os.getenv("HF_TOKEN")

# Setup the LLM
llm = HuggingFaceEndpoint(
    huggingfacehub_api_token=hf_token,
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    temperature=0.5,
)

# Setup the Prompt
custom_prompt_template = """
Use the pieces of information provided in the context to answer the user's question.
If the question is not related to the context, respond with "The question is not related to the provided context." 
Do not attempt to make up an answer or provide unrelated information

Context: {context}
Question: {question}

Start the answer directly. No small talk please.
"""

prompt = PromptTemplate(
    template=custom_prompt_template, input_variables=["context", "question"]
)

# Load Database
DB_FAISS_PATH = "vectorstore/db_faiss"
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

try:
    # Debugging: Log before loading FAISS
    print(f"Loading FAISS index from: {DB_FAISS_PATH}")
    
    db = FAISS.load_local(
        DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True
    )
    
    # Debugging: Log after successful load
    print("FAISS index loaded successfully.")
except Exception as error:
    # Debugging: Log any errors during loading
    print(f"Error loading FAISS index: {error}")
    raise error

# Create the RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=False,  # Ensure only the result is returned
    chain_type_kwargs={"prompt": prompt},
)

