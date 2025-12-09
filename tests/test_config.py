from __future__ import annotations

import os

from pifeed import DroneConfig


def test_from_env_flags():
    env = {
        "ENABLE_VIDEO": "1",
        "ENABLE_IMAGES": "1",
        "ENABLE_RTSP": "1",
    }

    old_env = os.environ.copy()
    try:
        os.environ.update(env)
        cfg = DroneConfig.from_env()
    finally:
        os.environ.clear()
        os.environ.update(old_env)

    assert cfg.video_mode is True
    assert cfg.image_mode is True
    assert cfg.rtsp_mode is True
