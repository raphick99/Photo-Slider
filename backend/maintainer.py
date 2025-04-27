import asyncio
from backend.main import DRIVE_PHOTOS_FOLDER, LOCAL_PHOTOS_PATH
from google_drive_api import GoogleDriveAPI


class Maintainer:
	def __init__(self, google_api: GoogleDriveAPI, refresh_interval: float = 10):
		self.google_api = google_api
		self.refresh_interval = refresh_interval
		self.refresh_task: asyncio.Task | None = None

	def start(self):
		self.refresh_task = asyncio.create_task(self.periodic_photos_refresh())

	async def periodic_photos_refresh(self):
		try:
			while True:
				self.google_api.download_folder(DRIVE_PHOTOS_FOLDER, LOCAL_PHOTOS_PATH)
				asyncio.sleep(self.refresh_interval)
		except asyncio.CancelledError:
			pass
