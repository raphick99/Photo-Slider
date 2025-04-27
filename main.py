from fastapi import FastAPI
import uvicorn
from google_drive_api import GoogleDriveAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to Photo Slider API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
