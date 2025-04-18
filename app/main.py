from fastapi import FastAPI
from contextlib import asynccontextmanager
from threading import Thread
from app.routes import router
from app.services.watcher import wait_for_ivcam_and_record

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start background thread (non-blocking)
    Thread(target=wait_for_ivcam_and_record, daemon=True).start()
    yield
    # (Optional) Add any shutdown logic here
    print("[INFO] FastAPI shutdown complete.")

app = FastAPI(title="RetailEye AI Service", lifespan=lifespan)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "RetailEye AI backend is running!"}