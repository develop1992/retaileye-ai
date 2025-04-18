import keyboard  # NEW
import cv2
import datetime
import os

output_dir = r"C:\Users\bahra\OneDrive\Desktop\School\CS 4366\recordings"
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Camera not accessible.")
    exit()

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS) or 30

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"recorded_{timestamp}.mp4"
output_path = os.path.join(output_dir, filename)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

print("[INFO] Recording... Press 'q' to stop.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        out.write(frame)

        if keyboard.is_pressed('q'):
            print("[INFO] 'q' pressed. Exiting recording.")
            break

except KeyboardInterrupt:
    print("\n[INFO] KeyboardInterrupt received. Exiting...")

finally:
    cap.release()
    out.release()
    print(f"[INFO] Saved to: {output_path}")