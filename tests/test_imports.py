"""Import-focused tests for the scaffold package.

This file checks that the package layout is healthy from Python's point of
view. If these tests fail, the project may look correct in the file tree but be
broken as an installable package.
"""

from __future__ import annotations

import importlib

import article2lean
import pytest


def test_package_exposes_a_version_string() -> None:
    """Verify that the package exposes a simple public version string.

    This is a tiny smoke test for the package root: if importing the top-level
    package already fails, the rest of the scaffold is not ready to use.
    """

    assert article2lean.__version__ == "0.1.0"


@pytest.mark.parametrize(
    "module_name",
    [
        "article2lean.ingestion.markdown_loader",
        "article2lean.segmentation.block_classifier",
        "article2lean.references.dependency_graph",
        "article2lean.sketches.sketch_extractor",
        "article2lean.formalization.statement_formalizer",
        "article2lean.proving.lean_backend",
        "article2lean.orchestrators.article_formalization",
        "article2lean.exporters.report_exporter",
    ],
)
def test_key_modules_are_importable(module_name: str) -> None:
    """Verify that representative modules from each subsystem import cleanly.

    The goal is not to test their logic yet. The goal is to confirm that the
    scaffold is wired correctly and that each main subsystem already has a valid
    Python module behind it.
    """

    module = importlib.import_module(module_name)
    assert module.__doc__
