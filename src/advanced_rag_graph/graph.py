from dotenv import load_dotenv

from consts import RETRIEVE, GENERATE, WEB_SEARCH, GRADE_DOCUMENTS
from nodes import retrieve, grade_documents, generate, web_search
from src.advanced_rag_graph.chains.answer_grader import answer_grader
from src.advanced_rag_graph.chains.hallucination_grader import hallucination_grader
from state import GraphState
from langgraph.graph import END, StateGraph

load_dotenv()


def decide_to_generate(state):
    print("---ASSESS GRADED DOCUMENTS---")

    if state["web_search"]:
        print("--- DECISION: NOT ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, INCLUDE")
        return WEB_SEARCH

    print("--- DECISION: GENERATE ---")
    return GENERATE

def grade_generation_grounded_in_documents_and_question(state: GraphState)-> str:
    print("--- CHECK HALLUCINATIONS ---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    score = hallucination_grader.invoke(
        {"documents": documents, "generation": generation}
    )

    if hallucination_grade := score.binary_score:
        print("--- DECISION: GENERATION IS GROUNDED IN DOCUMENTS ---")
        print("--- GRADE GENERATION vs QUESTION ---")
        score = answer_grader.invoke({
            "question": question,
            "generation": generation,
        })
        if answer_grade := score.binary_score:
            print("--- DECISION: GENERATION IS GROUNDED IN QUESTION ---")
            return "useful"
        else:
            print("--- DECISION: GENERATION DOES NOT ADDRESS QUESTION ---")
            return "not useful"
    else:
        print("--- DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-GENERATE ---")
        return "not supported"

workflow = StateGraph(GraphState)

## Adding Nodes
workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEB_SEARCH, web_search)

## Entry point
workflow.set_entry_point(RETRIEVE)

## Adding Edges
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_conditional_edges(
    GRADE_DOCUMENTS, decide_to_generate,
    {
        WEB_SEARCH: WEB_SEARCH,
        GENERATE: GENERATE
    }
)

workflow.add_conditional_edges(
    GENERATE, grade_generation_grounded_in_documents_and_question,
    {
        "useful": END,
        "not useful": WEB_SEARCH,
        "not supported": GENERATE
    }
)


workflow.add_edge(WEB_SEARCH, GENERATE)
workflow.add_edge(GENERATE, END)

app = workflow.compile()
print(app.get_graph().draw_mermaid())

if __name__ == "__main__":
    print("Hello Advanced RAG")
