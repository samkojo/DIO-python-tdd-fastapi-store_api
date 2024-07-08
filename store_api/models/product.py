from datetime import datetime

from pydantic import Field
from store_api.models.base import CreateBaseModel
from store_api.schemas.product import ProductIn, ProductUpdate


class ProductModel(ProductIn, CreateBaseModel):
    ...


class ProductUpdateModel(ProductUpdate, CreateBaseModel):
    updated_at: datetime = Field(default_factory=datetime.utcnow)
