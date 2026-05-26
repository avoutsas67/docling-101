from pathlib import Path

import click

from .extractor import (
    extract_md_headings,
    extract_md_list_items,
    extract_md_tables,
    extract_md_text,
    extract_pdf_headings,
    extract_pdf_list_items,
    extract_pdf_tables,
    extract_pdf_text,
)
from .loader import find_pairs, validate_dirs
from .models import Issue, PairResult
from .reporter import generate_report
from .scorer import score_pair


@click.command()
@click.argument("pdf_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.argument("md_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option(
    "--output", "-o",
    type=click.Path(dir_okay=False, path_type=Path),
    default=None,
    help="Write CSV report to this path (prints to stdout if omitted).",
)
@click.option(
    "--threshold", "-t",
    type=float,
    default=0.8,
    show_default=True,
    help="Semantic similarity score below which a pair is flagged as a warning.",
)
def main(
    pdf_dir: Path,
    md_dir: Path,
    output: Path | None,
    threshold: float,
) -> None:
    """Compare PDF files in PDF_DIR against converted markdown files in MD_DIR.

    Files are matched by stem (e.g. report.pdf ↔ report.md).
    Unmatched files are skipped with a warning.
    """
    validate_dirs(pdf_dir, md_dir)
    pairs = find_pairs(pdf_dir, md_dir)

    results: list[PairResult] = []

    for pair in pairs:
        pdf_text = extract_pdf_text(pair.pdf_path)
        md_text = extract_md_text(pair.md_path)

        pdf_tables = extract_pdf_tables(pair.pdf_path)
        md_tables = extract_md_tables(pair.md_path)

        pdf_headings = extract_pdf_headings(pair.pdf_path)
        md_headings = extract_md_headings(pair.md_path)

        pdf_list_items = extract_pdf_list_items(pair.pdf_path)
        md_list_items = extract_md_list_items(pair.md_path)

        score = score_pair(
            pdf_text=pdf_text,
            md_text=md_text,
            pdf_tables=pdf_tables,
            md_tables=md_tables,
            pdf_headings=pdf_headings,
            md_headings=md_headings,
            pdf_list_items=pdf_list_items,
            md_list_items=md_list_items,
        )

        issues: list[Issue] = []
        if score.text.semantic_similarity < threshold:
            issues.append(Issue(
                severity="warning",
                message=f"Semantic similarity {score.text.semantic_similarity:.2f} is below threshold {threshold}",
            ))

        results.append(PairResult(pair=pair, score=score, issues=issues))

    generate_report(results, output_path=output)
