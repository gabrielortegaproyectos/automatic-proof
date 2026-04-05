"""Tests for the pedagogical command line interface.

This file answers one simple question: can a new collaborator discover the
project through the CLI?

The tests here do not check real mathematical processing yet. They only check
that the command line exposes the intended entry points and that each command
prints an explanation of its future responsibility.
"""

from __future__ import annotations

import pytest

from article2lean.cli import main


def test_help_message_is_available(capsys: pytest.CaptureFixture[str]) -> None:
    """Verify that ``--help`` introduces the available commands.

    Why this matters:
    a user who installs the scaffold should be able to discover the system map
    without opening the source code first.
    """

    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])

    captured = capsys.readouterr()
    assert exc_info.value.code == 0
    assert "article2lean" in captured.out
    assert "architecture" in captured.out


@pytest.mark.parametrize(
    ("argv", "expected_text"),
    [
        (["architecture"], "Mapa de subsistemas"),
        (["article"], "modo article"),
        (["theorem"], "modo theorem"),
    ],
)
def test_placeholder_commands_explain_their_future_role(
    argv: list[str],
    expected_text: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Verify that each placeholder command teaches its future role.

    At this stage the commands are intentionally simple. The value of the test
    is not "does the pipeline work?" but "does the CLI explain what will later
    live behind this command?".
    """

    exit_code = main(argv)
    captured = capsys.readouterr()

    assert exit_code == 0
    assert expected_text in captured.out
