from sqlalchemy import select

import app.models  # noqa: F401
from app.db.session import SessionLocal
from app.models import Document
from app.services.document_service import get_document_chunks
from app.services.embedding_service import index_document_chunks


def main():
    db = SessionLocal()
    try:
        documents = db.execute(select(Document)).scalars().all()

        for document in documents:
            chunks = get_document_chunks(db=db, document_id=document.id)

            if not chunks:
                print(f"Skipping document {document.id}: no chunks found")
                continue

            try:
                index_document_chunks(document=document, chunks=chunks) 
                document.upload_status = "ready"
                db.add(document)
                db.commit()
                print(
                    f"Indexed document {document.id} "
                    f"({document.original_filename}) with {len(chunks)} chunks"
                )
            except Exception as exc:
                document.upload_status = "failed"
                db.add(document)
                db.commit()
                print(f"Failed indexing document {document.id}: {exc}")

    finally:
        db.close()


if __name__ == "__main__":
    main()