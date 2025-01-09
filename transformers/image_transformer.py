from transformers.content_transformer import ContentTransformer

from services.amazon_service import AmazonService

class ImageTransformer(ContentTransformer):
    def __init__(self, amazon_service: AmazonService):
        super().__init__(amazon_service)

    def transform(self, key: str, s3_content):
        pass