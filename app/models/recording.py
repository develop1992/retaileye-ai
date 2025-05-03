from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.models.body_camera import BodyCamera

class Recording(BaseModel):
    id: Optional[str] = None
    filePath: Optional[str] = None
    fileName: Optional[str] = None
    fileType: Optional[str] = None
    fileSize: Optional[str] = None
    startTime: Optional[datetime] = None
    endTime: Optional[datetime] = None
    isAnalyzed: Optional[bool] = None
    bodyCameraDto: Optional[BodyCamera] = None