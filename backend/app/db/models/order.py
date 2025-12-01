from datetime import datetime, timezone

from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    signal_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("signals.id", ondelete="SET NULL"),
        nullable=True,
    )

    symbol: Mapped[str] = mapped_column(String(50), index=True)
    market: Mapped[str] = mapped_column(String(20))
    direction: Mapped[str] = mapped_column(String(10))     # BUY / SELL
    entry: Mapped[float] = mapped_column(Float)
    sl: Mapped[float] = mapped_column(Float)
    tp: Mapped[float] = mapped_column(Float)

    quantity: Mapped[float] = mapped_column(Float, default=1.0)  # فعلاً ساده

    status: Mapped[str] = mapped_column(
        String(20),
        default="pending",                                  # pending / open / closed / cancelled
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    signal = relationship("Signal", backref="orders")
