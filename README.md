
# RetailEye AI - Motion Detection and Incident Reporting

RetailEye AI is a motion detection system designed to monitor surveillance footage in real time. Built with **FastAPI**, and **OpenCV**. The system processes live-streamed videos and recorded footage to detect motion and send incidents and recordings to [RetailEye API](https://github.com/develop1992/retaileye-api). This project is designed for retail security applications where surveillance data needs to be analyzed in real time for suspicious activity.

## Key Features

- **Real-time Motion Detection**: Capture and analyze video streams or recordings to detect motion using **OpenCV**.
- **Incident Reporting**: When motion is detected, incidents are reported to a backend system for logging and further analysis.
- **Video Recording**: Record live video footage for incident documentation and future reference.
- **API Integration**: Integrates with [RetailEye API](https://github.com/develop1992/retaileye-api) to send recorded video data and detected incidents.

## Folder Structure

### `app/main.py`
Contains the entry point for the FastAPI application. It initializes routes, connects to backend APIs, and handles the motion detection process.

### `app/config.py`
Contains application configurations like video recording directory and RTMP stream URL.

### `app/routes.py`
Defines the FastAPI routes that handle incoming requests for starting the motion detection process.

### `app/models/`
Contains the data models used within the application.

#### `incident.py`
Defines the **IncidentDto** model representing the detected incidents, including details like **occurrence time**, **severity**, and **description**.

#### `body_camera.py`
Defines the **BodyCamera** model representing the body cameras used to capture video footage.

#### `recording.py`
Defines the **RecordingDto** model for managing video files captured during the motion detection process.

### `app/services/`
Contains the core business logic of the application, including motion detection, recording, and incident reporting.

#### `detect_motion.py`
The core of the motion detection logic. Uses **OpenCV** to compare video frames and identify significant changes indicating motion.

##### `detect_motion_frame` Algorithm:
The `detect_motion_frame` function works by comparing the **previous frame** to the **current frame**. The following steps describe the process:

1. **Frame Difference**: First, the absolute difference between the current and previous frames is calculated using `cv2.absdiff()`.
2. **Convert to Grayscale**: The resulting frame difference is then converted to grayscale using `cv2.cvtColor()`.
3. **Apply Gaussian Blur**: A **Gaussian blur** is applied using `cv2.GaussianBlur()` to reduce noise and enhance detection accuracy.
4. **Thresholding**: A threshold is applied with `cv2.threshold()` to binarize the image, where motion areas are highlighted as white pixels.
5. **Dilation**: The threshold image is dilated using `cv2.dilate()` to fill gaps in the contours of detected motion.
6. **Contour Detection**: `cv2.findContours()` is used to identify areas of the image where motion is occurring. These contours represent regions of interest.
7. **Bounding Box**: For each contour, if its area exceeds a threshold (500 pixels in this case), a bounding box is drawn around the detected motion.
8. **Motion Detection**: If any contours are large enough, motion is detected, and the event is logged.

The function returns a dictionary with information about the **motion event** (e.g., timestamp and frame number) and the **updated frame** with the bounding boxes drawn around detected motion.

#### `send_incident.py`
Handles the process of sending detected incidents to the backend API for further logging and processing.

#### `send_recording.py`
Handles sending video recording metadata (such as file path, file name, and size) to the backend API.

#### `rtmp_capture.py`
Handles capturing video streams, recording them, and invoking the motion detection service.

## How to Run

### Prerequisites
Ensure the following software is installed:
- Python 3.x
- FastAPI
- OpenCV
- Uvicorn (ASGI server)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/develop1992/retaileye-ai.git
   cd retaileye-ai
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI application:
   ```bash
   uvicorn app.main:app --reload
   ```

   The application will be available at `http://127.0.0.1:8000`.

### Configuration

- **RTMP Stream URL**: Configure the RTMP stream URL from which the video feed will be captured.
- **Recording Directory**: Set the directory where the recorded videos will be stored.

## API Documentation

Once the app is running, you can access the **Swagger UI** for API documentation at:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Technologies Used
- **FastAPI**: For building the REST API service.
- **OpenCV**: For motion detection and video frame manipulation.
- **RTMP**: For handling live video streams.
- **Uvicorn**: ASGI server for serving the FastAPI application.

## Future Work
- Improve motion detection accuracy with machine learning models.
- Add user authentication and authorization.
- Implement real-time alerting and notifications.