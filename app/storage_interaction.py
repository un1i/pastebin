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

    def put(self, filename, message):
        self.__os.put_object(Bucket='pastebin', Key=filename, Body=message, StorageClass='Standard')

    def get(self, filename):
        response = self.__os.get_object(Bucket='pastebin', Key=filename)
        return response['Body'].read().decode('UTF-8')




