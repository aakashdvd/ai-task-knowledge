from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uploaded_by: int
    original_filename: str
    stored_filename: str
    file_path: str
    mime_type: str | None
    file_size_bytes: int | None
    total_chunks: int
    upload_status: str
    created_at: datetime
    updated_at: datetime


class DocumentChunkOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    document_id: int
    chunk_index: int
    chunk_text: str
    vector_id: str
    created_at: datetime


class DocumentDetailOut(DocumentOut):
    chunks: list[DocumentChunkOut]