from pprint import pprint

from src.advanced_rag_graph.chains import hallucination_grader
from src.advanced_rag_graph.chains.generation import generation_chain
from src.advanced_rag_graph.chains.hallucination_grader import hallucination_grader, GradeHallucinations
from src.advanced_rag_graph.chains.retrival_grader_chain import GradeDocuments, retrieval_grader
from src.advanced_rag_graph.ingestion import retriever


def test_retrieval_grader_answer_yes() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)
    doc_txt = docs[0].page_content

    res: GradeDocuments = retrieval_grader.invoke(
        {"question": question, "document": doc_txt}
    )
    assert res.binary_score == "yes"


def test_retrieval_grader_answer_no() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)
    doc_txt = docs[0].page_content

    res: GradeDocuments = retrieval_grader.invoke(
        {"question": "How to make pizza", "document": doc_txt}
    )
    assert res.binary_score == "no"

def test_generation_chain() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)
    generation = generation_chain.invoke({"question": question, "context": docs})
    pprint(generation)


def test_hallucination_grader_answer_yes() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)

    generation = generation_chain.invoke({'question': question, 'context': docs})
    res: GradeHallucinations = hallucination_grader.invoke(
        {"documents": docs, "generation": generation}
    )
    assert res.binary_score


def test_hallucination_grader_answer_no() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)

    # generation not needed
    # generation = generation_chain.invoke({'question': question, 'context': docs})
    res: GradeHallucinations = hallucination_grader.invoke(
        {"documents": docs, "generation": "In order to make pizza we need to first start with the dough"}
    )
    assert not res.binary_score