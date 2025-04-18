from fastapi import APIRouter
from pydantic import BaseModel
from app.services.detect_motion import detect_motion
from app.services.send_incident import send_incident
import os
from app.config import RECORDINGS_DIR

router = APIRouter()

class AnalyzeRequest(BaseModel):
    filename: str  # Relative to your recordings directory

@router.post("/analyze-video")
def analyze_video(request: AnalyzeRequest):
    input_path = os.path.join(RECORDINGS_DIR, request.filename)
    output_path = os.path.join(RECORDINGS_DIR, f"annotated_{request.filename}")

    if not os.path.exists(input_path):
        return {"error": f"File {request.filename} not found."}

    try:
        motion_events = detect_motion(input_path, output_path)

        incidents = [
            {
                "occurrenceTime": event["timestamp"],
                "severity": "Low",
                "status": "Open",
                "description": f"Motion detected at frame {event['frame']}"
            }
            for event in motion_events
        ]

        send_incident(incidents)

        return {
            "message": "Video analysis complete",
            "motion_events": len(motion_events),
            "annotated_output": output_path
        }
    except Exception as e:
        return {"error": str(e)}