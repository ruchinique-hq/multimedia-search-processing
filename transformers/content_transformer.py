from services.amazon_service import AmazonService

class ContentTransformer:
    def __init__(self, amazon_service: AmazonService):
        self.amazon_service = amazon_service

    def transform(self, key: str, s3_content):
        pass