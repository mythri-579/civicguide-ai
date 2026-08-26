from fastapi import APIRouter
from pydantic import BaseModel

from app.services.chroma_service import search_similar_chunks

router = APIRouter(prefix="/api/search", tags=["Search"])


class SearchRequest(BaseModel):
    query: str


@router.post("/")
def search_documents(request: SearchRequest):
    results = search_similar_chunks(request.query)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    matches = []

    for index, document_text in enumerate(documents):
        matches.append({
            "text": document_text,
            "metadata": metadatas[index],
            "distance": distances[index]
        })

    return {
        "query": request.query,
        "matches": matches
    }