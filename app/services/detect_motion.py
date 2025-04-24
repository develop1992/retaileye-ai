import cv2
from datetime import datetime

def detect_motion(video_path, output_path=None):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return []

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    motion_events = []
    height, width = frame1.shape[:2]

    if output_path:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, 20.0, (width, height))
    else:
        out = None

    frame_count = 0
    while ret:
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        for contour in contours:
            if cv2.contourArea(contour) < 500:
                continue
            motion_detected = True
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

        timestamp = datetime.now().isoformat(timespec="seconds")

        if motion_detected:
            motion_events.append({
                "frame": frame_count,
                "timestamp": timestamp,
            })

        if out:
            out.write(frame1)

        frame1 = frame2
        ret, frame2 = cap.read()
        frame_count += 1

        if frame_count % 500 == 0:
            print(f"Processing frame {frame_count}...")

    cap.release()
    if out:
        out.release()

    return motion_events

def detect_motion_frame(prev_frame, curr_frame, frame_number):
    diff = cv2.absdiff(prev_frame, curr_frame)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=2)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False
    for contour in contours:
        if cv2.contourArea(contour) < 500:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(curr_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        motion_detected = True

    if motion_detected:
        return {
            "event": {
                "frame": frame_number,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
            },
            "frame": curr_frame
        }

    return {
        "event": None,
        "frame": curr_frame
    }