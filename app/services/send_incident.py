import requests
from app.config import INCIDENT_API_URL

def send_incident(incidents):
    try:
        response = requests.post(INCIDENT_API_URL, json=incidents, timeout=30)
        response.raise_for_status()
        print(f"\n Sent {len(incidents)} incidents in bulk.")
    except Exception as e:
        print(f"\n Failed to send bulk incidents: {e}")