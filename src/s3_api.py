from collections.abc import AsyncGenerator

import aioboto3
from botocore.config import Config


class S3Api:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name

    async def list_files(self) -> AsyncGenerator[str, None]:
        session = aioboto3.Session()
        async with session.resource('s3') as s3:
            bucket = await s3.Bucket(self.bucket_name)
            async for s3_object in bucket.objects.all():
                yield s3_object.key

    async def get_presigned_url(self, key: str, expires_in: int = 60) -> str:
        session = aioboto3.Session()
        config = Config(signature_version='s3v4')
        async with session.client('s3', config=config) as s3:
            url = await s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': key},
                ExpiresIn=expires_in,
            )
            return url

    async def exists(self, key: str) -> bool:
        session = aioboto3.Session()
        async with session.client('s3') as s3:
            try:
                await s3.head_object(Bucket=self.bucket_name, Key=key)
                return True
            except Exception:
                return False
