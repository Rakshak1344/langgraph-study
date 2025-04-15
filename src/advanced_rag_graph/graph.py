from dotenv import load_dotenv

from consts import RETRIEVE, GENERATE, WEB_SEARCH, GRADE_DOCUMENTS
from nodes import retrieve, grade_documents, generate, web_search
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

workflow.add_edge(WEB_SEARCH, GENERATE)
workflow.add_edge(GENERATE, END)

app = workflow.compile()
app.get_graph().print_ascii()

if __name__ == "__main__":
    print("Hello Advanced RAG")
