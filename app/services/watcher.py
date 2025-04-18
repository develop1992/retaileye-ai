import cv2
import time
from app.services.record import record_ivcam
from app.config import RECORDINGS_DIR  # ✅ imported from config

def wait_for_ivcam_and_record(poll_interval=5, max_attempts=30):
    attempts = 0
    while attempts < max_attempts:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("[INFO] iVCam is live. Starting recording...")
            cap.release()
            record_ivcam(RECORDINGS_DIR, duration_sec=10)
            return
        else:
            print(f"[INFO] iVCam not ready. Retrying in {poll_interval}s...")
            cap.release()
            time.sleep(poll_interval)
            attempts += 1

    print("[ERROR] iVCam feed was not detected after several attempts.")