import os
import boto3
import filetype

from botocore.exceptions import ClientError

from logger import logger

class AmazonService:
    def __init__(self, access_key: str, secret_key: str, region: str, bucket: str):

        self.sqs = boto3.client(
            'sqs',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

        self.s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

        self.bucket = bucket

    def get_queue_by_name(self, queue_name: str):
        return self.sqs.get_queue_url(QueueName=queue_name)

    def receive_message(self, queue_url: str):
        response = self.sqs.receive_message(QueueUrl=queue_url,
                                            MessageAttributeNames=['All'],
                                            MaxNumberOfMessages=1,
                                            WaitTimeSeconds=10)

        return response.get('Messages', [])

    def delete_message(self, queue_url: str, receipt_handle: str):
        self.sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
        logger.info(f"message {receipt_handle} deleted from the queue")

    def upload_directory_to_s3(self, local_directory, s3_prefix=''):

        parts = s3_prefix.split('/')
        parts_without_last = parts[:-1]
        prefix = "/".join(parts_without_last) + "/frames"

        for root, dirs, files in os.walk(local_directory):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, local_directory)
                s3_key = os.path.join(prefix, relative_path).replace(os.sep, '/')

                try:

                    logger.debug(f"uploading file {relative_path} to s3")

                    metadata = {'Content-Type': self.get_file_type(local_path)}
                    self.s3.upload_file(local_path, self.bucket, s3_key, ExtraArgs={'Metadata': metadata})

                    logger.info(f"uploaded file {relative_path} to s3")

                except ClientError as err:
                    logger.error(f"failed to upload files from {local_directory} to s3 {err.__str__()}")

    def get_object(self, key: str):
        return self.s3.get_object(Bucket=self.s3_bucket, Key=key)

    def download_file(self, key: str, path: str):
        self.s3.download_file(self.bucket, key, path)

    def get_file_type(self, file_path):
        content_type = filetype.guess(file_path)
        return content_type.mime
