"""Tests for the pedagogical Markdown ingestion layer.

These tests focus on one question: can we turn a Markdown source into a small
set of raw blocks that later stages can navigate and classify?
"""

from __future__ import annotations

from pathlib import Path

from article2lean.ingestion import load_markdown_file, parse_markdown_text


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "garrido2025inexact.md"


def test_parse_markdown_text_extracts_headings_paragraphs_and_lists() -> None:
    """Verify that the loader separates the basic Markdown block families."""

    markdown_text = """# Section

This is the opening paragraph.

## Details

- first item
- second item
"""

    document = parse_markdown_text(markdown_text)

    assert [block.block_type for block in document.blocks] == [
        "heading",
        "paragraph",
        "heading",
        "list",
    ]
    assert document.blocks[0].title == "Section"
    assert document.blocks[1].raw_text == "This is the opening paragraph."
    assert document.blocks[3].metadata["items"] == ["first item", "second item"]


def test_parse_markdown_text_preserves_section_paths_and_line_metadata() -> None:
    """Verify that each block keeps the navigation context needed downstream."""

    markdown_text = """# Parent

Intro text.

## Child

1. first step
2. second step
"""

    document = parse_markdown_text(markdown_text)

    parent_heading, intro_paragraph, child_heading, ordered_list = document.blocks

    assert parent_heading.section_path == ["Parent"]
    assert parent_heading.metadata["heading_level"] == 1
    assert intro_paragraph.section_path == ["Parent"]
    assert intro_paragraph.metadata["start_line"] == 3
    assert intro_paragraph.metadata["end_line"] == 3
    assert child_heading.section_path == ["Parent", "Child"]
    assert ordered_list.section_path == ["Parent", "Child"]
    assert ordered_list.metadata["list_kind"] == "ordered"
    assert ordered_list.metadata["item_count"] == 2


def test_load_markdown_file_reads_the_real_fixture() -> None:
    """Verify that the file-based API can ingest the repository fixture."""

    document = load_markdown_file(FIXTURE_PATH)

    assert document.source_path == str(FIXTURE_PATH)
    assert document.raw_text.startswith("arXiv:2501.04781v1")
    assert len(document.blocks) > 10
    assert document.blocks[0].block_type == "paragraph"
    assert document.blocks[1].block_type == "heading"
    assert document.blocks[1].title == (
        "Inexact Catching-Up Algorithm for Moreau’s Sweeping Processes"
    )
