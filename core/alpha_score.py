"""
AlphaHunter AI
Alpha Score Engine
"""

def calculate_alpha_score(row, confidence):

    score = 0

    # EMA Trend
    if row["EMA20"] > row["EMA50"]:
        score += 20

    if row["EMA50"] > row["EMA200"]:
        score += 15

    # RSI
    if 45 <= row["RSI"] <= 65:
        score += 15

    # MACD
    if row["MACD"] > row["MACD_SIGNAL"]:
        score += 15

    # ADX
    if row["ADX"] >= 25:
        score += 10

    # AI Confidence
    score += min(confidence * 0.25, 25)

    return round(score, 1)