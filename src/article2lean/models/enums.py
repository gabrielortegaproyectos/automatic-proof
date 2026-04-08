"""Enumerations shared across the domain model layer."""

from __future__ import annotations

from enum import Enum


class BlockKind(str, Enum):
    """Classification of an ``ArticleBlock`` by its mathematical role.

    Blocks produced by the ingestion layer initially carry a structural type
    (``heading``, ``paragraph``, ``list``).  The segmentation layer refines
    these into semantic roles so the rest of the pipeline can reason about the
    *meaning* of each block rather than its raw Markdown shape.
    """

    DEFINITION = "definition"
    THEOREM = "theorem"
    LEMMA = "lemma"
    PROPOSITION = "proposition"
    COROLLARY = "corollary"
    REMARK = "remark"
    EXAMPLE = "example"
    PROOF = "proof"
    OBSERVATION = "observation"
    CLAIM = "claim"
    CONJECTURE = "conjecture"
    SECTION = "section"
    PARAGRAPH = "paragraph"
    LIST = "list"
    HEADING = "heading"
    UNKNOWN = "unknown"

