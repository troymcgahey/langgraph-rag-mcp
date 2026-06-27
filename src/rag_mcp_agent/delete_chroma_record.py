import argparse
import chromadb

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "travel_docs"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("ids", nargs="+")
    args = parser.parse_args()

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(COLLECTION_NAME)

    before = collection.get(ids=args.ids)

    if not before["ids"]:
        print("No matching IDs found. Nothing deleted.")
        return

    print("Found IDs:")
    for doc_id in before["ids"]:
        print(f"  {doc_id}")

    collection.delete(ids=args.ids)

    after = collection.get(ids=args.ids)

    if after["ids"]:
        print("Some IDs still exist:")
        for doc_id in after["ids"]:
            print(f"  {doc_id}")
    else:
        print("Delete verified. Records no longer exist.")


if __name__ == "__main__":
    main()
