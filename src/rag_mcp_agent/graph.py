from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

CHROMA_DIR = "chrome_db"
COLLECTION_NAME = "travel_docs"

class AgentState(TypedDict):
    question: str
    documents: list[Document]

def retrieve_docs(state: AgentState) -> AgentState:
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vector_store = Chroma(
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION_NAME,
        embeddings_function=embeddings,
    )

    documents = vector_store.similarity_search(
        query=state["question"],
        k=2,
    )

    return {
        "question": state["question"],
        "documents": documents,
    }

def build_graph():
    graph_builder = StateGraph(AgentState)

    graph_builder.add_node("retrieve_docs", retrieve_docs)

    graph_builder.add_edge(START, "retrieve_docs")
    graph_builder.add_edge("retrieve_docs", END)


    return grpah_builder.compile()
