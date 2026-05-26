from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FilePair:
    stem: str
    pdf_path: Path
    md_path: Path


@dataclass
class PageText:
    page_number: int
    text: str


@dataclass
class TableData:
    """Normalised table representation used for TEDS comparison."""
    rows: list[list[str]]           # row-major cell text
    col_spans: list[list[int]]      # colspan per cell
    row_spans: list[list[int]]      # rowspan per cell


@dataclass
class Heading:
    level: int      # 1–6 (H1–H6)
    text: str


@dataclass
class ListItem:
    depth: int          # nesting depth, 0-indexed
    ordered: bool       # True = ordered list, False = unordered
    text: str


@dataclass
class TextScore:
    semantic_similarity: float  # cosine similarity via sentence-transformers [0, 1]
    rouge_l: float              # ROUGE-L F1 [0, 1]
    coverage_ratio: float       # len(md_text) / len(pdf_text)


@dataclass
class TableScore:
    teds: float                 # Tree Edit Distance Similarity [0, 1]
    table_count_pdf: int        # number of tables detected in PDF
    table_count_md: int         # number of tables detected in MD


@dataclass
class HeadingScore:
    precision: float            # matched headings / md headings
    recall: float               # matched headings / pdf headings
    level_accuracy: float       # headings with correct H-level / matched headings


@dataclass
class ListScore:
    f1: float                   # harmonic mean of list-item precision and recall
    depth_accuracy: float       # list items with correct nesting depth / matched items


@dataclass
class Score:
    text: TextScore
    table: TableScore
    heading: HeadingScore
    list: ListScore


@dataclass
class Issue:
    severity: str   # "warning" | "error"
    message: str


@dataclass
class PairResult:
    pair: FilePair
    score: Score
    issues: list[Issue] = field(default_factory=list)
