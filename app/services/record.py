import cv2
import datetime
import os
from app.config import IVCAM_INDEX  # Camera index configured in the config

# Function to record video from the camera for a given duration
def record_ivcam(output_dir: str, duration_sec: int = 10) -> str:
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Open the camera using the specified index from the configuration (IVCAM_INDEX)
    cap = cv2.VideoCapture(IVCAM_INDEX)

    # Check if the camera was opened successfully
    if not cap.isOpened():
        raise RuntimeError(f"Could not access camera at index {IVCAM_INDEX}.")

    # Get the camera's frame width, height, and frames per second (fps)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # Frame width
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Frame height
    fps = cap.get(cv2.CAP_PROP_FPS) or 30  # Default fps is 30 if not available

    # Generate a timestamped filename for the recorded video
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recorded_{timestamp}.mp4"

    # Create the full output path where the video will be saved
    output_path = os.path.join(output_dir, filename)

    # Define the video codec and initialize the VideoWriter to save the video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' codec for MP4 file
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Initialize frame count and calculate maximum number of frames to record based on duration
    frame_count = 0
    max_frames = int(fps * duration_sec)  # Total frames = fps * duration in seconds

    # Start capturing frames from the camera and writing them to the video file
    while frame_count < max_frames:
        ret, frame = cap.read()  # Capture a frame from the camera
        if not ret:
            break  # Stop recording if there's an issue capturing frames

        # Write the captured frame to the video file
        out.write(frame)
        frame_count += 1  # Increment frame count

    # Release the video capture and writer objects
    cap.release()
    out.release()

    # Return the path to the saved video file
    return output_path