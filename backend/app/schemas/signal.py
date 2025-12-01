# app/schemas/signal.py
from datetime import datetime
from pydantic import BaseModel


class SignalBase(BaseModel):
    symbol: str
    market: str
    timeframe: str
    direction: str
    entry: float
    sl: float
    tp: float
    strategy: str
    mode: str
    status: str 


class SignalOut(SignalBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
