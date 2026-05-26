from .loader import find_pairs, validate_dirs
from .extractor import extract_pdf_text, extract_md_text
from .scorer import score_pair
from .reporter import generate_report
from .models import FilePair, Score, PairResult

__all__ = [
    "find_pairs",
    "validate_dirs",
    "extract_pdf_text",
    "extract_md_text",
    "score_pair",
    "generate_report",
    "FilePair",
    "Score",
    "PairResult",
]
