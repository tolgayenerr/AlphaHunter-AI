"""
AlphaHunter AI
Risk Manager
"""

def calculate_risk(row):

    entry = float(row["Close"])
    atr = float(row["ATR"])

    stop = round(entry - atr * 2, 2)

    target = round(entry + atr * 4, 2)

    rr = round((target - entry) / (entry - stop), 2)

    return {
        "entry": entry,
        "stop": stop,
        "target": target,
        "rr": rr
    }