"""Allow ``python -m article2lean`` to behave like the CLI entry point."""

from article2lean.cli import main


if __name__ == "__main__":
    raise SystemExit(main())

