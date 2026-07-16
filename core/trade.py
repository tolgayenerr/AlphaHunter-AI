"""
AlphaHunter AI Professional
Trade Object

Represents a single completed or open trade.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class Trade:
    # Basic Information
    symbol: str

    # Entry
    entry_date: datetime
    entry_price: float

    # Risk Management
    stop_loss: float
    take_profit: float
    position_size: int = 0

    # AI Scores
    ai_probability: float = 0.0
    alpha_score: float = 0.0
    opportunity_score: float = 0.0

    # Exit
    exit_date: Optional[datetime] = None
    exit_price: Optional[float] = None
    exit_reason: str = "OPEN"

    # Performance
    holding_days: int = 0
    profit_pct: float = 0.0

    @property
    def is_open(self) -> bool:
        """Returns True if the trade is still open."""
        return self.exit_date is None

    def close(
        self,
        exit_price: float,
        exit_date: datetime,
        reason: str
    ):
        """Close the trade."""

        self.exit_price = exit_price
        self.exit_date = exit_date
        self.exit_reason = reason

        self.holding_days = (
            exit_date - self.entry_date
        ).days

        self.profit_pct = round(
            ((exit_price - self.entry_price) / self.entry_price) * 100,
            2
        )

    def risk_reward_ratio(self) -> float:
        """Calculate Risk/Reward ratio."""

        risk = self.entry_price - self.stop_loss
        reward = self.take_profit - self.entry_price

        if risk <= 0:
            return 0.0

        return round(reward / risk, 2)

    @property
    def profit_amount(self) -> float:
        """Returns realized profit/loss amount."""

        return (
            self.position_size
            * self.entry_price
            * self.profit_pct
            / 100
        )

    def to_dict(self):
        """Convert Trade object to dictionary."""
        return asdict(self)