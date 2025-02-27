import json

from repositories.asset.asset_repository import AssetRepository
from services.amazon_service import AmazonService

from transformers.video_transformer import VideoTransformer
from transformers.image_transformer import ImageTransformer
from transformers.pdf_transformer import PDFTransformer

from constants.content_type import VIDEO_TYPE_CODE, IMAGE_TYPE_CODE, PDF_TYPE_CODE

from models.asset.asset import Asset

from logger import logger

METADATA_KEYS = ['ContentType', 'ContentLength', 'LastModified', 'ETag']

class AssetService:
    def __init__(self, asset_repository: AssetRepository, amazon_service: AmazonService):
        self.asset_repository = asset_repository
        self.amazon_service = amazon_service

    def process(self, message: str):
        try:
            
            logger.debug("processing asset %s", message)

            asset = self.asset_service.fetch_one_by_id(message)
            if not asset or not asset.metadata:
                logger.error(f"asset {message} not found")
                return

            s3_object = self.amazon_service.get_object(asset.metadata.key)
            if not s3_object:
                logger.error(f"failed to get s3 object for {asset.id}")
                return
            
            metadata = self.get_metadata(METADATA_KEYS, s3_object)
            if not metadata or not metadata.get('contenttype'):
                logger.error(f"failed to get metadata for {asset.id}")
                return

            transformer = self.get_transformer(metadata)
            if not transformer:
                logger.error(f"failed to get transformer for {asset.id}")
                return
            
            transformer.transform(asset.metadata.key, s3_object)

        except Exception as err:
            logger.error(f"failed to process file {message} {str(err)}")

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
