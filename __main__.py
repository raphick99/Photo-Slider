import os
import time
import shutil
import pathlib
import threading

from google_drive_api import GoogleDriveAPI

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DRIVE_DIRECTORY = 'Samples'
CREDENTIALS_PATH = pathlib.Path('credentials.json')
DOWNLOAD_INTERVAL = 60

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