import pathlib
from google_drive_api import GoogleDriveAPI

DRIVE_DIRECTORY = 'Samples'
CREDENTIALS_PATH = pathlib.Path('credentials.json')
# DOWNLOADS_DIR = pathlib.Path('/tmp/downloads')
DOWNLOADS_DIR = pathlib.Path('./downloads')

def main():
    api = GoogleDriveAPI(CREDENTIALS_PATH)
    folders = api.list_folder(DRIVE_DIRECTORY)
    print(folders)
    api.download_file('bird.jpg', DOWNLOADS_DIR / 'bird.jpg')


if __name__ == "__main__":
  main()