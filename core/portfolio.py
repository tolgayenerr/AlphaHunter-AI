"""
AlphaHunter AI Professional
Portfolio Manager

Handles portfolio cash, positions and equity.
"""

from dataclasses import dataclass, field
from typing import List

from core.trade import Trade


@dataclass
class Portfolio:

    # Starting Capital
    initial_cash: float = 100000.0

    # Limits
    max_positions: int = 5
    risk_per_trade: float = 0.01

    # Runtime
    cash: float = field(init=False)
    equity: float = field(init=False)

    open_trades: List[Trade] = field(default_factory=list)
    closed_trades: List[Trade] = field(default_factory=list)

    def __post_init__(self):
        self.cash = self.initial_cash
        self.equity = self.initial_cash

    @property
    def available_slots(self) -> int:
        """Remaining position slots."""
        return self.max_positions - len(self.open_trades)

    def can_open_position(self) -> bool:
        """Can a new trade be opened?"""
        return len(self.open_trades) < self.max_positions

    def add_trade(self, trade: Trade):
        """Add new open trade."""
        self.open_trades.append(trade)

    def close_trade(self, trade: Trade):

        if trade in self.open_trades:

            self.open_trades.remove(trade)

            self.closed_trades.append(trade)

    def update_equity(self):

        realized_profit = 0

        for trade in self.closed_trades:

            realized_profit += trade.profit_amount

        self.equity = self.initial_cash + realized_profit

    def total_trades(self):

        return len(self.closed_trades)

    def win_rate(self):

        if not self.closed_trades:
            return 0

        wins = sum(
            1
            for t in self.closed_trades
            if t.profit_pct > 0
        )

        return round(
            wins / len(self.closed_trades) * 100,
            2
        )

    def summary(self):

        return {

            "Initial Cash": self.initial_cash,

            "Cash": round(self.cash, 2),

            "Equity": round(self.equity, 2),

            "Open Trades": len(self.open_trades),

            "Closed Trades": len(self.closed_trades),

            "Win Rate": self.win_rate()

        }