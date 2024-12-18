import boto3

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
        return self.sqs.get_queue_url(QueueName='multimodal-asset-processing')

    def receive_message(self, queue_url: str):
        response = self.sqs.receive_message(QueueUrl=queue_url,
                                            MessageAttributeNames=['All'],
                                            MaxNumberOfMessages=1,
                                            WaitTimeSeconds=10)

        return response.get('Messages', [])

    def delete_message(self, queue_url: str, receipt_handle: str):
        self.sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
        logger.info(f"message {receipt_handle} deleted from the queue")

    def get_object(self, key: str):
        return self.s3.get_object(Bucket=self.s3_bucket, Key=key)
