from dependency_injector import containers, providers

from config.app_config import read_config


class Container(containers.DeclarativeContainer):
    config = read_config()