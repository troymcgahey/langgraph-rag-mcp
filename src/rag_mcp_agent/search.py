from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "travel_docs"

def main() -> None:
    print("In Search.Main.PY")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vector_store = Chroma(
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )

    query = "What city is a good base for visiting Pompeii?"

    results = vector_store.similarity_search(
        query=query,
        k=2,
    )
    
    print(f"\nQuery: {query}\n")

    for index,document in enumerate(results, start=1):
        print(f"Result {index}")
        print("Source:", document.metadata.get("source"))
        print("Content:", document.page_content)
        print("-" * 50)
        
if __name__ == "__main__":
    main()
