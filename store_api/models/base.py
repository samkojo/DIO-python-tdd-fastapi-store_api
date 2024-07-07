from datetime import datetime
from decimal import Decimal
from typing import Any
import uuid
from bson import Binary, Decimal128, UuidRepresentation
from pydantic import UUID4, BaseModel, Field, model_serializer


class CreateBaseModel(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @model_serializer
    def set_model(self) -> dict[str, Any]:
        self_dict = dict(self)

        for key, value in self_dict.items():
            if isinstance(value, Decimal):
                self_dict[key] = Decimal128(str(value))
            elif isinstance(value, uuid.UUID):
                self_dict[key] = Binary.from_uuid(value, UuidRepresentation.STANDARD)


        return self_dict
