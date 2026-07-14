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
from core.backtest import run_backtest
from core.ranking import (
    build_results,
    filter_opportunities,
    save_results,
)

FEATURES = [
    "EMA20",
    "EMA50",
    "EMA200",
    "RSI",
    "MACD",
    "ATR",
    "ADX",
]

print("Scanner çalışıyor...\n")

market = scan_market()

print(f"{len(market)} hisse bulundu.\n")

results = []

for symbol, df in market.items():

    # AI'nın kullandığı kolonlarda NaN varsa o hisseyi atla
    if df[FEATURES].tail(1).isna().any().any():
        print(f"{symbol} -> NaN veri bulundu, atlandı.")
        continue

    models = train_models(df)

    if models is None:
        continue

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

    backtest = run_backtest(df)

    results.append({
        "Symbol": symbol,
        "Signal": signal,
        "Confidence": confidence,
        "Alpha": alpha,
        "Entry": risk["entry"],
        "Stop": risk["stop"],
        "Target": risk["target"],
        "RR": risk["rr"],
        "Trades": backtest["Trades"],
        "WinRate": backtest["WinRate"],
    })

results = build_results(results)

save_results(results)

print("\n========== TÜM SONUÇLAR ==========\n")
print(results.to_string(index=False))

print("\n========== TOP FIRSATLAR ==========\n")

top = filter_opportunities(results)

if top.empty:
    print("Filtreye uyan fırsat bulunamadı.")
else:
    print(top.to_string(index=False))