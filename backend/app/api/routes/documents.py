from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_admin
from app.models import Document, User
from app.schemas.document import DocumentChunkOut, DocumentDetailOut, DocumentOut
from app.services.document_service import (
    get_document_by_id,
    get_document_chunks,
    process_uploaded_document,
)
from app.services.embedding_service import index_document_chunks
from app.services.logging_service import create_activity_log

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    document = process_uploaded_document(
        db=db,
        uploaded_by=admin_user.id,
        upload_file=file,
    )

    chunks = get_document_chunks(db=db, document_id=document.id)

    try:
        index_document_chunks(document=document, chunks=chunks)
        document.upload_status = "ready"
    except Exception as exc:
        document.upload_status = "failed"
        db.add(document)
        db.commit()
        raise HTTPException(
            status_code=500,
            detail=f"Document uploaded but vector indexing failed: {str(exc)}",
        ) from exc

    create_activity_log(
        db=db,
        user_id=admin_user.id,
        action="DOCUMENT_UPLOAD",
        entity_type="document",
        entity_id=document.id,
        details={
            "original_filename": document.original_filename,
            "stored_filename": document.stored_filename,
            "total_chunks": document.total_chunks,
            "upload_status": document.upload_status,
        },
    )

    db.add(document)
    db.commit()
    db.refresh(document)
    return document


@router.get("", response_model=list[DocumentOut])
def list_documents(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    stmt = select(Document).order_by(Document.created_at.desc())
    documents = db.execute(stmt).scalars().all()
    return documents


@router.get("/{document_id}", response_model=DocumentDetailOut)
def get_document_detail(
    document_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    document = get_document_by_id(db=db, document_id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    chunks = get_document_chunks(db=db, document_id=document_id)

    return DocumentDetailOut(
        id=document.id,
        uploaded_by=document.uploaded_by,
        original_filename=document.original_filename,
        stored_filename=document.stored_filename,
        file_path=document.file_path,
        mime_type=document.mime_type,
        file_size_bytes=document.file_size_bytes,
        total_chunks=document.total_chunks,
        upload_status=document.upload_status,
        created_at=document.created_at,
        updated_at=document.updated_at,
        chunks=[
            DocumentChunkOut.model_validate(chunk)
            for chunk in chunks
        ],
    )