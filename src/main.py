import argparse
import pathlib
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from loguru import logger

from maintainer import Maintainer
from models import PhotoResponse, RuntimeConfig

maintainer: Maintainer | None = None


@asynccontextmanager
async def lifespan(_app: FastAPI):
    global maintainer
    maintainer = Maintainer(bucket_name='ickovics-home')
    logger.info('Starting maintainer')
    maintainer.start()
    yield
    maintainer.stop()
    logger.info('Maintainer stopped')


app = FastAPI(lifespan=lifespan)


@app.get('/photos/next')
async def get_next_photo_endpoint() -> PhotoResponse:
    photo_url = await maintainer.get_next_photo()
    logger.info('Getting next photo', photo_id=photo_url)
    if not photo_url:
        raise HTTPException(status_code=404, detail='No photos available')
    return PhotoResponse(photo_url=photo_url)


@app.get('/configuration')
async def get_configuration() -> RuntimeConfig:
    return RuntimeConfig(display_time=1)


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
    uvicorn.run('main:app', host=host, port=9000, reload=args.debug)
