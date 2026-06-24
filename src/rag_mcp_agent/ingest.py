from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

CHROMA_DIR = "chroma_db"
DOCS_DIR = Path("docs")

def load_documents() -> list[Document]:
    documents = []
    
    for path in DOCS_DIR.glob("*.txt"):
        text = path.read_text()
        documents.append(
            Document(
                page_content=text,
                metadata={"source": str(path)},
            )
        )

    return documents

def main() -> None:
    documents = load_documents()

    if not documents:
        print("No documents found.")
        return
    
    embeddings = OpenAIEmbeddings()

    Chroma.from_documents(
        document=documents,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
        collection_name="travel_docs",
    )

    print(f"Ingested {len(documents)} document(s).")

if __name__ == "__main__":
    main()
