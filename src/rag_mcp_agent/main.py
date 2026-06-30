import asyncio

from rag_mcp_agent.graph import build_graph

async def main() -> None:
    graph = build_graph()


    result = await graph.ainvoke(
        {
            "question": "What travel advice do you have for for visiting Pompeii?",
            "documents": [],
            "mcp_result": "",
            "answer": "",
            "use_rag": False,
            "use_mcp": False,
        }
    )

    print("\nQuestion:")
    print(result["question"])

    print("\nRetrieved Documents:")
    for index, document in enumerate(result["documents"], start=1):
        print(f"\nResult {index}")
        print("Source:", document.metadata.get("source"))
        print("Content:", document.page_content)

    print("\nAnswer")
    print(result["answer"])

if __name__ == "__main__":
    asyncio.run(main())
