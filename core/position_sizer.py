"""
AlphaHunter AI Professional
Position Sizer

Calculates position size based on portfolio risk
and available capital.
"""


class PositionSizer:

    def __init__(self, risk_per_trade: float = 0.01):
        """
        risk_per_trade = 0.01 means 1% risk per trade
        """
        self.risk_per_trade = risk_per_trade

    def calculate_position_size(
        self,
        portfolio_value: float,
        available_cash: float,
        entry_price: float,
        stop_loss: float
    ) -> int:
        """
        Calculate maximum shares based on:
        1. Risk per trade
        2. Available cash
        """

        # Maximum money willing to lose
        risk_amount = portfolio_value * self.risk_per_trade

        # Risk per share
        risk_per_share = entry_price - stop_loss

        if risk_per_share <= 0:
            return 0

        # Shares allowed by risk
        shares_by_risk = int(risk_amount / risk_per_share)

        # Shares allowed by cash
        shares_by_cash = int(available_cash / entry_price)

        # Use the smaller value
        return max(min(shares_by_risk, shares_by_cash), 0)

    def calculate_trade_value(
        self,
        position_size: int,
        entry_price: float
    ) -> float:
        """
        Capital required for trade.
        """

        return round(position_size * entry_price, 2)

    def calculate_portfolio_risk(
        self,
        portfolio_value: float
    ) -> float:
        """
        Maximum acceptable loss.
        """

        return round(
            portfolio_value * self.risk_per_trade,
            2
        )

    def has_enough_cash(
        self,
        available_cash: float,
        trade_value: float
    ) -> bool:
        """
        Check if enough cash exists.
        """

        return available_cash >= trade_value