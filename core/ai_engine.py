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

    # 5 gün sonraki getiri
    df["FutureReturn"] = (
        df["Close"].shift(-5) / df["Close"] - 1
    )

    # %2 üzeri yükseliş = BUY
    df["Target"] = (
        df["FutureReturn"] > 0.02
    ).astype(int)

    # Sadece gerekli kolonlarda NaN temizle
    df = df.dropna(subset=FEATURES + ["Target"])

    # Yeterli veri yoksa modeli eğitme
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

    # Model oluşturulamadıysa
    if models is None:
        return "HOLD", 0.0

    # Son satırda eksik veri varsa
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