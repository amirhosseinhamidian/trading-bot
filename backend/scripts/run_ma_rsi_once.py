# scripts/run_ma_rsi_once.py

from app.db.session import SessionLocal
from app.trading.services.signal_generator import generate_signal_for_symbol


def main() -> None:
    db = SessionLocal()
    try:
        # لیست سیمبل‌ها و تایم‌فریم‌هایی که می‌خوای روشون استراتژی رو اجرا کنی
        # می‌تونی هر چقدر خواستی اضافه/کم کنی
        tasks: list[tuple[str, str, str]] = [
            ("BTC/USDT", "crypto", "15m"),
            ("BTC/USDT", "crypto", "1h"),
            ("ETH/USDT", "crypto", "15m"),
            ("ETH/USDT", "crypto", "1h"),
            ("SOL/USDT", "crypto", "15m"),
            ("XRP/USDT", "crypto", "1h"),
        ]

        for symbol, market, timeframe in tasks:
            print(f"\n=== Generating signal for {symbol} @ {timeframe} ({market}) ===")
            generate_signal_for_symbol(
                db=db,
                symbol=symbol,
                market=market,
                timeframe=timeframe,
                exchange_id="bybit",  # فعلاً همه روی Bybit
            )

        print("\nDone running MaRsiStrategy for all tasks.")

    finally:
        db.close()


if __name__ == "__main__":
    main()
