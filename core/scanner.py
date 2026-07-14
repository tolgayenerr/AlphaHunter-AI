import yfinance as yf
import pandas as pd

from symbols import BIST_SYMBOLS
from core.indicators import (
    add_ema,
    add_rsi,
    add_macd,
    add_atr,
    add_adx,
)


def scan_market():

    market = {}

    for symbol in BIST_SYMBOLS:

        try:

            df = yf.download(
                symbol,
                period="2y",
                auto_adjust=True,
                progress=False
            )

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            if len(df) < 200:
                continue

            df = add_ema(df)
            df = add_rsi(df)
            df = add_macd(df)
            df = add_atr(df)
            df = add_adx(df)

            df["Symbol"] = symbol

            market[symbol] = df

        except Exception as e:

            print(f"{symbol} -> {e}")

    return market