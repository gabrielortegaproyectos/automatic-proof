"""Detect likely block types from inline labels such as 'Lemma' or 'Proof'.

Some mathematical documents do not use headings to introduce results.
Instead they open a paragraph with a label like ``"Proposition 3.1."`` or
``"**Theorem 2.3**"``.  This module detects such patterns at the start of a
block's raw text and maps them to ``BlockKind`` values.

The pattern accepts full English keyword names as well as common abbreviations
(``Def``, ``Thm``, ``Prop``, ``Lem``, ``Cor``, ``Rem``, ``Obs``, ``Conj``)
so that documents that use shorthand notation are handled naturally.
"""

from __future__ import annotations

import re

from article2lean.models.enums import BlockKind


# ---------------------------------------------------------------------------
# Regex
# ---------------------------------------------------------------------------

# Matches an inline mathematical label at the *start* of a text block.
#
# The pattern accepts:
#   • an optional Markdown emphasis marker (``*``, ``**``, ``_``, ``__``)
#   • a keyword (full name or abbreviation)
#   • an optional period right after an abbreviation (``Thm. 4.1``)
#   • an optional numeric label
#   • an optional closing emphasis marker
#   • optional trailing punctuation
#
# Full-name examples:
#   "**Lemma 3.1**"              → keyword="Lemma",       label="3.1"
#   "*Proposition 3.1*"          → keyword="Proposition",  label="3.1"
#   "Theorem 3.2. Assume …"      → keyword="Theorem",      label="3.2"
#   "Proof. Fix x ∈ H"           → keyword="Proof",         label=None
#
# Abbreviation examples:
#   "Thm. 4.1 …"                 → keyword="Thm",         label="4.1"
#   "Def. 2.3 Let S be …"        → keyword="Def",         label="2.3"
_INLINE_LABEL_PATTERN = re.compile(
    r"^(?:\*{1,2}|_{1,2})?"
    r"(?P<keyword>"
    # Full English names
    r"Definition|Theorem|Lemma|Proposition|Corollary|Remark|"
    r"Example|Proof|Observation|Claim|Conjecture|Notation|Note|"
    # Common abbreviations
    r"Def|Thm|Prop|Lem|Cor|Rem|Obs|Conj"
    r")"
    r"\.?"                               # optional period right after abbreviation
    r"(?:\s+(?P<label>\d+(?:\.\d+)*))?"  # optional numeric label
    r"(?:\*{1,2}|_{1,2})?"
    r"\s*[.:]?\s*",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Normalization — abbreviations and aliases
# ---------------------------------------------------------------------------

# Maps abbreviated or alias forms to the canonical English keyword so that
# ``_KEYWORD_TO_KIND`` can always do a simple lookup.
_NORMALIZE: dict[str, str] = {
    "def": "definition",
    "thm": "theorem",
    "prop": "proposition",
    "lem": "lemma",
    "cor": "corollary",
    "rem": "remark",
    "obs": "observation",
    "conj": "conjecture",
    "note": "remark",
    "notation": "remark",
}

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


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


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

    raw_keyword = match.group("keyword").lower()
    canonical = _NORMALIZE.get(raw_keyword, raw_keyword)
    label = match.group("label")
    kind = _KEYWORD_TO_KIND.get(canonical)
    return kind, label
