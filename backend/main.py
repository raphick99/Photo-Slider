import argparse
import pathlib
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from loguru import logger

from google_drive_api import GoogleDriveAPI
from maintainer import Maintainer
from models import RuntimeConfig

google_api: GoogleDriveAPI | None = None
LOCAL_PHOTOS_PATH = pathlib.Path('./photos')
DRIVE_PHOTOS_FOLDER = 'Samples'
CREDENTIALS_PATH = pathlib.Path('credentials.json')


maintainer: Maintainer | None = None


@asynccontextmanager
async def lifespan(_app: FastAPI):
    if not LOCAL_PHOTOS_PATH.exists():
        LOCAL_PHOTOS_PATH.mkdir(parents=True)
    global google_api, maintainer
    google_api = GoogleDriveAPI(CREDENTIALS_PATH)
    maintainer = Maintainer(google_api, LOCAL_PHOTOS_PATH, DRIVE_PHOTOS_FOLDER)
    logger.info('Starting maintainer')
    maintainer.start()
    logger.info('Maintainer started')
    yield
    maintainer.stop()
    logger.info('Maintainer stopped')


app = FastAPI(lifespan=lifespan)


class PhotoNotFoundError(Exception):
    pass


@app.get('/photos/next')
async def get_next_photo_endpoint() -> FileResponse:
    photo_path = maintainer.get_next_photo()
    logger.info('Getting next photo', photo_id=photo_path)
    if not photo_path:
        raise HTTPException(status_code=404, detail='No photos available')
    if not (photo_path).exists():
        raise PhotoNotFoundError()
    return FileResponse(photo_path)


@app.get('/configuration')
async def get_configuration() -> RuntimeConfig:
    return RuntimeConfig(display_time=10)


@app.get('/photos-slide')
async def photo_slide():
    return FileResponse('frontend/photo_slide.html', media_type='text/html')



def parse_args():
    parser = argparse.ArgumentParser(description='Run the FastAPI server.')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    host = '0.0.0.0' if not args.debug else 'localhost'
    uvicorn.run('main:app', host=host, port=9000, reload=args.debug)
