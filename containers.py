from dependency_injector import containers, providers

from services.amazon_service import AmazonService
from services.file_service import FileService

from config.app_config import read_config


class Container(containers.DeclarativeContainer):
    config = read_config()

    amazon_service = providers.Singleton(
        AmazonService,
        config.aws.access_key_id,
        config.aws.secret_access_key,
        config.aws.region,
        config.aws.bucket
    )

    file_service = providers.Singleton(
        FileService,
        amazon_service
    )

