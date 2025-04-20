from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.detect_motion import detect_motion
from app.services.send_incident import send_incident
from app.config import RECORDINGS_DIR
from app.models.incident import Incident
import os
from fastapi import HTTPException

router = APIRouter()

class AnalyzeRequest(BaseModel):
    filename: str

class AnalyzeResponse(BaseModel):
    message: str
    motion_events: int
    annotated_output: str

@router.post("/analyze-video", response_model=AnalyzeResponse, tags=["AI"])
def analyze_video(request: AnalyzeRequest) -> AnalyzeResponse:
    input_path = os.path.join(RECORDINGS_DIR, request.filename)
    output_path = os.path.join(RECORDINGS_DIR, f"annotated_{request.filename}")

    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail=f"File {request.filename} not found.")

    try:
        motion_events = detect_motion(input_path, output_path)

        incidents: List[Incident] = [
            Incident(
                occurrenceTime=event["timestamp"],
                severity="Low",
                status="Open",
                description=f"Motion detected at frame {event['frame']}"
            )
            for event in motion_events
        ]

        send_incident(incidents)

        return AnalyzeResponse(
            message="Video analysis complete. Motion events detected.",
            motion_events=len(motion_events),
            annotated_output=output_path
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred during analysis: {str(e)}")