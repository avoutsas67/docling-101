from pathlib import Path
from typing import Any

from .models import PairResult


_COLUMNS = [
    "stem",
    # text
    "text.semantic_similarity",
    "text.rouge_l",
    "text.coverage_ratio",
    # tables
    "table.teds",
    "table.table_count_pdf",
    "table.table_count_md",
    # headings
    "heading.precision",
    "heading.recall",
    "heading.level_accuracy",
    # lists
    "list.f1",
    "list.depth_accuracy",
    # issues
    "issues",
]


def _flatten(result: PairResult) -> dict:
    """Flatten a PairResult into a dict keyed by _COLUMNS."""
    pass


def print_summary(results: list[PairResult]) -> None:
    """Print a rich-formatted table with one row per file pair to stdout.

    Rows with any Issue of severity 'error' are highlighted in red;
    'warning' rows in yellow.
    """
    pass


def to_dataframe(results: list[PairResult]) -> Any:
    """Convert results to a pandas DataFrame with columns matching _COLUMNS."""
    pass


def to_csv(results: list[PairResult], output_path: Path) -> None:
    """Write per-file scores and issues to a CSV at output_path via to_dataframe."""
    pass


def generate_report(results: list[PairResult], output_path: Path | None = None) -> None:
    """Print summary table to stdout and optionally write a CSV report.

    Args:
        results:     Scored pair results from the main pipeline.
        output_path: If provided, write a CSV to this path in addition to stdout.
    """
    pass
