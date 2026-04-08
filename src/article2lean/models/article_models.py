"""Domain models used by the article-oriented ingestion pipeline.

The project will eventually grow richer article models for segmentation,
reference resolution, and formalization. For Tarea 02 we only need the first
pedagogical layer: a document and its raw Markdown blocks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ArticleBlock:
    """Represent one raw block extracted from a Markdown source.

    The ingestion layer keeps this model intentionally simple. It records what
    kind of block we found, the raw text that produced it, and enough metadata
    to navigate the document before any mathematical classification happens.
    """

    block_id: str
    block_type: str
    raw_text: str
    title: str | None = None
    label: str | None = None
    section_path: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
    proof_for: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class MarkdownDocument:
    """Hold the raw Markdown text plus its navigable block structure."""

    source_path: str | None = None
    raw_text: str = ""
    blocks: list[ArticleBlock] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
