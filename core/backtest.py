"""
AlphaHunter AI
Backtest Engine v1
"""

import pandas as pd


def run_backtest(df):

    total = 0
    wins = 0
    losses = 0

    for i in range(200, len(df) - 10):

        entry = df.iloc[i]["Close"]
        exit_price = df.iloc[i + 10]["Close"]

        if exit_price > entry:
            wins += 1
        else:
            losses += 1

        total += 1

    if total == 0:
        return {
            "Trades": 0,
            "WinRate": 0
        }

    return {

        "Trades": total,

        "Wins": wins,

        "Losses": losses,

        "WinRate": round((wins / total) * 100, 2)

    }