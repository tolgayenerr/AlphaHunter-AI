"""
AlphaHunter AI Professional
Metrics Engine

Calculates professional portfolio statistics.
"""

import math
from typing import List

from core.trade import Trade


class Metrics:

    @staticmethod
    def total_return(trades: List[Trade]) -> float:

        if not trades:
            return 0.0

        return round(sum(t.profit_pct for t in trades), 2)

    @staticmethod
    def win_rate(trades: List[Trade]) -> float:

        if not trades:
            return 0.0

        wins = sum(1 for t in trades if t.profit_pct > 0)

        return round((wins / len(trades)) * 100, 2)

    @staticmethod
    def average_win(trades: List[Trade]) -> float:

        wins = [t.profit_pct for t in trades if t.profit_pct > 0]

        if not wins:
            return 0.0

        return round(sum(wins) / len(wins), 2)

    @staticmethod
    def average_loss(trades: List[Trade]) -> float:

        losses = [t.profit_pct for t in trades if t.profit_pct < 0]

        if not losses:
            return 0.0

        return round(sum(losses) / len(losses), 2)

    @staticmethod
    def profit_factor(trades: List[Trade]) -> float:

        gross_profit = sum(
            t.profit_pct
            for t in trades
            if t.profit_pct > 0
        )

        gross_loss = abs(sum(
            t.profit_pct
            for t in trades
            if t.profit_pct < 0
        ))

        if gross_loss == 0:
            return 0.0

        return round(gross_profit / gross_loss, 2)

    @staticmethod
    def expectancy(trades: List[Trade]) -> float:

        if not trades:
            return 0.0

        win_rate = Metrics.win_rate(trades) / 100

        avg_win = Metrics.average_win(trades)

        avg_loss = abs(Metrics.average_loss(trades))

        expectancy = (
            win_rate * avg_win
            -
            (1 - win_rate) * avg_loss
        )

        return round(expectancy, 2)

    @staticmethod
    def max_drawdown(equity_curve: List[float]) -> float:

        if not equity_curve:
            return 0.0

        peak = equity_curve[0]

        max_dd = 0

        for value in equity_curve:

            if value > peak:
                peak = value

            drawdown = (peak - value) / peak

            if drawdown > max_dd:
                max_dd = drawdown

        return round(max_dd * 100, 2)

    @staticmethod
    def sharpe_ratio(
        returns: List[float],
        risk_free_rate: float = 0.0
    ) -> float:

        if len(returns) < 2:
            return 0.0

        mean = sum(returns) / len(returns)

        variance = sum(
            (r - mean) ** 2
            for r in returns
        ) / (len(returns) - 1)

        std = math.sqrt(variance)

        if std == 0:
            return 0.0

        return round(
            (mean - risk_free_rate) / std,
            2
        )

    @staticmethod
    def summary(
        trades: List[Trade],
        equity_curve: List[float],
        returns: List[float]
    ):

        return {

            "Trades": len(trades),

            "Win Rate": Metrics.win_rate(trades),

            "Average Win": Metrics.average_win(trades),

            "Average Loss": Metrics.average_loss(trades),

            "Profit Factor": Metrics.profit_factor(trades),

            "Expectancy": Metrics.expectancy(trades),

            "Max Drawdown": Metrics.max_drawdown(
                equity_curve
            ),

            "Sharpe Ratio": Metrics.sharpe_ratio(
                returns
            ),

            "Total Return": Metrics.total_return(
                trades
            )

        }