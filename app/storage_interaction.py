import boto3
import config


class ObjectStorage:
    __bucket = 'pastebin'
    __dir = 'data/'

    def __init__(self):
        self.__os = boto3.client(
            's3',
            aws_access_key_id=config.KEY_ID,
            aws_secret_access_key=config.KEY,
            region_name='ru-central1',
            endpoint_url='https://storage.yandexcloud.net'
        )

    def download(self, filename):
        path = self.__dir + filename
        self.__os.download_file(self.__bucket, filename, path)

    def upload(self, filename):
        path = self.__dir + filename
        self.__os.upload_file(path, self.__bucket, filename)

