import pathlib
from google_drive_api import GoogleDriveAPI

DRIVE_DIRECTORY = 'Samples'
CREDENTIALS_PATH = pathlib.Path('credentials.json')
# DOWNLOADS_DIR = '/tmp/downloads'
DOWNLOADS_DIR = './downloads'

def main():
    try:
        api = GoogleDriveAPI(CREDENTIALS_PATH)
        folder_id = api.get_folder_id(DRIVE_DIRECTORY)
        files_info = api.get_files_under_folder(folder_id)
        for file_info in files_info:
            file_data = api.download_file(file_info['id'])
            file_name = DOWNLOADS_DIR + '/' + file_info['name']
            with open(file_name, 'wb') as f:
                f.write(file_data)

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()