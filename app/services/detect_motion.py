import cv2
from datetime import datetime

# Function to detect motion in a video file
def detect_motion(video_path, output_path=None):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return []

    # Read the first two frames from the video
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    # Initialize list to store motion events
    motion_events = []
    height, width = frame1.shape[:2]  # Get the frame height and width

    # Prepare the video writer if an output path is specified
    if output_path:
        fourcc = cv2.VideoWriter_fourcc(*'avc1')  # Define video codec
        out = cv2.VideoWriter(output_path, fourcc, 20.0, (width, height))
    else:
        out = None  # No output video

    # Initialize frame counter
    frame_count = 0

    # Loop through all the frames in the video
    while ret:
        # Calculate the absolute difference between two frames
        diff = cv2.absdiff(frame1, frame2)

        # Convert the difference image to grayscale for easier processing
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to smooth the image and reduce noise
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Threshold the blurred image to create a binary image
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

        # Dilate the binary image to fill in gaps and make contours more prominent
        dilated = cv2.dilate(thresh, None, iterations=2)

        # Find contours in the dilated image
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False  # Flag to check if motion is detected

        # Iterate over contours and filter out small ones that aren't significant
        for contour in contours:
            if cv2.contourArea(contour) < 500:  # Ignore small contours
                continue
            motion_detected = True
            (x, y, w, h) = cv2.boundingRect(contour)  # Get bounding box for each contour
            # Draw rectangle around the detected motion area
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Record the timestamp when motion is detected
        timestamp = datetime.now().isoformat(timespec="seconds")

        if motion_detected:
            # Store the frame and timestamp of the detected motion
            motion_events.append({
                "frame": frame_count,
                "timestamp": timestamp,
            })

        # Write the frame with bounding boxes (if output video path is specified)
        if out:
            out.write(frame1)

        # Move to the next frame
        frame1 = frame2
        ret, frame2 = cap.read()
        frame_count += 1

        # Print progress every 500 frames
        if frame_count % 500 == 0:
            print(f"Processing frame {frame_count}...")

    # Release the video capture and output writer objects
    cap.release()
    if out:
        out.release()

    return motion_events  # Return list of detected motion events


# Function to detect motion in individual video frames (used in live processing)
def detect_motion_frame(prev_frame, curr_frame, frame_number):
    # Calculate the absolute difference between the previous and current frames
    diff = cv2.absdiff(prev_frame, curr_frame)

    # Convert the difference image to grayscale
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold the image to create a binary image for better contour detection
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # Dilate the thresholded image to fill in contours
    dilated = cv2.dilate(thresh, None, iterations=2)

    # Find contours in the dilated image
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False  # Flag to indicate if motion is detected

    # Iterate over contours and filter out small ones
    for contour in contours:
        if cv2.contourArea(contour) < 500:  # Ignore small contours
            continue
        (x, y, w, h) = cv2.boundingRect(contour)  # Get bounding box for each contour
        # Draw a rectangle around the detected motion area
        cv2.rectangle(curr_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        motion_detected = True

    # If motion was detected, return the event and the modified frame
    if motion_detected:
        return {
            "event": {
                "frame": frame_number,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
            },
            "frame": curr_frame
        }

    # If no motion detected, return the current frame with no event
    return {
        "event": None,
        "frame": curr_frame
    }