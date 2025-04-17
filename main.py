import sys
from detect_motion import detect_motion
from send_incident import send_incident
import time

if __name__ == "__main__":
    video_file = sys.argv[1]
    output_file = "annotated_" + video_file

    motion_events = detect_motion(video_file, output_file)

    print(f"\n Finished. {len(motion_events)} motion events detected.")

    incidents = [
        {
            "occurrenceTime": event["timestamp"],
            "severity": "Low",
            "status": "Open",
            "description": f"Motion detected at frame {event['frame']}"
        }
        for event in motion_events
    ]

    send_incident(incidents)