from typing import Optional

import pandas as pd
import pandas_ta as ta

from app.trading.strategies.base import BaseStrategy, SignalDecision


def _find_indicator_column(df: pd.DataFrame, key: str, length: int | None = None) -> Optional[str]:
    """
    پیدا کردن اسم ستون اندیکاتور بر اساس یه کلید (مثل 'rsi' یا 'ema')
    و در صورت نیاز طول (مثلا 14، 9، 21).
    """
    key = key.lower()
    candidates: list[str] = []

    for c in df.columns:
        lc = c.lower()
        if key in lc:
            if length is None or lc.endswith(f"_{length}"):
                candidates.append(c)

    if not candidates:
        return None

    # اگر چند تا بود، اولی رو برمی‌داریم
    return candidates[0]


class MaRsiStrategy(BaseStrategy):
    name = "ma_rsi"

    def __init__(
        self,
        rsi_length: int = 14,
        ema_fast: int = 9,
        ema_slow: int = 21,
        risk_reward: float = 2.0,
        sl_atr_mult: float = 1.5,
    ) -> None:
        self.rsi_length = rsi_length
        self.ema_fast = ema_fast
        self.ema_slow = ema_slow
        self.risk_reward = risk_reward
        self.sl_atr_mult = sl_atr_mult

    def generate(self, df: pd.DataFrame) -> Optional[SignalDecision]:
        """
        df: DataFrame با ستون‌های ['open','high','low','close','volume']
        خروجی: یک SignalDecision یا None
        """

        if df.shape[0] < max(self.ema_slow, self.rsi_length) + 2:
            print("[MaRsi] Not enough candles")
            return None

        df = df.copy()

        # اندیکاتورها را اضافه کن
        df.ta.rsi(length=self.rsi_length, append=True)
        df.ta.ema(length=self.ema_fast, append=True)
        df.ta.ema(length=self.ema_slow, append=True)
        df.ta.atr(length=14, append=True)

        # برای دیباگ: می‌تونی موقتاً این رو باز کنی
        # print(df.columns)

        # پیدا کردن اسم درست ستون‌ها
        rsi_col = _find_indicator_column(df, "rsi", self.rsi_length)
        ema_fast_col = _find_indicator_column(df, "ema", self.ema_fast)
        ema_slow_col = _find_indicator_column(df, "ema", self.ema_slow)
        atr_col = _find_indicator_column(df, "atr", 14)

        if not rsi_col or not ema_fast_col or not ema_slow_col or not atr_col:
            print("[MaRsi] Missing indicator columns:", rsi_col, ema_fast_col, ema_slow_col, atr_col)
            return None

        last = df.iloc[-1]
        prev = df.iloc[-2]

        close = float(last["close"])
        rsi = float(last[rsi_col])
        ema_fast_val = float(last[ema_fast_col])
        ema_slow_val = float(last[ema_slow_col])
        atr = float(last[atr_col])

        prev_ema_fast = float(prev[ema_fast_col])
        prev_ema_slow = float(prev[ema_slow_col])

        # کراس صعودی/نزولی EMA
        buy_cross = prev_ema_fast <= prev_ema_slow and ema_fast_val > ema_slow_val
        sell_cross = prev_ema_fast >= prev_ema_slow and ema_fast_val < ema_slow_val

        # اگر ATR خیلی کوچیک بود، یه مقدار حداقلی در نظر بگیر
        if atr <= 0:
            atr = close * 0.005  # مثلا 0.5%

        # BUY: کراس صعودی + RSI زیر 70
        if buy_cross and rsi < 70:
            sl = close - self.sl_atr_mult * atr
            tp = close + self.risk_reward * (close - sl)
            return SignalDecision(
                action="BUY",
                entry=close,
                sl=sl,
                tp=tp,
                strategy=self.name,
            )

        # SELL: کراس نزولی + RSI بالای 30
        if sell_cross and rsi > 30:
            sl = close + self.sl_atr_mult * atr
            tp = close - self.risk_reward * (sl - close)
            return SignalDecision(
                action="SELL",
                entry=close,
                sl=sl,
                tp=tp,
                strategy=self.name,
            )

        print("[MaRsi] No signal conditions met")
        return None
