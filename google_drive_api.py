import io
import os.path
import pathlib

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from loguru import logger


class GoogleDriveAPI:
    PORT = 12345
    SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly", "https://www.googleapis.com/auth/drive.readonly"]
    TOKEN_PATH = 'token.json'

    def __init__(self, credentials: pathlib.Path):
        self.service = self._get_service(credentials)

    def list_folder(self, folder_name):
        folder_id = self._get_folder_id(folder_name)
        files_info = self._get_files_under_folder(folder_id)
        return [file_info['name'] for file_info in files_info]
    
    def download_folder(self, folder_name: str, destination_folder: pathlib.Path):
        logger.info('downloading folder', folder_name=folder_name, destination_folder=destination_folder)
        folder_id = self._get_folder_id(folder_name)
        files_info = self._get_files_under_folder(folder_id)

        for file_info in files_info:
            file_data = self._download_raw_file(file_info['id'])
            file_name = destination_folder / file_info['name']
            with open(file_name, 'wb') as f:
                f.write(file_data)
    
    def download_file(self, file_name: str, destination_path: pathlib.Path):
        file_id = self._get_file_id(file_name)
        file_data = self._download_raw_file(file_id)
        destination_path.write_bytes(file_data)

    def _get_file_id(self, file_name):
        return self._get_id(name=file_name)

    def _get_folder_id(self, folder_name):
        return self._get_id(name=folder_name, mimeType='application/vnd.google-apps.folder')
    
    def _get_id(self, name: str, mimeType: str = None):
        query = f'name = \'{name}\''
        if mimeType:
            query += f' and mimeType = \'{mimeType}\''

        results = (
            self.service.files()
            .list(
                q=query,
                fields="files(id)",
            ).execute()
        ) 
        files = results.get('files', [])
        if len(files) != 1:
            raise RuntimeError(f'there should be a single file matcing, but there are {len(files)} matching instead')
        return files[0]['id']

    def _get_files_under_folder(self, folder_id):
        results = (
            self.service.files()
            .list(
                q=f'\'{folder_id}\' in parents',
                fields="files(id, name)",
            ).execute()
        ) 
        files = results.get('files', [])
        return files

    def _download_raw_file(self, file_id):
        request = self.service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        return file.getvalue()

    @staticmethod
    def _get_creds(credentials: pathlib.Path):
        creds = None

        if os.path.exists(GoogleDriveAPI.TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(GoogleDriveAPI.TOKEN_PATH, GoogleDriveAPI.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials, GoogleDriveAPI.SCOPES)
                creds = flow.run_local_server(port=GoogleDriveAPI.PORT)

            with open(GoogleDriveAPI.TOKEN_PATH, "w") as token:
                token.write(creds.to_json())
        return creds

    @staticmethod
    def _get_service(credentials: pathlib.Path) -> build:
        creds = GoogleDriveAPI._get_creds(credentials)
        return build(serviceName='drive', version='v3', credentials=creds)
