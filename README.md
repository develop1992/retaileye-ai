# 🧠 RetailEye AI

FastAPI-based microservice for motion detection in recorded or live-streamed videos from surveillance cameras (e.g., iVCam). Uses OpenCV for motion detection and reports incidents to a Spring Boot backend.

---

## 📁 Project Structure

```plaintext
retaileye-ai/
├── app/
│   ├── main.py                  # FastAPI entrypoint
│   ├── config.py                # Environment variable loading
│   ├── routes.py                # API endpoints
│   ├── models/
│   │   └── incident.py          # Pydantic model for incidents
│   └── services/
│       ├── detect_motion.py     # Motion detection logic
│       ├── record.py            # Stream & record camera video
|       ├── watcher.py           # Watches for new recordings
│       └── send_incident.py     # Sends detected incidents to backend
├── .env                         # Contains RECORDINGS_DIR & INCIDENT_API_URL
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Motion Detection Flow
```flowchart TD
  A[IVCam (Phone)] --> B[PC Webcam Input]
  B --> C[record.py]
  C --> D[Video Saved in recordings/]
  D --> E[detect_motion.py]
  E --> F[Motion Events]
  F --> G[send_incident.py]
  G --> H[Spring Boot API - /incidents/bulk]
```

## API Endpoints
```graph LR
  A[FastAPI App] -->|GET| B[/]
  A -->|POST| C[/analyze-video]
  C --> D[Motion Detection]
  D --> E[Incident Bulk Send]
```

## .env Configuration
```flowchart TB
  A[.env file]
  A --> B[RECORDINGS_DIR]
  A --> C[INCIDENT_API_URL]
  B --> D[Used by record.py]
  C --> E[Used by send_incident.py]
```

## Installation Requirements Flow
```flowchart TD
  A[pip install -r requirements.txt]
  A --> B[fastapi]
  A --> C[uvicorn]
  A --> D[opencv-python]
  A --> E[requests]
  A --> F[python-dotenv]
  A --> G[keyboard]
```

## Running the Application
```bash
# Install dependencies
pip install -r requirements.txt
# Run the FastAPI app
uvicorn app.main:app --reload`
```