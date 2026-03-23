from __future__ import annotations

from functools import lru_cache

import chromadb
from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.models import Document, DocumentChunk


COLLECTION_NAME = "knowledge_base"


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer("all-MiniLM-L6-v2")


@lru_cache(maxsize=1)
def get_chroma_client() -> chromadb.PersistentClient:
    return chromadb.PersistentClient(path=settings.CHROMA_DIR)


def get_collection():
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_embedding_model()
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return embeddings.tolist()


def index_document_chunks(
    document: Document,
    chunks: list[DocumentChunk],
) -> None:
    if not chunks:
        return

    collection = get_collection()

    ids = [chunk.vector_id for chunk in chunks]
    texts = [chunk.chunk_text for chunk in chunks]
    metadatas = [
        {
            "document_id": document.id,
            "filename": document.original_filename,
            "chunk_index": chunk.chunk_index,
        }
        for chunk in chunks
    ]
    embeddings = embed_texts(texts)

    collection.upsert(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
    )


def search_similar_chunks(query: str, top_k: int = 5) -> list[dict]:
    collection = get_collection()

    if collection.count() == 0:
        return []

    query_embedding = embed_texts([query])[0]

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]

    parsed_results: list[dict] = []

    for doc_text, metadata, distance in zip(documents, metadatas, distances):
        distance_value = float(distance)
        score = max(0.0, round(1.0 - distance_value, 4))

        parsed_results.append(
            {
                "document_id": int(metadata["document_id"]),
                "filename": str(metadata["filename"]),
                "chunk_index": int(metadata["chunk_index"]),
                "score": score,
                "distance": round(distance_value, 4),
                "text": doc_text,
            }
        )

    return parsed_results