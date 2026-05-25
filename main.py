from pathlib import Path

import requests
import torch
from docling.document_converter import DocumentConverter

PATH_DOCUMENTS = Path("./documents")
PATH_SOURCE = PATH_DOCUMENTS / "source"
PATH_TARGET = PATH_DOCUMENTS / "target"
PATH_TARGET_NATIVE = PATH_TARGET / "native"

regulations_phv = {
    "726/2004": {
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32004R0726",
        "file": PATH_SOURCE / "CELEX_32004R0726_EN_TXT.pdf",
    },
    "520/2012": {
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32012R0520"
    },
    "2025/1466": {
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:L_202501466"
    },
}


def resolve_source(doc_uris: dict) -> tuple[Path, str]:
    if "file" in doc_uris:
        path = doc_uris["file"]
        return path, path.name + ".md"

    url = doc_uris["url"]
    file_stem = url.split(":")[-1]
    doc_location = PATH_SOURCE / (file_stem + ".pdf")
    response = requests.get(url)
    response.raise_for_status()
    doc_location.write_bytes(response.content)
    return doc_location, file_stem + ".pdf.md"


def main():
    if torch.backends.mps.is_available():
        print("Using Apple Silicon GPU for processing!")

    converter = DocumentConverter()

    for doc_uris in regulations_phv.values():
        doc_location, file_name_target = resolve_source(doc_uris)
        result = converter.convert(doc_location)
        output_file = PATH_TARGET_NATIVE / file_name_target
        output_file.write_text(result.document.export_to_markdown())


if __name__ == "__main__":
    main()
