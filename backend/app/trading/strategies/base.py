from dataclasses import dataclass
from typing import Optional


@dataclass
class SignalDecision:
    action: str       # "BUY" / "SELL" / "HOLD" / "EXIT"
    entry: float
    sl: float
    tp: float
    strategy: str = "ma_rsi"
    mode: str = "MANUAL"  # فعلاً سیگنال برای مود دستی


class BaseStrategy:
    name: str = "base"

    def generate(self, df) -> Optional[SignalDecision]:
        raise NotImplementedError
