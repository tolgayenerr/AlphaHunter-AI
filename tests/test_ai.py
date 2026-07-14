import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.scanner import scan_market

from core.ai_engine import (
    train_models,
    ensemble_predict,
)

print("Scanner çalışıyor...")

df = scan_market()

print()

print("AI Testi")

models = train_models(df)

signal, confidence = ensemble_predict(
    models,
    df.iloc[-1]
)
print(signal)

print(confidence)