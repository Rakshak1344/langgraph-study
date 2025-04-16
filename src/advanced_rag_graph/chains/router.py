from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from src.advanced_rag_graph.consts import LLM


class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource"""

    datasource: Literal["vectorstore", "websearch"] = Field(
        ...,
        description="Given a user question choose the route it to web search or a vectorstore"
    )

structured_llm_route = LLM.with_structured_output(RouteQuery)

system="""You are an expert at routing a user question to a vectorstore or web search.
The vectorstore contains documents related to agents, prompt engineering, adversarial attacks.
Use the vectorstore for questions on these topics. For all else, use web-search."""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}")
    ]
)

question_router = prompt | structured_llm_route