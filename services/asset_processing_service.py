import json

from services.amazon_service import AmazonService
from services.asset_service import AssetService
from transformers.video_transformer import VideoTransformer
from transformers.image_transformer import ImageTransformer
from transformers.pdf_transformer import PDFTransformer

from constants.content_type_code import VIDEO_TYPE_CODE, IMAGE_TYPE_CODE, PDF_TYPE_CODE

from logger import logger

METADATA_KEYS = ['ContentType', 'ContentLength', 'LastModified', 'ETag']

class AssetProcessingService:
    def __init__(self, amazon_service: AmazonService, asset_service: AssetService):
        self.amazon_service = amazon_service
        self.asset_service = asset_service

    def process(self, message: str):
        try:

            message_json = json.loads(message)

            logger.debug(f"processing message {message_json['key']}")
           
            s3_object = self.amazon_service.get_object(message_json['key'])
            
            metadata = self.get_metadata(METADATA_KEYS, s3_object)
            
            transformer = self.get_transformer(metadata)
            if not  transformer:
                logger.error(f"failed to get transformer for {message_json['key']}")
                return
            
            transformer.transform(message_json['key'], s3_object)

            logger.info(f"message {message_json['key']} processed successfully")

        except Exception as err:
            logger.error(f"failed to process file {message_json['key']} {err.__str__()}")

    
    def get_metadata(self, keys: list, s3_object):
        return {key.lower(): s3_object[key] for key in keys if key in s3_object}

    def get_transformer(self, metadata):
        if metadata['contenttype'] in VIDEO_TYPE_CODE:
            return VideoTransformer(self.amazon_service)
        elif metadata['contenttype'] in IMAGE_TYPE_CODE:
            return ImageTransformer(self.amazon_service)
        elif metadata['contenttype'] in PDF_TYPE_CODE:
            return PDFTransformer(self.amazon_service)
        else:
            return None
