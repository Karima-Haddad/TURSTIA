from fastapi import APIRouter
from schemas.application_package import ApplicationPackage
from agents.document_agent import process_documents

router = APIRouter()

@router.post("/submit-application")
def submit_application(payload: ApplicationPackage):
    doc_results = process_documents(
        case_id=payload.case_id,
        documents=payload.documents
    )

    return {
        "case_id": payload.case_id,
        "doc_results": doc_results
    }
