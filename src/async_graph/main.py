from typing import TypedDict, Annotated, Any
from langgraph.graph import StateGraph, START, END

from dotenv import load_dotenv
load_dotenv()

import  operator

class State(TypedDict):
    aggregate: Annotated[list, operator.add]

class ReturnNodeValue:
    def __init__(self, node_secret:str):
        self._value = node_secret

    def __call__(self, state: State)-> Any:
        import time
        time.sleep(1)
        print(f'Adding {self._value} to {state['aggregate']}')
        return {"aggregate": [self._value]}


builder = StateGraph(State)
builder.add_node("a", ReturnNodeValue("I'm A"))

builder.add_node("b", ReturnNodeValue("I'm B"))
builder.add_node("c", ReturnNodeValue("I'm C"))
builder.add_node("d", ReturnNodeValue("I'm D"))

builder.add_edge(START, "a")
builder.add_edge("a", "b")
builder.add_edge("a", "c")
builder.add_edge("b", "d")
builder.add_edge("c", "d")
builder.add_edge("d", END)

graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path="async_graph.png")


if __name__ == "__main__":
    print("---ASYNC GRAPH---")
    graph.invoke({"aggregate": []}, {"configurable": {"thread_id": "foo"}})