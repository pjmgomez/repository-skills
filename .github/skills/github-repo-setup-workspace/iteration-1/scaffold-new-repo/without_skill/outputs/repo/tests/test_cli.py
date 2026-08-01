"""Tests for the packmule command-line interface."""

import pytest

from packmule import __version__
from packmule.cli import build_parser, main


def test_version_is_defined():
    assert isinstance(__version__, str)
    assert __version__


def test_parser_builds():
    parser = build_parser()
    assert parser.prog == "packmule"


def test_main_returns_zero(capsys):
    exit_code = main([])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "usage" in captured.out.lower()


def test_version_flag_exits_cleanly(capsys):
    with pytest.raises(SystemExit) as excinfo:
        main(["--version"])
    captured = capsys.readouterr()
    assert excinfo.value.code == 0
    assert __version__ in captured.out
