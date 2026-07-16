"""
AlphaHunter AI Professional v1.0
Main Application
"""

from core.scanner import scan_market
from core.ai_engine import run_ai_engine
from core.ranking import (
    build_results,
    filter_opportunities,
    save_results,
)


def main():

    print("=" * 50)
    print(" AlphaHunter AI Professional v1.0")
    print("=" * 50)

    print("\n[1/4] Market taranıyor...")
    market = scan_market()

    print(f"{len(market)} hisse bulundu.")

    print("\n[2/4] AI analizleri yapılıyor...")
    results = run_ai_engine(market)

    print(f"{len(results)} analiz tamamlandı.")

    print("\n[3/4] Ranking oluşturuluyor...")
    df = build_results(results)

    opportunities = filter_opportunities(df)

    save_results(df)

    print("\n[4/4] Fırsatlar")

    if opportunities.empty:
        print("\nUygun fırsat bulunamadı.")

    else:

        print(
            opportunities[
                [
                    "Symbol",
                    "Signal",
                    "Confidence",
                    "Alpha",
                    "RR",
                ]
            ]
        )

    print("\nİşlem tamamlandı.")


if __name__ == "__main__":
    main()