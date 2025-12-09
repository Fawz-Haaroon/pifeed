from __future__ import annotations

import sys

from pifeed import run_streamer


def main() -> int:
    return run_streamer()


if __name__ == "__main__":
    sys.exit(main())
