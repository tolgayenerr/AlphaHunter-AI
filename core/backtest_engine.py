"""
AlphaHunter AI Professional
Backtest Engine v2

Institutional-grade backtesting engine.
"""

from typing import List

from core.trade import Trade
from core.portfolio import Portfolio
from core.position_sizer import PositionSizer
from core.metrics import Metrics


class BacktestEngine:

    def __init__(self):

        self.portfolio = Portfolio()

        self.position_sizer = PositionSizer(
            risk_per_trade=self.portfolio.risk_per_trade
        )

        self.trades: List[Trade] = []

        self.equity_curve = []

        self.daily_returns = []

    def run(self, data):

        """
        Main backtest loop.
        """

        print("Backtest started...")

        # Buraya ana döngü gelecek

        print("Backtest finished.")

        return self.summary()

    def open_trade(self, trade: Trade):

        """
        Open a new trade.
        """

        self.portfolio.add_trade(trade)

    def close_trade(self, trade: Trade):

        """
        Close an existing trade.
        """

        self.portfolio.close_trade(trade)

    def update_equity(self):

        """
        Update portfolio equity.
        """

        self.portfolio.update_equity()

        self.equity_curve.append(
            self.portfolio.equity
        )

    def summary(self):

        """
        Return performance statistics.
        """

        return Metrics.summary(
            self.portfolio.closed_trades,
            self.equity_curve,
            self.daily_returns
        )