import os
import time
import shutil
import pathlib
import logging

from google_drive_api import GoogleDriveAPI

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DRIVE_DIRECTORY = 'Samples'
CREDENTIALS_PATH = pathlib.Path('credentials.json')
# DOWNLOADS_DIR = pathlib.Path('/tmp/downloads')
DOWNLOADS_DIR = pathlib.Path('./downloads')
DOWNLOAD_INTERVAL = 60

# So i now have the API, so i periodically download everything, then rerun

def main():
    google_api = GoogleDriveAPI(CREDENTIALS_PATH)
    while True:
        logger.info('running again..')
        # shutil.move(DOWNLOADS_DIR, pathlib.Path(str(DOWNLOADS_DIR) + '_bak')))
        shutil.rmtree(DOWNLOADS_DIR)
        logger.info('deleted downloads directory')
        os.makedirs(DOWNLOADS_DIR)
        google_api.download_folder(DRIVE_DIRECTORY, DOWNLOADS_DIR)
        logger.info('downloaded again :)')
        logger.info(f'sleeping {DOWNLOAD_INTERVAL} seconds')
        time.sleep(DOWNLOAD_INTERVAL)



if __name__ == "__main__":
  main()