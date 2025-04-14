from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

# APIKEY = os.getenv("OPENAI_API_KEY")
# print(APIKEY)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
VECTOR_DB_PATH = os.path.join(PROJECT_ROOT, ".faiss_index")
VECTORSTORE_COLLECTION_NAME = "faiss_collection"

## LLM
CHAT_MODEL="gpt-4o-mini"
LLM = ChatOpenAI(model=CHAT_MODEL, temperature=0)
EMBEDDING_MODEL = OpenAIEmbeddings()