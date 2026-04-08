"""Tests for the rule-based mathematical segmentation layer (Tarea 03).

The segmentation layer takes ``ArticleBlock`` objects produced by the ingestion
layer and annotates them with mathematical roles (theorem, lemma, proof, …).
These tests exercise each rule independently as well as the combined
``classify_blocks`` pipeline, including a smoke test against the real fixture.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from article2lean.ingestion import load_markdown_file, parse_markdown_text
from article2lean.models.enums import BlockKind
from article2lean.segmentation import classify_blocks, classify_heading, classify_inline


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "garrido2025inexact.md"


# ---------------------------------------------------------------------------
# classify_heading
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "title, expected_kind, expected_label",
    [
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
def test_classify_heading_recognises_math_keywords(
    title: str, expected_kind: BlockKind, expected_label: str | None
) -> None:
    """Verify that headings with known keywords are classified correctly."""

    kind, label = classify_heading(title)
    assert kind == expected_kind
    assert label == expected_label


@pytest.mark.parametrize(
    "title",
    [
        "1 Introduction",
        "2 Mathematical Preliminaries",
        "3 Inexact Catching-Up Algorithm for Sweeping Processes",
        "Abstract",
        "References",
        "Conclusion",
    ],
)
def test_classify_heading_returns_heading_for_section_titles(title: str) -> None:
    """Verify that plain section headings are not misclassified as math blocks."""

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


# ---------------------------------------------------------------------------
# classify_inline
# ---------------------------------------------------------------------------


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
        # mismatched markers — we detect the keyword regardless
        ("*Theorem 5.1** …", BlockKind.THEOREM, "5.1"),
    ],
)
def test_classify_inline_recognises_labels(
    text: str, expected_kind: BlockKind, expected_label: str | None
) -> None:
    """Verify that inline labels at the start of text are detected correctly."""

    kind, label = classify_inline(text)
    assert kind == expected_kind
    assert label == expected_label


@pytest.mark.parametrize(
    "text",
    [
        "The following proposition provides …",
        "In this section, we prove …",
        "We use the theorem from Section 2.",
        "It is clear that convex sets …",
        "",
    ],
)
def test_classify_inline_returns_none_for_non_labels(text: str) -> None:
    """Verify that normal prose paragraphs are not incorrectly classified."""

    kind, label = classify_inline(text)
    assert kind is None
    assert label is None


# ---------------------------------------------------------------------------
# classify_blocks — unit tests with synthetic documents
# ---------------------------------------------------------------------------


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
    # Headings become math types; paragraphs stay as paragraphs.
    assert block_types == [
        "definition",
        "paragraph",
        "theorem",
        "paragraph",
        "proof",
        "paragraph",
    ]

    definition_heading = classified[0]
    assert definition_heading.label == "2.1"

    theorem_heading = classified[2]
    assert theorem_heading.label == "3.2"

    proof_heading = classified[4]
    assert proof_heading.label is None


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

    prop_block = classified[1]
    assert prop_block.label == "3.1"

    thm_block = classified[2]
    assert thm_block.label == "3.2"


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
    # The section heading keeps the original block_type "heading"
    assert classified[0].block_type == "heading"


# ---------------------------------------------------------------------------
# classify_blocks — smoke test against the real fixture
# ---------------------------------------------------------------------------


def test_classify_blocks_on_fixture_detects_definitions_and_proofs() -> None:
    """Verify that the classifier finds math blocks in the real fixture."""

    document = load_markdown_file(FIXTURE_PATH)
    classified = classify_blocks(document)

    block_types_set = {b.block_type for b in classified}

    # The fixture contains definitions, propositions, and proofs.
    assert "definition" in block_types_set
    assert "proposition" in block_types_set
    assert "proof" in block_types_set


def test_classify_blocks_on_fixture_counts_math_blocks() -> None:
    """Verify that the fixture yields a plausible count of math blocks."""

    document = load_markdown_file(FIXTURE_PATH)
    classified = classify_blocks(document)

    math_kinds = {
        "definition", "theorem", "lemma", "proposition",
        "corollary", "remark", "proof", "observation", "claim", "conjecture",
    }
    math_blocks = [b for b in classified if b.block_type in math_kinds]

    # The fixture is a real paper; we expect at least a handful of math blocks.
    assert len(math_blocks) >= 5
