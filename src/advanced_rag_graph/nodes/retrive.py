from dotenv import load_dotenv
from typing import Any, Dict

from src.advanced_rag_graph.ingestion import retriever
from src.advanced_rag_graph.state import GraphState

load_dotenv()

def retrieve(state: GraphState) -> Dict[str, Any]:
    print("--- RETRIEVE---")
    question = state["question"]

    # This below line get the relevant documents based on the question
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}

if __name__ == "__main__":
    state = {"question": "Agent memory"}
    output = retrieve(state)
    print(output)