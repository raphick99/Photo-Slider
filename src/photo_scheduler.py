import queue
import time

from loguru import logger

from s3_api import S3Api


class PhotoScheduler:
    def __init__(self, bucket_name: str, fetch_interval: float, tenant_id: str):
        self.s3_api = S3Api(bucket_name, tenant_id)
        self.fetch_interval = fetch_interval
        self.photo_queue = queue.PriorityQueue()
        self.photos_in_queue = set()
        self.current_age = 1
        self.last_fetch_time = 0
        self.tenant_id = tenant_id

    async def _fetch_new_photos(self):
        logger.info('Fetching new photos')
        self.last_fetch_time = time.perf_counter()
        file_list = [key async for key in self.s3_api.list_files()]

        for photo_key in file_list:
            if photo_key not in self.photos_in_queue:
                self.photos_in_queue.add(photo_key)
                self.photo_queue.put((0, photo_key))

    async def _should_fetch_new_photos(self) -> bool:
        return time.perf_counter() - self.last_fetch_time > self.fetch_interval

    async def get_next_photo(self) -> str | None:
        if await self._should_fetch_new_photos():
            await self._fetch_new_photos()

        try:
            photo_key = self.photo_queue.get(block=False)[1]
        except queue.Empty:
            logger.warning('Photo queue is empty')
            return None

        if not await self.s3_api.exists(photo_key):
            logger.warning('Photo does not exist, removing it and fetching next photo', photo_key=photo_key)
            self.photos_in_queue.remove(photo_key)
            return await self.get_next_photo()

        self.photo_queue.put((self.current_age, photo_key))
        logger.info('Photo added to queue', photo_key=photo_key, age=self.current_age)
        self.current_age += 1
        return await self.s3_api.get_presigned_url(photo_key)
