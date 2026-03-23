from app.core.config import settings


def generate_grounded_answer(query: str, results: list[dict]) -> str | None:
    if not settings.GEMINI_ENABLED:
        return None

    if not settings.GEMINI_API_KEY:
        return None

    if not results:
        return None

    try:
        from google import genai
    except ImportError:
        return None

    context_blocks = []
    for idx, item in enumerate(results, start=1):
        context_blocks.append(
            f"[Source {idx}] "
            f"Document: {item['filename']} | Chunk: {item['chunk_index']}\n"
            f"{item['text']}"
        )

    context_text = "\n\n".join(context_blocks)

    prompt = f"""
You are answering strictly from retrieved company knowledge base content.

Rules:
1. Use only the provided context.
2. If the answer is not clearly supported by the context, say:
   "The uploaded documents do not contain a reliable answer to that question."
3. Keep the answer concise and factual.
4. Do not invent steps or policies.

User question:
{query}

Retrieved context:
{context_text}
:
{context_text}
""".strip()

    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
        )
        text = getattr(response, "text", None)
        return text.strip() if text else None
    except Exception:
        return None