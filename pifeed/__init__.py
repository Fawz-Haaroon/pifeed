"""Core API surface for the pifeed package."""

from __future__ import annotations

from pifeed._types import ExportList
from pifeed._metadata import (
    __package__,
    __version__,
)

from pifeed._libs.streamer.core import DroneConfig
from pifeed._libs.streamer.drone import DroneController


__all__: ExportList = [
    "DroneConfig",
    "DroneController",
    "__package__",
    "__version__",
    "run_streamer",
]

# NOTE: keep this list sorted
assert __all__ == sorted(__all__)


def run_streamer(config: DroneConfig | None = None) -> int:
    """Run the streaming pipeline until interrupted"""

    # run def env conf if none
    if config is None:
        config = DroneConfig.from_env()

    controller = DroneController(config)
    controller.start()
    controller.run()
    return 0
