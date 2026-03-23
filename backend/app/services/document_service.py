from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import Document, DocumentChunk
from app.utils.file_parser import parse_txt_bytes
from app.utils.text_chunker import chunk_text


def validate_document_upload(upload_file: UploadFile) -> None:
    filename = upload_file.filename or ""

    if not filename.lower().endswith(".txt"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .txt uploads are supported in this MVP",
        )


def save_uploaded_file(upload_file: UploadFile, file_bytes: bytes) -> tuple[str, str]:
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    original_filename = upload_file.filename or "uploaded.txt"
    safe_name = original_filename.replace(" ", "_")
    stored_filename = f"{uuid4().hex}_{safe_name}"
    file_path = upload_dir / stored_filename

    file_path.write_bytes(file_bytes)

    return stored_filename, str(file_path)


def create_document_record(
    db: Session,
    uploaded_by: int,
    original_filename: str,
    stored_filename: str,
    file_path: str,
    mime_type: str | None,
    file_size_bytes: int,
) -> Document:
    document = Document(
        uploaded_by=uploaded_by,
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_path=file_path,
        mime_type=mime_type,
        file_size_bytes=file_size_bytes,
        total_chunks=0,
        upload_status="processing",
    )
    db.add(document)
    db.flush()
    return document


def ingest_document_chunks(db: Session, document: Document, text: str) -> int:
    chunks = chunk_text(text=text, chunk_size=800, overlap=100)

    for index, chunk in enumerate(chunks):
        vector_id = f"doc_{document.id}_chunk_{index}"

        row = DocumentChunk(
            document_id=document.id,
            chunk_index=index,
            chunk_text=chunk,
            vector_id=vector_id,
        )
        db.add(row)

    db.flush()

    document.total_chunks = len(chunks)
    document.upload_status = "processing"
    db.add(document)
    db.flush()

    return len(chunks)


def get_document_by_id(db: Session, document_id: int) -> Document | None:
    stmt = select(Document).where(Document.id == document_id)
    return db.execute(stmt).scalars().first()


def get_document_chunks(db: Session, document_id: int) -> list[DocumentChunk]:
    stmt = (
        select(DocumentChunk)
        .where(DocumentChunk.document_id == document_id)
        .order_by(DocumentChunk.chunk_index.asc())
    )
    return db.execute(stmt).scalars().all()


def process_uploaded_document(
    db: Session,
    uploaded_by: int,
    upload_file: UploadFile,
) -> Document:
    validate_document_upload(upload_file)

    file_bytes = upload_file.file.read()
    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty",
        )

    text = parse_txt_bytes(file_bytes)
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded text file contains no usable content",
        )

    stored_filename, file_path = save_uploaded_file(upload_file, file_bytes)

    document = create_document_record(
        db=db,
        uploaded_by=uploaded_by,
        original_filename=upload_file.filename or "uploaded.txt",
        stored_filename=stored_filename,
        file_path=file_path,
        mime_type=upload_file.content_type,
        file_size_bytes=len(file_bytes),
    )

    ingest_document_chunks(db=db, document=document, text=text)
    return document