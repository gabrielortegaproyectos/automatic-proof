"""Minimal command line interface for the project scaffold."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from article2lean import __version__
from article2lean.app import (
    describe_architecture,
    describe_article_mode,
    describe_theorem_mode,
)


def build_parser() -> argparse.ArgumentParser:
    """Create the command parser used by the scaffold CLI."""

    parser = argparse.ArgumentParser(
        prog="article2lean",
        description=(
            "Esqueleto pedagogico para un sistema que convierte texto matematico "
            "en flujos de formalizacion hacia Lean."
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command")

    article_parser = subparsers.add_parser(
        "article",
        help="Explica el flujo futuro para procesar articulos.",
    )
    article_parser.add_argument(
        "source",
        nargs="?",
        help="Ruta opcional al Markdown que se procesara mas adelante.",
    )
    article_parser.set_defaults(handler=_handle_article_command)

    theorem_parser = subparsers.add_parser(
        "theorem",
        help="Explica el flujo futuro para un teorema aislado.",
    )
    theorem_parser.add_argument(
        "statement",
        nargs="?",
        help="Enunciado opcional para mostrarlo en la salida placeholder.",
    )
    theorem_parser.set_defaults(handler=_handle_theorem_command)

    architecture_parser = subparsers.add_parser(
        "architecture",
        help="Imprime el mapa actual del sistema y sus responsabilidades.",
    )
    architecture_parser.set_defaults(handler=_handle_architecture_command)

    return parser


def _handle_article_command(args: argparse.Namespace) -> int:
    """Run the placeholder article command."""

    print(describe_article_mode(args.source))
    return 0


def _handle_theorem_command(args: argparse.Namespace) -> int:
    """Run the placeholder theorem command."""

    print(describe_theorem_mode(args.statement))
    return 0


def _handle_architecture_command(_: argparse.Namespace) -> int:
    """Run the architecture command."""

    print(describe_architecture())
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process-style exit code."""

    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "handler"):
        parser.print_help()
        return 0

    return args.handler(args)
