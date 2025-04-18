import sqlite3

from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver

class GraphState(TypedDict):
    input:str
    user_feedback:str


def step_1(state: GraphState):
    print("---STEP 1---")
    return state

def human_feedback(state: GraphState):
    print("---HUMAN-FEEDBACK---")
    return state

def step_3(state: GraphState):
    print("---STEP 3---")
    return state


if __name__ == "__main__":
    print("HUMAN IN THE LOOP")


builder = StateGraph(GraphState)
builder.add_node("step_1", step_1)
builder.add_node("human_feedback", human_feedback)
builder.add_node("step_3", step_3)

builder.add_edge(START, "step_1")
builder.add_edge("step_1", "human_feedback")
builder.add_edge("human_feedback", "step_3")
builder.add_edge( "step_3",END)

conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
memory = SqliteSaver(conn)
# memory = MemorySaver()

graph = builder.compile(checkpointer=memory, interrupt_before=["human_feedback"])
# graph.get_graph().print_ascii()
graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

if __name__ == "__main__":
    thread = {"configurable": {"thread_id": "888"}}

    initial_input= {"input": "Hello world"}

    for event in graph.stream(initial_input, thread, stream_mode="values"):
        print(event)

    print(graph.get_state(thread).next)

    user_input = input("Tell me how you want to update the state: ")

    graph.update_state(thread, {"user_feedback": user_input}, as_node="human_feedback")

    print("---State after update---")
    print(graph.get_state(thread))
    print(graph.get_state(thread).next)

    for event in graph.stream(None, thread, stream_mode="values"):
        print(event)

pass
