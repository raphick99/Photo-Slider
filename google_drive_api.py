import io
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly", "https://www.googleapis.com/auth/drive.readonly"]
TOKEN_PATH = 'token.json'
CREDENTIALS_PATH = 'credentials.json'
PORT = 12345
DRIVE_DIRECTORY = 'Samples'
# DOWNLOADS_DIR = '/tmp/downloads'
DOWNLOADS_DIR = './downloads'



class GoogleDriveAPI:
    def __init__(self):
        self.service = self.get_service()

    def get_folder_id(self, folder_name):
        results = (
            self.service.files()
            .list(
                q=f'mimeType = \'application/vnd.google-apps.folder\' and name = \'{folder_name}\'',
                fields="files(id)",
            ).execute()
        ) 
        files = results.get('files', [])
        if len(files) != 1:
            raise RuntimeError(f'there should be a single file matcing, but there are {len(files)} matching instead')
        return files[0]['id']

    def get_files_under_folder(self, folder_id):
        results = (
            self.service.files()
            .list(
                q=f'\'{folder_id}\' in parents',
                fields="files(id, name)",
            ).execute()
        ) 
        files = results.get('files', [])
        return files

    def download_file(self, file_id):
        request = self.service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        return file.getvalue()

    @staticmethod
    def get_creds():
        creds = None

        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=PORT)

            with open(TOKEN_PATH, "w") as token:
                token.write(creds.to_json())
        return creds

    @staticmethod
    def get_service():
        creds = GoogleDriveAPI.get_creds()
        return build(serviceName='drive', version='v3', credentials=creds)


def main():
    try:
        api = GoogleDriveAPI()
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