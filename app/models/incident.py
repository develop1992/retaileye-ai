from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Incident(BaseModel):
    occurrenceTime: datetime
    severity: str
    status: str
    description: str