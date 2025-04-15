from langchain import hub

from src.advanced_rag_graph.consts import LLM
from langchain_core.output_parsers import StrOutputParser

prompt = hub.pull("rlm/rag-prompt")

generation_chain = prompt | LLM | StrOutputParser()