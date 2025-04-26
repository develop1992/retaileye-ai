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

# Hardcoded serial number for the body camera used in the system
CAMERA_SERIAL_NUMBER = "CAMERA-001"

# Initialize timezones
utc_timezone = pytz.utc
est_timezone = pytz.timezone("US/Eastern")

# Function to check if the RTMP stream is live
def is_rtmp_stream_live(url: str) -> bool:
    """
    Probes the RTMP stream using FFmpeg to check if the stream is live.

    Args:
        url (str): The RTMP stream URL to check.

    Returns:
        bool: True if the stream is live, False otherwise.
    """
    print(f"[DEBUG] Probing stream with ffmpeg at {url}")
    try:
        # Use ffmpeg to probe the stream
        result = subprocess.run([
            "C:/ffmpeg/bin/ffmpeg.exe",
            "-y", "-t", "1", "-i", url, "-f", "null", "-"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check if the stream is live based on the output from ffmpeg
        if "Press [q] to stop" in result.stderr or result.returncode == 0:
            print("\n Stream is LIVE")
            return True

        return False

    except Exception as e:
        print(f"\n Probe error: {e}")
        return False

# Function to record and detect motion in an RTMP stream
def record_and_detect_live(duration_sec=60):
    """
    Captures video from an RTMP stream, detects motion, and sends incidents to the backend.

    Args:
        duration_sec (int): The duration for recording and detecting motion in seconds.

    Returns:
        str: The path to the saved video file.
    """
    # Create a timestamp for the video file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(RECORDINGS_DIR, f"live_rtmp_{timestamp}.mp4")
    os.makedirs(RECORDINGS_DIR, exist_ok=True)  # Ensure the recordings directory exists

    # Initialize video capture from the RTMP stream
    cap = cv2.VideoCapture(RTMP_STREAM_URL)
    if not cap.isOpened():
        print("\n Failed to open RTMP stream!")
        return None

    # Get video frame properties like width, height, and FPS
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 1280
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 720
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 25

    # Prepare the video writer to save the captured video
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    print(f"\n Capturing and analyzing stream for {duration_sec}s...")

    # Read the first two frames
    ret, prev = cap.read()
    if not ret:
        print("\n No frame received from stream.")
        return None

    motion_events = []  # List to store detected motion events

    # Get start time in UTC and convert to EST
    start_time_utc = datetime.now(utc_timezone)
    start_time_est = start_time_utc.astimezone(est_timezone)

    start = time.time()
    frame_count = 0

    # Process video frames for the specified duration
    while time.time() - start < duration_sec:
        ret, frame = cap.read()
        if not ret:
            print("\n Dropped frame")
            break

        # Detect motion in the current frame
        result = detect_motion_frame(prev, frame, frame_count)
        out.write(result["frame"])  # Write the frame to output file

        # If motion is detected, add it to the list of motion events
        if result["event"]:
            motion_events.append(result["event"])
            print(f" Motion detected: {result['event']}")

        prev = frame  # Update the previous frame
        frame_count += 1

    # Release the video capture and writer objects
    cap.release()
    out.release()

    # Get end time in UTC and convert to EST
    end_time_utc = datetime.now(utc_timezone)
    end_time_est = end_time_utc.astimezone(est_timezone)

    print(f"\n Video saved to: {output_path}")

    try:
        # Send recording metadata to the backend
        file_name = os.path.basename(output_path)
        file_size = str(os.path.getsize(output_path))

        # Create the recording object with metadata
        recording = Recording(
            filePath=output_path,
            fileName=file_name,
            fileType="video/mp4",
            fileSize=file_size,
            startTime=start_time_est,
            endTime=end_time_est,
            bodyCameraDto=BodyCamera(serialNumber=CAMERA_SERIAL_NUMBER),
        )

        # Send the recording to the backend
        recording_id = send_recording(recording)

        # If motion events were detected, send them as incidents to the backend
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

# Function to continuously capture and analyze RTMP streams
def capture_rtmp_forever():
    """
    Continuously listens for an RTMP stream to become available, then captures and analyzes it.
    This function runs indefinitely.
    """
    print("\n Listening for RTMP streams forever...")

    while True:
        # Wait for the RTMP stream to go live
        while not is_rtmp_stream_live(RTMP_STREAM_URL):
            print("[...] Still waiting...")
            time.sleep(2)

        # Run the motion detection and recording logic when the stream is live
        record_and_detect_live(duration_sec=60)

        # Small delay before checking again
        time.sleep(2)