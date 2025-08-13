from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.api import router as api_router

app = FastAPI(title="JobFinderPro API")

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "JobFinderPro API is running"}

@app.get("/api/health")
async def health():
    return {"status": "ok"}