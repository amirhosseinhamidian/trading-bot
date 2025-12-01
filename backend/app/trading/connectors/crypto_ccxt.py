import ccxt
import pandas as pd
from typing import Literal

ExchangeId = Literal["binance", "bybit", "kucoin", "kraken"]


class CryptoConnector:
    def __init__(self, exchange_id: ExchangeId = "bybit") -> None:
        exchange_class = getattr(ccxt, exchange_id)
        self.exchange = exchange_class(
            {
                "enableRateLimit": True,
                "timeout": 5000,  # مثلا ۵ ثانیه
            }
        )

    def fetch_ohlcv_df(
        self,
        symbol: str,
        timeframe: str = "15m",
        limit: int = 200,
    ) -> pd.DataFrame | None:
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        except ccxt.NetworkError as e:
            print(f"[ERROR] Network error fetching OHLCV from {self.exchange.id}: {e}")
            return None
        except ccxt.BaseError as e:
            print(f"[ERROR] CCXT error from {self.exchange.id}: {e}")
            return None

        df = pd.DataFrame(
            ohlcv,
            columns=["timestamp", "open", "high", "low", "close", "volume"],
        )
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        return df
