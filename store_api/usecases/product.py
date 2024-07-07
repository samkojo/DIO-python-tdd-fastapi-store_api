from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from store_api.db.mongo import db_client
from store_api.models.product import ProductModel
from store_api.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store_api.core.exceptions import NotFoundException
from bson import Binary, UuidRepresentation

class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        await self.collection.insert_one(product_model.model_dump())

        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> ProductOut:
        id_binary = Binary.from_uuid(id, UuidRepresentation.STANDARD)
        result = await self.collection.find_one({"id": id_binary})

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductOut(**result)

    async def query(self) -> List[ProductOut]:
        return [ProductOut(**item) async for item in self.collection.find()]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        id_binary = Binary.from_uuid(id, UuidRepresentation.STANDARD)
        result = await self.collection.find_one_and_update(
            filter={"id": id_binary},
            update={"$set": body.model_dump(exclude_none=True)},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        id_binary = Binary.from_uuid(id, UuidRepresentation.STANDARD)
        product = await self.collection.find_one({"id": id_binary})
        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        result = await self.collection.delete_one({"id": id_binary})

        return True if result.deleted_count > 0 else False


product_usecase = ProductUsecase()
