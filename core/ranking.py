"""
AlphaHunter AI
Ranking Engine
"""

import pandas as pd


def build_results(results):

    df = pd.DataFrame(results)

    df = df.sort_values(
        by=["Alpha", "Confidence"],
        ascending=False
    )

    return df


def filter_opportunities(df):

    return df[
        (df["Signal"] == "BUY")
        &
        (df["Confidence"] >= 60)
        &
        (df["Alpha"] >= 40)
        &
        (df["RR"] >= 2)
        
    ]


def save_results(df):

    df.to_csv(
        "results.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nresults.csv oluşturuldu.")