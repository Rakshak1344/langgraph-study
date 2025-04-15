from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from src.advanced_rag_graph.consts import LLM


class GradeDocuments(BaseModel):
    binary_score: str = Field(
        description="Documents are relevant to the question or not. Answer with 'yes' or 'no'."
    )


structured_llm_grader = LLM.with_structured_output(GradeDocuments)

system = """You are a grader assessing relevance of a retrieved document to a user question.\n
If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant.\n
Give a binary score 'yes' or 'no' to indicate whether the document is relevant to the question."""

grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ]
)

retrieval_grader = grade_prompt | structured_llm_grader
