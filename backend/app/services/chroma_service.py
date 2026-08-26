import chromadb

from app.config import CHROMA_DIR

client = chromadb.PersistentClient(path=CHROMA_DIR)

collection = client.get_or_create_collection(
    name="public_service_documents"
)


def store_document_chunks(document_id: int, chunks: list[str], metadata: dict):
    ids = []
    metadatas = []

    for index, chunk in enumerate(chunks):
        ids.append(f"doc_{document_id}_chunk_{index}")
        metadatas.append({
            **metadata,
            "document_id": document_id,
            "chunk_index": index
        })

    collection.add(
        ids=ids,
        documents=chunks,
        metadatas=metadatas
    )

    return len(chunks)


def search_similar_chunks(query: str, n_results: int = 8):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return results