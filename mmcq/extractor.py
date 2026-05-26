from pathlib import Path

from .models import Heading, ListItem, PageText, TableData


# --- PDF extraction (via pdfplumber) ---

def extract_pdf_text(pdf_path: Path) -> str:
    """Return full plain text extracted from all pages of a PDF, concatenated."""
    pass


def extract_pdf_pages(pdf_path: Path) -> list[PageText]:
    """Return per-page plain text for finer-grained comparison."""
    pass


def extract_pdf_tables(pdf_path: Path) -> list[TableData]:
    """Extract all tables from a PDF in document order using pdfplumber.

    Merged cells are captured via col_spans / row_spans on TableData.
    """
    pass


def extract_pdf_headings(pdf_path: Path) -> list[Heading]:
    """Infer headings from PDF font size and boldness relative to body text.

    H-level is assigned by bucketing distinct font sizes in descending order.
    """
    pass


def extract_pdf_list_items(pdf_path: Path) -> list[ListItem]:
    """Detect list items from PDF by identifying bullet/number prefixes and indentation."""
    pass


# --- Markdown extraction (via markdown-it-py) ---

def extract_md_text(md_path: Path) -> str:
    """Parse markdown and return plain text with all markup stripped."""
    pass


def extract_md_tables(md_path: Path) -> list[TableData]:
    """Parse markdown tables into TableData structures."""
    pass


def extract_md_headings(md_path: Path) -> list[Heading]:
    """Extract ATX and Setext headings with their H-level from a markdown file."""
    pass


def extract_md_list_items(md_path: Path) -> list[ListItem]:
    """Extract list items with nesting depth and ordered/unordered flag."""
    pass
