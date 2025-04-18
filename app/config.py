import os
from dotenv import load_dotenv

load_dotenv()

RECORDINGS_DIR = os.getenv("RECORDINGS_PATH")
INCIDENT_API_URL = os.getenv("INCIDENT_API_URL")

if not RECORDINGS_DIR:
    raise ValueError("RECORDINGS_PATH not found in .env file")

if not INCIDENT_API_URL:
    raise ValueError("INCIDENT_API_URL not found in .env file")