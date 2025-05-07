import asyncio
import pathlib

from google_drive_api import GoogleDriveAPI


class Maintainer:
    def __init__(
        self,
        google_api: GoogleDriveAPI,
        local_photos_path: pathlib.Path,
        remote_photos_folder: str,
        refresh_interval: float = 300,  # 5 minutes
    ):
        self.google_api = google_api
        self.local_photos_path = local_photos_path
        self.remote_photos_folder = remote_photos_folder
        self.refresh_interval = refresh_interval
        self.refresh_task: asyncio.Task | None = None
        self.file_list: list[str] = []
        self.current_photo_index: int = 0

    def start(self):
        self.refresh_task = asyncio.create_task(self.periodic_photos_refresh())

    def stop(self):
        if self.refresh_task:
            self.refresh_task.cancel()
            self.refresh_task = None

    def get_next_photo(self) -> str | None:
        if not self.file_list:
            return None
        self.current_photo_index = (self.current_photo_index + 1) % len(self.file_list)
        return self.file_list[self.current_photo_index]

    async def periodic_photos_refresh(self):
        try:
            while True:
                downloaded_files = self.google_api.download_folder(self.remote_photos_folder, self.local_photos_path)
                downloaded_files.sort()

                if self.file_list != downloaded_files:
                    self.file_list = downloaded_files
                    self.current_photo_index = 0
                await asyncio.sleep(self.refresh_interval)
        except asyncio.CancelledError:
            pass
