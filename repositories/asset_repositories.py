from pymongo.results import InsertOneResult
from bson import ObjectId

from repositories.mongo_repository import MongoRepository

from constants.database import ASSETS_COLLECTION


class AssetRepository:
    def __init__(self, mongo_repository: MongoRepository):
        self.mongo_repository = mongo_repository

    def save(self, asset: dict) -> str:
        result: InsertOneResult = self.mongo_repository.insert_one(ASSETS_COLLECTION, asset)
        return str(result.inserted_id)

    def find_one_by_id(self, asset_id: str):
        return self.mongo_repository.find_one(ASSETS_COLLECTION, {"_id": ObjectId(asset_id)})
