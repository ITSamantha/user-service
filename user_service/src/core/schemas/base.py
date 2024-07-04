import datetime

from pydantic import BaseModel, ConfigDict, Extra


class BaseSchemaModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class BaseResponseSchemaModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra=Extra.allow)


class BaseDeleteSchema(BaseSchemaModel):
    deleted_at: datetime.datetime = datetime.datetime.now()
