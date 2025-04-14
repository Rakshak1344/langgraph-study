import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS

from src.advanced_rag_graph.consts import VECTOR_DB_PATH, EMBEDDING_MODEL

load_dotenv()

def ingest():
    urls = [
        "https://lilianweng.github.io/posts/2023-06-23-agent/",
        "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
        "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
    ]

    docs = [WebBaseLoader(url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250, chunk_overlap=0
    )

    docs_splits = text_splitter.split_documents(docs_list)

    if not os.path.exists(VECTOR_DB_PATH):
        vectorstore = FAISS.from_documents(
            documents=docs_splits,
            embedding=EMBEDDING_MODEL # Use the consistent embedding model
        )
        vectorstore.save_local(folder_path=VECTOR_DB_PATH)
        print("Vector Ingestion Complete")
        return

    print("vectorstore already exists, if you want to re-ingest, delete the directory")


loaded_vectorstore = FAISS.load_local(
    folder_path=VECTOR_DB_PATH,
    embeddings=EMBEDDING_MODEL,
    allow_dangerous_deserialization=True
)

retriever = loaded_vectorstore.as_retriever()

if __name__ == "__main__":
    # Do The Ingest to create a vector DB
    # ingest()
    # Then Invoke with question related to it
    data = retriever.invoke("agent memory")
    print(data)
