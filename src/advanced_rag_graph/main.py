from dotenv import load_dotenv

load_dotenv()

from src.advanced_rag_graph.graph import app

if __name__ == "__main__":
    print("Hello Advanced RAG")
    print(app.invoke(input={"question": "what is Pydantic why it is used?"}))