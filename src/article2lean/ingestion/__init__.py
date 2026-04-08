"""Document ingestion package for raw source loading and normalization."""

from article2lean.ingestion.markdown_loader import (
    load_markdown_file,
    parse_markdown_text,
)

__all__ = ["load_markdown_file", "parse_markdown_text"]
