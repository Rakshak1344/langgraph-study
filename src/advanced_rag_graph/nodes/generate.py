from typing import Any, Dict

from src.advanced_rag_graph.chains.generation import generation_chain
from src.advanced_rag_graph.state import GraphState


def generate(state: GraphState) -> Dict[str, Any]:
    print("---GENERAE---")
    question = state["question"]
    documents = state["documents"]

    generation = generation_chain.invoke({"context": documents, "question": question})
    return {"documents": documents, "question": question, "generation": generation}
