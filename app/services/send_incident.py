import requests
import json
from app.config import INCIDENT_API_URL
from datetime import datetime
from pydantic import BaseModel

def convert_to_json_serializable(obj):
    if isinstance(obj, BaseModel):
        obj = obj.model_dump()

    def default_serializer(o):
        if isinstance(o, datetime):
            return o.isoformat()
        raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")

    return json.loads(json.dumps(obj, default=default_serializer))

def send_incident(incidents):
    try:
        payload = [convert_to_json_serializable(i) for i in incidents]

        response = requests.post(INCIDENT_API_URL, json=payload, timeout=30)
        response.raise_for_status()
        print(f"\n Sent {len(payload)} incidents in bulk.")
    except Exception as e:
        print(f"\n Failed to send bulk incidents: {e}")