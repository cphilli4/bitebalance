import json

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

# from humps import camelize
from pydantic import BaseModel


class CoreModel(BaseModel):
    class Config:
        # alias_generator = camelize
        populate_by_name= True


class IDModelMixin(CoreModel):
    id: Optional[UUID] = None

    # For Deduplication
    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(("id", self.id))


class CreatedAtMixin(CoreModel):
    created_at: datetime


class UpdatedAtMixin(CoreModel):
    updated_at: Optional[datetime]


class DeletedAtMixin(CoreModel):
    deleted_at: Optional[datetime]


class TimestampsMixin(DeletedAtMixin, UpdatedAtMixin, CreatedAtMixin):
    ...


class Count(CoreModel):
    count: int


CreatedCount = Count
DeletedCount = Count


class RecordStatus(UpdatedAtMixin, IDModelMixin):
    status: str


class UpdatedRecord(UpdatedAtMixin, IDModelMixin):
    ...


class BooleanResponse(CoreModel):
    value: bool


class StringResponse(CoreModel):
    value: str


class StatusResponse(CoreModel):
    status: str
    details: Optional[Any]


class RedirectResponse(CoreModel):
    status_code: int
    request_id: Optional[str]
    redirect_url: Optional[str]


def decode_json(cls, v):
    if not isinstance(v, str):
        try:
            return json.dumps(v)
        except Exception as err:
            raise ValueError(f"Could not parse value into valid JSON: {err}")

    return v
