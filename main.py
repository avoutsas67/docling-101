import json
from pathlib import Path
from urllib.parse import unquote

import requests
import torch
from docling.document_converter import DocumentConverter
from playwright.sync_api import sync_playwright

PATH_DOCUMENTS = Path("./documents")
PATH_SOURCE = PATH_DOCUMENTS / "source"
PATH_TARGET = PATH_DOCUMENTS / "target"
PATH_TARGET_NATIVE = PATH_TARGET / "native"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
}

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


def load_acts(file_name: str) -> dict[str, dict[str, str]]:
    acts_path = Path(file_name)
    with acts_path.open(encoding="utf-8") as f:
        return json.load(f)


def download_pdf_playwright(url: str, output_path: Path):
    target_path = None
    assert output_path.parent.exists()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Intercept the PDF response and save it
        with page.expect_download() as download_info:
            page.goto(url, wait_until="networkidle", timeout=30000)

        download = download_info.value
        download.save_as(output_path)
        print(f"✓ Saved to {output_path}")
        browser.close()

        target_path = output_path
    return target_path


def resolve_source(doc_uris: dict) -> tuple[Path, str]:
    if "file" in doc_uris:
        path = Path(doc_uris["file"])
        assert path.exists()
        return path, path.name + ".md"

    url = unquote(doc_uris["url"])
    file_stem = url.split(":")[-1]
    doc_location = PATH_SOURCE / (file_stem + ".pdf")
    if download_pdf_playwright(url, doc_location) is None:
        raise FileNotFoundError(f"Downloading {url} failed!")
    return doc_location, file_stem + ".pdf.md"


def main():
    if torch.backends.mps.is_available():
        print("Using Apple Silicon GPU for processing!")

    converter = DocumentConverter()

    legislative_acts = load_acts("legislative-acts.json")

    for doc_uris in legislative_acts.values():
        doc_location, file_name_target = resolve_source(doc_uris)
        result = converter.convert(doc_location)
        output_file = PATH_TARGET_NATIVE / file_name_target
        output_file.write_text(result.document.export_to_markdown())


if __name__ == "__main__":
    main()
