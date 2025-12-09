# Camera → Recorder + RTSP Streaming Pipeline

We run one camera and split that feed into two paths: a local recorder and a live RTSP server. RTSP is the way people consume the live video. Internally, the media still rides on RTP/RTCP (so UDP when possible, TCP interleaved only if the network forces it), but the thing you hand to anyone is simply:

```
rtsp://<host-ip>:8554/live
```

When you start it, the first process up is the camera feeder. It opens the camera with `v4l2src`, asks for MJPEG, decodes to raw I420, fixes the frame rate and size you configured, and then tees that raw stream into two shared‑memory sockets:

```
/tmp/drone_cam_rec.sock   # recorder
/tmp/drone_cam_str.sock   # RTSP server
```

Shared memory matters because it isolates the camera from whatever the recorder or network is doing. If a client hiccups or the disk is slow, the camera keeps flowing coz we’d rather drop a frame than build latency.


## Recorder

If you enable recording, the recorder pulls frames from its SHM socket and splits into two little branches:<br>
One encodes H.264 and writes MP4 chunks around 5.5 seconds long using splitmux<br>
the other takes one frame per second and saves a JPEG.<br>


Every time a chunk or snapshot appears, we update symlinks:

```
drone_temp/latest_video.mp4
drone_temp/latest_image.jpg
```

This way, anything reading “the latest” never needs to scan directories.

## RTSP Worker

The RTSP path reads from its own SHM socket, runs `x264enc` with low‑latency settings (no B‑frames, keyframe ~1s), pushes the stream through `h264parse` (with regular SPS/PPS injection so late joiners sync fast), and hands payload to `rtph264pay` as `pay0`.

The server exposes the stream at `/live` on port **8554**.

Clients negotiate RTP/RTCP over UDP by default. If UDP is blocked, they fall back to TCP interleaving inside the RTSP connection. Latency rises, but the stream stays alive.

We use a shared media factory so **one encoder can serve many viewers** without extra CPU. A tiny leaky queue prevents buildup on short back‑pressure spikes.


## Controller / Watchdog

A small controller sits above everything. It spawns each worker, logs output, and includes a watchdog. If any worker dies, we shut the whole stack down cleanly and bring it up again, just enough to avoid long‑run stalls.



```bash
export SSD_PATH="$HOME/capture"
export ENABLE_RTSP=1
export ENABLE_VIDEO=1 ENABLE_IMAGES=1
export CAMERA="/dev/video0"
export VIDEO_FPS=30 VIDEO_WIDTH=1280 VIDEO_HEIGHT=720 VIDEO_BITRATE=2000000
python3 -m streamer.drone
```


One camera goes in, optional local storage is written out, and a clean RTSP URL comes out the other side<br>
low latency by default, UDP when available, TCP fallback when needed, and a small watchdog to keep everything alive.
