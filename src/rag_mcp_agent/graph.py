import asyncio

from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.documents import Document
from langchain_mcp_adapters.client import MultiServerMCPClient

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "travel_docs"

class AgentState(TypedDict):
    question: str
    documents: list[Document]
    mcp_result: str
    answer: str
    use_rag: bool
    use_mcp: bool
    route: str

def plan_route(state: AgentState) -> AgentState:
    question = state["question"].lower()

    use_rag = (
        "document" in question
        or "according to" in question
        or "pompeii" in question
        or "paris" in question
        or "naples" in question
    )

    use_mcp = (
        "tip" in question
        or "advice" in question
        or "recommend" in question
    )

    if not use_rag and not use_mcp:
        use_rag = True

    return {
        **state,
        "use_rag": use_rag,
        "use_mcp": use_mcp,
    }

def choose_route(state: AgentState) -> str:
    if state["use_rag"] and state["use_mcp"]:
        return "both"

    if state["use_rag"]:
        return "rag"

    if state["use_mcp"]:
        return "mcp"

    return "rag"

def retrieve_docs(state: AgentState) -> AgentState:
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vector_store = Chroma(
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )

    documents = vector_store.similarity_search(
        query=state["question"],
        k=2,
    )

    return {
        "question": state["question"],
        "documents": documents,
    }

def generate_answer(state: AgentState) -> AgentState:
    context="\n\n".join(
        document.page_content for document in state["documents"]
    )

    prompt = f"""
You are a helpful travel assistant.

Answer the user's question using only the retreived context and MCP tool result..

Question: 
{state["question"]}

Retreived context:
{context}

MCP tool result:
{state["mcp_result"]}
"""

    llm = ChatOllama(model="llama3.2")

    response = llm.invoke(prompt)

    return {
        "question": state["question"],
        "documents": state["documents"],
        "answer": response.content,
    }

async def call_mcp_tool(state: AgentState) -> AgentState:
    client = MultiServerMCPClient(
        {
            "travel_tools": {
                "command": "uv",
                "args": [
                    "run",
                    "python",
                    "-m",
                    "rag_mcp_agent.mcp_server",
                ],
                "transport": "stdio",
            }
        }
    )

    tools = await client.get_tools()

    get_travel_tip = next(
        tool for tool in tools if tool.name == "get_travel_tip"
    )

    city = "naples" if "pompeii" in state["question"].lower() else "paris"

    result = await get_travel_tip.ainvoke({"city": city})

    return {
        **state,
        "mcp_result": result,
    }

def build_graph():
    graph_builder = StateGraph(AgentState)

    graph_builder.add_node("plan_route", plan_route)
    graph_builder.add_node("retrieve_docs", retrieve_docs)
    graph_builder.add_node("call_mcp_tool", call_mcp_tool)
    graph_builder.add_node("generate_answer", generate_answer)

    graph_builder.add_edge(START, "plan_route")

    graph_builder.add_conditional_edges(
        "plan_route",
        choose_route,
        {
            "rag": "retrieve_docs",
            "mcp": "call_mcp_tool",
            "both": "retrieve_docs",
        },
    )

    graph_builder.add_conditional_edges(
        "retrieve_docs",
        lamdba state: "mcp" if state["use_mcp"] else "answer",
        {
            "mcp": "call_mcp_tool",
            "answer": "generate_answer",
        }

    graph_builder.add_edge("call_mcp_tool", "generate_answer")
    graph_builder.add_edge("generate_answer", END)


    return graph_builder.compile()
