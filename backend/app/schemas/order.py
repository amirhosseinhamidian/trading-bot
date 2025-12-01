from datetime import datetime
from pydantic import BaseModel


class OrderBase(BaseModel):
    symbol: str
    market: str
    direction: str
    entry: float
    sl: float
    tp: float
    quantity: float
    status: str


class OrderOut(OrderBase):
    id: int
    signal_id: int | None
    created_at: datetime

    class Config:
        orm_mode = True

class AcceptSignalRequest(BaseModel):
    quantity: float | None = None  # اگر null بود، 1.0 می‌ذاریم