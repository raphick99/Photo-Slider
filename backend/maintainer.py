import asyncio
import pathlib

from google_drive_api import GoogleDriveAPI


class Maintainer:
	def __init__(
			self,
			google_api: GoogleDriveAPI,
			local_photos_path: pathlib.Path,
			remote_photos_folder: str,
			refresh_interval: float = 10,
	):
		self.google_api = google_api
		self.local_photos_path = local_photos_path
		self.remote_photos_folder = remote_photos_folder
		self.refresh_interval = refresh_interval
		self.refresh_task: asyncio.Task | None = None

	def start(self):
		self.refresh_task = asyncio.create_task(self.periodic_photos_refresh())

	async def periodic_photos_refresh(self):
		try:
			while True:
				self.google_api.download_folder(self.remote_photos_folder, self.local_photos_path)
				await asyncio.sleep(self.refresh_interval)
		except asyncio.CancelledError:
			pass
