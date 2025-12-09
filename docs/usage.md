```
uv sync --all-extras


export SSD_PATH="$HOME/Desktop/dev/capture"
export ENABLE_RTSP=1
export ENABLE_VIDEO=1
export ENABLE_IMAGES=1
export CAMERA="/dev/video0"
export VIDEO_FPS=30 VIDEO_WIDTH=1280 VIDEO_HEIGHT=720 VIDEO_BITRATE=2000000


uv run python -m pifeed
```
