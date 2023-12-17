from pydantic import BaseModel
from datetime import datetime


class MenuItemCreate(BaseModel):
    name: str
    description: str = None
    price: float
    image_url: str = None
    category: str