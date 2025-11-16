We run one camera and split that feed into two paths: a local recorder and a live RTSP server. RTSP is the way people consume the live video. Internally, the media still rides on RTP/RTCP (so UDP when possible, TCP interleaved only if the network forces it), but the thing you hand to anyone is just `rtsp://<host-ip>:8554/live`.
When you start it, the first process up is the camera feeder. It opens the camera with `v4l2src`, asks for MJPEG, decodes to raw I420, fixes the frame rate and size you configured, and then tees that raw stream into two shared‑memory sockets: `/tmp/drone_cam_rec.sock` for recording and `/tmp/drone_cam_str.sock` for the RTSP server. SHM matters because it decouples the camera capture from whatever the recorder or the network is doing. If a client hiccups or the disk is slow for a moment, the camera keeps flowing and we’d rather drop a frame than build latency.
If you enable recording, the recorder pulls frames from its SHM socket and splits into two little branches. One encodes H.264 and writes MP4 chunks around 5.5 seconds long using splitmux; the other takes one frame per second and saves a JPEG. Every time a chunk or image lands, we refresh a symlink in a temp dir (`drone_temp/latest_video.mp4` and `drone_temp/latest_image.jpg`) so anything that “watches the latest” never has to scan directories. The recorder lives entirely on disk; if you don’t need it, disable it and save CPU.
The RTSP worker is the live path. It also reads from its own SHM, runs `x264enc` with low‑latency settings (no B‑frames, keyframe roughly once per second), passes the bitstream through `h264parse` (we re‑emit SPS/PPS regularly so late joiners lock quickly), and hands the payload to `rtph264pay` as `pay0`. The RTSP server mounts that pipeline at `/live` on port 8554. A viewer connects to 8554 for the RTSP control conversation; for the actual media, the client and server normally choose UDP ports for RTP/RTCP. If UDP is blocked by the network, most players flip to interleaved TCP inside the same RTSP connection. That raises latency but the stream keeps working. We keep the RTSP media factory shared, so one encoder feeds as many viewers as you have bandwidth for. There’s a tiny leaky queue in front of the encoder to keep us from buffering on transient back pressure.
On top of these workers sits a very boring controller. It spawns processes, logs and it has a small watchdog: if any worker dies, we tear everything down cleanly and bring it back up. No fancy backoff, just enough to avoid a dead stream during long unattended runs.

```
export SSD_PATH="$HOME/Desktop/dev/capture"
export ENABLE_RTSP=1
export ENABLE_VIDEO=1 ENABLE_IMAGES=1
export CAMERA="/dev/video0"
export VIDEO_FPS=30 VIDEO_WIDTH=1280 VIDEO_HEIGHT=720 VIDEO_BITRATE=2000000
python3 -m streamer.drone
```

One camera goes in, an optional local storage on disk, and a clean RTSP URL comes out. Low‑latency defaults, UDP when we can, TCP fallback when we must, and a tiny watchdog keeping it alive.
