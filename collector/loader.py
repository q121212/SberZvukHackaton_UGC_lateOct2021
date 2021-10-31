import aioboto3
import aiofiles
import asyncio
import httpx
import os
from django.conf import settings
from .analyze.results_handler import Results


class UploaderToCloud:
    def __init__(self):
        self.s3_endpoint_url = 'https://obs.ru-moscow-1.hc.sbercloud.ru'
        self.key_id = 'SPMPXJSYCCVS5QBN8EXY'
        self.access_key = 'NG14HhRDYSUCX2sIOeVxxvJKNKAJ859TkmeS99yX'
        self.bucket_name = 'hackathon-ecs-23'
        self.session = aioboto3.Session()

    async def upload_one_file_to_cloud(self, file_name, file_path):
        async with self.session.client(
                service_name="s3",
                endpoint_url=self.s3_endpoint_url,
                aws_access_key_id=self.key_id,
                aws_secret_access_key=self.access_key
        ) as s3:
            try:
                async with aiofiles.open(file_path, mode='rb') as f:
                    await s3.upload_fileobj(f, self.bucket_name, file_name)
            except Exception as e:
                print(e)
                return ""

        return f'WORK DONE for {file_name}'

    async def save_to_cloud(self, prefix, result_file_paths):
        """Upload all result's files to Cloud"""
        result_file_paths = Results(result_file_paths).get_results_file_paths(prefix)
        for file_name in result_file_paths:
            await self.upload_one_file_to_cloud(file_name, result_file_paths.get(file_name))

    async def get_file(self, file_name):
        '''Checking uploading success (for test use case only)'''
        async with self.session.client(
                service_name="s3",
                endpoint_url=s3_endpoint_url,
                aws_access_key_id=key_id,
                aws_secret_access_key=access_key
        ) as s3:
            try:
                esp = await s3.get_object(
                Bucket='hackathon-ecs-23',
                Key=file_name
                )
                data = await resp['Body'].read()
                if data:
                    print(f'fragment of file: {data[:100]}')
            except Exception as e:
                print(f'For `{file_name = }` happened exception:\n\n {e}')


async def async_save_file(url, prefix):
    """Save file to localhost"""
    folder = settings.MEDIA_ROOT
    filename = prefix
    file_extension = '.mp4'
    os.makedirs(folder, exist_ok=True)
    local_file_path = os.path.join(folder, filename + file_extension)
    if os.path.exists(local_file_path):
        return
    with open(local_file_path, 'wb') as f:
        async with httpx.AsyncClient() as client:
            async with client.stream('GET', url) as r:

                async for chunk in r.aiter_bytes():
                    f.write(chunk)


def get_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError as e:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop


def download_file(url, prefix):
    """Download file to localhost"""
    loop = get_loop()
    if loop.is_running():
        print('loop has already been running!')
        loop.run_in_executor(None, async_save_file, url, prefix)
    else:
        print('loop has just started!')
        asyncio.run(async_save_file(url, prefix))

