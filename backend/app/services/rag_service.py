from app.services.chroma_service import search_similar_chunks


def format_sources(metadatas: list[dict]) -> list[dict]:
    seen = set()
    sources = []

    for meta in metadatas:
        title = meta.get("title", "Unknown Document")
        scheme_name = meta.get("scheme_name", "")
        department = meta.get("department", "")
        source_url = meta.get("source_url", "")

        key = f"{title}-{source_url}"

        if key in seen:
            continue

        seen.add(key)

        sources.append({
            "title": title,
            "scheme_name": scheme_name,
            "department": department,
            "source_url": source_url
        })

    return sources


def clean_text(text: str, limit: int = 900) -> str:
    text = " ".join(text.split())

    if len(text) > limit:
        return text[:limit] + "..."

    return text


def ask_question(question: str):
    results = search_similar_chunks(question, n_results=4)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not documents:
        return {
            "answer": "Not enough verified information is available for this question.",
            "sources": []
        }

    answer_parts = [
        "AI answer generation is currently unavailable, but I found relevant verified source content from the uploaded documents:",
        ""
    ]

    for index, document_text in enumerate(documents[:3], start=1):
        metadata = metadatas[index - 1]
        title = metadata.get("title", "Unknown Document")

        answer_parts.append(f"{index}. Source: {title}")
        answer_parts.append(clean_text(document_text))
        answer_parts.append("")

    answer_parts.append("Please verify the source text above before taking any action.")

    return {
        "answer": "\n".join(answer_parts),
        "sources": format_sources(metadatas)
    }