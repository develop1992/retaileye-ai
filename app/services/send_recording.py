import requests
import json
from datetime import datetime
from pydantic import BaseModel
from app.config import RECORDING_API_URL

def convert_to_json_serializable(obj):
    if isinstance(obj, BaseModel):
        obj = obj.model_dump()

    def default_serializer(o):
        if isinstance(o, datetime):
            return o.replace(tzinfo=None).isoformat()  # remove timezone before formatting
        raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")

    return json.loads(json.dumps(obj, default=default_serializer))

def send_recording(recording):
    try:
        payload = convert_to_json_serializable(recording)

        res = requests.post(RECORDING_API_URL, json=payload, timeout=20)
        res.raise_for_status()
        data = res.json()
        recording_id = data.get("id")

        print(f"\n Recording saved successfully to backend. ID: {recording_id}")
        return recording_id
    except Exception as e:
        print(f"\n Failed to save recording: {e}")
        return None