from datetime import datetime, timezone

from sqlalchemy import String, Integer, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Signal(Base):
    __tablename__ = "signals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    symbol: Mapped[str] = mapped_column(String(50), index=True)
    market: Mapped[str] = mapped_column(String(20))        # crypto / forex
    timeframe: Mapped[str] = mapped_column(String(10))     # e.g. 15m, 1h
    direction: Mapped[str] = mapped_column(String(10))     # BUY / SELL / EXIT

    entry: Mapped[float] = mapped_column(Float)
    sl: Mapped[float] = mapped_column(Float)
    tp: Mapped[float] = mapped_column(Float)

    strategy: Mapped[str] = mapped_column(String(50))
    mode: Mapped[str] = mapped_column(String(10))          # MANUAL / AUTO

    status: Mapped[str] = mapped_column(
        String(20),
        default="new",                                     # new / accepted / rejected
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
