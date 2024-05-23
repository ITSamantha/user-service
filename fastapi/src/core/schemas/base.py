from pydantic import BaseModel, ConfigDict, Extra


class BaseSchemaModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra=Extra.allow)
