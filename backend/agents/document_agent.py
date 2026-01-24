import re
import os
import base64
import uuid
import tempfile
import pytesseract
from PIL import Image
from pathlib import Path
from typing import List, Dict
from services.document_parser import parse_pdf
from schemas.document_analysis import (
    DocumentAnalysisResult, Evidence, TextChunk
)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

TMP_DIR = Path("tmp_docs")
TMP_DIR.mkdir(exist_ok=True)

def extract_financials(pages: List[Dict]):
    income = None
    expenses = None
    evidences = []

    for page in pages:
        for line in page["text"]:
            if not income:
                match = re.search(r"(salary|income).*?(\d+)", line.lower())
                if match:
                    income = int(match.group(2))
                    evidences.append(
                        Evidence(
                            doc_id="D1",
                            page=page["page"],
                            lines=[line]
                        )
                    )

            if not expenses:
                match = re.search(r"(expense|debit).*?(\d+)", line.lower())
                if match:
                    expenses = int(match.group(2))
                    evidences.append(
                        Evidence(
                            doc_id="D1",
                            page=page["page"],
                            lines=[line]
                        )
                    )

    return income, expenses, evidences


def extract_contract_duration(pages: List[Dict], evidence_map: List[Evidence]):
    for page in pages:
        for line in page["text"]:
            match = re.search(r"(\d+)\s+months", line.lower())
            if match:
                evidence_map.append(
                    Evidence(
                        doc_id="D2",
                        page=page["page"],
                        lines=[line]
                    )
                )
                return int(match.group(1))
    return None


def extract_text_from_image(image_path: str) -> list[str]:
    try:
        img = Image.open(image_path)

        text = pytesseract.image_to_string(
            img,
            lang="ara+fra+eng",
            config="--psm 6"
        )

        return [line.strip() for line in text.split("\n") if line.strip()]

    except Exception as e:
        print("❌ OCR ERROR:", e)
        return []

    # on retourne une liste de lignes (comme parse_pdf)
    return [line.strip() for line in text.split("\n") if line.strip()]

def extract_cin_from_lines(lines: list[str]):
    for line in lines:
        match = re.search(r"\b\d{8}\b", line)
        if match:
            return match.group()
    return None


def run_document_agent(case_id, documents, applicant_form):
    print("📄 Documents reçus par l'agent :", documents)

    doc_signals = {}
    chunks = []
    evidence_map = []

    for doc in documents:
        if "content" not in doc:
            print(f"⚠️ Document {doc.get('doc_id')} sans content")
            continue
    
        filename = doc.get("filename", f"{uuid.uuid4()}.pdf")
        file_path = TMP_DIR / filename
        file_path.write_bytes(base64.b64decode(doc["content"]))

        # Détection PDF vs image
        if filename.lower().endswith(".pdf"):
            pages = parse_pdf(str(file_path))
        else:
            lines = extract_text_from_image(str(file_path))
            pages = [{
                "page": 1,
                "text": lines
            }]

        if doc["type"] == "BANK_STATEMENT":
            income, expenses, evidences = extract_financials(pages)
            if income is not None:
                doc_signals["detected_income"] = income

            if expenses is not None:
                doc_signals["detected_expenses"] = expenses
            
            evidence_map.extend(evidences)

            chunks.append(
                TextChunk(
                    section="BANK_STATEMENT",
                    text=" ".join(sum([p["text"] for p in pages], []))
                )
            )
        if doc["type"] == "CONTRACT":
            duration = extract_contract_duration(pages,evidence_map)
            if duration is not None:
                doc_signals["contract_duration_months"] = duration

            chunks.append(
                TextChunk(
                    section="CONTRACT",
                    text=" ".join(sum([p["text"] for p in pages], []))
                )
            )

        if doc["type"] == "ID_CARD":
            lines = extract_text_from_image(str(file_path))
            cin = extract_cin_from_lines(lines)
            if cin:
                doc_signals["cin"] = cin

                evidence_map.append(
                    Evidence(
                        doc_id="D3",
                        page=1,
                        lines=[f"CIN détecté: {cin}"]
                    )
                )
            chunks.append(
                TextChunk(
                    section="IDENTITY",
                    text=" ".join(sum([p["text"] for p in pages], []))
                )
            )

            doc_signals["id_detected"] = True



    doc_signals["documents_count"] = len(documents)

    return DocumentAnalysisResult(
        doc_signals=doc_signals,
        chunks=chunks,
        evidence_map=evidence_map
    )
