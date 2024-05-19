from pydantic import BaseModel, ConfigDict


class BaseSchemaModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
