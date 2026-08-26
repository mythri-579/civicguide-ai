from groq import Groq

from app.config import GROQ_API_KEY
from app.services.chroma_service import search_similar_chunks

client = Groq(api_key=GROQ_API_KEY)


def format_sources(metadatas: list[dict]) -> list[dict]:
    seen = set()
    sources = []

    for meta in metadatas:
        title = meta.get("title", "Unknown Document")
        scheme_name = meta.get("scheme_name", "")
        department = meta.get("department", "")
        source_url = meta.get("source_url", "")

        key = title

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


def ask_question(question: str):
    results = search_similar_chunks(question, n_results=4)

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not documents:
        return {
            "answer": "Not enough verified information is available for this question.",
            "sources": []
        }

    context_blocks = []
    for i, doc in enumerate(documents):
        source_title = metadatas[i].get("title", "Unknown Document")
        context_blocks.append(f"[Source: {source_title}]\n{doc}")

    context = "\n\n".join(context_blocks)

    prompt = f"""You are CivicGuide AI, a public-service assistant.
Answer the user's question using ONLY the context below.
Each context block shows which document it came from.
If the answer is not in the context, say exactly: "Not enough verified information is available."
Do not use outside knowledge. Do not guess.

Context:
{context}

Question: {question}

Give a concise, direct answer based only on the context above."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=500
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": format_sources(metadatas)
    }