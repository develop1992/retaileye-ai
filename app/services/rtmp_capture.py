import subprocess
from datetime import datetime, timezone
import os
import time

import pytz

import cv2
from app.services.detect_motion import detect_motion_frame
from app.services.send_incident import send_incident
from app.services.send_recording import send_recording
from app.models.incident import Incident
from app.models.body_camera import BodyCamera
from app.models.recording import Recording

from typing import List

from app.config import RECORDINGS_DIR, RTMP_STREAM_URL

CAMERA_SERIAL_NUMBER = "CAMERA-001"  # Hardcoded serialNumber for body camera

# Initialize timezones
utc_timezone = pytz.utc
est_timezone = pytz.timezone("US/Eastern")

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

def record_and_detect_live(duration_sec=60):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(RECORDINGS_DIR, f"live_rtmp_{timestamp}.mp4")
    os.makedirs(RECORDINGS_DIR, exist_ok=True)

    cap = cv2.VideoCapture(RTMP_STREAM_URL)
    if not cap.isOpened():
        print("\n Failed to open RTMP stream!")
        return None

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 1280
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 720
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 25

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    print(f"\n Capturing and analyzing stream for {duration_sec}s...")

    ret, prev = cap.read()
    if not ret:
        print("\n No frame received from stream.")
        return None

    motion_events = []

    # Get start time in UTC and convert to EST
    start_time_utc = datetime.now(utc_timezone)
    start_time_est = start_time_utc.astimezone(est_timezone)

    start = time.time()
    frame_count = 0

    while time.time() - start < duration_sec:
        ret, frame = cap.read()
        if not ret:
            print("\n Dropped frame")
            break

        result = detect_motion_frame(prev, frame, frame_count)
        out.write(result["frame"])

        if result["event"]:
            motion_events.append(result["event"])
            print(f" Motion detected: {result['event']}")

        prev = frame
        frame_count += 1

    cap.release()
    out.release()

    # Get end time in UTC and convert to EST
    end_time_utc = datetime.now(utc_timezone)
    end_time_est = end_time_utc.astimezone(est_timezone)

    print(f"\n Video saved to: {output_path}")

    try:

        # 1. Send recording info
        file_name = os.path.basename(output_path)
        file_size = str(os.path.getsize(output_path))

        recording = Recording(
            filePath=output_path,
            fileName=file_name,
            fileType="video/mp4",
            fileSize=file_size,
            startTime=start_time_est,
            endTime=end_time_est,
            bodyCameraDto=BodyCamera(serialNumber=CAMERA_SERIAL_NUMBER),
        )

        recording_id = send_recording(recording)

        # 2. Send incidents if detected
        if motion_events:
            incidents: List[Incident] = [
                Incident(
                    occurrenceTime=event["timestamp"],
                    severity="Low",
                    status="Open",
                    description=f"Motion detected at frame {event['frame']}",
                    recordingDto=Recording(id=recording_id)
                )
                for event in motion_events
            ]
            send_incident(incidents)

    except Exception as e:
        print(f"\n Failed to send metadata: {e}")

    return output_path

def capture_rtmp_forever():
    print("\n Listening for RTMP streams forever...")

    while True:
        # Wait for stream to go live
        while not is_rtmp_stream_live(RTMP_STREAM_URL):
            print("[...] Still waiting...")
            time.sleep(2)

        # Run real-time detection + recording logic
        record_and_detect_live(duration_sec=60)

        # Small delay before checking again
        time.sleep(2)