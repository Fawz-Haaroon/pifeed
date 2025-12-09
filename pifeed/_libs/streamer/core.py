#!/usr/bin/env python3
# Configuration for the streamer module

from __future__ import annotations

import os
from pathlib import Path
from typing import Self


Flag = bool


class DroneConfig:
    def __init__(
        self: Self,
        *,
        # enabled workers
        video_mode: Flag = True,
        image_mode: Flag = True,
        rtsp_mode: Flag = True,

        # network / service
        rtsp_port: int = 8554,

        # camera / encoder
        camera_dev: str = "/dev/video0",
        video_bitrate: int = 2_000_000,
        video_fps: int = 25,
        video_width: int = 1280,
        video_height: int = 720,
        image_quality: int = 95,

        # storage
        storage_path: str | Path = "/home/lexitron/capture",

    ) -> None:
        self.video_mode: Flag = video_mode
        self.image_mode: Flag = image_mode
        self.rtsp_mode: Flag = rtsp_mode

        self.rtsp_port: int = rtsp_port

        self.camera_dev: str = camera_dev
        self.video_bitrate: int = video_bitrate
        self.video_fps: int = video_fps
        self.video_width: int = video_width
        self.video_height: int = video_height
        self.image_quality: int = image_quality

        self.storage_path: Path = Path(storage_path)
        self.archive_video: Path = self.storage_path / "drone_archive" / "videos"
        self.archive_image: Path = self.storage_path / "drone_archive" / "images"
        self.temp_path: Path = self.storage_path / "drone_temp"


    @classmethod
    def from_env(cls: type[Self]) -> Self:
        def getb(k: str, d: Flag) -> Flag:
            v = os.getenv(k, "").lower()
            return v in ("1", "true", "yes", "on") if v else d

        def geti(k: str, d: int) -> int:
            try:
                return int(os.getenv(k, str(d)))
            except Exception:
                return d

        return cls(
            video_mode=getb("ENABLE_VIDEO", True),
            image_mode=getb("ENABLE_IMAGES", True),
            rtsp_mode=getb("ENABLE_RTSP", True),

            rtsp_port=geti("RTSP_PORT", 8554),

            camera_dev=os.getenv("CAMERA", "/dev/video0"),
            video_bitrate=geti("VIDEO_BITRATE", 2_000_000),
            video_fps=geti("VIDEO_FPS", 30),
            video_width=geti("VIDEO_WIDTH", 1280),
            video_height=geti("VIDEO_HEIGHT", 720),
            image_quality=geti("IMAGE_QUALITY", 95),

            storage_path=os.getenv("SSD_PATH", "/home/lexitron/capture"),
        )

    def setup_storage(self: Self) -> None:
        for p in (self.archive_video, self.archive_image, self.temp_path):
            p.mkdir(parents=True, exist_ok=True)

    def __str__(self: Self) -> str:
        return (
            f"StreamerConfig: video={self.video_mode}, images={self.image_mode}, rtsp={self.rtsp_mode}, "
            f"rtsp_port={self.rtsp_port}, storage={self.storage_path}"
        )
