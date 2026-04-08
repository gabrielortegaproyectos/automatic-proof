"""Detect likely block types from Markdown headings.

A heading block produced by the ingestion layer carries a ``title`` string
such as ``"Definition 2.1."`` or ``"3 Inexact Catching-Up Algorithm"``.
This module inspects that title and maps it to a ``BlockKind`` value so the
block classifier can annotate the block without touching the raw text.
"""

from __future__ import annotations

import re

from article2lean.models.enums import BlockKind


# Matches a heading that starts with a known mathematical keyword optionally
# followed by a numeric label (e.g. "2.1", "3").  A trailing period is
# allowed but not required.
#
# Examples that match:
#   "Definition 2.1."  → keyword="Definition", label="2.1"
#   "Theorem 3"        → keyword="Theorem",    label="3"
#   "Proof."           → keyword="Proof",       label=None
#   "Proof"            → keyword="Proof",       label=None
_HEADING_MATH_PATTERN = re.compile(
    r"^(?P<keyword>Definition|Theorem|Lemma|Proposition|Corollary|Remark|"
    r"Example|Proof|Observation|Claim|Conjecture)"
    r"(?:\s+(?P<label>\d+(?:\.\d+)*))?"
    r"\s*\.?\s*$",
    re.IGNORECASE,
)

_KEYWORD_TO_KIND: dict[str, BlockKind] = {
    "definition": BlockKind.DEFINITION,
    "theorem": BlockKind.THEOREM,
    "lemma": BlockKind.LEMMA,
    "proposition": BlockKind.PROPOSITION,
    "corollary": BlockKind.COROLLARY,
    "remark": BlockKind.REMARK,
    "example": BlockKind.EXAMPLE,
    "proof": BlockKind.PROOF,
    "observation": BlockKind.OBSERVATION,
    "claim": BlockKind.CLAIM,
    "conjecture": BlockKind.CONJECTURE,
}


def classify_heading(heading_title: str) -> tuple[BlockKind, str | None]:
    """Return the mathematical kind and optional label for *heading_title*.

    Parameters
    ----------
    heading_title:
        The title extracted from a ``heading`` block (e.g. ``"Lemma 2.4."``).

    Returns
    -------
    tuple[BlockKind, str | None]
        A pair ``(kind, label)`` where *kind* is ``BlockKind.HEADING`` when
        no mathematical keyword is found, and *label* is the numeric
        identifier extracted from the heading (e.g. ``"2.4"``) or ``None``.
    """
    if not heading_title:
        return BlockKind.HEADING, None

    match = _HEADING_MATH_PATTERN.match(heading_title.strip())
    if match:
        keyword = match.group("keyword").lower()
        label = match.group("label")
        kind = _KEYWORD_TO_KIND.get(keyword, BlockKind.UNKNOWN)
        return kind, label

    return BlockKind.HEADING, None
