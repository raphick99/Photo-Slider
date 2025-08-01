import argparse
import pathlib
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

import config
from models import PhotoResponse, RuntimeConfig
from photo_scheduler import PhotoScheduler
from setup_logging import setup_logging

scheduler: PhotoScheduler | None = None


@asynccontextmanager
async def lifespan(_app: FastAPI):
    setup_logging()
    global scheduler
    scheduler = PhotoScheduler(bucket_name=config.BUCKET_NAME, fetch_interval=config.FETCH_INTERVAL)
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/photos/next')
async def get_next_photo_endpoint() -> PhotoResponse:
    photo_url = await scheduler.get_next_photo()
    if not photo_url:
        raise HTTPException(status_code=404, detail='No photos available')
    return PhotoResponse(photo_url=photo_url)


@app.get('/configuration')
async def get_configuration() -> RuntimeConfig:
    return RuntimeConfig(display_time=config.DISPLAY_TIME)


@app.get('/')
async def start_photo_slide():
    current_dir = pathlib.Path(__file__).parent
    file_path = current_dir / 'www/index.html'
    return FileResponse(file_path, media_type='text/html')


def parse_args():
    parser = argparse.ArgumentParser(description='Run the FastAPI server.')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    host = '0.0.0.0' if not args.debug else 'localhost'  # noqa: S104
    uvicorn.run('main:app', host=host, port=8080, reload=args.debug)
