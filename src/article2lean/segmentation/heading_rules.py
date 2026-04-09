"""Detect likely block types from Markdown headings.

A heading block produced by the ingestion layer carries a ``title`` string
such as ``"Definition 2.1."`` or ``"3 Inexact Catching-Up Algorithm"``.
This module inspects that title and maps it to a ``BlockKind`` value so the
block classifier can annotate the block without touching the raw text.

Two classification strategies are combined:

1. **Regex** — fast exact match against a vocabulary of full English keyword
   names and common abbreviations (``Def``, ``Thm``, ``Prop``, …).
2. **Fuzzy fallback** — for headings whose first word is not caught by the
   regex, we look it up first in an explicit map of linguistic variants
   (Spanish, French, Portuguese) and then use ``difflib`` as a last resort
   to handle near-identical spellings and common typos.
"""

from __future__ import annotations

import difflib
import re

from article2lean.models.enums import BlockKind


# ---------------------------------------------------------------------------
# Regex — fast path (English full names + abbreviations)
# ---------------------------------------------------------------------------

# Matches a heading that starts with a full English keyword *or* a recognised
# abbreviation, optionally followed by a numeric label and a trailing period.
#
# Full-name examples:
#   "Definition 2.1."  → keyword="Definition", label="2.1"
#   "Theorem 3"        → keyword="Theorem",    label="3"
#   "Proof."           → keyword="Proof",       label=None
#
# Abbreviation examples (the period that follows the abbreviation itself is
# consumed by the optional `\.?` immediately after the keyword group):
#   "Def. 2.1"         → keyword="Def",        label="2.1"
#   "Def. 2.1."        → keyword="Def",        label="2.1"
#   "Thm 4.1."         → keyword="Thm",        label="4.1"
#   "Note 7."          → keyword="Note",        label="7"
_HEADING_MATH_PATTERN = re.compile(
    r"^(?P<keyword>"
    # Full English names
    r"Definition|Theorem|Lemma|Proposition|Corollary|Remark|"
    r"Example|Proof|Observation|Claim|Conjecture|Notation|Note|"
    # Common abbreviations (period handled by the \.? below)
    r"Def|Thm|Prop|Lem|Cor|Rem|Obs|Conj"
    r")"
    r"\.?"                               # optional period right after abbreviation
    r"(?:\s+(?P<label>\d+(?:\.\d+)*))?"  # optional numeric label
    r"\s*\.?\s*$",                        # optional trailing period
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Normalization — abbreviations, aliases and linguistic variants
# ---------------------------------------------------------------------------

# Map any abbreviated or non-English form to the corresponding canonical
# English keyword so that ``_KEYWORD_TO_KIND`` can always do a simple lookup.
_NORMALIZE: dict[str, str] = {
    # Abbreviations
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
    # Spanish
    "definicion": "definition",
    "definición": "definition",
    "teorema": "theorem",
    "lema": "lemma",
    "proposicion": "proposition",
    "proposición": "proposition",
    "corolario": "corollary",
    "observacion": "observation",
    "observación": "observation",
    "demostracion": "proof",
    "demostración": "proof",
    "prueba": "proof",
    "ejemplo": "example",
    "conjetura": "conjecture",
    # French
    "définition": "definition",
    "theoreme": "theorem",
    "théorème": "theorem",
    "lemme": "lemma",
    "corollaire": "corollary",
    "remarque": "remark",
    "preuve": "proof",
    "demonstration": "proof",
    "démonstration": "proof",
    "exemple": "example",
    # Portuguese
    "definicao": "definition",
    "definição": "definition",
    "proposicao": "proposition",
    "proposição": "proposition",
    "observacao": "observation",
    "observação": "observation",
    "prova": "proof",
    "demonstracao": "proof",
    "demonstração": "proof",
    "corolario": "corollary",
    "exemplo": "example",
    "conjectura": "conjecture",
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

# Pre-built list for difflib — only canonical English names.
_ALL_CANONICAL_KEYWORDS: list[str] = list(_KEYWORD_TO_KIND.keys())


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


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

    title = heading_title.strip()

    # --- Fast path: regex on known English names and abbreviations ----------
    match = _HEADING_MATH_PATTERN.match(title)
    if match:
        raw_keyword = match.group("keyword").lower()
        canonical = _NORMALIZE.get(raw_keyword, raw_keyword)
        label = match.group("label")
        kind = _KEYWORD_TO_KIND.get(canonical, BlockKind.UNKNOWN)
        return kind, label

    # --- Slow path: fuzzy match on the first word ---------------------------
    kind = _fuzzy_match_first_word(title)
    if kind is not None:
        return kind, None

    return BlockKind.HEADING, None


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _fuzzy_match_first_word(title: str) -> BlockKind | None:
    """Return the most likely ``BlockKind`` for the first word of *title*.

    The function first checks the explicit ``_NORMALIZE`` map which covers
    linguistic variants and abbreviations that fall outside the main regex.
    If that fails it uses ``difflib.get_close_matches`` as a last resort to
    catch typos and near-identical spellings (e.g. ``"Theoreme"``).
    """
    words = title.split()
    if not words:
        return None

    first_word = words[0].rstrip(".:,;").lower()

    # Explicit variant map (fastest, most reliable)
    canonical = _NORMALIZE.get(first_word)
    if canonical:
        return _KEYWORD_TO_KIND.get(canonical)

    # difflib fallback — only worth calling for words at least 4 chars long
    # to avoid false positives on short tokens.
    if len(first_word) >= 4:
        candidates = difflib.get_close_matches(
            first_word, _ALL_CANONICAL_KEYWORDS, n=1, cutoff=0.75
        )
        if candidates:
            return _KEYWORD_TO_KIND.get(candidates[0])

    return None
