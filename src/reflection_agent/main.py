from typing import Sequence, List
from dotenv import load_dotenv

from langchain_core.messages import BaseMessage, HumanMessage
from chains import generate_chain, reflection_chain
from langgraph.graph import END, MessageGraph

load_dotenv()


REFLECT = "reflect"
GENERATE = "generate"


def generation_node(state: Sequence[BaseMessage]):
    return generate_chain.invoke({"messages": state})


def reflection_node(state: Sequence[BaseMessage]) -> List[BaseMessage]:
    res = reflection_chain.invoke({"messages": state})
    return [HumanMessage(content=res.content)]


builder = MessageGraph()
builder.add_node(GENERATE, generation_node)
builder.add_node(REFLECT, reflection_node)
builder.set_entry_point(GENERATE)


def should_continue(state: List[BaseMessage]):
    if len(state) > 2:
        return END
    return REFLECT


builder.add_conditional_edges(GENERATE, should_continue)
builder.add_edge(REFLECT, GENERATE)


graph = builder.compile()
print(graph.get_graph().draw_mermaid_png())
graph.get_graph().print_ascii()

if __name__ == "__main__":
    print("LangGraph")
    inputs = HumanMessage(content="""
        Make this tweet better:"
        @LangChainAl newly Tool Calling feature is seriously underrated
        After a long wait, it's here- making the implementation of agents across
        different models with function calling - super easy.
        Made a video covering their newest blog post
    """)
    graph.invoke(inputs)
