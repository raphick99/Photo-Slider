import io
import os.path
import pathlib

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload



class GoogleDriveAPI:
    PORT = 12345
    SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly", "https://www.googleapis.com/auth/drive.readonly"]
    TOKEN_PATH = 'token.json'

    def __init__(self, credentials: pathlib.Path):
        self.service = self.get_service(credentials)

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
    def get_creds(credentials: pathlib.Path):
        creds = None

        if os.path.exists(GoogleDriveAPI.TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(GoogleDriveAPI.TOKEN_PATH, GoogleDriveAPI.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials, GoogleDriveAPI.SCOPES)
                creds = flow.run_local_server(port=self.PORT)

            with open(GoogleDriveAPI.TOKEN_PATH, "w") as token:
                token.write(creds.to_json())
        return creds

    @staticmethod
    def get_service(credentials: pathlib.Path):
        creds = GoogleDriveAPI.get_creds(credentials)
        return build(serviceName='drive', version='v3', credentials=creds)
