from pathlib import Path

from .models import FilePair


def validate_dirs(pdf_dir: Path, md_dir: Path) -> None:
    """Raise ValueError if either directory does not exist or is not a directory."""
    pass


def find_pairs(pdf_dir: Path, md_dir: Path) -> list[FilePair]:
    """Match PDF and MD files by stem and return paired entries.

    Files without a counterpart in the other directory are silently skipped.
    Call validate_dirs before this function.
    """
    pass
