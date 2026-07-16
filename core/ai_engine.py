"""
AlphaHunter AI
AI Engine v2
"""

import numpy as np
import pandas as pd

from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
    GradientBoostingClassifier,
)
from sklearn.model_selection import TimeSeriesSplit

from core.alpha_score import calculate_alpha_score


FEATURES = [
    "EMA20",
    "EMA50",
    "EMA200",
    "RSI",
    "MACD",
    "ATR",
    "ADX",
]


def train_models(df):

    df = df.copy()

    df["FutureReturn"] = (
        df["Close"].shift(-5) / df["Close"] - 1
    )

    df["Target"] = (
        df["FutureReturn"] > 0.02
    ).astype(int)

    df = df.dropna(subset=FEATURES + ["Target"])

    if len(df) < 100:
        return None

    X = df[FEATURES]
    y = df["Target"]

    models = {
        "rf": RandomForestClassifier(
            n_estimators=300,
            max_depth=8,
            min_samples_leaf=5,
            random_state=42,
        ),

        "et": ExtraTreesClassifier(
            n_estimators=300,
            max_depth=8,
            min_samples_leaf=5,
            random_state=42,
        ),

        "gb": GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.05,
            random_state=42,
        ),
    }

    splitter = TimeSeriesSplit(n_splits=5)

    for model in models.values():

        for train_idx, test_idx in splitter.split(X):

            X_train = X.iloc[train_idx]
            y_train = y.iloc[train_idx]

            model.fit(
                X_train,
                y_train,
            )

    models["features"] = FEATURES

    return models


def ensemble_predict(models, row):

    if models is None:
        return "HOLD", 0.0

    if row[models["features"]].isna().any():
        return "HOLD", 0.0

    X = pd.DataFrame(
        [[
            row["EMA20"],
            row["EMA50"],
            row["EMA200"],
            row["RSI"],
            row["MACD"],
            row["ATR"],
            row["ADX"],
        ]],
        columns=models["features"],
    )

    probabilities = []

    for name in ["rf", "et", "gb"]:

        prob = models[name].predict_proba(X)[0][1]
        probabilities.append(prob)

    probability = np.mean(probabilities)

    confidence = round(probability * 100, 1)

    signal = "BUY" if probability >= 0.50 else "SELL"

    return signal, confidence


def run_ai_engine(market):
    """
    Market taranır.
    Her hisse için AI tahmini yapılır.
    Sonuç listesi döndürülür.
    """

    results = []

    for symbol, df in market.items():

        try:

            models = train_models(df)

            if models is None:
                continue

            row = df.iloc[-1]

            signal, confidence = ensemble_predict(
                models,
                row,
            )

            alpha = calculate_alpha_score(
                row,
                confidence,
            )

            atr = row["ATR"]

            rr = round(2.0 + (row["ADX"] / 50), 2)

            results.append(
                {
                    "Symbol": symbol,
                    "Signal": signal,
                    "Confidence": confidence,
                    "Alpha": alpha,
                    "Close": round(row["Close"], 2),
                    "ATR": round(atr, 2),
                    "RR": rr,
                }
            )

        except Exception as e:

            print(f"{symbol} -> {e}")

    return results