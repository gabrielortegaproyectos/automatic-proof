"""Layout tests that keep the scaffold aligned with the specification.

These tests treat the repository structure as part of the public contract of
Tarea 01. They help us catch regressions where a file or package disappears and
the project stops matching the intended architecture.
"""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_expected_top_level_paths_exist() -> None:
    """Verify that the top-level files promised by Tarea 01 exist.

    This is the most direct check that the scaffold task was actually completed:
    the project root should already contain the files needed to install, read,
    and explore the repository.
    """

    expected_paths = [
        PROJECT_ROOT / "pyproject.toml",
        PROJECT_ROOT / "README.md",
        PROJECT_ROOT / "configs" / "app.yaml",
        PROJECT_ROOT / "configs" / "segmentation.yaml",
        PROJECT_ROOT / "configs" / "refinement.yaml",
        PROJECT_ROOT / "configs" / "lean.yaml",
        PROJECT_ROOT / "src" / "article2lean" / "cli.py",
        PROJECT_ROOT / "tests" / "test_cli.py",
    ]

    for path in expected_paths:
        assert path.exists(), f"Missing expected scaffold path: {path}"


def test_expected_subpackages_exist() -> None:
    """Verify that the main subsystem directories are already present.

    This test is architectural rather than behavioral. It checks that the code
    base already exposes the intended separation between ingestion,
    segmentation, sketches, formalization, proving, and the other supporting
    layers.
    """

    expected_directories = [
        PROJECT_ROOT / "src" / "article2lean" / "models",
        PROJECT_ROOT / "src" / "article2lean" / "ingestion",
        PROJECT_ROOT / "src" / "article2lean" / "segmentation",
        PROJECT_ROOT / "src" / "article2lean" / "references",
        PROJECT_ROOT / "src" / "article2lean" / "sketches",
        PROJECT_ROOT / "src" / "article2lean" / "formalization",
        PROJECT_ROOT / "src" / "article2lean" / "proving",
        PROJECT_ROOT / "src" / "article2lean" / "orchestrators",
        PROJECT_ROOT / "src" / "article2lean" / "exporters",
        PROJECT_ROOT / "src" / "article2lean" / "utils",
    ]

    for directory in expected_directories:
        assert directory.is_dir(), f"Missing expected package directory: {directory}"
