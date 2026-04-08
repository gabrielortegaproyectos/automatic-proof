"""Detect likely block types from inline labels such as 'Lemma' or 'Proof'.

Some mathematical documents do not use headings to introduce results.
Instead they open a paragraph with a label like ``"Proposition 3.1."`` or
``"**Theorem 2.3**"``.  This module detects such patterns at the start of a
block's raw text and maps them to ``BlockKind`` values.
"""

from __future__ import annotations

import re

from article2lean.models.enums import BlockKind


# Matches an inline mathematical label at the *start* of a text block.
#
# The pattern accepts:
#   • an optional Markdown emphasis marker: single or double asterisk/underscore
#     (``*``, ``**``, ``_``, ``__``).  We match 1–2 repetitions intentionally
#     so that both italic (``*…*``) and bold (``**…**``) styles are handled.
#     Symmetry between opening and closing markers is not enforced because we
#     only need to detect the keyword; we do not need to validate Markdown.
#   • a keyword from the recognised vocabulary
#   • an optional numeric label (e.g. ``3.1``, ``2``)
#   • an optional closing emphasis marker (same lenient matching as above)
#   • optional trailing punctuation (period or colon)
#
# Examples that match:
#   "**Lemma 3.1**"      → keyword="Lemma",       label="3.1"
#   "*Proposition 3.1*"  → keyword="Proposition",  label="3.1"
#   "Proposition 3.1."   → keyword="Proposition",  label="3.1"
#   "Theorem 3.2."       → keyword="Theorem",      label="3.2"
#   "Proof."             → keyword="Proof",         label=None
#   "Proof. Fix x ∈ H"  → keyword="Proof",         label=None
_INLINE_LABEL_PATTERN = re.compile(
    r"^(?:\*{1,2}|_{1,2})?"
    r"(?P<keyword>Definition|Theorem|Lemma|Proposition|Corollary|Remark|"
    r"Example|Proof|Observation|Claim|Conjecture)"
    r"(?:\s+(?P<label>\d+(?:\.\d+)*))?"
    r"(?:\*{1,2}|_{1,2})?"
    r"\s*[.:]?\s*",
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


def classify_inline(text: str) -> tuple[BlockKind | None, str | None]:
    """Return ``(kind, label)`` when *text* opens with a mathematical label.

    Parameters
    ----------
    text:
        The raw text of a paragraph block.

    Returns
    -------
    tuple[BlockKind | None, str | None]
        ``(kind, label)`` when a mathematical keyword is found at the start
        of *text*; ``(None, None)`` otherwise.
    """
    if not text:
        return None, None

    match = _INLINE_LABEL_PATTERN.match(text.strip())
    if not match:
        return None, None

    keyword = match.group("keyword").lower()
    label = match.group("label")
    kind = _KEYWORD_TO_KIND.get(keyword)
    return kind, label
