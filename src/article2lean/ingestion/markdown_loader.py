"""Load Markdown sources into a small, navigable internal representation.

The parser implemented here is intentionally small and explicit. Its job is not
to understand mathematical meaning yet. Its job is only to preserve the raw
document structure that later stages can classify more intelligently.
"""

from __future__ import annotations

from pathlib import Path
import re

from article2lean.models import ArticleBlock, MarkdownDocument


HEADING_PATTERN = re.compile(r"^(#{1,6})[ \t]+(.+?)\s*$")
UNORDERED_LIST_PATTERN = re.compile(r"^[ \t]*[-+*][ \t]+(.+?)\s*$")
ORDERED_LIST_PATTERN = re.compile(r"^[ \t]*\d+[.)][ \t]+(.+?)\s*$")


def load_markdown_file(path: str | Path) -> MarkdownDocument:
    """Read a Markdown file from disk and parse it into raw blocks."""

    markdown_path = Path(path)
    return parse_markdown_text(
        markdown_path.read_text(encoding="utf-8"),
        source_path=str(markdown_path),
    )


def parse_markdown_text(
    markdown_text: str,
    source_path: str | None = None,
) -> MarkdownDocument:
    """Convert Markdown text into a navigable list of raw blocks.

    The output deliberately stays close to the source. We keep headings,
    paragraphs, and simple lists as separate blocks together with section
    context and line-number metadata so the next subsystem can reason from a
    stable structure instead of plain text.
    """

    blocks: list[ArticleBlock] = []
    current_section_path: list[str] = []
    paragraph_lines: list[str] = []
    paragraph_start_line: int | None = None
    list_lines: list[str] = []
    list_items: list[str] = []
    list_start_line: int | None = None
    list_kind: str | None = None

    def next_block_id() -> str:
        """Create a readable sequential identifier for each extracted block."""

        return f"block-{len(blocks) + 1:04d}"

    def append_block(
        block_type: str,
        raw_text: str,
        start_line: int,
        end_line: int,
        *,
        title: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> None:
        """Append one block with shared metadata fields already normalized."""

        normalized_metadata = {"start_line": start_line, "end_line": end_line}
        if metadata:
            normalized_metadata.update(metadata)

        blocks.append(
            ArticleBlock(
                block_id=next_block_id(),
                block_type=block_type,
                raw_text=raw_text,
                title=title,
                section_path=current_section_path.copy(),
                metadata=normalized_metadata,
            )
        )

    def flush_paragraph() -> None:
        """Emit the buffered paragraph block, if one is currently open."""

        nonlocal paragraph_lines, paragraph_start_line

        if paragraph_start_line is None:
            return

        append_block(
            "paragraph",
            "\n".join(paragraph_lines).strip(),
            paragraph_start_line,
            paragraph_start_line + len(paragraph_lines) - 1,
        )
        paragraph_lines = []
        paragraph_start_line = None

    def flush_list() -> None:
        """Emit the buffered list block, if one is currently open."""

        nonlocal list_lines, list_items, list_start_line, list_kind

        if list_start_line is None or list_kind is None:
            return

        append_block(
            "list",
            "\n".join(list_lines),
            list_start_line,
            list_start_line + len(list_lines) - 1,
            metadata={
                "items": list_items.copy(),
                "item_count": len(list_items),
                "list_kind": list_kind,
            },
        )
        list_lines = []
        list_items = []
        list_start_line = None
        list_kind = None

    def classify_list_item(line: str) -> tuple[str, str] | None:
        """Return the list kind and item text when the line starts a list item."""

        ordered_match = ORDERED_LIST_PATTERN.match(line)
        if ordered_match:
            return ("ordered", ordered_match.group(1))

        unordered_match = UNORDERED_LIST_PATTERN.match(line)
        if unordered_match:
            return ("unordered", unordered_match.group(1))

        return None

    for line_number, raw_line in enumerate(markdown_text.splitlines(), start=1):
        stripped_line = raw_line.strip()
        heading_match = HEADING_PATTERN.match(raw_line)
        list_match = classify_list_item(raw_line)

        if not stripped_line:
            flush_paragraph()
            flush_list()
            continue

        if heading_match:
            flush_paragraph()
            flush_list()

            heading_level = len(heading_match.group(1))
            heading_title = heading_match.group(2).strip()
            current_section_path = (
                current_section_path[: heading_level - 1] + [heading_title]
            )

            append_block(
                "heading",
                raw_line,
                line_number,
                line_number,
                title=heading_title,
                metadata={"heading_level": heading_level},
            )
            continue

        if list_match:
            flush_paragraph()

            item_kind, item_text = list_match
            if list_kind not in (None, item_kind):
                flush_list()

            if list_start_line is None:
                list_start_line = line_number
                list_kind = item_kind

            list_lines.append(raw_line)
            list_items.append(item_text)
            continue

        flush_list()

        if paragraph_start_line is None:
            paragraph_start_line = line_number

        paragraph_lines.append(raw_line)

    flush_paragraph()
    flush_list()

    return MarkdownDocument(
        source_path=source_path,
        raw_text=markdown_text,
        blocks=blocks,
    )
