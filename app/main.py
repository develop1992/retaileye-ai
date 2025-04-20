from fastapi import FastAPI
from contextlib import asynccontextmanager
from threading import Thread
from app.routes import router
from app.services.rtmp_capture import capture_rtmp_stream
# from app.config import ENABLE_AUTO_RECORDING

# for automatic iVCam recording
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     if ENABLE_AUTO_RECORDING:
#         Thread(target=wait_for_ivcam_and_record, daemon=True).start()
#     yield
#     print("[INFO] FastAPI shutdown complete.")

# for RTMP stream capture
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start RTMP listener in background
    Thread(target=capture_rtmp_stream, daemon=True).start()
    yield
    print("[INFO] FastAPI shutdown complete.")

app = FastAPI(title="RetailEye AI Service", lifespan=lifespan)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "RetailEye AI backend is running!"}