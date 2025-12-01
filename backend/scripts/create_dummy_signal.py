from datetime import datetime, timezone

from app.db.session import SessionLocal, Base, engine
from app.db.models.signal import Signal


def main():
    # مطمئن می‌شیم جدول‌ها ساخته شدن
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        s = Signal(
            symbol="BTC/USDT",
            market="crypto",
            timeframe="15m",
            direction="BUY",
            entry=60000,
            sl=59000,
            tp=62000,
            strategy="dummy_test",
            mode="MANUAL",
            created_at=datetime.now(timezone.utc),
        )
        db.add(s)
        db.commit()
        print(f"Created signal with id={s.id}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
