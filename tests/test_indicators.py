import os
import sys
import pandas as pd
import yfinance as yf

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.indicators import (
    add_ema,
    add_rsi,
    add_macd,
    add_atr,
    add_adx,
)

print("Veri indiriliyor...")

df = yf.download(
    "THYAO.IS",
    period="6mo",
    auto_adjust=True,
    progress=False
)
# MultiIndex'i düzleştir
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

df = add_ema(df)
df = add_rsi(df)
df = add_macd(df)
df = add_atr(df)
df = add_adx(df)

print(
    df[
        [
            "Close",
            "EMA20",
            "EMA50",
            "EMA200",
            "RSI",
            "MACD",
            "MACD_SIGNAL",
            "ATR",
            "ADX",
        ]
    ].tail()
)