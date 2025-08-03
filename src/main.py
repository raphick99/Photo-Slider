import argparse
import pathlib
from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from loguru import logger

import config
from models import PhotoResponse, RuntimeConfig
from photo_scheduler import PhotoScheduler
from setup_logging import setup_logging


@asynccontextmanager
async def lifespan(_app: FastAPI):
    setup_logging()
    yield


tenant_schedulers: dict[str, PhotoScheduler] = {}
template_dir = pathlib.Path(__file__).parent / 'templates'
templates = Jinja2Templates(directory=template_dir)
app = FastAPI(lifespan=lifespan)


async def get_or_create_scheduler(tenant_id: str) -> PhotoScheduler:
    """Get existing scheduler for tenant or create a new one."""
    global tenant_schedulers
    if tenant_id not in tenant_schedulers:
        tenant_schedulers[tenant_id] = PhotoScheduler(
            bucket_name=config.BUCKET_NAME,
            fetch_interval=config.FETCH_INTERVAL,
            tenant_id=tenant_id,
        )
    return tenant_schedulers[tenant_id]


@app.get('/photos/next')
async def get_next_photo_endpoint(tenant_id: Annotated[str, Header(alias='X-TENANT-ID')]) -> PhotoResponse:
    logger.info('Photo request received', tenant_id=tenant_id)
    scheduler = await get_or_create_scheduler(tenant_id)
    photo_url = await scheduler.get_next_photo()
    if not photo_url:
        logger.warning('No photos available for tenant', tenant_id=tenant_id)
        raise HTTPException(status_code=404, detail='No photos available')
    logger.info('Returning photo URL to client', tenant_id=tenant_id, url_domain=photo_url.split('?')[0].split('/')[-3:] if '?' in photo_url else 'unknown')
    return PhotoResponse(photo_url=photo_url)


@app.get('/configuration')
async def get_configuration(_tenant_id: Annotated[str, Header(alias='X-TENANT-ID')]) -> RuntimeConfig:
    return RuntimeConfig(display_time=config.DISPLAY_TIME)


@app.get('/')
async def start_photo_slide(request: Request, tenant_id: str) -> HTMLResponse:
    return templates.TemplateResponse('index.html', {'request': request, 'tenant_id': tenant_id})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Run the FastAPI server.')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    host = '0.0.0.0' if not args.debug else 'localhost'  # noqa: S104
    uvicorn.run('main:app', host=host, port=8080, reload=args.debug)
