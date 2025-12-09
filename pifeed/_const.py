"""Core filesystem constants for pifeed."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Final

from pifeed._utils.fspathlib import get_fspath


_BASE_DIR_PATH: Final[Path] = get_fspath(
    os.path.join(os.path.dirname(__file__), "./../"),
)


MODULE_BASE_DIR_PATH: Final[Path] = get_fspath(
    _BASE_DIR_PATH / "pifeed",
)
PYPROJECT_TOML_FILE_PATH: Final[Path] = get_fspath(
    _BASE_DIR_PATH / "pyproject.toml",
)
