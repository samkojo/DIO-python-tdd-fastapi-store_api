from datetime import datetime
from decimal import Decimal
from uuid import UUID
from bson import Decimal128, Binary
from pydantic import UUID4, BaseModel, Field, model_validator


class BaseSchemaMixin(BaseModel):
    class Config:
        from_attributes = True


class OutSchema(BaseModel):
    id: UUID4 = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()

    @model_validator(mode="before")
    def set_schema(cls, data):
        for key, value in data.items():
            if isinstance(value, Decimal128):
                data[key] = Decimal(str(value))
            elif isinstance(value, Binary):
                data[key]=UUID(bytes=value)
        return data
