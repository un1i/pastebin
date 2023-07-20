import enum
from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class LifeTime(Enum):
    TEN_MINUTES = '10M'
    ONE_WEEK = '1W'
    TWO_WEEKS = '2W'
    ONE_MONTH = '1M'
    THREE_MONTHS = '3M'
    SIX_MONTHS = '6M'
    ONE_YEAR = '1Y'


class PasteCreate(BaseModel):
    message: str
    lifetime: LifeTime

