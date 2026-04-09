"""Combine segmentation rules into a single block classification decision.

The ingestion layer produces ``ArticleBlock`` objects that only know their
structural type (``heading``, ``paragraph``, ``list``).  This module applies
the heading and inline-label rules to produce semantically classified blocks
whose ``block_type`` reflects the *mathematical* role of each block
(``theorem``, ``proof``, ``definition``, …).

The original blocks are never mutated; new instances are returned instead.
"""

from __future__ import annotations

from dataclasses import replace

from article2lean.models import ArticleBlock, MarkdownDocument
from article2lean.models.enums import BlockKind
from article2lean.segmentation.heading_rules import classify_heading
from article2lean.segmentation.inline_label_rules import classify_inline


def classify_blocks(document: MarkdownDocument) -> list[ArticleBlock]:
    """Return a new block list with mathematical types applied to each block.

    The function applies two classification strategies in order:

    1. **Heading rule** – heading blocks whose title matches a known
       mathematical keyword (e.g. ``"Theorem 3.2."``) are reclassified to
       the corresponding ``BlockKind`` value and have their ``label``
       attribute set to the extracted numeric identifier.

    2. **Inline-label rule** – paragraph blocks whose raw text begins with
       a mathematical label (e.g. ``"Proposition 3.1. Let …"``) are
       reclassified in the same way.

    Blocks that carry no detectable mathematical role are returned unchanged.

    Parameters
    ----------
    document:
        A ``MarkdownDocument`` produced by the ingestion layer.

    Returns
    -------
    list[ArticleBlock]
        A new list of ``ArticleBlock`` objects.  Each block is a fresh copy
        with potentially updated ``block_type`` and ``label`` fields.
    """
    classified: list[ArticleBlock] = []

    for block in document.blocks:
        updated = _classify_single_block(block)
        classified.append(updated)

    return classified


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _classify_single_block(block: ArticleBlock) -> ArticleBlock:
    """Apply classification rules to one block and return the updated copy."""

    if block.block_type == "heading" and block.title is not None:
        kind, label = classify_heading(block.title)
        if kind not in (BlockKind.HEADING, BlockKind.UNKNOWN):
            return replace(block, block_type=kind.value, label=label)

    elif block.block_type == "paragraph":
        kind, label = classify_inline(block.raw_text)
        if kind is not None:
            return replace(block, block_type=kind.value, label=label)

    return block
