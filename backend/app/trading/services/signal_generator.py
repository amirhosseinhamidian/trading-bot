from sqlalchemy.orm import Session

from app.db.models.signal import Signal
from app.trading.connectors.crypto_ccxt import CryptoConnector
from app.trading.strategies.ma_rsi import MaRsiStrategy


def generate_signal_for_symbol(
    db: Session,
    symbol: str,
    market: str = "crypto",
    timeframe: str = "15m",
    exchange_id: str = "bybit",
) -> None:
    """
    ۱. گرفتن دیتای کندل از صرافی
    ۲. اجرای استراتژی EMA+RSI
    ۳. اگر سیگنالی بود، ذخیره‌اش در جدول signals
    """

    connector = CryptoConnector(exchange_id=exchange_id)
    df = connector.fetch_ohlcv_df(symbol, timeframe=timeframe, limit=200)
    if df is None or df.empty:
        print("No data fetched, skipping signal generation")
        return

    strat = MaRsiStrategy()
    decision = strat.generate(df)

    if decision is None:
        print("No signal generated for", symbol, timeframe)
        return

    signal = Signal(
        symbol=symbol,
        market=market,
        timeframe=timeframe,
        direction=decision.action,
        entry=decision.entry,
        sl=decision.sl,
        tp=decision.tp,
        strategy=decision.strategy,
        mode=decision.mode,
    )
    db.add(signal)
    db.commit()
    print("New signal saved:", symbol, decision.action, decision.entry)
