from pydantic import BaseModel
from datetime import datetime

from app.models.recording import Recording

class Incident(BaseModel):
    occurrenceTime: datetime
    severity: str
    status: str
    description: str
    recordingDto: Recording