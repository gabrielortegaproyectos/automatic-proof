"""Tests for the rule-based mathematical segmentation layer (Tarea 03).

The segmentation layer takes ``ArticleBlock`` objects produced by the ingestion
layer and annotates them with mathematical roles (theorem, lemma, proof, …).
These tests exercise each rule independently as well as the combined
``classify_blocks`` pipeline.

Test cases are drawn from three sources:
* synthetic inputs that exercise edge cases
* exact heading titles and paragraph openings taken from the real fixture
  ``garrido2025inexact.md`` (one test group per paper section)
* abbreviation and fuzzy/linguistic-variant inputs that exercise the flexible
  matching layer added in Tarea 03
"""

from __future__ import annotations

from pathlib import Path

import pytest

from article2lean.ingestion import load_markdown_file, parse_markdown_text
from article2lean.models.enums import BlockKind
from article2lean.segmentation import classify_blocks, classify_heading, classify_inline


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "garrido2025inexact.md"


# ===========================================================================
# classify_heading — basic keyword recognition
# ===========================================================================


@pytest.mark.parametrize(
    "title, expected_kind, expected_label",
    [
        # --- full English names, exact spelling ---
        ("Definition 2.1.", BlockKind.DEFINITION, "2.1"),
        ("Theorem 3.2.", BlockKind.THEOREM, "3.2"),
        ("Lemma 4", BlockKind.LEMMA, "4"),
        ("Proposition 2.2.", BlockKind.PROPOSITION, "2.2"),
        ("Corollary 5.1", BlockKind.COROLLARY, "5.1"),
        ("Remark 3", BlockKind.REMARK, "3"),
        ("Example 1.2", BlockKind.EXAMPLE, "1.2"),
        ("Proof.", BlockKind.PROOF, None),
        ("Proof", BlockKind.PROOF, None),
        ("Observation 2", BlockKind.OBSERVATION, "2"),
        ("Claim 1", BlockKind.CLAIM, "1"),
        ("Conjecture 3", BlockKind.CONJECTURE, "3"),
    ],
)
def test_classify_heading_recognises_full_english_keywords(
    title: str, expected_kind: BlockKind, expected_label: str | None
) -> None:
    """Verify that full English keywords are classified correctly."""

    kind, label = classify_heading(title)
    assert kind == expected_kind
    assert label == expected_label


# ===========================================================================
# classify_heading — headings extracted directly from the fixture
# ===========================================================================


@pytest.mark.parametrize(
    "title, expected_kind, expected_label",
    [
        # Section 2: Mathematical Preliminaries (p. 3–4)
        ("Definition 2.1.", BlockKind.DEFINITION, "2.1"),
        ("Proposition 2.2.", BlockKind.PROPOSITION, "2.2"),
        ("Definition 2.3.", BlockKind.DEFINITION, "2.3"),
        # Section 2 continues — numbered results without keyword (p. 5)
        # These cannot be classified by keyword, so they stay as HEADING.
        # (See test_classify_heading_returns_heading_for_numbered_only_titles)
        # Section 2 continued (p. 6)
        ("Proposition 2.9.", BlockKind.PROPOSITION, "2.9"),
        ("Proof.", BlockKind.PROOF, None),
        # Section 4: Prox-Regular Moving Sets
        ("Theorem 4.1.", BlockKind.THEOREM, "4.1"),
        # Section 5: Uniformly Subsmooth Moving Sets
        ("Theorem 5.1.", BlockKind.THEOREM, "5.1"),
        # Section 6: Fixed Set
        ("Theorem 6.1.", BlockKind.THEOREM, "6.1"),
        # Section 7: Application
        ("Remark 7.1.", BlockKind.REMARK, "7.1"),
        ("Lemma 7.2.", BlockKind.LEMMA, "7.2"),
        ("Example 7.3.", BlockKind.EXAMPLE, "7.3"),
    ],
)
def test_classify_heading_fixture_math_headings(
    title: str, expected_kind: BlockKind, expected_label: str | None
) -> None:
    """Verify that every math heading in the fixture is classified correctly."""

    kind, label = classify_heading(title)
    assert kind == expected_kind
    assert label == expected_label


@pytest.mark.parametrize(
    "title",
    [
        # Section headings from the fixture
        "1 Introduction",
        "2 Mathematical Preliminaries",
        "3 Inexact Catching-Up Algorithm for Sweeping Processes",
        "4 The Case of Prox-Regular Moving Sets",
        "The Case of Uniformly Subsmooth Moving Sets",
        "6 The Case of a Fixed Set",
        "7 An Application to Complementarity Dynamical Systems",
        "8 Concluding Remarks",
        # Meta headings
        "Abstract",
        "References",
        "Figure 2",
        "Figure 3",
        "January 10, 2025",
    ],
)
def test_classify_heading_returns_heading_for_section_titles(title: str) -> None:
    """Verify that plain section/meta headings are not misclassified."""

    kind, label = classify_heading(title)
    assert kind == BlockKind.HEADING
    assert label is None


@pytest.mark.parametrize(
    "title",
    [
        # Numbered-only results from the fixture (no keyword present)
        "2.4",
        "2.5",
        "2.6",
        "2.7",
        "2.8",
    ],
)
def test_classify_heading_returns_heading_for_numbered_only_titles(title: str) -> None:
    """Verify that bare number headings (no keyword) stay as HEADING.

    The fixture contains results labelled only by number (``# 2.4``, ``# 2.5``
    …).  These have no keyword and cannot be classified without additional
    context.  The segmentation layer correctly leaves them as ``HEADING``.
    """

    kind, label = classify_heading(title)
    assert kind == BlockKind.HEADING
    assert label is None


def test_classify_heading_returns_heading_for_empty_string() -> None:
    """Verify that an empty heading title is handled gracefully."""

    kind, label = classify_heading("")
    assert kind == BlockKind.HEADING
    assert label is None


def test_classify_heading_is_case_insensitive() -> None:
    """Verify that keyword matching ignores case."""

    kind, label = classify_heading("THEOREM 1.1.")
    assert kind == BlockKind.THEOREM
    assert label == "1.1"


# ===========================================================================
# classify_heading — abbreviations
# ===========================================================================


@pytest.mark.parametrize(
    "title, expected_kind, expected_label",
    [
        ("Def. 2.1", BlockKind.DEFINITION, "2.1"),
        ("Def 2.1.", BlockKind.DEFINITION, "2.1"),
        ("Thm. 4.1", BlockKind.THEOREM, "4.1"),
        ("Thm 4.1.", BlockKind.THEOREM, "4.1"),
        ("Prop. 2.9", BlockKind.PROPOSITION, "2.9"),
        ("Lem. 7.2", BlockKind.LEMMA, "7.2"),
        ("Cor. 5.1", BlockKind.COROLLARY, "5.1"),
        ("Rem. 7.1", BlockKind.REMARK, "7.1"),
        ("Obs. 3", BlockKind.OBSERVATION, "3"),
        ("Conj. 2", BlockKind.CONJECTURE, "2"),
        # "Note" is treated as a remark
        ("Note 1.", BlockKind.REMARK, "1"),
        ("Note.", BlockKind.REMARK, None),
        ("Notation 3.", BlockKind.REMARK, "3"),
    ],
)
def test_classify_heading_recognises_abbreviations(
    title: str, expected_kind: BlockKind, expected_label: str | None
) -> None:
    """Verify that abbreviated headings (Def, Thm, Prop, …) are classified."""

    kind, label = classify_heading(title)
    assert kind == expected_kind
    assert label == expected_label


# ===========================================================================
# classify_heading — fuzzy / linguistic-variant matching
# ===========================================================================


@pytest.mark.parametrize(
    "title, expected_kind",
    [
        # Spanish
        ("Teorema 2.1.", BlockKind.THEOREM),
        ("Lema 3.2.", BlockKind.LEMMA),
        ("Prueba.", BlockKind.PROOF),
        ("Definición 1.1.", BlockKind.DEFINITION),
        ("Proposición 3.1.", BlockKind.PROPOSITION),
        ("Corolario 5.1.", BlockKind.COROLLARY),
        ("Observación 4.", BlockKind.OBSERVATION),
        ("Ejemplo 7.3.", BlockKind.EXAMPLE),
        ("Conjetura 2.", BlockKind.CONJECTURE),
        # French
        ("Théorème 5.1.", BlockKind.THEOREM),
        ("Preuve.", BlockKind.PROOF),
        ("Définition 2.1.", BlockKind.DEFINITION),
        ("Lemme 7.2.", BlockKind.LEMMA),
        ("Corollaire 3.", BlockKind.COROLLARY),
        # Near-typo (caught by difflib)
        ("Theoreme 4.1.", BlockKind.THEOREM),
        ("Definicion 2.3.", BlockKind.DEFINITION),
        ("Proposicion 2.9.", BlockKind.PROPOSITION),
    ],
)
def test_classify_heading_recognises_linguistic_and_fuzzy_variants(
    title: str, expected_kind: BlockKind
) -> None:
    """Verify that linguistic variants and near-typos are classified correctly."""

    kind, _label = classify_heading(title)
    assert kind == expected_kind


# ===========================================================================
# classify_inline — basic keyword recognition
# ===========================================================================


@pytest.mark.parametrize(
    "text, expected_kind, expected_label",
    [
        ("**Lemma 3.1**", BlockKind.LEMMA, "3.1"),
        ("Proposition 3.1. Let us assume …", BlockKind.PROPOSITION, "3.1"),
        ("Theorem 3.2. Assume, in addition to …", BlockKind.THEOREM, "3.2"),
        ("Proof. Fix x ∈ H and ε > 0.", BlockKind.PROOF, None),
        ("Proof.", BlockKind.PROOF, None),
        ("Definition 1.1. Let S be …", BlockKind.DEFINITION, "1.1"),
        ("Corollary 2.3.", BlockKind.COROLLARY, "2.3"),
        ("Remark 1.", BlockKind.REMARK, "1"),
        ("Example 3.", BlockKind.EXAMPLE, "3"),
        ("**Theorem 2.3** The result follows …", BlockKind.THEOREM, "2.3"),
        # italic (single asterisk) markers
        ("*Lemma 4.1* …", BlockKind.LEMMA, "4.1"),
        # mismatched markers — keyword is still detected
        ("*Theorem 5.1** …", BlockKind.THEOREM, "5.1"),
    ],
)
def test_classify_inline_recognises_basic_labels(
    text: str, expected_kind: BlockKind, expected_label: str | None
) -> None:
    """Verify that inline labels at the start of text are detected correctly."""

    kind, label = classify_inline(text)
    assert kind == expected_kind
    assert label == expected_label


# ===========================================================================
# classify_inline — inline labels extracted directly from the fixture
# ===========================================================================


@pytest.mark.parametrize(
    "text, expected_kind, expected_label",
    [
        # Inline proofs: Section 2 (p. 5 of fixture)
        (
            "Proof. Fix x ∈ H and let η > 0. Since S ⊂ Sη ⊂ S + ηB, we obtain that "
            "dS+ηB(x) ≤ dSη(x) ≤ dS(x)",
            BlockKind.PROOF,
            None,
        ),
        (
            "Proof. Fix x ∈ H. The first assertion follows directly from the definition "
            "of the ε − η approximate projection.",
            BlockKind.PROOF,
            None,
        ),
        (
            "Proof. Fix x ∈ H and ε, η > 0, let z ∈ projε,η(x). Then, by Proposition 2.7,",
            BlockKind.PROOF,
            None,
        ),
        # Section 3 inline math blocks
        (
            "Proposition 3.1. Let us assume that H is a separable Hilbert space. Moreover "
            "we suppose F(·, x) is measurable for all x ∈ H, then HF3 holds for all γ > 0.",
            BlockKind.PROPOSITION,
            "3.1",
        ),
        (
            "Theorem 3.2. Assume, in addition to HF1, HF2 and HF3, that C: [0, T] ⇒ H is "
            "a set-valued map with nonempty and closed values",
            BlockKind.THEOREM,
            "3.2",
        ),
        (
            "Proof. (a): Set µn := T /n and let (εn) and (ηn) be sequences of non-negative "
            "numbers such that εn/µ2 → 0 and ηn/µn → 0.",
            BlockKind.PROOF,
            None,
        ),
        # Section 6 inline proof
        (
            "Proof.  We are going to use the properties of Theorem 3.2, where now we have "
            "LC = 0.",
            BlockKind.PROOF,
            None,
        ),
        # Section 7 inline proof
        (
            "Proof. Assertion (i) follows directly from relation (22). To prove (ii), "
            "we observe that",
            BlockKind.PROOF,
            None,
        ),
    ],
)
def test_classify_inline_fixture_paragraphs(
    text: str, expected_kind: BlockKind, expected_label: str | None
) -> None:
    """Verify inline labels taken verbatim from the fixture are classified."""

    kind, label = classify_inline(text)
    assert kind == expected_kind
    assert label == expected_label


# ===========================================================================
# classify_inline — abbreviations
# ===========================================================================


@pytest.mark.parametrize(
    "text, expected_kind, expected_label",
    [
        ("Thm. 4.1 Suppose, in addition to …", BlockKind.THEOREM, "4.1"),
        ("Def. 2.3 Let S be a closed subset …", BlockKind.DEFINITION, "2.3"),
        ("Prop. 3.1. Let us assume …", BlockKind.PROPOSITION, "3.1"),
        ("Lem. 7.2. Let y* and λ* be solutions …", BlockKind.LEMMA, "7.2"),
        ("Rem. 7.1.", BlockKind.REMARK, "7.1"),
        ("Cor. 5.1. If S is prox-regular …", BlockKind.COROLLARY, "5.1"),
        ("Note 3. This follows from …", BlockKind.REMARK, "3"),
        ("Note. We emphasise that …", BlockKind.REMARK, None),
    ],
)
def test_classify_inline_recognises_abbreviations(
    text: str, expected_kind: BlockKind, expected_label: str | None
) -> None:
    """Verify that abbreviated inline labels are classified correctly."""

    kind, label = classify_inline(text)
    assert kind == expected_kind
    assert label == expected_label


# ===========================================================================
# classify_inline — negative cases (no label at start)
# ===========================================================================


@pytest.mark.parametrize(
    "text",
    [
        # General fixture prose (should NOT be classified)
        "The following proposition provides a characterization of uniformly prox-regular sets.",
        "In this section, we prove the convergence of the inexact catching-up algorithm.",
        "We use the theorem from Section 2.",
        "It is clear that convex sets are ρ-uniformly prox-regular for any ρ > 0.",
        "From now on, H denotes a real Hilbert space.",
        "The sweeping process, originally introduced by J.-J. Moreau",
        "Additionally, we apply our numerical results to address complementarity dynamical",
        "Figure 1: Electrical circuit with ideal diodes.",
        "",
    ],
)
def test_classify_inline_returns_none_for_non_labels(text: str) -> None:
    """Verify that normal prose paragraphs are not incorrectly classified."""

    kind, label = classify_inline(text)
    assert kind is None
    assert label is None


# ===========================================================================
# classify_blocks — unit tests with synthetic documents
# ===========================================================================


def test_classify_blocks_updates_math_headings() -> None:
    """Verify that heading blocks with math keywords are reclassified."""

    markdown_text = """# Definition 2.1.

Let S be a closed subset of H.

# Theorem 3.2.

If S is ρ-uniformly prox-regular then the projection exists.

# Proof.

The result follows directly from the definition.
"""

    document = parse_markdown_text(markdown_text)
    classified = classify_blocks(document)

    block_types = [b.block_type for b in classified]
    assert block_types == [
        "definition",
        "paragraph",
        "theorem",
        "paragraph",
        "proof",
        "paragraph",
    ]

    assert classified[0].label == "2.1"
    assert classified[2].label == "3.2"
    assert classified[4].label is None


def test_classify_blocks_updates_inline_labeled_paragraphs() -> None:
    """Verify that paragraphs opening with inline labels are reclassified."""

    markdown_text = """# 3 Results

Proposition 3.1. Let us assume that H is a separable Hilbert space.

Theorem 3.2. Assume, in addition to HF1 and HF2, that C satisfies (9).

Proof. Set µn := T/n and proceed by induction.
"""

    document = parse_markdown_text(markdown_text)
    classified = classify_blocks(document)

    block_types = [b.block_type for b in classified]
    assert block_types == [
        "heading",    # "3 Results" — plain section heading
        "proposition",
        "theorem",
        "proof",
    ]

    assert classified[1].label == "3.1"
    assert classified[2].label == "3.2"


def test_classify_blocks_handles_abbreviation_headings() -> None:
    """Verify that abbreviated headings are reclassified correctly."""

    markdown_text = """# Def. 1.1.

Let S be a closed subset.

# Thm. 2.3.

The result holds under these conditions.

# Prf.

Wait, this is not a known abbreviation, so it stays as a heading.
"""

    document = parse_markdown_text(markdown_text)
    classified = classify_blocks(document)

    # "Def. and Thm. should be recognised; Prf. is not in the vocabulary.
    # We intentionally use "Prf." (not the known "Proof.") to verify that
    # unrecognised abbreviations are not misclassified.
    assert classified[0].block_type == "definition"
    assert classified[0].label == "1.1"
    assert classified[2].block_type == "theorem"
    assert classified[2].label == "2.3"
    # "Prf." is not a known keyword or abbreviation
    assert classified[4].block_type == "heading"


def test_classify_blocks_does_not_mutate_input_document() -> None:
    """Verify that the original document is left unchanged."""

    markdown_text = "# Definition 1.1.\n\nLet S be closed.\n"
    document = parse_markdown_text(markdown_text)
    original_types = [b.block_type for b in document.blocks]

    classify_blocks(document)

    assert [b.block_type for b in document.blocks] == original_types


def test_classify_blocks_preserves_plain_blocks_unchanged() -> None:
    """Verify that blocks without math keywords are returned as-is."""

    markdown_text = """# Introduction

This paper studies sweeping processes.

- first item
- second item
"""

    document = parse_markdown_text(markdown_text)
    classified = classify_blocks(document)

    assert [b.block_type for b in classified] == ["heading", "paragraph", "list"]
    assert classified[0].block_type == "heading"


# ===========================================================================
# classify_blocks — fixture-based tests
# ===========================================================================


def test_classify_blocks_on_fixture_detects_all_expected_kinds() -> None:
    """Verify that every expected mathematical kind appears in the fixture output."""

    document = load_markdown_file(FIXTURE_PATH)
    classified = classify_blocks(document)
    block_types_set = {b.block_type for b in classified}

    for kind in ("definition", "proposition", "theorem", "remark", "lemma", "example", "proof"):
        assert kind in block_types_set, f"Expected kind {kind!r} not found in fixture output"


def test_classify_blocks_on_fixture_counts_math_blocks() -> None:
    """Verify that the fixture yields a plausible count of each math kind."""

    document = load_markdown_file(FIXTURE_PATH)
    classified = classify_blocks(document)

    counts: dict[str, int] = {}
    for b in classified:
        counts[b.block_type] = counts.get(b.block_type, 0) + 1

    # These counts come from manual inspection of the fixture.
    assert counts.get("definition", 0) >= 2     # Def 2.1, Def 2.3
    assert counts.get("proposition", 0) >= 3    # Prop 2.2, Prop 2.9, Prop 3.1
    assert counts.get("theorem", 0) >= 4        # Thm 3.2, 4.1, 5.1, 6.1
    assert counts.get("proof", 0) >= 7          # multiple inline + heading proofs
    assert counts.get("remark", 0) >= 1         # Rem 7.1
    assert counts.get("lemma", 0) >= 1          # Lem 7.2
    assert counts.get("example", 0) >= 1        # Ex 7.3


def test_classify_blocks_on_fixture_specific_heading_math_blocks() -> None:
    """Verify specific math heading blocks are classified with correct labels."""

    document = load_markdown_file(FIXTURE_PATH)
    classified = classify_blocks(document)

    # Build a lookup by (block_type, label)
    found: set[tuple[str, str | None]] = {(b.block_type, b.label) for b in classified}

    expected = [
        ("definition", "2.1"),
        ("proposition", "2.2"),
        ("definition", "2.3"),
        ("proposition", "2.9"),
        ("theorem", "4.1"),
        ("theorem", "5.1"),
        ("theorem", "6.1"),
        ("remark", "7.1"),
        ("lemma", "7.2"),
        ("example", "7.3"),
    ]
    for block_type, label in expected:
        assert (block_type, label) in found, (
            f"Expected block ({block_type!r}, label={label!r}) not found in fixture output"
        )


def test_classify_blocks_on_fixture_section_headings_stay_as_heading() -> None:
    """Verify that plain section headings in the fixture are not reclassified."""

    document = load_markdown_file(FIXTURE_PATH)
    classified = classify_blocks(document)

    # Build a dict: title → block_type for all heading blocks
    heading_titles = {
        b.title: b.block_type
        for b in classified
        if b.title is not None
    }

    plain_section_titles = [
        "1 Introduction",
        "2 Mathematical Preliminaries",
        "3 Inexact Catching-Up Algorithm for Sweeping Processes",
        "4 The Case of Prox-Regular Moving Sets",
        "The Case of Uniformly Subsmooth Moving Sets",
        "6 The Case of a Fixed Set",
        "8 Concluding Remarks",
        "Abstract",
        "References",
    ]

    for title in plain_section_titles:
        if title in heading_titles:
            assert heading_titles[title] == "heading", (
                f"Section title {title!r} was wrongly reclassified as "
                f"{heading_titles[title]!r}"
            )

