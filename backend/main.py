import pathlib
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from loguru import logger

from google_drive_api import GoogleDriveAPI
from maintainer import Maintainer
from models import RuntimeConfig

google_api: GoogleDriveAPI | None = None
LOCAL_PHOTOS_PATH = pathlib.Path('./photos')
DRIVE_PHOTOS_FOLDER = 'Samples'
CREDENTIALS_PATH = pathlib.Path('credentials.json')


@asynccontextmanager
async def lifespan(_app: FastAPI):
	if not LOCAL_PHOTOS_PATH.exists():
		LOCAL_PHOTOS_PATH.mkdir(parents=True)
	global google_api
	google_api = GoogleDriveAPI(CREDENTIALS_PATH)
	maintainer = Maintainer(google_api, LOCAL_PHOTOS_PATH, DRIVE_PHOTOS_FOLDER)
	logger.info('Starting maintainer')
	maintainer.start()
	logger.info('Maintainer started')
	yield


app = FastAPI(lifespan=lifespan)


@app.get('/photos')
async def get_photos() -> list[str]:
	return google_api.list_folder(DRIVE_PHOTOS_FOLDER)


@app.get('/photos/{photo_id}')
async def get_photo(photo_id: str) -> FileResponse:
	if not (LOCAL_PHOTOS_PATH / photo_id).exists():
		google_api.download_file(photo_id, LOCAL_PHOTOS_PATH / photo_id)
	return FileResponse(LOCAL_PHOTOS_PATH / photo_id)


@app.get('/photos/refresh')
async def refresh_photos():
	google_api.download_folder(DRIVE_PHOTOS_FOLDER, LOCAL_PHOTOS_PATH)
	return {'message': 'Photos refreshed'}


@app.get('/configuration')
async def get_configuration() -> RuntimeConfig:
	return RuntimeConfig(refresh_interval=60)


@app.get('/photos-slide')
async def photo_slide():
    return FileResponse('frontend/photo_slide.html', media_type='text/html')



if __name__ == '__main__':
	uvicorn.run('main:app', host='0.0.0.0', port=9000, reload=True)
