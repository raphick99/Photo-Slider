import random

from s3_api import S3Api


class Maintainer:
    def __init__(self, bucket_name: str):
        self.s3_api = S3Api(bucket_name)
        self.file_list: list[str] = []

    def start(self):
        pass

    def stop(self):
        pass

    async def get_next_photo(self) -> str | None:
        if not self.file_list:
            file_list = [key async for key in self.s3_api.list_files()]
            if not file_list:
                return None
            self.file_list = random.shuffle(file_list)
        current_photo_key = self.file_list.pop(0)
        return await self.s3_api.get_presigned_url(current_photo_key)
