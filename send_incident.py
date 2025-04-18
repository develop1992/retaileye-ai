import requests

def send_incident(incidents):
    try:
        response = requests.post("https://d700-47-19-81-210.ngrok-free.app/retaileye/incidents/bulk", json=incidents, timeout=30)
        response.raise_for_status()
        print(f"\n {len(incidents)} incidents sent in bulk.")
    except Exception as e:
        print(f"\n Failed to send bulk incidents: {e}")
