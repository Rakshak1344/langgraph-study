from typing import TypedDict, Annotated, Any, Sequence
from langgraph.graph import StateGraph, START, END

from dotenv import load_dotenv
load_dotenv()

import  operator

class State(TypedDict):
    aggregate: Annotated[list, operator.add]
    ## Which can be used to decide which node should be used next
    which: str

class ReturnNodeValue:
    def __init__(self, node_secret:str):
        self._value = node_secret

    def __call__(self, state: State)-> Any:
        import time
        time.sleep(1)
        print(f'Adding {self._value} to {state['aggregate']}')
        return {"aggregate": [self._value]}


def route_bc_or_cd(state: State) ->Sequence[str]:
    if state["which"] =="cd":
        return ["c", "d"]
    return ["b", "c"]


builder = StateGraph(State)

## Nodes
builder.add_node("a", ReturnNodeValue("I'm A"))
builder.add_node("b", ReturnNodeValue("I'm B"))
builder.add_node("c", ReturnNodeValue("I'm C"))
builder.add_node("d", ReturnNodeValue("I'm D"))
builder.add_node("e", ReturnNodeValue("I'm E"))



## Edges
builder.add_edge(START, "a")

intermediates = ["b", "c", "d"]
builder.add_conditional_edges("a", route_bc_or_cd, intermediates)

for node in intermediates:
    builder.add_edge(node, "e")

builder.add_edge("e", END)

graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path="async_graph.png")


if __name__ == "__main__":
    print("---ASYNC GRAPH---")
    graph.invoke({"aggregate": [], "which": "cd"}, {"configurable": {"thread_id": "foo"}})