from dependency_injector import containers, providers

from services.amazon_service import AmazonService

from config.app_config import read_config


class Container(containers.DeclarativeContainer):
    config = read_config()

    amazon_service = AmazonService(
        AmazonService,
        config.aws.access_key_id,
        config.aws.secret_access_key,
        config.aws.region,
        config.aws.bucket
    )