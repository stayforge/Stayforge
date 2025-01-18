"""
document tools
"""
from pathlib import Path

import settings


def read_document(doc_path: str | Path):
    with open(settings.DOCS_API_DESCRIPTION / doc_path, "r", encoding="utf-8") as file:
        document_content = file.read()
    return document_content
