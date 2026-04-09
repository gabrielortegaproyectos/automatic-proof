"""Rule-based segmentation package for mathematical block detection."""

from article2lean.segmentation.block_classifier import classify_blocks
from article2lean.segmentation.heading_rules import classify_heading
from article2lean.segmentation.inline_label_rules import classify_inline

__all__ = ["classify_blocks", "classify_heading", "classify_inline"]

