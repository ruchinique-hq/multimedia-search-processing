from dependency_injector import containers, providers

from repositories.mongo_repository import MongoRepository
from repositories.asset.asset_repository import AssetRepository

from services import asset_service
from services.amazon_service import AmazonService
from services.asset_service import AssetService    

from config.app_config import read_config


class Container(containers.DeclarativeContainer):
    config = read_config()

    mongo_repository = providers.Singleton(
        MongoRepository,
        config.mongo.uri,
        config.mongo.database
    )

    asset_repository = providers.Singleton(
        AssetRepository,
        mongo_repository
    )

    amazon_service = providers.Singleton(
        AmazonService,
        config.aws.access_key_id,
        config.aws.secret_access_key,
        config.aws.region,
        config.aws.bucket
    )

    asset_service = providers.Singleton(
        AssetService,
        asset_repository,
        amazon_service
    )

    

