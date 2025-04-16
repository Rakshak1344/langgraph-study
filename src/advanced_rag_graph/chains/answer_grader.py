from pydantic import BaseModel, Field
from src.advanced_rag_graph.consts import LLM
from langchain_core.prompts import ChatPromptTemplate


class GradeAnswer(BaseModel):
    binary_score: bool = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )

structured_llm_grader = LLM.with_structured_output(GradeAnswer)

system= """You are a grader assessing whether an answer addresses / resolves a question\n
Give a binary score 'yes' or 'no'. Yes means that the answer resolves the question."""

prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("human", "User Question: \n\n{question} \n\n LLM generation: {generation}")
])

answer_grader = prompt | structured_llm_grader