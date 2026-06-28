from rag_mcp_agent.graph import build_graph

def main() -> None:
    graph = build_graph()


    result = graph.invoke(
        {
            "question": "What city is good for visiting museums?",
            "documents": [],
            "answer": "",
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
    main()
