from pydantic import BaseModel, ConfigDict
from typing import Optional


class ItemRequest(BaseModel):
    name: str
    price: float

class ItemPatchRequest(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

    model_config = ConfigDict(extra="forbid")