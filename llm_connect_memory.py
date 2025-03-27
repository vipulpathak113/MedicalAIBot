from langchain_huggingface import HuggingFaceEmbeddings,HuggingFaceEndpoint
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

# Load environment variables from .env file    
load_dotenv()
hf_token = os.getenv("HF_TOKEN");

# Setup the LLM
llm = HuggingFaceEndpoint(
	huggingfacehub_api_token=hf_token,
	repo_id="mistralai/Mistral-7B-Instruct-v0.3",
	temperature=0.5
)



