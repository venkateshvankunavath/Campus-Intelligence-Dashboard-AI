"""RAG router: upload a PDF into ChromaDB and ask document questions."""
import os
import tempfile

from fastapi import APIRouter, Depends, File, UploadFile
from pydantic import BaseModel

from app.auth.security import get_current_user
from app.models import Student
from app.services.rag_service import get_rag, tool_search_documents

router = APIRouter(prefix="/rag", tags=["RAG / Documents"])


class DocQuery(BaseModel):
    query: str


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...), user: Student = Depends(get_current_user)
):
    suffix = os.path.splitext(file.filename or "doc.pdf")[1] or ".pdf"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    try:
        result = get_rag().ingest_pdf(tmp_path, doc_name=file.filename or "document")
    finally:
        os.unlink(tmp_path)
    return result


@router.post("/query")
def query_documents(payload: DocQuery):
    return {"answer": tool_search_documents(payload.query)}
