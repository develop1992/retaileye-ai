import cv2
import datetime
import os
from app.config import IVCAM_INDEX

def record_ivcam(output_dir: str, duration_sec: int = 10) -> str:
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(IVCAM_INDEX)

    if not cap.isOpened():
        raise RuntimeError(f"Could not access camera at index {IVCAM_INDEX}.")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recorded_{timestamp}.mp4"
    output_path = os.path.join(output_dir, filename)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0
    max_frames = int(fps * duration_sec)

    while frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        out.write(frame)
        frame_count += 1

    cap.release()
    out.release()

    return output_path