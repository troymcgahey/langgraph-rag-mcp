import chromadb

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "travel_docs"

def main() -> None:
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(COLLECTION_NAME)

    results = collection.get(
        include=["documents", "metadatas"]
    )

    ids = results["ids"]
    documents = results["documents"]
    metadatas = results["metadatas"]

    print(f"\nCollection: {COLLECTION_NAME}")
    print(f"\nDocument count: {len(ids)}\n")

    for index, doc_id in enumerate(ids):
        print(f"Record {index + 1}")
        print("ID:", doc_id)
        print("Source:", metadatas[index].get("source"))
        print("Content preview:", documents[index][:200])
        print("-" * 80)

if __name__ == "__main__":
    main()



