import asyncio

from rag_mcp_agent.graph import build_graph

async def main() -> None:
    graph = build_graph()

    user_input = input("What travel advice are you inquiring about: ")

    result = await graph.ainvoke(
        {
            "question": user_input,
            "documents": [],
            "mcp_result": "",
            "answer": "",
            "use_rag": False,
            "use_mcp": False,
            "route": "",
            "plan_reason": "",
        }
    )

    print("\nQuestion:")
    print(result["question"])

    print("\nPlanner decision:")
    print("use_rag:", result["use_rag"])
    print("use_mcp:", result["use_mcp"])
    print("reason:", result["plan_reason"])
    print("\n\nRoute:")
    print(result["route"])

#    print("\nRetrieved Documents:")
#    for index, document in enumerate(result["documents"], start=1):
#        print(f"\nResult {index}")
#        print("Source:", document.metadata.get("source"))
#        print("Content:", document.page_content)

    print("\nAnswer")
    print(result["answer"])

if __name__ == "__main__":
    asyncio.run(main())
