import pandas as pd
import numpy as np

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

    df["FutureReturn"] = df["Close"].shift(-5) / df["Close"] - 1

    df["Target"] = (df["FutureReturn"] > 0.02).astype(int)

    df = df.dropna()

    X = df[FEATURES]
    y = df["Target"]

    models = {
        "rf": RandomForestClassifier(
            n_estimators=300,
            random_state=42
        ),
        "et": ExtraTreesClassifier(
            n_estimators=300,
            random_state=42
        ),
        "gb": GradientBoostingClassifier(
            random_state=42
        )
    }

    splitter = TimeSeriesSplit(n_splits=5)

    for model in models.values():

        for train_idx, test_idx in splitter.split(X):

            model.fit(
                X.iloc[train_idx],
                y.iloc[train_idx]
            )

    return models


def ensemble_predict(models, row):

    X = pd.DataFrame(
        [row[FEATURES]],
        columns=FEATURES
    )

    probs = []

    for model in models.values():

        p = model.predict_proba(X)[0][1]

        probs.append(p)

    confidence = round(np.mean(probs) * 100, 1)

    signal = "BUY" if confidence >= 50 else "SELL"

    return signal, confidence