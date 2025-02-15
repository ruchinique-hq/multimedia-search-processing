from models.asset import Asset

from repositories.asset_repositories import AssetRepository


class AssetService:
    def __init__(self, asset_repository: AssetRepository):
        self.asset_repository = asset_repository

    def fetch_one_by_id(self, asset_id: str) -> Asset | None:
        document = self.asset_repository.find_one_by_id(asset_id)
        if document:
            return Asset(**document)
