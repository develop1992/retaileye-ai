import subprocess
import datetime
import os
from app.config import RECORDINGS_DIR, RTMP_STREAM_URL

def capture_rtmp_stream(duration_sec=60, prebuffer_sec=3):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(RECORDINGS_DIR, f"rtmp_recorded_{timestamp}.mkv")
    os.makedirs(RECORDINGS_DIR, exist_ok=True)

    command = [
        "C:/ffmpeg/bin/ffmpeg.exe",
        "-y",
        "-rw_timeout", "5000000",  # wait for RTMP readiness
        "-i", RTMP_STREAM_URL,
        "-t", str(duration_sec + prebuffer_sec),  # add buffer time to capture more
        "-c", "copy",
        "-movflags", "+faststart",
        output_path
    ]

    print(f"\n Starting RTMP capture to: {output_path}\n")

    try:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for line in proc.stdout:
            print(line.strip())  # Print live FFmpeg output (optional but helpful)

        proc.wait()

        if proc.returncode == 0:
            print(f"\n Saved RTMP recording to: {output_path}")
            return output_path
        else:
            print(f"\n FFmpeg exited with error code {proc.returncode}")
            return None

    except Exception as e:
        print(f"\n Failed to capture RTMP stream: {e}")
        return None