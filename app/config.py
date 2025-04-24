import os
from dotenv import load_dotenv

load_dotenv()

RECORDINGS_DIR = os.getenv("RECORDINGS_PATH")
INCIDENT_API_URL = os.getenv("INCIDENT_API_URL")
ENABLE_AUTO_RECORDING = os.getenv("ENABLE_AUTO_RECORDING", "false").lower() == "true"
IVCAM_INDEX = int(os.getenv("IVCAM_INDEX", 1))
RTMP_STREAM_URL = os.getenv("RTMP_STREAM_URL")
RECORDING_API_URL = os.getenv("RECORDING_API_URL")

if not RECORDINGS_DIR:
    raise ValueError("RECORDINGS_PATH not found in .env file")

if not INCIDENT_API_URL:
    raise ValueError("INCIDENT_API_URL not found in .env file")

if not os.path.exists(ENABLE_AUTO_RECORDING):
    raise ValueError("ENABLE_AUTO_RECORDING not found in .env file")

if not os.path.exists(IVCAM_INDEX):
    raise ValueError("IVCAM_INDEX not found in .env file")

if not RTMP_STREAM_URL:
    raise ValueError("RTMP_STREAM_URL not found in .env file")