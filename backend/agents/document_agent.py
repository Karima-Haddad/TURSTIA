#Règles d’extraction
import re
import os
from pathlib import Path
from typing import List, Dict
from backend.services.document_parser import parse_pdf
from backend.schemas.document_analysis import (
    DocumentAnalysisResult, Evidence, TextChunk
)

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
                            doc_id="D2",
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
                            doc_id="D2",
                            page=page["page"],
                            lines=[line]
                        )
                    )

    return income, expenses, evidences

def extract_contract_duration(pages: List[Dict]):
    for page in pages:
        for line in page["text"]:
            match = re.search(r"(\d+)\s+months", line.lower())
            if match:
                return int(match.group(1))
    return None

def run_document_agent(case_id: str, documents: List[Dict], applicant_form=None):
    doc_signals = {}
    chunks = []
    evidence_map = []

    for doc in documents:
        # retirer file:// si présent
        path_str = doc["uri"].replace("file://", "")
        path = Path(path_str)

        # Vérifier si le fichier existe
        if not path.exists():
            print(f"[WARNING] Document not found: {path}")  # log
            continue  # passer au document suivant

        if doc["type"] in ["BANK_STATEMENT", "CONTRACT"]:
            pages = parse_pdf(str(path))  # tu passes le chemin valide

            if doc["type"] == "BANK_STATEMENT":
                income, expenses, evidences = extract_financials(pages)
                doc_signals["detected_income"] = income
                doc_signals["detected_expenses"] = expenses
                evidence_map.extend(evidences)

                chunks.append(
                    TextChunk(
                        section="FINANCE",
                        text=" ".join(sum([p["text"] for p in pages], []))
                    )
                )

            elif doc["type"] == "CONTRACT":
                duration = extract_contract_duration(pages)
                doc_signals["contract_duration_months"] = duration

    return DocumentAnalysisResult(
        doc_signals=doc_signals,
        chunks=chunks,
        evidence_map=evidence_map
    )
