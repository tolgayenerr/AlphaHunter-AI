import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.scanner import scan_market

from core.ai_engine import (
    train_models,
    ensemble_predict,
)

from core.alpha_score import calculate_alpha_score
from core.risk_manager import calculate_risk

from core.ranking import (
    build_results,
    filter_opportunities,
    save_results,
)

print("Scanner çalışıyor...")

market = scan_market()

print(f"{len(market)} hisse bulundu.")
print()

results = []

for symbol, df in market.items():

    models = train_models(df)

    signal, confidence = ensemble_predict(
        models,
        df.iloc[-1]
    )

    alpha = calculate_alpha_score(
        df.iloc[-1],
        confidence
    )

    risk = calculate_risk(
        df.iloc[-1]
    )

    results.append({
        "Symbol": symbol,
        "Signal": signal,
        "Confidence": confidence,
        "Alpha": alpha,
        "Entry": risk["entry"],
        "Stop": risk["stop"],
        "Target": risk["target"],
        "RR": risk["rr"],
    })

results = build_results(results)

save_results(results)

print("\n========== TOP FIRSATLAR ==========\n")

top = filter_opportunities(results)

if len(top) == 0:
    print("Filtreye uyan fırsat bulunamadı.")
else:
    print(top.to_string(index=False))