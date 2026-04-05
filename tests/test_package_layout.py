"""Layout tests that keep the scaffold aligned with the specification."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_expected_top_level_paths_exist() -> None:
    """The first task should create the expected top-level project files."""

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
    """The scaffold should make the main subsystem boundaries explicit."""

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
