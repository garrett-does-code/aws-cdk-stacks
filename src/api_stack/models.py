from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    id: str
    name: str
    email: str
    price: float
    ordered_date: str
    is_shipped: bool = False
    item_ttl: Optional[float] = None

class NewItemRequest(BaseModel):
    name: str
    email: str
    price: float