from typing import Dict, Any

from src.advanced_rag_graph.chains.retrival_grader_chain import retrieval_grader
from src.advanced_rag_graph.state import GraphState


def grade_documents(state: GraphState)-> Dict[str, Any]:
    """
    Determines whether the retrieved documents are relevant to the question.
    If any document is not relevant, we will set a flag to run web search

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Filtered out irrelevant documents and updated web_search state
    """
    print("--- CHECK DOCUMENTS RELEVANCE TO QUESTION ---")
    documents = state["documents"]
    question = state["question"]

    filtered_docs = []
    web_search = False
    for doc in documents:
        score = retrieval_grader.invoke(
            { "question": question,"document": doc.page_content }
        )
        grade = score.binary_score
        if grade.lower() == "yes":
            print("--- GRADE: DOCUMENT RELEVANT ---")
            filtered_docs.append(doc)
        else:
            print("--- GRADE: DOCUMENT NOT RELEVANT ---")
            web_search = True
            continue

    return {"documents": filtered_docs, "question": question, "web_search": web_search}