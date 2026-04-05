"""Small tests for the pedagogical command line interface."""

from __future__ import annotations

import pytest

from article2lean.cli import main


def test_help_message_is_available(capsys: pytest.CaptureFixture[str]) -> None:
    """The scaffold should teach the available commands from the CLI itself."""

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
    """Each placeholder command should explain what it will eventually do."""

    exit_code = main(argv)
    captured = capsys.readouterr()

    assert exit_code == 0
    assert expected_text in captured.out
