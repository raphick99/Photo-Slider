import os
import time
import shutil
import pathlib
import logging
import threading
import subprocess

from google_drive_api import GoogleDriveAPI

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DRIVE_DIRECTORY = 'Samples'
CREDENTIALS_PATH = pathlib.Path('credentials.json')
# DOWNLOADS_DIR = pathlib.Path('/tmp/downloads')
DOWNLOADS_DIR = pathlib.Path('./downloads')
DOWNLOAD_INTERVAL = 60
SLIDESHOW_DELAY = 1

# So i now have the API, so i periodically download everything, then rerun

def download_photos():
    google_api = GoogleDriveAPI(CREDENTIALS_PATH)
    while True:
        if DOWNLOADS_DIR.exists():
            shutil.rmtree(DOWNLOADS_DIR)
        os.makedirs(DOWNLOADS_DIR)
        google_api.download_folder(DRIVE_DIRECTORY, DOWNLOADS_DIR)
        logger.info('downloaded again :)')
        logger.info(f'sleeping {DOWNLOAD_INTERVAL} seconds')
        time.sleep(DOWNLOAD_INTERVAL)


def display_photos():
    while True:
        command = (
            'feh '
            '--auto-zoom '
            '--fullscreen '
            '--borderless '
            '--hide-pointer '  # check that this works
            f'--slideshow-delay={SLIDESHOW_DELAY} '
            f'{DOWNLOADS_DIR}/*'
        )
        logger.info(f'executing: {command}')
        subprocess.run(command, shell=True)


def main():
    logger.info('starting photo downloading..')
    display_photos_thread = threading.Thread(target=display_photos)
    # download_photos_thread = threading.Thread(target=download_photos)

    # download_photos_thread.start()
    display_photos_thread.start()

    # display_photos_thread.join()
    # download_photos_thread.join()
    download_photos()


if __name__ == "__main__":
  main()