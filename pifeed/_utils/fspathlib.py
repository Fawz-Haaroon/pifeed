"""Filesystem path helpers for pifeed."""

from __future__ import annotations

from pathlib import Path


def get_fspath(path: str | Path) -> Path:
    return Path(path).resolve()
