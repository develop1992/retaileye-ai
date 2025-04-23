import subprocess
import datetime
import os
import time
from app.config import RECORDINGS_DIR, RTMP_STREAM_URL

def is_rtmp_stream_live(url: str) -> bool:
    print(f"[DEBUG] Probing stream with ffmpeg at {url}")
    try:
        result = subprocess.run([
            "C:/ffmpeg/bin/ffmpeg.exe",
            "-y",
            "-t", "1",
            "-i", url,
            "-f", "null", "-"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if "Press [q] to stop" in result.stderr or result.returncode == 0:
            print("\n Stream is LIVE")
            return True

        return False

    except Exception as e:
        print(f"\n Probe error: {e}")
        return False

def record_once(duration_sec=60, prebuffer_sec=3):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(RECORDINGS_DIR, f"rtmp_recorded_{timestamp}.mkv")
    os.makedirs(RECORDINGS_DIR, exist_ok=True)

    command = [
        "C:/ffmpeg/bin/ffmpeg.exe",
        "-y",
        "-rw_timeout", "5000000",
        "-i", RTMP_STREAM_URL,
        "-t", str(duration_sec + prebuffer_sec),
        "-c", "copy",
        "-movflags", "+faststart",
        output_path
    ]

    print(f"\n Starting capture to: {output_path}")

    try:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in proc.stdout:
            print(line.strip())

        proc.wait()

        if proc.returncode == 0:
            print(f"\n Saved to: {output_path}")
        else:
            print(f"\n FFmpeg exited with code {proc.returncode}")

    except Exception as e:
        print(f"\n Failed to record: {e}")

def capture_rtmp_forever():
    print("\n Listening for RTMP streams forever...")

    while True:
        # Wait for stream to go live
        while not is_rtmp_stream_live(RTMP_STREAM_URL):
            print("[...] Still waiting...")
            time.sleep(2)

        # Start one capture session
        record_once(duration_sec=60)

        # Small delay before checking again
        time.sleep(2)