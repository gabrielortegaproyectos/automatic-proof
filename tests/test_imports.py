"""Import-focused tests for the scaffold package."""

from __future__ import annotations

import importlib

import article2lean
import pytest


def test_package_exposes_a_version_string() -> None:
    """The top-level package should expose a readable version."""

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
    """Important modules from each subsystem should import cleanly."""

    module = importlib.import_module(module_name)
    assert module.__doc__

