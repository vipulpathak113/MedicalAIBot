from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
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
Use the pieces of information provided in the context to answer user's question.
If you dont know the answer, just say that you dont know, dont try to make up an answer. 
Dont provide anything out of the given context

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
db = FAISS.load_local(
    DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True
)
