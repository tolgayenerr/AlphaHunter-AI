"""
AlphaHunter AI Professional
Trade Manager
"""

from core.trade import Trade


class TradeManager:

    def __init__(self):

        self.active_trades = []

        self.closed_trades = []

    def open_trade(
        self,
        symbol,
        entry_price,
        position_size,
        entry_date,
    ):

        trade = Trade(
            symbol=symbol,
            entry_price=entry_price,
            position_size=position_size,
            entry_date=entry_date,
        )

        self.active_trades.append(trade)

        return trade

    def close_trade(
        self,
        trade,
        exit_price,
        exit_date,
    ):

        trade.close_trade(
            exit_price,
            exit_date,
        )

        self.active_trades.remove(trade)

        self.closed_trades.append(trade)

    def get_active_trades(self):

        return self.active_trades

    def get_closed_trades(self):

        return self.closed_trades

    @property
    def total_trades(self):

        return len(self.closed_trades)

    @property
    def open_positions(self):

        return len(self.active_trades)