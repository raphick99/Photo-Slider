import os
import time
import shutil
import logging
import pathlib
import tempfile

from google_drive_api import GoogleDriveAPI

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DRIVE_DIRECTORY = 'Samples'
CREDENTIALS_PATH = pathlib.Path('credentials.json')
# todo: move to config file
# DOWNLOADS_DIR = pathlib.Path('/tmp/downloads')
DOWNLOADS_DIR = pathlib.Path('./downloads')
DOWNLOAD_INTERVAL = 60

def download_photos():
    google_api = GoogleDriveAPI(CREDENTIALS_PATH)
    while True:
        with tempfile.TemporaryDirectory() as tempdir:
            tempdir = pathlib.Path(tempdir)
            google_api.download_folder(DRIVE_DIRECTORY, tempdir)
            if DOWNLOADS_DIR.exists():
                shutil.rmtree(DOWNLOADS_DIR)
            os.makedirs(DOWNLOADS_DIR)
            os.rename(tempdir, DOWNLOADS_DIR)
            
        logger.info('downloaded again :)')
        logger.info(f'sleeping {DOWNLOAD_INTERVAL} seconds')
        time.sleep(DOWNLOAD_INTERVAL)


def main():
    logger.info('starting photo downloading..')
    try:
        download_photos()
    except BaseException as e:
        logger.error(f'caught exception! {e}')


if __name__ == "__main__":
    main()
