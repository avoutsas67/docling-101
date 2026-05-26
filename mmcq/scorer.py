from .models import (
    Heading,
    HeadingScore,
    ListItem,
    ListScore,
    Score,
    TableData,
    TableScore,
    TextScore,
)


# --- Text ---

def compute_semantic_similarity(reference: str, candidate: str) -> float:
    """Return cosine similarity [0, 1] between sentence-transformer embeddings."""
    pass


def compute_rouge_l(reference: str, candidate: str) -> float:
    """Return ROUGE-L F1 score [0, 1] measuring longest common subsequence recall."""
    pass


def compute_coverage_ratio(pdf_text: str, md_text: str) -> float:
    """Return ratio of md character count to pdf character count."""
    pass


def score_text(pdf_text: str, md_text: str) -> TextScore:
    """Compute semantic similarity, ROUGE-L, and coverage ratio."""
    pass


# --- Tables ---

def compute_teds(pdf_table: TableData, md_table: TableData) -> float:
    """Return TEDS score [0, 1] comparing table tree structures via edit distance."""
    pass


def score_tables(pdf_tables: list[TableData], md_tables: list[TableData]) -> TableScore:
    """Pair tables by position, compute mean TEDS, and record table counts."""
    pass


# --- Headings ---

def compute_heading_precision_recall(
    pdf_headings: list[Heading], md_headings: list[Heading]
) -> tuple[float, float]:
    """Return (precision, recall) for heading text matches (case-insensitive)."""
    pass


def compute_heading_level_accuracy(
    pdf_headings: list[Heading], md_headings: list[Heading]
) -> float:
    """Return fraction of matched headings where the H-level is also correct."""
    pass


def score_headings(
    pdf_headings: list[Heading], md_headings: list[Heading]
) -> HeadingScore:
    """Compute precision, recall, and level accuracy for document headings."""
    pass


# --- Lists ---

def compute_list_f1(
    pdf_items: list[ListItem], md_items: list[ListItem]
) -> float:
    """Return F1 score over list item text matches."""
    pass


def compute_list_depth_accuracy(
    pdf_items: list[ListItem], md_items: list[ListItem]
) -> float:
    """Return fraction of matched list items with correct nesting depth."""
    pass


def score_lists(
    pdf_items: list[ListItem], md_items: list[ListItem]
) -> ListScore:
    """Compute F1 and depth accuracy for list items."""
    pass


# --- Aggregate ---

def score_pair(
    pdf_text: str,
    md_text: str,
    pdf_tables: list[TableData],
    md_tables: list[TableData],
    pdf_headings: list[Heading],
    md_headings: list[Heading],
    pdf_list_items: list[ListItem],
    md_list_items: list[ListItem],
) -> Score:
    """Compute all metric dimensions for a single PDF/MD pair and return a Score."""
    pass
