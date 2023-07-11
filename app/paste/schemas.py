from datetime import datetime
from pydantic import BaseModel


class PasteCreate(BaseModel):
    message: str
    date: datetime
    lifetime: datetime


class Paste(BaseModel):
    table: str
    hash: str
    url: str
    date_creation: datetime
    date_delete: datetime
