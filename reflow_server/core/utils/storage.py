from django.conf import settings

from urllib import parse
from functools import wraps
from boto3.s3.transfer import TransferConfig
import boto3
import botocore
import logging


class BucketUploadException(ConnectionError):
    pass


class Bucket:
    """
    Instead of using django-storages we decided to use the default package for managing S3 from AWS called 
    boto3.
    This class is used for many s3 related operations, for checking if the file exists in a bucket to duplicating data between buckets
    and uploading data.
    """
    def __init__(self, bucket=None):
        if not bucket:
            bucket = settings.S3_BUCKET

        self.__config = TransferConfig(multipart_threshold=1024 * 25, max_concurrency=10, multipart_chunksize=1024 * 25, use_threads=True)

        self.__session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        s3 = self.__session.resource('s3', region_name=settings.S3_REGION_NAME, config=botocore.client.Config(signature_version='s3v4'))\
            if settings.ENV != 'development' else \
            self.__session.resource(service_name='s3', endpoint_url='http://{}:{}'.format(settings.LOCALSTACK_ENDPOINT, settings.LOCALSTACK_PORT))
        self.bucket = s3.Bucket(bucket)

    def __get_client(self):
        return self.__session.client('s3', region_name=settings.S3_REGION_NAME, config=botocore.client.Config(signature_version='s3v4')) \
                if settings.ENV != 'development' else \
                boto3.client('s3', endpoint_url='http://{}:{}'.format(settings.LOCALSTACK_ENDPOINT, settings.LOCALSTACK_PORT), use_ssl=False, aws_access_key_id='foo', aws_secret_access_key='bar')

    def get_temp_url(self, key):
        """
        Retrieves a temporary url for the user to download the file.

        Args:
            key (str):  the key with the name of the file you want to recieve the temporary url

        Returns:
            str: A temporary url that you can use to download a file or any other stuff
        """
        bucket = self.__get_client()
        url = bucket.generate_presigned_url('get_object', Params={
            'Bucket': settings.S3_BUCKET,
            'Key': key
        }, ExpiresIn=30)
        url = url if settings.ENV != 'development' else url.replace(settings.LOCALSTACK_ENDPOINT, 'localhost')
        return url

    def upload(self, file, key, is_public=False):
        """
        Upload the file to S3 at a specific key.

        Args:
            file (io.BytesIO / django.core.files.uploadedFile.InMemoryUploadedFile): The metadata you want to upload to s3
            key (str): This is the key with the name of the file.

        Returns:
            str: the url for the file
        """
        if is_public:
            self.bucket.upload_fileobj(
                file,
                key,
                ExtraArgs={'ACL': 'public-read'},
                Config=self.__config
            ) 
        else:
            self.bucket.upload_fileobj(
                file,
                key,
                Config=self.__config
            )
        response = parse.urljoin(self.get_temp_url(key), parse.urlparse(self.get_temp_url(key)).path)
        return response

    def delete(self, key):
        """
        Deletes a file from Amazon S3.

        Args:
            key (str): the key with the name of the file you want to delete
        """
        self.bucket.delete_objects(
            Delete={
                'Objects': [{
                    'Key': key
                }]
            }
        )

    def copy(self, from_key, to_key):
        """
        Copy a file from one location to another in S3

        Args:
            from_key (str): the key you want to copy
            to_key (str): the new key of the file

        Returns:
            str: returns the url of the new uploaded file. It creates a temporary file and extract the parameters from the url.
        """
        self.bucket.copy({
            'Bucket': settings.S3_BUCKET,
            'Key': from_key
            }, to_key
        )
        response = parse.urljoin(self.get_temp_url(to_key), parse.urlparse(self.get_temp_url(to_key)).path)
        return response

    def check(self, key):
        """
        Check if a key exists in s3
        :param key: str - the key you want to check
        """
        bucket = self.__get_client()
        try: 
            response = bucket.get_object(Bucket=settings.S3_BUCKET, Key=key)
            return 'found'
        except Exception as e:
            return 'not_found'
