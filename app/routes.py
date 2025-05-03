from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from app.models.recording import Recording
from app.services.detect_motion import detect_motion
from app.services.send_incident import send_incident
from app.config import RECORDINGS_DIR
from app.models.incident import Incident
import os
from fastapi import HTTPException

import pytz

from app.services.send_recording import send_recording

# Initialize timezones
utc_timezone = pytz.utc
est_timezone = pytz.timezone("US/Eastern")

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
        # Get start time in UTC and convert to EST
        start_time_utc = datetime.now(utc_timezone)
        start_time_est = start_time_utc.astimezone(est_timezone)

        motion_events = detect_motion(input_path, output_path)

        # Get end time in UTC and convert to EST
        end_time_utc = datetime.now(utc_timezone)
        end_time_est = end_time_utc.astimezone(est_timezone)

        # Send recording metadata to the backend
        file_name = os.path.basename(output_path)
        file_size = str(os.path.getsize(output_path))

        # Create the recording object with metadata
        recording = Recording(
            filePath=output_path,
            fileName=file_name,
            fileType="video/mp4",
            fileSize=file_size,
            startTime=start_time_est,
            endTime=end_time_est,
            isAnalyzed=True
        )

        # Send the recording to the backend
        recording_id = send_recording(recording)

        incidents: List[Incident] = [
            Incident(
                occurrenceTime=event["timestamp"],
                severity="Low",
                status="Open",
                description=f"Motion detected at frame {event['frame']}",
                recordingDto = Recording(id=recording_id)
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