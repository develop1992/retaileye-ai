from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Incident(BaseModel):
    occurrenceTime: datetime
    severity: str
    status: str
    description: str
    recordingDto: Optional[dict] = None
    managerDto: Optional[dict] = None